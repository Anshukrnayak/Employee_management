from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
import stripe

from .models import ClientModel, LeadModel, UserProfile, SubscriptionPlan, SubscriptionHistory, StripePayment
from .forms import LeadForm, ClientForm, SubscriptionPlanForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionRequiredMixin(LoginRequiredMixin):
    """Mixin to check if user has active subscription"""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile') or not request.user.profile.is_subscription_active:
            messages.warning(request, 'An active subscription is required to access this feature.')
            return redirect('subscription_plans')
        return super().dispatch(request, *args, **kwargs)


class ClientView(SubscriptionRequiredMixin, generic.ListView):
    model = ClientModel
    template_name = 'home/index.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        # Only show clients belonging to the current user's leads
        return ClientModel.objects.filter(lead__user=self.request.user).select_related('lead')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.profile
        context['subscription_plan'] = self.request.user.profile.subscription_plan
        return context


class ClientCreate(SubscriptionRequiredMixin, generic.View):
    def get(self, request):
        if not request.user.profile.can_create_client:
            messages.error(request, 'Client limit reached. Please upgrade your subscription to add more clients.')
            return redirect('subscription_plans')

        form = ClientForm(user=request.user)
        return render(request, 'home/create_client.html', {'form': form})

    def post(self, request):
        if not request.user.profile.can_create_client:
            messages.error(request, 'Client limit reached. Please upgrade your subscription to add more clients.')
            return redirect('subscription_plans')

        form = ClientForm(data=request.POST, user=request.user)
        if form.is_valid():
            try:
                client = form.save(commit=False)
                # Get the user's lead profile
                client.lead = LeadModel.objects.get(user=request.user)
                client.save()
                messages.success(request, 'Client created successfully!')
                return redirect('home')
            except LeadModel.DoesNotExist:
                messages.error(request, 'Please create your lead profile first.')
                return redirect('create_lead_profile')
        return render(request, 'home/create_client.html', {'form': form})


class ClientUpdateView(SubscriptionRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(ClientModel, id=kwargs['pk'], lead__user=request.user)
        form = ClientForm(instance=instance, user=request.user)
        return render(request, 'home/create_client.html', {'form': form})

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(ClientModel, id=kwargs['pk'], lead__user=request.user)
        form = ClientForm(instance=instance, data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully!')
            return redirect('home')
        return render(request, 'home/create_client.html', {'form': form})


class ClientDeleteView(SubscriptionRequiredMixin, generic.DeleteView):
    model = ClientModel
    template_name = 'home/delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return ClientModel.objects.filter(lead__user=self.request.user)


# Lead Views
class LeadsView(SubscriptionRequiredMixin, generic.ListView):
    template_name = 'home/leads.html'
    model = LeadModel
    context_object_name = 'leads'
    paginate_by = 20

    def get_queryset(self):
        return LeadModel.objects.filter(user=self.request.user)


class LeadUpdateView(SubscriptionRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(LeadModel, id=kwargs['pk'], user=request.user)
        form = LeadForm(instance=instance)
        return render(request, 'home/create_client.html', {'form': form})

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(LeadModel, id=kwargs['pk'], user=request.user)
        form = LeadForm(data=request.POST, instance=instance, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated successfully!')
            return redirect('leads')
        return render(request, 'home/create_client.html', {'form': form})


class DeleteLeadView(SubscriptionRequiredMixin, generic.DeleteView):
    template_name = 'home/delete.html'
    model = LeadModel
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return LeadModel.objects.filter(user=self.request.user)


class LeadView(SubscriptionRequiredMixin, generic.DetailView):
    template_name = 'home/profile.html'
    model = LeadModel
    context_object_name = 'profile'

    def get_queryset(self):
        return LeadModel.objects.filter(user=self.request.user)


# Profile Views
class DisplayLeadProfile(SubscriptionRequiredMixin, generic.View):
    def get(self, request):
        profile = get_object_or_404(LeadModel, user=request.user)
        user_profile = request.user.profile
        return render(request, 'home/profile.html', {
            'profile': profile,
            'user_profile': user_profile
        })


class CreateLeadProfile(LoginRequiredMixin, generic.View):
    def get(self, request):
        # Check if profile already exists
        if LeadModel.objects.filter(user=request.user).exists():
            messages.info(request, 'Your profile already exists.')
            return redirect('display_lead_profile')

        form = LeadForm()
        return render(request, 'home/create_client.html', {'form': form})

    def post(self, request):
        if LeadModel.objects.filter(user=request.user).exists():
            messages.info(request, 'Your profile already exists.')
            return redirect('display_lead_profile')

        form = LeadForm(request.POST, request.FILES)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.user = request.user
            lead.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('home')
        return render(request, 'home/create_client.html', {'form': form})


class UpdateLeadProfile(SubscriptionRequiredMixin, generic.UpdateView):
    template_name = 'home/create_client.html'
    form_class = LeadForm
    model = LeadModel
    success_url = reverse_lazy('display_lead_profile')

    def get_queryset(self):
        return LeadModel.objects.filter(user=self.request.user)


class DeleteLeadProfile(SubscriptionRequiredMixin, generic.DeleteView):
    model = LeadModel
    template_name = 'home/delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return LeadModel.objects.filter(user=self.request.user)


# Subscription and Payment Views
class SubscriptionPlansView(LoginRequiredMixin, generic.ListView):
    model = SubscriptionPlan
    template_name = 'subscription/plans.html'
    context_object_name = 'plans'

    def get_queryset(self):
        return SubscriptionPlan.objects.filter(is_active=True).order_by('price_monthly')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'profile'):
            context['current_plan'] = self.request.user.profile.subscription_plan
            context['user_profile'] = self.request.user.profile
        return context


class CreateCheckoutSessionView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        plan_id = kwargs.get('plan_id')
        billing_cycle = request.POST.get('billing_cycle', 'monthly')

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)

            # Get or create Stripe customer
            profile, created = UserProfile.objects.get_or_create(user=request.user)

            if not profile.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=f"{request.user.first_name} {request.user.last_name}",
                    metadata={'user_id': request.user.id}
                )
                profile.stripe_customer_id = customer.id
                profile.save()

            # Create checkout session
            price_id = plan.stripe_price_id_monthly if billing_cycle == 'monthly' else plan.stripe_price_id_yearly

            checkout_session = stripe.checkout.Session.create(
                customer=profile.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=request.build_absolute_uri(
                    reverse_lazy('subscription_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse_lazy('subscription_plans')),
                metadata={
                    'plan_id': str(plan.id),
                    'user_id': request.user.id,
                    'billing_cycle': billing_cycle
                }
            )

            return redirect(checkout_session.url)

        except Exception as e:
            messages.error(request, f'Error creating checkout session: {str(e)}')
            return redirect('subscription_plans')


class SubscriptionSuccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'subscription/success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id:
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                # You might want to verify the session and update user's subscription here
                messages.success(request, 'Subscription activated successfully!')
            except Exception as e:
                messages.error(request, 'Error verifying subscription.')

        return super().get(request, *args, **kwargs)


class CustomerPortalView(LoginRequiredMixin, generic.View):
    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.stripe_customer_id:
            messages.error(request, 'No subscription found.')
            return redirect('subscription_plans')

        try:
            portal_session = stripe.billing_portal.Session.create(
                customer=profile.stripe_customer_id,
                return_url=request.build_absolute_uri(reverse_lazy('display_lead_profile')),
            )
            return redirect(portal_session.url)
        except Exception as e:
            messages.error(request, f'Error accessing customer portal: {str(e)}')
            return redirect('display_lead_profile')


class UsageDashboardView(SubscriptionRequiredMixin, generic.TemplateView):
    template_name = 'subscription/usage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        plan = profile.subscription_plan

        context.update({
            'user_profile': profile,
            'subscription_plan': plan,
            'leads_usage_percentage': (profile.leads_count / plan.max_leads * 100) if plan.max_leads > 0 else 0,
            'clients_usage_percentage': (profile.clients_count / plan.max_clients * 100) if plan.max_clients > 0 else 0,
        })
        return context


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(generic.View):
    """Handle Stripe webhooks for subscription updates"""

    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] == 'customer.subscription.updated':
            self.handle_subscription_updated(event['data']['object'])
        elif event['type'] == 'customer.subscription.deleted':
            self.handle_subscription_deleted(event['data']['object'])
        elif event['type'] == 'invoice.payment_succeeded':
            self.handle_payment_succeeded(event['data']['object'])

        return HttpResponse(status=200)

    def handle_subscription_updated(self, subscription):
        """Update user's subscription status when changed in Stripe"""
        try:
            profile = UserProfile.objects.get(stripe_customer_id=subscription.customer)
            profile.subscription_status = subscription.status
            profile.subscription_id = subscription.id
            profile.current_period_start = subscription.current_period_start
            profile.current_period_end = subscription.current_period_end
            profile.cancel_at_period_end = subscription.cancel_at_period_end
            profile.save()
        except UserProfile.DoesNotExist:
            pass

    def handle_subscription_deleted(self, subscription):
        """Handle subscription cancellation"""
        try:
            profile = UserProfile.objects.get(stripe_customer_id=subscription.customer)
            profile.subscription_status = 'canceled'
            profile.subscription_id = ''
            profile.save()
        except UserProfile.DoesNotExist:
            pass

    def handle_payment_succeeded(self, invoice):
        """Handle successful payments"""
        # You can add payment tracking logic here
        pass


# Updated Forms to include user parameter
class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['first_name', 'last_name', 'contact', 'email', 'location', 'about', 'status', 'company', 'job_title']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


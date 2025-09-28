from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SubscriptionPlan(BaseModel):
    """Subscription plans (Basic, Premium, Enterprise, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stripe_price_id_monthly = models.CharField(max_length=100, blank=True)
    stripe_price_id_yearly = models.CharField(max_length=100, blank=True)

    # Feature limits
    max_leads = models.IntegerField(default=10)
    max_clients = models.IntegerField(default=5)
    max_team_members = models.IntegerField(default=1)
    has_analytics = models.BooleanField(default=False)
    has_api_access = models.BooleanField(default=False)
    has_priority_support = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['display_order', 'price_monthly']


class UserProfile(BaseModel):
    """Extended user profile with subscription information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    stripe_customer_id = models.CharField(max_length=100, blank=True, db_index=True)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscribers'
    )
    subscription_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('canceled', 'Canceled'),
            ('past_due', 'Past Due'),
            ('unpaid', 'Unpaid'),
            ('trialing', 'Trialing'),
            ('incomplete', 'Incomplete'),
            ('incomplete_expired', 'Incomplete Expired'),
        ],
        default='active'
    )
    subscription_id = models.CharField(max_length=100, blank=True)  # Stripe subscription ID
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)

    # Usage tracking
    leads_count = models.IntegerField(default=0)
    clients_count = models.IntegerField(default=0)

    # Team management
    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    is_team_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def can_create_lead(self):
        """Check if user can create more leads based on subscription"""
        if not self.subscription_plan:
            return False
        return self.leads_count < self.subscription_plan.max_leads

    @property
    def can_create_client(self):
        """Check if user can create more clients based on subscription"""
        if not self.subscription_plan:
            return False
        return self.clients_count < self.subscription_plan.max_clients

    @property
    def is_subscription_active(self):
        """Check if subscription is currently active"""
        active_statuses = ['active', 'trialing']
        return self.subscription_status in active_statuses

    @property
    def days_until_expiry(self):
        """Calculate days until subscription expires"""
        if self.current_period_end and self.is_subscription_active:
            return (self.current_period_end - timezone.now()).days
        return 0


class Team(BaseModel):
    """Team model for multi-user accounts"""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()


class LeadModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    location = models.TextField()
    about = models.TextField()
    profile_pic = models.ImageField(upload_to='leads/profile_pics/', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('qualified', 'Qualified'),
            ('converted', 'Converted'),
            ('lost', 'Lost')
        ],
        default='new'
    )
    score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    source = models.CharField(max_length=50, blank=True)  # Where lead came from
    tags = models.JSONField(default=list, blank=True)  # For flexible tagging

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self._state.adding:  # Only on creation
            profile = self.user.profile
            if profile.can_create_lead:
                profile.leads_count += 1
                profile.save()
            else:
                raise PermissionError("Lead limit reached for current subscription plan")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        profile = self.user.profile
        profile.leads_count -= 1
        profile.save()
        super().delete(*args, **kwargs)


class ClientModel(BaseModel):
    lead = models.ForeignKey(LeadModel, on_delete=models.CASCADE, related_name='clients')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    location = models.TextField()
    about = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('on_hold', 'On Hold')
        ],
        default='pending'
    )
    company = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    lifetime_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_contact = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['lead', 'status']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self._state.adding:  # Only on creation
            profile = self.lead.user.profile
            if profile.can_create_client:
                profile.clients_count += 1
                profile.save()
            else:
                raise PermissionError("Client limit reached for current subscription plan")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        profile = self.lead.user.profile
        profile.clients_count -= 1
        profile.save()
        super().delete(*args, **kwargs)


class StripePayment(BaseModel):
    """Track Stripe payments and invoices"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    stripe_payment_intent_id = models.CharField(max_length=100, db_index=True)
    stripe_invoice_id = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')
    status = models.CharField(max_length=20)  # succeeded, pending, failed
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']


class SubscriptionHistory(BaseModel):
    """Track subscription changes for auditing"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription_history')
    old_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    new_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    change_type = models.CharField(
        max_length=20,
        choices=[
            ('created', 'Created'),
            ('updated', 'Updated'),
            ('canceled', 'Canceled'),
            ('renewed', 'Renewed')
        ]
    )
    stripe_event_id = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']


class WebhookEvent(BaseModel):
    """Store Stripe webhook events for debugging"""
    stripe_event_id = models.CharField(max_length=100, unique=True, db_index=True)
    type = models.CharField(max_length=100)
    data = models.JSONField()
    processed = models.BooleanField(default=False)
    error = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import ClientModel,LeadModel
from .forms import LeadForm,ClientForm

class ClientView(LoginRequiredMixin,generic.ListView):
    model = ClientModel
    template_name = 'home/index.html'
    context_object_name = 'clients'


class ClientCreate(LoginRequiredMixin,generic.View):
    def get(self,request):
        form=ClientForm()
        return render(request,'home/create_client.html',{'form':form})

    def post(self,request):
        form=ClientForm(data=request.POST)
        if form.is_valid():
            client=form.save(commit=False)
            client.lead=LeadModel.objects.get(user=request.user)
            client.save()

            return redirect('home')
        return render(request,'home/create_client.html',{'form':form})


class ClientUpdateView(LoginRequiredMixin,generic.View):
    def get(self,request,*args,**kwargs):
        try:
            instance=ClientModel.objects.get(id=kwargs['pk'])
            form=ClientForm(instance=instance)
        except ClientModel.DoesNotExist():
            return redirect('home')

        return render(request,'home/create_client.html',{'form':form})

    def post(self,request,*args,**kwargs):
        try:
            instance=ClientModel.objects.get(id=kwargs['pk'])
        except ClientModel.DoesNotExist():
            return render('home')

        form=ClientForm(instance=instance,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request,'home/create_client.html',{'form':form})


class ClientDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = ClientModel
    template_name = 'home/delete.html'

    success_url = reverse_lazy('home')


# Logic for Lead profile

class LeadsView(LoginRequiredMixin,generic.ListView):
    template_name = 'home/leads.html'
    model = LeadModel
    context_object_name = 'leads'

class LeadUpdateView(LoginRequiredMixin,generic.View):


    def get(self,request,*args,**kwargs):
        try:
            instance=LeadModel.objects.get(id=kwargs['pk'])
        except LeadModel.DoesNotExist:
            return redirect('home')
        form=LeadForm(instance=instance)
        return render(request,'home/create_client.html',{'form':form})

    def post(self,request,*args,**kwargs):
        try:
            instance=LeadModel.objects.get(id=kwargs['pk'])
        except LeadModel.DoesNotExist:
            return redirect('home')
        form=LeadForm(data=request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request,'home/create_client.html',{'form':form})

class DeleteLeadView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'home/delete.html'
    model = LeadModel
    success_url = reverse_lazy('home')


class LeadView(LoginRequiredMixin,generic.DetailView):
    template_name = 'home/profile.html'
    model = LeadModel
    context_object_name = 'profile'


# Profile view :
class DisplayLeadProfile(LoginRequiredMixin,generic.View):
    def get(self,request):
        profile=LeadModel.objects.get(user=request.user)
        return render(request,'home/profile.html',{'profile':profile})

class CreateLeadProfile(LoginRequiredMixin,generic.View):
    def post(self,request):
        form=LeadForm(request.POST,request.FILES)
        if form.is_valid():
            lead=form.save(commit=False)
            lead.user=request.user
            lead.save()
            return redirect('home')
        return render(request,'home/create_client.html',{'form':form})

    def get(self,request):
        form=LeadForm()
        return render(request,'home/create_client.html',{'form':form})

class UpdateLeadProfile(LoginRequiredMixin,generic.UpdateView):
    template_name = 'home/create_client.html'
    form_class = LeadForm
    model = LeadModel
    success_url = reverse_lazy('home')


class DeleteLeadProfile(LoginRequiredMixin,generic.DeleteView):
    form_class = LeadForm
    model = LeadModel
    success_url = reverse_lazy('home')





from django.shortcuts import render,redirect
from django.views import generic
from app import models
from client.forms import ClientForm
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404
import logging
from .forms import ClientForm
from django.contrib.auth.decorators import login_required

# Configure logging
logger = logging.getLogger(__name__)


class ClientList(generic.ListView):
    model=models.ClientModel
    template_name='client.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_list"] = models.ClientModel.objects.all()[0:10]
        
        return context
    


class AddClient(View):
    
    def get(self,request):
        form=ClientForm()
        return render(request,'add_client.html',{'form':form})

    def post(self,request):

        form=ClientForm(request.POST,request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.manage_by=self.request.user 
            obj.save()
       
            messages.info(request,'New client add successfully.....')
            return redirect('clients')

        print(f' form error : {form.errors} ') 
        return render(request,'add_client.html',{'form':form})


class ClinetDetailView(View):

    def get(self,request,*args,**kwargs):
        
        client=models.ClientModel.objects.get(id=kwargs['pk'])
        return render(request,'client_detail.html',{'client':client})
    


class EditClientView(View):
    template_name = 'add_client.html'  # Define template name for consistency

    def get_instance(self, pk):
     
        try:
            return models.ClientModel.objects.get(id=pk) 
        except models.ClientModel.DoesNotExist:
            logger.error(f"Client with ID {pk} not found.")
            raise Http404("Client not found")

    def get(self, request, *args, **kwargs):
     
        instance = self.get_instance(kwargs['pk'])
        form = ClientForm(instance=instance)
        return render(request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
      
        instance = self.get_instance(kwargs['pk'])
        form = ClientForm(data=request.POST, files=request.FILES, instance=instance)

        if form.is_valid():
            form.save()
            messages.info(request,'successfully updated client data ')
            return redirect('clients')  # Redirect to a relevant page

        logger.warning(f"Form submission failed for client ID {kwargs['pk']}. Errors: {form.errors}")
        return render(request, self.template_name, {'form': form})

 

@login_required
def delete_client(request,*args,**kwargs):

    try:
        client=models.ClientModel.objects.get(id=kwargs['pk'])
        client.delete()
        messages.info(request,'Client has deleted successfully....')
        return redirect('clients')

    except models.ClientModel.DoesNotExist:
        raise Http404('client not exists..')









    



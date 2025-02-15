from django.shortcuts import render,redirect
from django.views import generic,View
from app.models import LeadModel,AgentModel
from app.forms import LeadForm,AgentForm
from django.contrib.auth.models import User

from django.contrib.auth import user_logged_in  
from django.contrib import messages

# home of the application 
def homePage(request):return render(request,'Home/index.html')

class AgentView(View):
    def get(self,request):
        form=AgentForm
        return render(request,'home/agent.html',{'form':form})

    def post(self,request):
        form=AgentForm(request.POST,request.FILES)
        if form.is_valid():
            agent=form.save(commit=False)
            agent.name=request.user
            agent.save()

            print('user is saved ')

            return redirect('home')

        return render(request,'home/agent.html',{'form':form})


# List of leads 
class ListLeads(generic.ListView):
    template_name='Home/home.html'
    model=LeadModel
    fields='__all__'
    context_object_name = 'lead_list'

# add agent :

    
# Agent profile 
class AgentProfile(View):    
    def get(self,request,*args,**kwargs):
        try:
            if User.is_authenticated:
                agent=AgentModel.objects.get(name=request.user)
                return render(request,'Home/agent_profile.html',{'agent':agent})
        except AgentModel.DoestNotExist:
            agent={}
            return render(request,'Home/agent_profile.html',{'agent':agent})

class AddLeads(View):
    
    def get(self,request,*args,**kwargs):
        form=LeadForm
        return render(request,'Home/add_leads.html',{'form':form})
    
    def post(self,request):
        form=LeadForm(request.POST,request.FILES)

        if form.is_valid():
            obj=form.save(commit=False)
            obj.agent=self.request.user
            obj.save()
            return redirect('home')

        messages.info(request,'Invalid form data please enter correct format data : ')
        return render(request,'Home/add_leads.html',{'form':form})

class LeadProfile(View):
    def get(self,request,*args,**kwargs):
        pk=kwargs['pk']
        
        lead_profile=LeadModel.objects.get(id=pk)
        return render(request,'Home/lead_profile.html',{'lead':lead_profile})

class UpdateLead(View):
        def get(self, request, *args, **kwargs):
                lead = LeadModel.objects.select_related('agent').get(id=kwargs['pk'])
                form = LeadForm(instance=lead)
                return render(request, 'Home/add_leads.html', {'form': form})

        def post(self, request, *args, **kwargs):
            try:
                lead = LeadModel.objects.select_related('agent').get(id=kwargs['pk'])
                form = LeadForm(request.POST, request.FILES, instance=lead)

                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.agent = request.user
                    obj.save()
                    return redirect('leads')

                return render(request, 'Home/add_leads.html', {'form': form})

            except LeadModel.DoesNotExist:
                return redirect('leads')


class DeletePage(generic.DeleteView):
    model=LeadModel
    template_name='Home/delete_lead.html'

    def post(self,request,pk):
        LeadModel.objects.get(id=pk).delete()
        return redirect('leads')

    
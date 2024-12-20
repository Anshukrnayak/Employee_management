from django.shortcuts import render,redirect
from django.views import generic,View
from app.models import LeadModel,AgentModel
from app.forms import LeadForm
from django.contrib.auth.models import User

from django.contrib import messages

# home of the application 
def homePage(request):return render(request,'Home/index.html')


# List of leads 
class ListLeads(generic.ListView):
    template_name='Home/home.html'
    model=LeadModel
    fields='__all__'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lead_list"] = LeadModel.objects.all() 
        return context
    
# Agent profile 
class AgentProfile(View):    
    def get(self,request,*args,**kwargs):
        try:
            if User.is_authenticated:
                agent=AgentModel.objects.get(name=request.user)
                return render(request,'Home/agent_profile.html',{'agent':agent})
        except:
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
    def get(self,request,*args,**kwargs):
        
        lead=LeadModel.objects.get(id=kwargs['pk'])
        form=LeadForm(instance=lead)
        print(kwargs['pk'])
        return render(request,'Home/add_leads.html',{'form':form})

        

    def post(self,request,*args,**kwargs):

        try:
            lead=LeadModel.objects.get(id=kwargs['pk'])
            form=LeadForm(request.POST,request.FILES,instance=lead)

            if form.is_valid():
                obj=form.save(commit=False)
                obj.agent=self.request.user
                obj.save() 
                print('user update successfully....')
                return redirect('leads')
            
            print('invalid form ')
            return render(request,'Home/add_leads.html',{'form':form})

        except: return redirect('leads')


class DeletePage(generic.DeleteView):
    model=LeadModel
    template_name='Home/delete_lead.html'

    def post(self,request,pk):
        LeadModel.objects.get(id=pk).delete()
        return redirect('leads')

    
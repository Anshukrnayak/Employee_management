from django.shortcuts import render,redirect
from django.views import generic
from app import models 
from django.contrib.auth.decorators import login_required
from app.forms import LeadForm


def create_todo():
    with open('todo.text','w') as f:
        f.write('\nDone Account and authenitcation  ')
        f.write('\n Done create client and lead model ')
        f.write('\n Done apply migrations and migrate ')
        f.write('\n Done create user interface for leads')


def home_page(request):
    create_todo()
    
    try:
        clients=models.ClientModel.objects.all()
        leads=models.LeadModel.objects.all()
    except models.ClientModel.DoesNotExist or models.LeadModel.DoesNotExist: 
        clients=0
        leads=0
    return render(request,'home/index.html',{'client':clients,'lead':leads})


@login_required
def setting_view(request,*args,**kwargs):


    if request.method=='POST':
        form=LeadForm(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.lead=request.user
            instance.save()

            return redirect('setting')

        return render(request,'home/setting.html',{'form':form})
    
    form=LeadForm()
    is_lead=False
    try:

        lead=models.LeadModel.objects.get(lead=request.user)
        is_lead=True
        return render(request,'home/setting.html',{'form':form,'is_lead':is_lead,'lead':lead})

    except:
        print(f'is lead {is_lead}')
        return render(request,'home/setting.html',{'form':form,'is_lead':is_lead})









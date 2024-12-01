from django.shortcuts import render,redirect
from django.views.generic import View
from .models import employee
from app.forms import employee_form
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView


class Home_page(View):

    def get(self,request):

        employee_list=employee.objects.all()
            
        return render(request,'home/index.html',{'employee_list':employee_list})



class employee_form(CreateView):
    template_name='home/employee_form.html'
    model=employee
    fields='__all__'

    success_url='/'


@login_required
def delete_employee(request,pk):
    object=employee.objects.get(id=pk)
    object.delete()

    return redirect('home')



class employee_update(UpdateView):

    template_name='home/employee_form.html'
    model=employee
    fields='__all__'

    success_url='/'
    





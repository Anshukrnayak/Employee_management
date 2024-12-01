
from django import forms
from .models import employee,department


class employee_form(forms.ModelForm):
    class Meta:
        model=employee
        fields='__all__'


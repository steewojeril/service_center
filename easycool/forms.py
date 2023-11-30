from collections.abc import Mapping
from typing import Any
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from easycool.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegistrationForm(UserCreationForm ):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']
        # widgets={
        #     'password':forms.PasswordInput(attrs={'class':'form-control'})
        # }

class CreateBrandForm(forms.ModelForm):
    class Meta:
        model= Brands
        fields=['name']

class CreateTechnicianForm(forms.ModelForm):
    class Meta:
        model= Technicians
        fields=['name']
class CreateApplianceForm(forms.ModelForm):
    class Meta:
        model= Appliances
        fields=['appliance_name','brand','inverter','fully_automatic','capacity','type']
        widgets={
            'appliance_name':forms.Select(attrs={'class':'form-control','id':'id_appliance_name'}),
            'brand':forms.Select(attrs={'class':'form-control'}),
            'capacity':forms.Select(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control','id':'id_type'}),
        }
            
class CreateCapacityForm(forms.ModelForm):
    class Meta:
        model= Capacity
        fields=['name','appliance_name']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'appliance_name':forms.Select(attrs={'class':'form-control'}),
        }
class CreateTypeForm(forms.ModelForm):
    class Meta:
        model= Types
        fields=['name','appliance_name']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'appliance_name':forms.Select(attrs={'class':'form-control'}),
        }


        
class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model= Customers
        fields=['name','address','place','phone1','phone2','email']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'place':forms.TextInput(attrs={'class':'form-control'}),
            'phone1':forms.TextInput(attrs={'class':'form-control'}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }
class EditCustomerForm(forms.ModelForm):
    class Meta:
        model= Customers
        fields=['name','address','place','phone1','phone2','email']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'place':forms.TextInput(attrs={'class':'form-control'}),
            'phone1':forms.TextInput(attrs={'class':'form-control'}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }


class CreateCommonComplaintForm(forms.ModelForm):
    class Meta:
        model= CommonComplaints
        fields=['complaint']

class CreateComplaintForm(forms.ModelForm):
    # to pass different queryset to a foriegnkey field in a form when the form is loaded
    def __init__(self, *args, **kwargs):
        appliance_id = kwargs.pop('appliance_id', None)  # Extract appliance_id from kwargs
        appliance=Appliances.objects.get(id=appliance_id)
        super(CreateComplaintForm, self).__init__(*args, **kwargs)

        if appliance_id is not None:
            self.fields['common_complaint'].queryset = CommonComplaints.objects.filter(appliance=appliance.appliance_name)
        else:
            self.fields['common_complaint'].queryset = CommonComplaints.objects.none()
            
    class Meta:
        model= Complaints
        fields=['common_complaint','complaint_type','technician','note']
        widgets={
            'common_complaint':forms.Select(attrs={'class':'form-control'}),
            'complaint_type':forms.Select(attrs={'class':'form-control'}),
            'technician':forms.Select(attrs={'class':'form-control'}),
            'note':forms.TextInput(attrs={'class':'form-control'}),
        }

class EditComplaintForm(forms.ModelForm):
    class Meta:
        model= Complaints
        fields=['appliance','common_complaint','complaint_type','note','technician','status','rectified_date','rectified_issue','remarks','bill_amt','bill_no']
        widgets={
            'appliance':forms.Select(attrs={'class':'form-control font-weight-bold'}),
            'common_complaint':forms.Select(attrs={'class':'form-control'}),
            'complaint_type':forms.Select(attrs={'class':'form-control'}),
            'technician':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'note':forms.TextInput(attrs={'class':'form-control'}),
            'rectified_issue':forms.TextInput(attrs={'class':'form-control'}),
            'rectified_date':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'remarks':forms.TextInput(attrs={'class':'form-control'}),
            'bill_amt':forms.TextInput(attrs={'class':'form-control'}),
            'bill_no':forms.TextInput(attrs={'class':'form-control'}),
        }

        
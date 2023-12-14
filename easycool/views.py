from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView,CreateView,ListView,UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from easycool.models import *
from django.urls import reverse_lazy,reverse
from easycool.forms import *
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q  # to perform or in orm
from easycool.decorators import sign_in_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.http import JsonResponse

# sending mail
def send_due_email(subject,body):
        send_mail(
            subject,
            body,
            'steewoj@gmail.com',
            ['steewoj@gmail.com'],
            fail_silently=True,
        )

class SendEmailView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        appliance = Appliances.objects.get(id=id)
        if appliance:
            subject = 'Time for A/C Maintenance'
            body = (
                f"Dear {appliance.customer.name},\n\n"
                "Your air conditioner is overdue for service. Kindly schedule an appointment promptly.\n\n"
                "Thank you,\n"
                "Easycool A/C service center\n"
                "Thrissur\n"
                "9447476035,9446576035"
            )
            send_due_email(subject=subject, body=body)
            messages.success(request, f"Mail has been successfully sent to {appliance.customer.name}")
            appliance.notified=True
            appliance.save()
            return redirect('duedate')
        else:
            messages.error(request, 'No customer found')
            return redirect('duedate')
       
        

class SignupView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name='registration.html'
    success_url=reverse_lazy('login')

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                messages.success(request,'You have been successfully Logged in. Welcome %s' %request.user)
                return redirect('home')
            else:
                messages.error(request,'Incorrect username/password')
                return render(request,'login.html',{'form':form})
            
@method_decorator(sign_in_required,name='dispatch')
class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        messages.success(request,'You have been succesfully logged out')
        return redirect('login')

# ajax view   (it always deals with json)
@sign_in_required
def get_capacities(request):
    selected_appliance = request.GET.get('appliance') #taking appliance from data passed through url get request (through ajax request. refer create_customer_to_appliance.html)
    capacities = Capacity.objects.filter(appliance_name=selected_appliance).values_list('id', 'name')
    types = Types.objects.filter(appliance_name=selected_appliance).values_list('id', 'name')
    data = {'capacities': dict(capacities),'types': dict(types)}
    return JsonResponse(data)


# pagination
@sign_in_required
def search_customer(request):
    search_query = request.GET.get('search_query', '')
    search_type=request.GET.get('search_type')

    # Fetch all customers
    customer_list = Customers.objects.all()

    # Filter customers based on the search query if provided
    if search_query and search_type.lower()=='name':
        customer_list = customer_list.filter(name__icontains=search_query)
    if search_query and search_type.lower()=='phone':
        customer_list = customer_list.filter(Q(phone1__icontains=search_query) | Q(phone2__icontains=search_query)) #performing or condition inside orm

    paginator = Paginator(customer_list.order_by('name'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer_list.html', {'customers': page_obj,'page_obj':page_obj,'query':search_query})

@method_decorator(sign_in_required,name='dispatch')
class HomeView(TemplateView):
    template_name='home.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['all_pending_complaints']=Complaints.objects.filter(status='pending')
        return context

@method_decorator(sign_in_required,name='dispatch')
class ServicedItems(ListView):
    model=Complaints
    context_object_name='complaints'
    template_name='serviced_list.html'

    def get_queryset(self):
        return Complaints.objects.exclude(status='pending')

@method_decorator(sign_in_required,name='dispatch')
class History(ListView):
    model=Complaints
    context_object_name='complaints'
    template_name='serviced_list.html'
    def get_queryset(self):
        id=self.kwargs.get('id')
        appliance_instance=Appliances.objects.get(id=id)
        return Complaints.objects.filter(appliance=appliance_instance)

@method_decorator(sign_in_required,name='dispatch')
class ListTechnician(ListView):
    model=Technicians
    context_object_name='technicians'
    template_name='tech_list.html'

@method_decorator(sign_in_required,name='dispatch')
class AddTechnician(CreateView):
    model=Technicians
    form_class=CreateTechnicianForm
    template_name='common_create_form.html'
    success_url=reverse_lazy('list_tech')

@method_decorator(sign_in_required,name='dispatch')
class EditTechnician(UpdateView):
    model=Technicians
    form_class=CreateTechnicianForm
    pk_url_kwarg='id'
    template_name='edit.html'
    success_url=reverse_lazy('list_tech')

@method_decorator(sign_in_required,name='dispatch')
class ListBrands(ListView):
    model=Brands
    context_object_name='brands'
    template_name='brands_list.html'

@method_decorator(sign_in_required,name='dispatch')
class AddBrand(CreateView):
    model=Brands
    form_class=CreateBrandForm
    template_name='common_create_form.html'
    success_url=reverse_lazy('brands_list')

@method_decorator(sign_in_required,name='dispatch')
class EditBrand(UpdateView):
    model=Brands
    form_class=CreateBrandForm
    pk_url_kwarg='id'
    template_name='edit.html'
    success_url=reverse_lazy('brands_list')

@method_decorator(sign_in_required,name='dispatch')
class ListCapacities(ListView):
    model=Capacity
    context_object_name='capacities'
    template_name='capacity_list.html'

@method_decorator(sign_in_required,name='dispatch')
class AddCapacity(CreateView):
    model=Capacity
    form_class=CreateCapacityForm
    template_name='common_create_form.html'
    success_url=reverse_lazy('capacity_list')

@method_decorator(sign_in_required,name='dispatch')
class EditCapacity(UpdateView):
    model=Capacity
    form_class=CreateCapacityForm
    pk_url_kwarg='id'
    template_name='edit.html'
    success_url=reverse_lazy('capacity_list')

@method_decorator(sign_in_required,name='dispatch')
class ListType(ListView):
    model=Types
    context_object_name='types'
    template_name='type_list.html'

@method_decorator(sign_in_required,name='dispatch')
class AddType(CreateView):
    model=Types
    form_class=CreateTypeForm
    template_name='common_create_form.html'
    success_url=reverse_lazy('type_list')

@method_decorator(sign_in_required,name='dispatch')
class EditType(UpdateView):
    model=Types
    form_class=CreateTypeForm
    pk_url_kwarg='id'
    template_name='edit.html'
    success_url=reverse_lazy('type_list')

@method_decorator(sign_in_required,name='dispatch')
class CustomerList(ListView):
    model=Customers
    context_object_name='customers'
    template_name='customer_list.html'
    paginate_by=10

@method_decorator(sign_in_required,name='dispatch')
class AddCustomer(CreateView):
    model=Customers
    form_class=CreateCustomerForm
    template_name='create_customer.html'
    success_url=reverse_lazy('add_customer')
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        try:
            # Save the form data to the database
            instance=form.instance.name
            messages.success(self.request, f'Customer, {instance} saved successfully')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Failed to save customer.{e}')
            return super().form_invalid(form)

@method_decorator(sign_in_required,name='dispatch')
class CustomerDetailView(DetailView):
    model=Customers
    pk_url_kwarg='id'
    template_name='customer_detail.html'
    context_object_name='customer'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['appliance_list']=Appliances.objects.filter(customer=self.get_object())
        return context
    
@method_decorator(sign_in_required,name='dispatch')
class FilterComComplaint(TemplateView):
    template_name='filter_com_complaint.html'

@method_decorator(sign_in_required,name='dispatch')
class ListCustomerComplaint(ListView):
    model=CommonComplaints
    context_object_name='com_complaints'
    template_name='com_compl_list.html'

    def get_queryset(self):
        if self.request.GET.get('filter')=='ac':
            return CommonComplaints.objects.filter(appliance='ac')
        elif self.request.GET.get('filter')=='rf':
            return CommonComplaints.objects.filter(appliance='refrigerator')
        elif self.request.GET.get('filter')=='wm':
            return CommonComplaints.objects.filter(appliance='washing_machine')
        return super().get_queryset()
    # to display create button for appropriate appliance com complatints in the listing template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_param'] = self.request.GET.get('filter')  # Pass the filter parameter to the template
        return context


@method_decorator(sign_in_required,name='dispatch')   
class AddCommonComplaint(CreateView):
    model=CommonComplaints
    form_class=CreateCommonComplaintForm
    template_name='common_create_form.html'
    # success_url=reverse_lazy('list_com_complaints')
    def form_valid(self, form):
        try:
            if self.request.GET.get('filter')=='ac':
                form.instance.appliance='ac'
                filter_value='ac'
            elif self.request.GET.get('filter')=='rf':
                form.instance.appliance='refrigerator'
                filter_value='rf'
            elif self.request.GET.get('filter')=='wm':
                form.instance.appliance='washing_machine'
                filter_value='wm'
            form.save()
            redirect_url = reverse('list_com_complaints') + f'?filter={filter_value}'
            return redirect(redirect_url)
        except:
            messages.error(self.request,'Already Exists')
            return render(self.request,'common_create_form.html',{'form':form})
        # return super().form_valid(form)
 
@method_decorator(sign_in_required,name='dispatch')
class AddCustomerAppliance(CreateView):
    model=Customers
    form_class=CreateCustomerForm
    template_name='create_customer_to_appliance.html'
    # success_url=reverse_lazy('')
    
    def form_valid(self, form):
        instance=form.save()#instance id only get after saving.but data passed through form can be accessible through form.instance.<fields>
        return redirect('add_appliance',id=instance.id)

@method_decorator(sign_in_required,name='dispatch')
class AddAppliance(CreateView):
    model=Appliances
    form_class=CreateApplianceForm
    template_name='create_customer_to_appliance.html'
    success_url=reverse_lazy('list_appliance')

    def form_valid(self, form):
        id=self.kwargs.get('id')
        customer_instance=Customers.objects.get(id=id)
        form.instance.customer=customer_instance
        instance=form.save()
        return redirect('register_complaint',cid=instance.customer.id,aid=instance.id)

@method_decorator(sign_in_required,name='dispatch')
class EditAppliance(UpdateView):
    model=Appliances
    form_class=CreateApplianceForm
    pk_url_kwarg='id'
    template_name='edit.html'
    # success_url=reverse_lazy('')
    def form_valid(self, form):
        instance=form.save()#instance id only get after saving.but data passed through form can be accessible through form.instance.<fields>
        return redirect('customer_details',id=instance.customer.id)

@method_decorator(sign_in_required,name='dispatch')
class ComplaintDetails(DetailView):
    model=Complaints
    pk_url_kwarg='id'
    template_name='complaint_detail.html'
    context_object_name='complaint'

@method_decorator(sign_in_required,name='dispatch')    
class RegisterComplaint(CreateView):
    model=Complaints
    form_class=CreateComplaintForm
    template_name='create_complaint_form.html'
    success_url=reverse_lazy('home')

# passing url data(aid) to the form __init__ method
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        aid = self.kwargs.get('aid')  # Extract appliance_id from URL kwargs
        kwargs['appliance_id'] = aid  # Pass appliance_id to the form
        return kwargs
    
    def form_valid(self, form):
        cid=self.kwargs.get('cid')
        customer_instance=Customers.objects.get(id=cid)
        aid=self.kwargs.get('aid')
        appliance_instance=Appliances.objects.get(id=aid)
        form.instance.customer=customer_instance
        form.instance.appliance=appliance_instance
        appliance_instance.notified=False
        appliance_instance.next_service_date=None
        appliance_instance.save()
        return super().form_valid(form)    

@method_decorator(sign_in_required,name='dispatch')
class UpdateComplaint(UpdateView):
    model=Complaints
    form_class=EditComplaintForm
    template_name='edit.html'
    pk_url_kwarg='id'
    # success_url=reverse_lazy('home')
    def form_valid(self, form):
        form_inst=form.save()
        form_inst.calc_next_service_date()
        
        return redirect('home')

@method_decorator(sign_in_required,name='dispatch')    
class UpdateCustomer(UpdateView):
    model=Customers
    form_class=EditCustomerForm
    template_name='edit.html'
    pk_url_kwarg='id'
    # success_url=reverse_lazy('customer_details')
    def form_valid(self, form):
        instance=form.save()#instance id only get after saving.but data passed through form can be accessible through form.instance.<fields>
        return redirect('customer_details',id=instance.id)


@method_decorator(sign_in_required,name='dispatch')
class DueDateView(ListView):
    model=Appliances
    context_object_name='appliances'
    template_name='appliance_list.html'

    def get_queryset(self):
        return Appliances.objects.filter(next_service_date__lte=datetime.now().date(),notified=False)


from django.urls import path
from easycool import views
urlpatterns=[
    path('signup',views.SignupView.as_view(),name='register'),
    path('',views.LoginView.as_view(),name='login'),
    path('signout',views.LogoutView.as_view(),name='signout'),
    path('home',views.HomeView.as_view(),name='home'),#@
    path('completed_services',views.ServicedItems.as_view(),name='serviced_items'),#@
    path('list_tech',views.ListTechnician.as_view(),name='list_tech'),#@
    path('add_tech',views.AddTechnician.as_view(),name='add_tech'),#@
    path('tech/<int:id>',views.EditTechnician.as_view(),name='edit_tech'),#@
    path('brands_list',views.ListBrands.as_view(),name='brands_list'),#@
    path('add_brand',views.AddBrand.as_view(),name='add_brand'),#@
    path('brand/<int:id>',views.EditBrand.as_view(),name='edit_brand'),#@
    path('add_capacity',views.AddCapacity.as_view(),name='add_capacity'),#@
    path('capacity_list',views.ListCapacities.as_view(),name='capacity_list'),#@
    path('capacity/<int:id>',views.EditCapacity.as_view(),name='edit_capacity'),#@
    path('add_type',views.AddType.as_view(),name='add_type'),#@
    path('type_list',views.ListType.as_view(),name='type_list'),#@
    path('type/<int:id>',views.EditType.as_view(),name='edit_type'),#@
    path('customers',views.CustomerList.as_view(),name='customer_list'),#@
    path('customer/<int:id>',views.CustomerDetailView.as_view(),name='customer_details'),#@
    path('customer/<int:id>update',views.UpdateCustomer.as_view(),name='edit_customer'),#@
    path('add_customer',views.AddCustomer.as_view(),name='add_customer'),#@
    path('add_customer_appliance',views.AddCustomerAppliance.as_view(),name='add_customer_appliance'),#@
    path('customer/<int:id>/add_appliances',views.AddAppliance.as_view(),name='add_appliance'),#@
    path('appliance/<int:id>',views.EditAppliance.as_view(),name='edit_appliance'),#@
    path('customer/<int:cid>/appliance/<int:aid>/register_complaint',views.RegisterComplaint.as_view(),name='register_complaint'),#@
    path('edit_complaint/<int:id>',views.UpdateComplaint.as_view(),name='edit_complaint'),#@
    path('complaint/<int:id>',views.ComplaintDetails.as_view(),name='complaint_detail'),#@
    path('filter_com_complaint',views.FilterComComplaint.as_view(),name='filter_com_complaint'),#@
    path('com_complaints',views.ListCustomerComplaint.as_view(),name='list_com_complaints'),  #@
    path('add_com_complaints',views.AddCommonComplaint.as_view(),name='add_com_complaints'),#@
    path('appliance/<int:id>/previous_history',views.History.as_view(),name='history'),#@
    path('due_date',views.DueDateView.as_view(),name='duedate'),#@
    path('due_date/<int:id>/send_mail',views.SendEmailView.as_view(),name='send_mail'),#@ sending mail
    path('customer/search',views.search_customer,name='search_customer_names'),#@
    path('get-capacities/', views.get_capacities, name='get_capacities'),  # URL for getting capacities via AJAX,#@

    # path('customer/<int:id>/appliance/<int:id>/',views. .as_view(),name='edit'), #edit appliance to customer in customrdetails page
    # path('customer/<int:id>/appliance',views. .as_view(),name='servic_history'), #servicehistory in customrdetails page   ?a,cooler,washing

]
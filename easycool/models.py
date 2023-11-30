from django.db import models
from datetime import timedelta
from datetime import datetime

class Customers(models.Model):
    name=models.CharField(max_length=100)
    address=models.TextField()
    place=models.CharField(max_length=60)
    phone1=models.CharField(max_length=15)
    phone2=models.CharField(max_length=15,null=True,blank=True)
    email=models.EmailField(null=True,blank=True)

    #Setting editable=False means that the field value can't be modified via forms or the admin interface. It's still accessible programmatically and can be modified in code.
    def __str__(self):
        return self.name

class Brands(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Technicians(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Capacity(models.Model):
    name=models.CharField(max_length=100)
    choices=(
        ('ac','A/C'),
        ('refrigerator','Refrigerator'),
        ('washing_machine','Washing Machine'),
    )
    appliance_name=models.CharField(max_length=100,choices=choices,default='ac',verbose_name='Appliance')

    def __str__(self):
        return self.name
    
class Types(models.Model):
    name=models.CharField(max_length=100)
    choices=(
        ('ac','A/C'),
        ('refrigerator','Refrigerator'),
        ('washing_machine','Washing Machine'),
    )
    appliance_name=models.CharField(max_length=100,choices=choices,default='ac',verbose_name='Appliance')

    def __str__(self):
        return self.name

class Appliances(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.PROTECT)
    choices=(
        ('ac','A/C'),
        ('refrigerator','Refrigerator'),
        ('washing_machine','Washing Machine'),
    )
    appliance_name=models.CharField(max_length=100,choices=choices,default='ac')
    brand=models.ForeignKey(Brands,on_delete=models.PROTECT,null=True,blank=True)
    inverter=models.BooleanField(default=False)
    fully_automatic=models.BooleanField(default=False)
    type=models.ForeignKey(Types,on_delete=models.PROTECT,null=True,blank=True)
    capacity=models.ForeignKey(Capacity,on_delete=models.PROTECT,null=True,blank=True)
    next_service_date=models.DateField(null=True,editable=False)
    notified=models.BooleanField(null=True,editable=False,default=False)

    def __str__(self):
        return self.appliance_name
    
class CommonComplaints(models.Model):
    choices=(
        ('ac','A/C'),
        ('refrigerator','Refrigerator'),
        ('washing_machine','Washing Machine'),
    )
    appliance=models.CharField(max_length=100,choices=choices,default='ac')
    complaint=models.CharField(max_length=100)
    class Meta:
        unique_together=("appliance","complaint")
    
    def __str__(self):
        return self.complaint

class Complaints(models.Model):
    customer=models.ForeignKey(Customers,on_delete=models.PROTECT)
    appliance=models.ForeignKey(Appliances,on_delete=models.PROTECT)
    common_complaint=models.ForeignKey(CommonComplaints,on_delete=models.PROTECT,verbose_name='complaint')
    choices=(
        ('new','New'),
        ('rework','Re-work'),
    )
    complaint_type=models.CharField(max_length=60,choices=choices,default='new')
    complaint_date=models.DateTimeField(auto_now_add=True)

    technician=models.ForeignKey(Technicians,on_delete=models.SET('technician_deleted'),null=True,blank=True)

    choices=(
        ('pending','Pending'),
        ('parts_pending','parts_pending'),
        ('completed','Completed'),
    )
    status=models.CharField(max_length=60,choices=choices,default='pending')
    rectified_date=models.DateField(null=True,blank=True)
    rectified_issue=models.TextField(null=True,blank=True)
    note=models.TextField(null=True,blank=True)
    remarks=models.TextField(null=True,blank=True)
    bill_amt=models.CharField(max_length=60,null=True,blank=True)
    bill_no=models.CharField(max_length=100,null=True,blank=True)

    def calc_next_service_date(self):
        if self.rectified_date and self.appliance.appliance_name=='ac':
            self.appliance.next_service_date=self.rectified_date+timedelta(30*6)
            return self.appliance.save()
        elif not self.rectified_date:
            self.appliance.next_service_date=None
            return self.appliance.save()
    

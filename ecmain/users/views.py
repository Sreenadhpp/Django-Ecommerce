from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Customer

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render (request, 'users/customer_registration.html', locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            messages.success(request, f'{username}! Your acccount has been created! You are now able to Login')
            return redirect('login')
        else:
            messages.warning(request, "Invalid input data")
        return render (request, 'users/customer_registration.html', locals())



class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'users/profile.html',locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.create(
            user=request.user,
            name = form.cleaned_data['name'],
            locality = form.cleaned_data.get('locality'),
            city = form.cleaned_data['city'],
            mobile = form.cleaned_data['mobile'],
            zipcode = form.cleaned_data['zipcode'],
            state = form.cleaned_data['state']
            )
            # customer = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, zipcode=zipcode, state=state )
            # customer.save()
            messages.success(request, "Congradulations! Profile Save Successfuly")
            return redirect('address')
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'users/profile.html', locals())



@login_required
def address(request):
    address = Customer.objects.filter(user = request.user)
    return render(request, 'users/address.html', locals())



class UpdateAddress(LoginRequiredMixin, View):
    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        form = CustomerProfileForm(instance=customer)
        return render(request, 'users/updateaddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(id=pk)
            customer.name = form.cleaned_data['name']
            customer.locality = form.cleaned_data['locality']
            customer.city = form.cleaned_data['city']
            customer.mobile = form.cleaned_data['mobile']
            customer.state = form.cleaned_data['state']
            customer.zipcode = form.cleaned_data['zipcode']
            customer.save()
            messages.success(request, "Congradulations! Profile Update successfully")
        else:
            messages.warning(request, "invalid Input Data")
        return redirect('address')
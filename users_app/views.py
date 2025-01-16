from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomRegisterForm
from django.contrib.auth import logout
from django.views import View

# Create your views here.
def register(request):
    if request.method == "POST":
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, ("Your account has been created!"))
            return redirect('login')
    else:
        register_form = CustomRegisterForm()
    return render(request, 'register.html', {'register_form': register_form})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, ("You have been logged out!"))
        return redirect('index')
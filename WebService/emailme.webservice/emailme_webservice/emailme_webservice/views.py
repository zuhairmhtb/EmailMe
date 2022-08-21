import os
from django.shortcuts import render, redirect

from .forms import EmailForm


def home(request):
    form = EmailForm()
    message = ""
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            print("Sending data to email service")
            message = f"You have successfully sent an email to {form.cleaned_data['recipient']}"
            form = EmailForm()
        
    return render(request, 'emailme_webservice/index.html', {
        'form': form,
        'title': 'Home',
        'message': message
    })
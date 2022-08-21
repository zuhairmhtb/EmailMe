import os
from django.shortcuts import render, redirect
from emailme_emailservice.commands.email_command import EmailCommand

from .forms import EmailForm
from .settings import framework

def home(request):
    form = EmailForm()
    message = ""
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            print("Sending data to email service")
            framework.publish_message(EmailCommand(
                body=form.cleaned_data["body"], 
                subject=form.cleaned_data["subject"], 
                recipient=form.cleaned_data["recipient"]
                ))
            message = f"You have successfully sent an email to {form.cleaned_data['recipient']}"
            form = EmailForm()
        
    return render(request, 'emailme_webservice/index.html', {
        'form': form,
        'title': 'Home',
        'message': message
    })
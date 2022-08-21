from django import forms

class EmailForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the email subject',
        'required': 'required'
    }))

    body = forms.CharField(label='Body', max_length=1000, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the message content here...',
        'required': 'required'
    }))

    recipient = forms.CharField(label='Subject', max_length=100, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter recipient email',
        'required': 'required'
    }))
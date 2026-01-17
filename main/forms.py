from django import forms
from .models import ContactMessage, NewsletterSubscriber, Testimonial, Donation


class ContactForm(forms.ModelForm):
    """Form for contact page"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'inquiry_type', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Phone (Optional)'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Message',
                'rows': 5
            }),
        }


class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscription"""
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Enter your email'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Name (Optional)'
            }),
        }


class TestimonialForm(forms.ModelForm):
    """Form for submitting testimonials"""
    class Meta:
        model = Testimonial
        fields = ['name', 'organization', 'testimonial_type', 'content', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Name'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Organization (Optional)'
            }),
            'testimonial_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Share your experience with us...',
                'rows': 5
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
        }


class DonationForm(forms.ModelForm):
    """Form for donations"""
    class Meta:
        model = Donation
        fields = ['donor_name', 'donor_email', 'donor_phone', 'amount', 'payment_method', 'purpose', 'partner', 'is_recurring', 'is_anonymous']
        widgets = {
            'donor_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Name'
            }),
            'donor_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Email'
            }),
            'donor_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Your Phone'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Amount (PKR)',
                'min': '100'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Purpose of donation (Optional)'
            }),
            'partner': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500'
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded'
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded'
            }),
        }

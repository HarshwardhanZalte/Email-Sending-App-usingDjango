from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from . models import euser


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            return redirect('email')
        else:
            return redirect('login')
    return render(request,'login.html')


def mailall(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        file = request.FILES['file']
        email_addresses = euser.objects.values_list('email', flat=True)
        for email_address in email_addresses:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email_address],
            )
            email.attach(file.name, file.read(), file.content_type)
            email.send()
        return redirect('mailall')
    return render(request, 'mailall.html')


def email(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        file = request.FILES['file']
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
        )
        email.attach(file.name, file.read(), file.content_type)
        email.send()
    return render(request, 'email.html')


def adduser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        new_user = euser(name = name, email = email)
        new_user.save()
    return render(request, 'adduser.html')


def display(request):
    bk = euser.objects.all()
    data= {
        'users' : bk
    }
    return render(request,'display.html',data)


def delete(request, id):
    dele = euser.objects.get(id = id)
    dele.delete()
    return redirect('display')


def update(request,id):
    up = euser.objects.get(id = id)
    if request.method == 'POST':
        id = request.POST.get('id')
        up.name = request.POST.get('name')
        up.email = request.POST.get('email')
        up.save()
        return redirect('display')
    return render(request,'updateuser.html',{'user':up})

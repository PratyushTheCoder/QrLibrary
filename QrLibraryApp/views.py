from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
import qrcode
import time
from datetime import datetime
from .models import QrCode

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Account registered, Please login')
            redirect("login")

    context = {"form": form}
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    user = request.user
    name = user.username
    messages.success(request, f"Welcome {name}, you are logged in")
    context = {
        "name": name,
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='login')
def profile(request):
    name = request.user.username
    email = request.user.email
    last_login = request.user.last_login
    date_joined = request.user.date_joined
    admin_stat = request.user.has_perm("admin")
    super_user_stat = request.user.has_perm("superuser")
    # expiry=request.user.date_expiry
    context = {"username": name,
               "email": email,
               "last_login": last_login,
               "date_joined": date_joined,
               "admin_stat": admin_stat,
               "super_user_stat": super_user_stat
               #  "expiry":expiry
               }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def change_password(request):
    username = request.user.username
    context = {
        'username': username
    }
    if request.method == "POST":
        u = User.objects.get(username__exact=username)
        if request.POST.get('new_password') == "":
            messages.error(request, "Password cannot be empty")
            # messages.warning(request,"Test")
        elif request.POST.get('new_password') == request.POST.get('confirm_password'):
            u.set_password(request.POST.get('new_password'))
            u.save()
            messages.success(
                request, "Password Changed Sucessfully, Please Login Again")
            return redirect("profile")
        else:
            messages.error(request, "Password does not match")
    return render(request, 'change_password.html', context)


@login_required(login_url='login')
def qrcode_manage(request):
    return render(request, '_manager.html')


@login_required(login_url='login')
def qrcode_create(request):
    now=datetime.now()
    ct=now.strftime("%H#%M$%S")
    if request.method == "POST":
        name = request.POST['name']
        location = request.POST['loc']
        qty = request.POST['qty']
        other = request.POST['other']
        special_code=name+ct
        data=f"Material Name:{name}, Material Location:{location}, Material Code:{special_code}, Material Qty:{qty}"
        img=qrcode.make(data)
        img_name='qr'+str(time.time())+'.png'
        img.save(settings.QR_CODE_DIR + '/' + img_name)
        context={
            "img_name":img_name
        }
        d=QrCode(material_name=name,material_location=location,material_qty=qty,material_other=other,material_special_code=special_code)
        d.save()
        return render(request, '_create.html', context)
        
    return render(request, '_create.html')
@login_required(login_url='login')
def qrcode_search(request):
    if request.method == 'POST':
        query=request.POST['query']
        # print(QrCode.objects.get(material_special_code=query))
        d=QrCode.objects.filter(material_special_code=query).values('material_name','material_location','material_qty','material_other')[0]
        context={
            'name':d['material_name'],
            'loc':d['material_location'],
            'qty':d['material_qty'],
            'other':d['material_other']
        }
        return render(request,'_search.html',context)
    return render(request,'_search.html')

from django.shortcuts import render, redirect
from .forms import SignUpForm, UpdateUserData
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Create your views here.
def home(request):
    return render(request, './home.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Account Created Successfully!')
                form.save()
                return redirect('login')
        else:
            form = SignUpForm()
        return render(request, './signup.html', {'form': form})
    else:
        return redirect('profile')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully!')
                return redirect('profile')            
    else:
        form = AuthenticationForm()
    return render(request, './login.html', {'form': form})

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUserData(request.POST, instance=request.user)
            if form.is_valid():
                messages.success(request, 'Account Updated Successfully')
                form.save()
        else:
            form = UpdateUserData(instance=request.user)
        return render(request, './profile.html', {'form': form})
    else:
        return redirect('signup')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return redirect('home')

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                messages.success(request, 'Password Changed Successfully!')
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})
    else:
        return redirect('login')

def forgot_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                messages.success(request, 'Forgot Password Successfully!')
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request, 'forgot_password.html', {'form': form})
    else:
        return redirect('login')

def update_user_date(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUserData(request.POST, instance=request.user)
            if form.is_valid():
                messages.success(request, 'Account Updated Successfully!')
                form.save()
                print(form.cleaned_data)
        else:
            form = UpdateUserData()
        return render(request, 'profile.html', {'form': form})
    else:
        return redirect('signup')
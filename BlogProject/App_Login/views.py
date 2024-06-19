from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError  
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import  SingUpForm,UserProfileChange,ProfilePIC
# Create your views here.
def SignUp(request):
    # form = UserCreationForm()
    form =SingUpForm()
    registered = False
    if request.method == "POST":
        # form = UserCreationForm(data=request.POST)
        if form.is_valid():
            try:
                user = form.save()  # Attempt to save the user
                login(request, user)  # Optional: Log in the newly created user
                registered = True
                print(user)  # Print the newly created user object (optional)
            except IntegrityError as e:
                if 'username' in str(e):  # Check if error is due to duplicate username
                    form.add_error(field_name='username', error='Username already exists')
                else:
                    raise e  # Re-raise other IntegrityErrors

    context = {'form': form, 'registered': registered}
    return render(request, 'App_Login/signup.html', context=context)

# views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

def LoginPage(request):
    form = AuthenticationForm()
    dict={'form':form}
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
    # Handle invalid credentials with a specific error message
                error_message = 'Invalid username or password.'  # You can customize this message
    # Or use form.errors to capture specific errors
    # error_message = form.errors.as_text()  # Uncomment if needed
                dict.update({'error_message': error_message})
                return render(request, 'App_Login/login.html', context=dict)
    return render(request, 'App_Login/login.html', context={'form': form})
@login_required
def LogoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def Profile(request):
    return render(request,'App_Login/profile.html')

@login_required
def UserChange(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method =="POST":
        form = UserProfileChange(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            form= UserProfileChange(instance=current_user)
    return render(request,'App_Login/changeprofile.html',context={'form':form})

@login_required
def PassChange(request):
    current_user = request.user
    changed= False
    form = PasswordChangeForm(current_user)
    if request.method =="POST":
        form = PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            changed=True
    return render(request,'App_Login/change_pass.html',context={'form':form,'changed':changed})

@login_required
def add_profile(request):
    form = ProfilePIC()
    if request.method =="POST":
        form = ProfilePIC(request.POST,request.FILES)
        if form.is_valid():
            user_obj=form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'App_Login/profilepic.html',context={'form':form})

@login_required
def change_pro_pic(request):
    form = ProfilePIC(instance=request.user.user_profile)
    if request.method =="POST":
        form = ProfilePIC(request.POST,request.FILES,instance=request.user.user_profile)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'App_Login/profilepic.html',context={'form':form})


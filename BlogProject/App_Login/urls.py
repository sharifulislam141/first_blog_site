from django.urls import path
from . import views
app_name = 'App_Login'
urlpatterns = [
    path('signup/',views.SignUp,name='signup'),
    path('login/',views.LoginPage,name='loginpage'),
    path('profile/',views.Profile,name='profile'),
    path('logout/',views.LogoutUser,name='logoutpage'),
    path('change_profile/',views.UserChange,name='changeprofile'),
    path('password/',views.PassChange,name='changepass'),
    path('add_picture/',views.add_profile,name='add_profile'),
    path('change_picture/',views.change_pro_pic,name='change_profile'),

 
]

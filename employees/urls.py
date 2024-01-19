
from django.urls import path
from .import views 

urlpatterns = [
    path('',views.loginpage,name='login'),
    path('signup/',views.signuppage,name='signup'),
    path('home/',views.homepage,name='home'),
    path('logout/',views.logoutbutton,name='logout'),
    
    path('adminlogin/',views.adminloginpage,name='adminlogin'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('adminhome/',views.adminhomepage,name='adminhome'),

    path('add/',views.add,name='add'),
    path('edit/',views.edit,name='edit'),
    path('update/<str:id>',views.update,name='update'),
    path('delete/<str:id>',views.delete,name='delete'),
    path('search/',views.search,name='search'),
    path('alert/',views.alert,name='alert')



]




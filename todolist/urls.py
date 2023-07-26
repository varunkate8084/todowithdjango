"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import ActionsController

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainpagetodo/',ActionsController.Action_Main_Page),
    path('submitworkapi',ActionsController.submit_work),
    path('displayworktodo/',ActionsController.Display_All_Work),
    path('editworklisttodo/',ActionsController.Edit_worklist),
    path('deleteworkapi/',ActionsController.Delet_Work),


#     Urls For LogIn and ReGistration
    path('logintodo/',ActionsController.Action_LogIn_Page),
    path('registration/',ActionsController.Action_Registration_Page),
    path('submitregistrationapi',ActionsController.submit_Registration_Record),
    path('checkloginapi',ActionsController.Check_LogIn),
    path('logout/',ActionsController.Log_Out),



]

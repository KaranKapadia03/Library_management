"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from book_management import views
from book_management.views import export_to_excel


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.user_login,name='login'),
    # path('',views.index.as_view(),name="index"),
    path('r/', include('book_management.urls'),name='i'),
    path('logout/',views.user_logout,name="logout"),
    path('export-to-excel/', export_to_excel, name='export_to_excel'),
]




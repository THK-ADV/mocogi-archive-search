"""
URL configuration for modules project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from modules import views

urlpatterns = [
    path("", views.get_template_view, name="get-temp"),
    path('courses/', views.get_courses_view.as_view(), name='item-detail'),
    path('data/', views.get_course_data_view.as_view(), name='item-detail'),

]

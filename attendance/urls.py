"""proj3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.start),
    url(r'^login/', views.login),
    url(r'^forgot_password/', views.forgot_password),
    url(r'^otp/', views.otp),
    url(r'^change_password/', views.change_password),
    url(r'^logout/', views.logout),

    url(r'^register_teacher/', views.register_teacher),
    url(r'^register_student/', views.register_student),

    url(r'^student_profile/', views.student_profile),
    url(r'^fee_summary/', views.fee_summary),
    url(r'^activities/', views.activities),
    url(r'^student_dashboard/', views.student_dashboard),

    url(r'^teacher_dashboard/', views.teacher_dashboard),
    url(r'^check_if_present/', views.check_if_present),
    url(r'^mark_attendance/', views.mark_attendance),
    url(r'^store_attendance/', views.store_attendance),
    url(r'^calculate_attendance/', views.calculate_attendance),
    url(r'^show_students/', views.show_students),
    url(r'^show_classes/', views.show_classes),

    url(r'^weekly_stats/', views.weekly_stats),

    url(r'^parent_dashboard/', views.parent_dashboard),
    url(r'^parent_profile/', views.parent_profile),

    url(r'^head_dashboard/', views.head_dashboard),
    url(r'^all_teachers/', views.all_teachers),
    url(r'^all_students/', views.all_students),
    url(r'^time_table/', views.time_table),

]

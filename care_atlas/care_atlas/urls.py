"""
URL configuration for care_atlas project.

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
from users import views as users_views
from base import views as base_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('home/', include('base.urls')),
    path('users/register/', users_views.register, name='register'),
    path('users/login/', users_views.login_page, name='login'),
    path('users/logout/', users_views.logout_page, name='logout'),
    path('base/application_home/', base_views.application_home_page, name='application-home'),
    path('base/application_patient_page/<int:page>', base_views.application_patient_page, name='application-page'),
    path('base/new_patient', base_views.new_patient_page, name='new-patient'),
    path('base/new_patient_vital/<int:patient_id>', base_views.new_patient_vital_page, name='new-patient-vital'),
    path('base/new_patient_record/<int:patient_id>', base_views.new_patient_record_page, name='new-patient-record'),
    path('base/patient/<int:patient_id>', base_views.patient_page, name='patient-page'),
    path('base/edit_patient_record/<int:patient_id>/<int:record_id>', base_views.edit_patient_record_page, name='edit-patient-record'),
    path('base/edit_vitals_record/<int:patient_id>/<int:vital_id>', base_views.edit_vitals_page, name='edit-vitals-record'),
    path('base/patient_vitals/<patient_id>', base_views.patient_vitals_page, name='patient-vitals-page'),
    path('base/medical_record/<patient_id>/<record_id>', base_views.medical_record_page, name='medical-record-page'),
    path('base/bill_patient/<patient_id>/<record_id>', base_views.bill_patient_page, name='bill-patient'),
    path('base/patient_bill/<patient_id>/<record_id>/<bill_id>', base_views.patient_bill_page, name='patient-bill-page'),
    path('base/edit_patient_bill/<patient_id>/<record_id>/<bill_id>', base_views.edit_patient_bill_page, name='edit-patient-bill'),
    path('base/bills/<int:page>/', base_views.bills_page, name='bills-page'),
    path('base/records/<int:page>/', base_views.records_page, name='records-page'),
    path('base/search/<int:page>/', base_views.search_page, name='search-page'),
    path('base/search/<int:page>/<str:search_string>/', base_views.search_page, name='search-page'),
    path('users/user_profile_page/', users_views.user_profile_page, name='profile-page'),
    path('users/edit_profile_page', users_views.edit_user_profile_page, name='edit-profile-page'),
    path('base/order_tests_page/<int:patient_id>', base_views.order_tests_page, name='order-tests'),
    path('base/update_investigations_page/<int:patient_id>/<int:record_id>', base_views.investigations_update_page, name='investigations-update'),
    path('base/delete_attachment/<int:patient_id>/<int:record_id>/<path:attachment>', base_views.delete_attachment, name='delete-attachment')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
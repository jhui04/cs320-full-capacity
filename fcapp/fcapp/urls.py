"""fcapp URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_mongoengine import routers
from fcapp.main.viewset import (DeviceViewSet, StatusViewSet, TenantViewSet,
    DefaultStatusViewSet, TriggeredStatusViewSet, AllDeviceViewSet, AllStatusViewSet,
    AllTenantViewSet)
from fcapp.main.api_views import DeviceDetail, StatusDetail

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet, base_name='device')
router.register(r'status', StatusViewSet, base_name='status')
router.register(r'triggered_status', TriggeredStatusViewSet, base_name='triggered_status')
router.register(r'tenant', TenantViewSet, base_name='tenant')

router.register(r'all_devices', AllDeviceViewSet, base_name='all_device')
router.register(r'all_status', AllStatusViewSet, base_name='all_status')
router.register(r'default_status', DefaultStatusViewSet, base_name='default_status')
router.register(r'all_tenant', AllTenantViewSet, base_name='all_tenant')
from fcapp.main import views as main

admin.site.site_header = 'Full Capacity Storage'
admin.site.index_title = 'Site Administration'
admin.site.site_title = 'Full Capacity Storage'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main.home_view, name='home-view'),
    url(r'^test/', main.test_view, name='test-view'),
    url(r'^api/devices/(?P<pk>.*)/', DeviceDetail.as_view(), name='device-detail'),
    url(r'^api/status/(?P<pk>.*)/', StatusDetail.as_view(), name='status-detail'),
    
    url(r'^api/', include(router.urls)),
    url(r'^login/', main.login_view, name='login-view'),
    url(r'^logout/', main.logout_view, name='logout-view'),
    
]

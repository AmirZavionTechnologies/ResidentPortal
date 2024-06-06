from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet,LoginAPI,GetUserData,VehicleViewSet,GuardSearchVehicleByEntryCode, VisitorViewSet, GuardViewSet, ResidentByEntryCode, GuardSearchResidentByEntryCode

router = DefaultRouter()
router.register(r'residents', ResidentViewSet)
router.register(r'visitors',VisitorViewSet)
router.register(r'guards',GuardViewSet)
router.register(r'vehicleset', VehicleViewSet)


urlpatterns = [
    path('', views.home, name='home'),
    path('', include(router.urls)),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('api/login/', LoginAPI.as_view(), name='login_api'),
    path('api/user/',GetUserData.as_view()),
    path('resident/<str:entry_code>/', ResidentByEntryCode.as_view(), name='resident-by-apartment-number'),
    path('guards/search-resident/<str:entry_code>/', GuardSearchResidentByEntryCode.as_view(), name='guard-search-resident'),
    path('guards/search-vehicle/<str:entry_codes>/', GuardSearchVehicleByEntryCode.as_view(), name='guard-search-resident'),
]

from django.contrib import admin
from django.urls import path

from ads.views import AdListView, AdCreateView, MyAdsView, AdDetailView, AdUpdateView, AdDeleteView
from ads.views import MyExchangesView, CreateExchangeView, AcceptExchangeView
from ads.views import CustomLoginView, register_view, logout_view



urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('', AdListView.as_view(), name='ad_list'),
    # path('new/', AdCreateView.as_view(), name='ad_create'),  #юзлес
    path('my-ads/', MyAdsView.as_view(), name='my_ads'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),

    path('ad/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_edit'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),

    path('my-exchanges/', MyExchangesView.as_view(), name='my_exchanges'),
    path('ad/<int:ad_id>/exchange/', CreateExchangeView.as_view(), name='create_exchange'),
    path('exchange/<int:pk>/accept/', AcceptExchangeView.as_view(), name='accept_exchange'),

]

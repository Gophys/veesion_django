from django.urls import path
from . import views

urlpatterns = [
    path('webhooks/alerts/', views.AlertWebhookView.as_view(), name='alert-webhook'),
    
    # API endpoints for listing and creating resources
    path('users', views.UserListView.as_view(), name='user-list-create'),
    path('stores/', views.StoreListView.as_view(), name='store-list-create'),
    path('subscriptions/', views.UserAlertSubscriptionListView.as_view(), name='subscription-list-create'),
    path('notifications/', views.SentNotificationListView.as_view(), name='notification-list-create'),
    path('alerts/', views.AlertListView.as_view(), name='alert-list-create'),
]

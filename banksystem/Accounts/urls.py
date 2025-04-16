from django.urls import path
from .views import AccountCreateView, AccountListView, AccountDetailView

urlpatterns = [
    path('create/', AccountCreateView.as_view(), name='create-account'),
    path('all-account/', AccountListView.as_view(), name='list-account'),
    path('detail/', AccountDetailView.as_view(), name='account-detail'),
]

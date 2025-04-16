from django.urls import path
from .views import BankListView, BranchListView

urlpatterns = [
    path('', BankListView.as_view(), name='bank-list'),
    path('<str:bank_code>/branches/', BranchListView.as_view(), name='branch-list'),
]
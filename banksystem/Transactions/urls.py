from django.urls import path
from .views import TransactionProcess, TransactionHistoryView

urlpatterns = [
    path('transfer/', TransactionProcess.as_view(), name='transfer'),
    path('history/', TransactionHistoryView.as_view(), name='transaction-history'),
]

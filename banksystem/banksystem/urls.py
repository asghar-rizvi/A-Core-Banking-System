from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls')),
    path('banks/', include('Banks.urls')),
    path('accounts/', include('Accounts.urls')),
    path('transactions/', include('Transactions.urls')),
]

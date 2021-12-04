from django.urls import path
from authentication.views import SignUpView, ProfileView, HomeView, EditUserProfileView, InvoiceView, InvoiceListView, InvoiceDetailView
from django.contrib.auth.views import LoginView, LogoutView

app_name='authentication'

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/profile/', EditUserProfileView.as_view(), name='profile'),
    path('create/invoice/', InvoiceView.as_view(), name='create_invoice'),
    path('invoice/list/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice/detail/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('home/', HomeView.as_view(), name='home'),

    path('', LoginView.as_view(), name='login')
]

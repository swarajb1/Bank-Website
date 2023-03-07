from django.urls import path
from . import views

app_name = "transaction"

urlpatterns = [
    path('coins_transfer/', views.coins_transfer_view, name="coins_transfer"),
    
    
    path('transaction/', views.transaction_view, name="transaction"),

    path('transaction_history/', views.transaction_history_view, name="transaction_history"),
    path('transaction_charges/', views.transaction_charges_view, name="transaction_charges"),
    path('annual_charges/', views.annual_charges_view, name="annual_charges"),


    path('coins_circulation/', views.coins_circulation_view, name="coins_circulation"),
    
    path('ttt/', views.trail_transactions_view, name="trail"),

]
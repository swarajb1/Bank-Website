from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.registration_view, name="register"),

    # logo
    path('account/', views.account_view, name="account"),


    # top nav
    path('deposits/', views.deposits_view, name="deposits"),
    path('services/', views.services_view, name="services"),

    # sidebar nav
    
    path('beneficiary_add/', views.beneficiary_add_view, name="beneficiary_add"),
    path('beneficiary_view/', views.beneficiary_view_view, name="beneficiary_view"),

    # other links
    path('change_password/', views.change_password_view, name="change_password"),
    path('session_summary/', views.session_summary_view, name="session_summary"),
    path('site_map/', views.site_map_view, name="site_map"),

    
    path('initialise/', views.initialise_view, name="initialise"),


    
    path('sorry/', views.sorry_view, name="sorry"),
]
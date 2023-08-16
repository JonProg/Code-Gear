from django.urls import path
from perfil import views

app_name='perfil'

urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('enderecos/', views.Enderecos.as_view(), name='adress'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]

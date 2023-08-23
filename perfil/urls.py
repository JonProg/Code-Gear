from django.urls import path
from perfil import views

app_name='perfil'

urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('endereco/update', views.EnderecoUpdate.as_view(), name='adress_update'),
    path('endereco/create', views.EnderecoCreate.as_view(), name='adress_create'),
    path('endereco/delete', views.EnderecoDelete.as_view(), name='adress_delete'),
]

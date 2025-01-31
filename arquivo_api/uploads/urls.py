from . import views
from django.urls import path
from django.urls import path


urlpatterns = [
    path('upload/', views.carregar_arquivo, name='carregar_arquivo'),
    path('history/', views.historia_arquivo, name='historia_arquivo'),
    path('search/', views.pesquisar_conteudo_arquivo, name='pesquisar_conteudo_arquivo'),
]
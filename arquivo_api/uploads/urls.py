from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include  # Aqui estamos importando o 'include' para incluir as URLs da app 'file_upload'


urlpatterns = [
    path('upload/', views.carregar_arquivo, name='carregar_arquivo'),
    path('history/', views.historia_arquivo, name='historia_arquivo'),
    path('search/', views.pesquisar_conteudo_arquivo, name='pesquisar_conteudo_arquivo'),
    path('admin/', admin.site.urls),
    path('api/uploads/', include('uploads.urls')),
]

'''

1. Configuração do Projeto Django
Primeiro, você precisa criar um novo projeto Django e uma nova aplicação. Execute os seguintes comandos:
Code
django-admin startproject arquivo_api
cd arquivo_api
django-admin startapp uploads

1. Instalação de Dependências
Certifique-se de que você tem o Django e o Django REST Framework instalados. 

Você pode instalar usando o pip:Codepip install django djangorestframework pandas openpyxl


último passo. Migrar e Rodar o Servidor
Agora, faça a migração e inicie o servidor:
Code
python manage.py makemigrations uploads
python manage.py migrate
python manage.py runserver

'''
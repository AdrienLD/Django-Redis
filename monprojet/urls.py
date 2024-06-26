from django.contrib import admin
from django.urls import path
import monapp.views
import monapp.initial_config

urlpatterns = [
    path('admin/', admin.site.urls),
    path('initialize/', monapp.initial_config.initialize, name='initialize'),
    path('manage/select', monapp.views.select_student, name='select_student'),
    path('manage/<int:id_etudiant>', monapp.views.manage_student, name='manage_student'),
    path('delete_cours/<int:id_etudiant>/<int:id_cours>', monapp.views.delete_cours, name='delete_cours'),
    path('add_cours/<int:id_etudiant>/<int:id_cours>', monapp.views.add_cours, name='add_cours'),
    path('subscribe_cours/<int:id_etudiant>/<int:id_cours>', monapp.views.subscribe_cours, name='subscribe_cours'),
    #path('update', monapp.views.update, name='update'),
    path('rechercher', monapp.views.rechercher, name='rechercher'),
    path('messages/<int:id_etudiant>/<int:id_cours>', monapp.views.messages, name='messages'),
]

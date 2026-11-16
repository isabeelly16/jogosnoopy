
from django.contrib import admin
from django.urls import path
from ranking import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/status/", views.status, name="api_status"),
    path("api/pontuacao/", views.salvar_pontuacao, name="salvar_pontuacao"),
    path("api/ranking/", views.ranking, name="ranking"),
]

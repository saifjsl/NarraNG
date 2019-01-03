from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:project_id>/<int:entry_id>/', views.entry, name='entry'),
    path('<str:project_name>/<int:project_id>/create_entry/', views.create_entry, name='create_entry'),
    path('<int:project_id>/new/<str:entry_name>', views.new_entry, name='new_entry'),
    path('<int:project_id>/save_entry', views.save_entry, name='save_entry')
]

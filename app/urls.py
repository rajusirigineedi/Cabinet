from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('<int:app_id>/', views.showproject, name='show'),
    path('prev_snap/<int:app_id>/', views.loadDataNext, name='prev_snap'),
    path('next_snap/<int:app_id>/', views.loadDataNext, name='next_snap'),
    path('like/<int:app_id>/', views.make_like,name='make_like'),
    path('create/', views.createProject, name='create'),
    path('addsnap/<int:app_id>/', views.addSnap, name='add_snap'),
    path('delete/<int:app_id>/', views.deleteSnap, name='delete_snap'),
    path('editsnap/<int:app_id>/', views.editSnap, name='edit_snap'),
    path('delete_project/<int:app_id>/', views.deleteProject, name='delete_project'),
    path('delete_stack/', views.deleteStack, name='delete_stack'),
    path('add_stack/<int:app_id>/', views.addStack, name='add_stack'),


]

from django.urls import path

from . import views

urlpatterns = [
    # ex: /exp/
    path('', views.index, name='index'),
    path('tables/', views.tables, name='tables'),
    path('table_struct/', views.table_struct, name='table_struct'),
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail')
]
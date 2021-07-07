from django.urls import path

from action_result import views

urlpatterns = [
    path('unauthorised/', views.anauthorised_opperation,
         name='unauthorised-AR'),
    ]

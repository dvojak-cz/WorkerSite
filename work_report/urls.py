from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard-WR'),
    path('over_view/', views.report_view, name='report_list-WR'),
    path('new/', views.create_new_report, name='new_reports-WR'),
    path('new_project/', views.create_new_project, name='new_project-WR'),
    path('edit/<int:pk>/', views.edit_report, name='edit_report-WR'),
    path('copy/<int:pk>/', views.copy_report, name='copy_report-WR'),
    path('delete/<int:pk>/', views.delete_report, name='delete_report-WR'),
    path('projects/', views.project_view, name='project_view-WR'),
    path('export_csv/', views.export_to_csv, name='export_csv-WR'),
    path('share_pdf/', views.export_to_pdf, name='export_pdf-WR'),
    ]

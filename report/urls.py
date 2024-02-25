from django.urls import path, include
from . import views
from .views import *

urlpatterns = [

    path('emplacements/', views.listEmplacementView, name='emplacements'),
    path("emplacements/delete-emplacement/<int:id>", views.deleteEmplacementView, name="delete_emplacement"),
    path("emplacements/edit-emplacement/<int:id>", views.editEmplacementView, name="edit_emplacement"),
    path("emplacements/create-emplacement/", views.createEmplacementView, name="create_emplacement"),
    
    path('transitors/', views.listTransitorView, name='transitors'),
    path("transitors/delete-transitor/<int:id>", views.deleteTransitorView, name="delete_transitor"),
    path("transitors/edit-transitor/<int:id>", views.editTransitorView, name="edit_transitor"),
    path("transitors/create-transitor/", views.createTransitorView, name="create_transitor"),
    
    path('budgets/', views.listBudgetCostView, name='budgets'),
    path("budgets/delete-budget/<int:id>", views.deleteBudgetCostView, name="delete_budget"),
    path("budgets/edit-budget/<int:id>", views.editBudgetCostView, name="edit_budget"),
    path("budgets/create-budget/", views.createBudgetCostView, name="create_budget"),

    path('reports/', ReportList.as_view(), name='list_report'),
    path('', ReportList.as_view(), name='list_report'),
    path('report/create/', ReportCreate.as_view(), name='create_report'),
    path('report/<int:pk>/update/', ReportUpdate.as_view(), name='edit_report'),
    path('report/<int:pk>/delete/', delete_report, name='delete_report'),
    path('report/<int:pk>/', ReportDetail.as_view(), name='view_report'),
    path('delete-product/<int:pk>/', delete_product, name='report_delete_product'),

    path('report/<int:pk>/confirm/', views.confirmReport, name='confirm_report'),
    path('report/<int:pk>/cancel/', views.cancelReport, name='cancel_report'),

    path('live_search/', live_search, name='live_search'),
    
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("puma_import_folder/admin/", admin.site.urls),
    path("", include('account.urls')),
    path("", include('report.urls')),
]

handler404 = 'account.views.page_not_found'

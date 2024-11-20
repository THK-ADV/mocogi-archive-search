from django.contrib import admin
from django.urls import path

from mocogiArchiveSearch.views import ProjectDetailByIdView, GetAllProjectsView, GetModulesView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('projects/<int:project_id>/', ProjectDetailByIdView.as_view(), name="project-detail-by-id"),
    path('projects/', GetAllProjectsView.as_view(), name="get-all-projects"),

    path ("projects/<int:project_id>/modules/", GetModulesView.as_view(), name="get-modules"),
]

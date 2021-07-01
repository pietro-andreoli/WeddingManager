from django.urls import path

from . import views

app_name="InvitationManager"

urlpatterns = [
	path('', views.index, name='index'),
	path('yourinvitation/<str:invitation_id>', views.invitation_endpoint, name='invitation_endpoint'),
	path("import/", views.guest_import_page, name="db_import_endpoint"),
]
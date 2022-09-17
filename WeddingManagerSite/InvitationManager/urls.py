from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name="InvitationManager"

urlpatterns = [
	path('', views.index, name='index'),
	# path('yourinvitation/<str:invitation_id>', views.invitation_endpoint, name='invitation_endpoint'),
	path('yourinvitation/<str:invitation_id>', views.InvitationHomepage.as_view(), name='invitation_endpoint'),
	path('yourinvitation/', views.missing_invitation, name='invalid_invitation_endpoint'),
	path("import/", views.ImportGuestsView.as_view(), name="db_import_endpoint"),
	path("help/", views.help_page, name="help_endpoint"),
	path("yourinvitation/rsvp/<str:invitation_id>", views.RSVPFormView.as_view(), name="rsvp"),
	path("location", views.location_page, name="location"),
	# path('media/<str:media_name>', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT })
]
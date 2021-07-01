from django import http
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import View
from .forms import ImportGuestsForm
from django.contrib.auth.decorators import login_required
import logging
import csv
from . import models as InvitationModels
from django.forms.models import model_to_dict
def index(request):
	return HttpResponse("Hello world! Welcome to the InvitationManager app!")

@login_required
def guest_import_page(request):
	logger = logging.getLogger(__name__)
	logger.info("LOGGING STARTED")
	def handle_input_file(file_obj):
		"""
		Handles CSV input for database import.

		1. Reads the csv data line by line or chunk by chunk.
		2. Creates SQL queries for each line that will be executed as the file is read.
			- Consider using transactions that only get applied after all rows have been successfully read.
			- Only insert into the database if ALL rows in the CSV are confirmed valid.

		Please note, some fields are foreign keys. Meaning you cannot assign them a value.
		Instead, you must create/find the relevant model for the foreign key.
		For example: Guest requires an assoc_group foreign key.
			- This can be satisfied by searching for the group by its primary key (group_label)
				or by creating a new group.
			- The following links will be relevant to getting this done.
				https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get
				https://docs.djangoproject.com/en/3.2/ref/models/querysets/#get-or-create

		Heres an example of how to insert into the database.
		This will create the guest Bob Belcher and fill in his information.
		Notice the foreign keys `relation` and `assoc_group` use Django SQL queries to acquire the foreign key.
		InvitationModels.Guest(
			first_name="Bob",
			last_name="Belcher",
			relation=InvitationModels.Guest_Relation.objects.get(relation_en="Father"),
			whose_guest=InvitationModels.Guest.WHOSE_GUEST_OPTION_DICT["PETER"][0],
			home_address="123 Wharftown",
			phone_number=None,
			email="bob_burger@bobsburgers.yum",
			fb_link=None,
			assoc_group=InvitationModels.Group.objects.get_or_create(group_label="The Belcher Family"),
			is_overseas=False,
			assoc_invitation=None,
			is_attending=None
		)
		Once all objects have been created, ensure it is valid by using the full_clean method.
		https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.full_clean
		If the object is not valid, itll raise a ValidationError to let you know.
		Handle this exception as is necessary to solve the problem.
		
		Once all objects are valid, go through and call the save() funciton on all of them.
		Note the code in this part of the Django tutorial.
		https://docs.djangoproject.com/en/3.2/intro/tutorial02/#playing-with-the-api

		Args:
			file_obj (InMemoryUploadedFile): In memory file object handling the CSV input.
		
		"""


		# This code takes the file-like object file_obj, creates a csv reader, then prints each row.
		# csv.DictReader: https://docs.python.org/3/library/csv.html#csv.DictReader
		# InMemoryUploadedFile: https://docs.djangoproject.com/en/3.0/_modules/django/core/files/uploadedfile/
		csv_reader = csv.DictReader(file_obj)
		for row in csv_reader:
			logger.debug(row)

	if request.method == "POST":
		form = ImportGuestsForm(request, request.FILES)
		if form.is_valid():
			logger.info("Form is valid")
			handle_input_file(request.FILES["file_upload"])
			return HttpResponse("<html><h1>File Uploaded Successfully</h1></html>")
		else:
			logger.error("form was not valid." + str(form.errors))
			return HttpResponseServerError(str(form.errors))
	elif request.method == "GET":
		form = ImportGuestsForm()
		return render(request, "InvitationManager/import_page.html", {"form": form})

	return HttpResponseBadRequest()

class InvitationHomepage(View):
	class HomepageButtonOptions():
		FILL_INVITATION = 0
		REJECT_INVITATION = 1

		@staticmethod
		def as_str(option_code):
			if option_code == InvitationHomepage.HomepageButtonOptions.FILL_INVITATION:
				return "FILL_INVITATION"
			elif option_code == InvitationHomepage.HomepageButtonOptions.REJECT_INVITATION:
				return "REJECT_INVITATION"
			raise ValueError("Invitation option code not recognized.")

	def get(self, request, invitation_id, *args, **kwargs):
		from .event_details import EventDetails
		invitation = get_object_or_404(InvitationModels.Invitation, invitation_url_id=invitation_id)
		#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page
		details = EventDetails()
		guests = InvitationModels.Guest.objects.filter(assoc_invitation=invitation)
		
		# temp_group = InvitationModels.Group.objects.get(group_label="Tea's Family")
		# guests = InvitationModels.Guest.objects.filter(assoc_group=temp_group)

		invitation_context = {
			"wedding_date": details.event_start_timestamp.strftime("%b %d, %Y"),
			"wedding_time": details.event_start_timestamp.strftime("%I:%M:%S %p %Z"),
			"venue_name": details.venue_name,
			"venue_address": details.venue_address,
			"group_name": invitation.invitation_name,
			"invitation_guests": [guest.get_full_name() for guest in guests],
			"reply_deadline": details.reply_deadline.strftime("%Y-%m-%d %I:%M:%S %p %Z"),
			"invitation_url_id": invitation_id
		}
		return render(request, "InvitationManager/your_invitation.html", context=invitation_context)
	
	def post(self, request, invitation_id, *args, **kwargs):
		from .event_details import EventDetails
		invitation = get_object_or_404(InvitationModels.Invitation, invitation_url_id=invitation_id)
		# The variable containing a response ID regarding which button was pressed on the home page.
		# See InvitationEndpointOptions for potential values.
		selected_response = None
		if "fill_inv" in request.POST:
			selected_response = InvitationHomepage.HomepageButtonOptions.FILL_INVITATION
		elif "reject_inv" in request.POST:
			selected_response =  InvitationHomepage.HomepageButtonOptions.REJECT_INVITATION
		else:
			return HttpResponseBadRequest()
		print(InvitationHomepage.HomepageButtonOptions.as_str(selected_response))
		return render(request, "InvitationManager/fill_invitation.html")


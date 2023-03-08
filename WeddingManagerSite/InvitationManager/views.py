import csv
from datetime import datetime
import logging
from xmlrpc.client import SERVER_ERROR

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core import exceptions as django_exceptions
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http.request import HttpRequest

from InvitationManager import event_details

from . import models as InvitationModels
from .forms import ImportGuestsForm, RSVPSubform

def get_invitation_by_url_id(url_id) -> InvitationModels.Invitation:
		"""
		Gets the Invitation object associated with this URL ID.
		If there is no Invitation associated with this URL, raises ObjectDoesNotExist exception.

		Args:
			url_id (str): URL ID of the invitation. Should come from InvitationModels.Invitation.invitation_url_id.

		Raises:
			django_exceptions.ObjectDoesNotExist: Raised if no Invitation was found for this URL ID.

		Returns:
			InvitationModels.Invitation: The invitation associated with this URL ID.
		"""

		try:
			invitation = InvitationModels.Invitation.objects.get(invitation_url_id=url_id)
			if invitation is None:
				raise django_exceptions.ObjectDoesNotExist()
			return invitation
		# This is raised when the url_id does not match a single invitation.
		except django_exceptions.ObjectDoesNotExist as no_inv_error:
			print("Invitation could not be found!")
			InvitationModels.LogEvent.log_get_invitation_by_url_id(
				"error",
				"func_call",
				f"URL ID could not be found: {url_id}",
				None
			)
			raise no_inv_error
		except Exception as err:
			print(str(err))

def index(request):
	return render(request, "InvitationManager/missing_invitation.html")

def help_page(request):
	context = {}
	if "invitation_url_id" in request.session:
		context["invitation_url_id"] = request.session["invitation_url_id"]
	InvitationModels.LogEvent.log_help_page_visit(
		"info",
		"page_visit",
		"Help page",
		None if "invitation_url_id" not in context else get_invitation_by_url_id(context["invitation_url_id"])
	)

	return render(request, "InvitationManager/help.html", context)

def missing_invitation(request):
	InvitationModels.LogEvent.log(
		"info",
		"page_visit",
		"Missing invitation page",
		None
	)
	return render(request, "InvitationManager/missing_invitation.html")

def location_page(request: HttpRequest):
	from .event_details import EventDetails
	details = EventDetails()
	context = {
		"venue_name": details.venue_name,
		"venue_addr": details.venue_address,
		"google_embed_url": details.venue_map_embed_link,
		"google_link": details.venue_google_link
	}
	if "invitation_url_id" in request.session:
		context["invitation_url_id"] = request.session["invitation_url_id"]
	
	InvitationModels.LogEvent.log_location_page_visit(
		"info",
		"page_visit",
		"Location page",
		context["invitation_url_id"] if "invitation_url_id" in context else None
	)
	return render(request, "InvitationManager/location.html", context)

def contact_us_page(request: HttpRequest):
	from .event_details import EventDetails
	details = EventDetails()
	context = {
		"help_phone": details.help_phone,
		"help_phone_formatted": "-".join([
			details.help_phone[:3],
			details.help_phone[3:6],
			details.help_phone[6:]
		]),
		"help_email": details.help_email
	}
	invitation_url_id = None
	if "invitation_url_id" in request.session:
		context["invitation_url_id"] = request.session["invitation_url_id"]
		invitation_url_id = request.session["invitation_url_id"]
	InvitationModels.LogEvent.log_contact_us_page_visit(
		"info",
		"page_visit",
		"Contact us page",
		invitation_url_id
	)
	return render(request, "InvitationManager/contact_us.html", context)

def info_page(request: HttpRequest):
	from .event_details import EventDetails
	details = EventDetails()
	ceremony_tstamp: datetime = details.ceremony_timestamp
	context = {
		"wedding_date_formatted": "{dt:%B} {dt.day}, {dt.year}".format(dt=details.ceremony_timestamp),
		"ceremony_time_formatted": "{hr}:{dt:%M} {m}".format(
			dt=details.ceremony_timestamp, 
			hr=event_details.hour24_as_hour12(details.ceremony_timestamp.hour),
			m='AM' if details.ceremony_timestamp.hour < 12 else 'PM'
		),
		"ceremony_location": details.ceremony_location_name,
		"reception_time_formatted": "{hr}:{dt:%M} {m}".format(
			dt=details.reception_timestamp, 
			hr=event_details.hour24_as_hour12(details.reception_timestamp.hour),
			m='AM' if details.reception_timestamp.hour < 12 else 'PM'
		),
		"reception_location": details.reception_location_name,
		"hotel_name": details.hotel_name,
		"hotel_url": details.hotel_url
	}
	if "invitation_url_id" in request.session:
		context["invitation_url_id"] = request.session["invitation_url_id"]
	InvitationModels.LogEvent.log_info_page_visit(
		"info",
		"page_visit",
		"Info page",
		context["invitation_url_id"] if "invitation_url_id" in context else None
	)
	return render(request, "InvitationManager/event_info.html", context)

@method_decorator(staff_member_required, name="dispatch")
class ImportGuestsView(View):
	"""
	View for importing guests into the database.
	"""

	def get(self, request):
		form = ImportGuestsForm()
		return render(request, "InvitationManager/import_page.html", {"form": form})

	def post(self, request):
		import WeddingManagerSite.db as AppDatabase
		form = ImportGuestsForm(request.POST, request.FILES)
		if form.is_valid():
			# // if form clear_db is checked, delete all guests
			if "clear_db" in form.cleaned_data and form.cleaned_data["clear_db"] == "True":
				backed_up = AppDatabase.backup_db()
				if backed_up:
					# InvitationModels.Guest.objects.all().delete()
					print("DB cleared")
					self.handle_input_file(request.FILES["file_upload"])
			# // handle_input_file(request.FILES["file_upload"])
			return HttpResponse("<html><h1>Import Successful</h1></html>")
		else:
			return HttpResponse("<html><h1>Import FAILED<br><a href=''</h1></html>")
	
	def handle_input_file(self, file_obj):
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
		# csv_reader = csv.DictReader(file_obj)
		print("CSV Reader: ")


class InvitationHomepage(View):
	class HomepageButtonOptions():
		"""
		An enum class that represents the possible options a user can choose on the invitation homepage.
		"""
		FILL_INVITATION = 0
		REJECT_INVITATION = 1

		@staticmethod
		def as_str(option_code):
			"""
			Returns the string version of the code used. Useful for logging.

			Args:
				option_code (int): An integer option in the HomepageButtonOptions class.

			Raises:
				ValueError: Raised if an option code is inputted that does not exist.

			Returns:
				str: String version of code.
			"""

			if option_code == InvitationHomepage.HomepageButtonOptions.FILL_INVITATION:
				return "FILL_INVITATION"
			elif option_code == InvitationHomepage.HomepageButtonOptions.REJECT_INVITATION:
				return "REJECT_INVITATION"
			raise ValueError("Invitation option code not recognized.")

	def get(self, request: HttpRequest, invitation_id, *args, **kwargs):
		from .event_details import EventDetails

		invitation = None
		try:
			invitation = self.get_invitation_by_url_id(invitation_id)
		except django_exceptions.ObjectDoesNotExist as no_inv_found_err:
			return missing_invitation(request)

		request.session["invitation_url_id"] = invitation.invitation_url_id

		#https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page
		details = EventDetails()
		guests = InvitationModels.Guest.objects.filter(assoc_invitation=invitation)
		
		# temp_group = InvitationModels.Group.objects.get(group_label="Tea's Family")
		# guests = InvitationModels.Guest.objects.filter(assoc_group=temp_group)

		InvitationModels.LogEvent.log(
			"info",
			"page_visit",
			"Home page GET",
			invitation
		)

		invitation_context = {
			"wedding_date": "{dt:%B} {dt.day}, {dt.year}".format(dt=details.event_start_timestamp),
			"wedding_time": "{hr}:{dt:%M} {m} {tz}".format(
				dt=details.event_start_timestamp, 
				hr=event_details.hour24_as_hour12(details.event_start_timestamp.hour),
				m='AM' if details.event_start_timestamp.hour < 12 else 'PM',
				tz=details.event_tz_short
			),
			"venue_name": details.venue_name,
			"venue_address": details.venue_address,
			"group_name": invitation.invitation_name,
			"invitation_guests": [guest.get_full_name() for guest in guests],
			"reply_deadline": "{dt:%B} {dt.day}, {dt.year}".format(dt=details.reply_deadline),
			"invitation_url_id": invitation_id,
			"partner_1": details.partner_1,
			"partner_2": details.partner_2
		}
		return render(request, "InvitationManager/your_invitation.html", context=invitation_context)
	
	def post(self, request, invitation_id, *args, **kwargs):
		from .event_details import EventDetails
		invitation = None
		try:
			invitation = self.get_invitation_by_url_id(invitation_id)
		except django_exceptions.ObjectDoesNotExist as no_inv_found_err:
			return render(request, "InvitationManager/missing_invitation.html")
		# The variable containing a response ID regarding which button was pressed on the home page.
		# See InvitationEndpointOptions for potential values.
		selected_response = None
		if "fill_inv" in request.POST:
			selected_response = InvitationHomepage.HomepageButtonOptions.FILL_INVITATION
		elif "reject_inv" in request.POST:
			selected_response =  InvitationHomepage.HomepageButtonOptions.REJECT_INVITATION
		else:
			# Redirect to the GET version of this page, as the payload seems to be missing required headers.
			return self.get(request, invitation_id, args, kwargs)
		print(InvitationHomepage.HomepageButtonOptions.as_str(selected_response))
		
		InvitationModels.LogEvent.log(
			"info",
			"page_visit",
			"Home page POST",
			invitation
		)
		return render(request, "InvitationManager/fill_invitation.html", context=None)

	def get_invitation_by_url_id(self, url_id) -> InvitationModels.Invitation:
		"""
		Gets the Invitation object associated with this URL ID.
		If there is no Invitation associated with this URL, raises ObjectDoesNotExist exception.

		Args:
			url_id (str): URL ID of the invitation. Should come from InvitationModels.Invitation.invitation_url_id.

		Raises:
			django_exceptions.ObjectDoesNotExist: Raised if no Invitation was found for this URL ID.

		Returns:
			InvitationModels.Invitation: The invitation associated with this URL ID.
		"""

		try:
			invitation = InvitationModels.Invitation.objects.get(invitation_url_id=url_id)
			if invitation is None:
				raise django_exceptions.ObjectDoesNotExist()
			return invitation
		# This is raised when the url_id does not match a single invitation.
		except django_exceptions.ObjectDoesNotExist as no_inv_error:
			print("Invitation could not be found!")
			#TODO: Add logging here
			raise no_inv_error
		except Exception as err:
			print(str(err))

class RSVPFormView(View):

	FORM_TEMPLATE_PATH = "InvitationManager/fill_rsvp.html"
	RSVP_SUCCESS_TEMPLATE_PATH = "InvitationManager/rsvp_success.html"

	ATTENDING_RB_TAG_NAME = "is_attending"
	ATTENDING_CEREMONY_RB_TAG_NAME = "is_attending_ceremony"
	IS_ATTENDING_RB_TAG_VALUE = "true"
	IS_ATTENDING_CEREMONY_RB_TAG_VALUE = "true"
	IS_NOT_ATTENDING_RB_TAG_VALUE = "false"
	IS_NOT_ATTENDING_CEREMONY_RB_TAG_VALUE = "false"
	IS_VEGAN_CB_TAG_NAME = "is_vegan"
	IS_VEGAN_CB_TAG_VALUE = "true"
	TAG_NAME_DELIMETER = "__"

	def get(self, request, invitation_id, *args, **kwargs):
		inv = self.get_assoc_invitation(invitation_id)
		
		InvitationModels.LogEvent.log(
			"info",
			"page_visit",
			"RSVP page GET",
			inv
		)
		return self.render_form(request, inv)
	
	def post(self, request, invitation_id, *args, **kwargs):

		# Get the invitation object associated with the inputted ID
		inv = InvitationModels.Invitation.get_invitation_by_url_id(invitation_id)

		# Convert the forms response into a dictionary
		form_response = dict(request.POST.lists())

		def get_form_value(guest, key):
			"""
			Gets from the form_response dict based on inputted guest and key.
			This is necessary because keys are in this format
			<guest_id>__key

			Args:
				guest (Guest): Guest to search for.
				key (str): Key string to search for.

			Returns:
				any: Value for inputted key, or None if it doesnt exist.
			"""

			form_key = str(guest.guest_id) + RSVPFormView.TAG_NAME_DELIMETER + key
			if form_key in form_response:
				return form_response[form_key][0]
			return None

		# list of form, guest pairs
		form_list = []
		raw_response_list = []

		# Loop through guests for this invitation
		# Fill an individual RSVP form for each guest
		# Add form and guest to form_list before saving
		for guest in inv.get_all_guests():
			# Get all models for this guest
			rsvp_model_set = InvitationModels.RSVP.objects.filter(guest__guest_id=guest.guest_id)
			rsvp_model = rsvp_model_set[0] if len(rsvp_model_set) > 0 else None
			print (f"rsvp_model: {rsvp_model}")

			# Get form input as dict
			is_attending = get_form_value(guest, RSVPFormView.ATTENDING_RB_TAG_NAME)
			is_attending_ceremony = get_form_value(guest, RSVPFormView.ATTENDING_CEREMONY_RB_TAG_NAME)
			guest_form_dict = {
				"is_attending": is_attending == RSVPFormView.IS_ATTENDING_RB_TAG_VALUE if is_attending is not None else None,
				"is_vegan": get_form_value(guest, RSVPFormView.IS_VEGAN_CB_TAG_NAME),
				"is_attending_ceremony": is_attending_ceremony == RSVPFormView.IS_ATTENDING_CEREMONY_RB_TAG_VALUE if is_attending_ceremony is not None else None,
			}
			raw_response_list.append({ "guest": guest.guest_id, "raw_response": guest_form_dict})

			# Create form object using instance and form input
			# If no RSVP has been created yet for a guest, instance is set to None, creating a new RSVP object
			form = RSVPSubform(guest_form_dict, instance=rsvp_model)
			if not form.is_valid():
				raise Exception("Form is not valid")
			form_list.append((form, guest))
		
		# loop through form and guest pairs, save both.
		# We do this after so no changes are made if a single form is not valid (from prev loop)
		for form, guest in form_list:
			form.save()
			guest.rsvp = form.instance
			guest.save()
		
		InvitationModels.LogEvent.log(
			"info",
			"RSVP Submit",
			f"Raw Response -> {raw_response_list}",
			inv
		)
		# Render the form again.
		return self.render_post_rsvp(request, inv)

	def get_assoc_invitation(self, invitation_id) -> InvitationModels.Invitation:
		return InvitationModels.Invitation.objects.get(invitation_url_id=invitation_id)

	def render_form(self, request, inv: InvitationModels.Invitation):
		from .event_details import EventDetails

		
		details = EventDetails()
		form = RSVPSubform(request.POST)
		form.parent_invitation = inv
		
		context = {
			"form": form,
			"invitees": inv.get_all_guests(),
			"ATTENDING_RB_TAG_NAME": RSVPFormView.ATTENDING_RB_TAG_NAME,
			"ATTENDING_CEREMONY_RB_TAG_NAME": RSVPFormView.ATTENDING_CEREMONY_RB_TAG_NAME,
			"IS_VEGAN_CB_TAG_NAME": RSVPFormView.IS_VEGAN_CB_TAG_NAME,
			"IS_VEGAN_CB_TAG_VALUE": RSVPFormView.IS_VEGAN_CB_TAG_VALUE,
			"IS_NOT_ATTENDING_RB_TAG_VALUE": RSVPFormView.IS_NOT_ATTENDING_RB_TAG_VALUE,
			"IS_NOT_ATTENDING_CEREMONY_RB_TAG_VALUE": RSVPFormView.IS_NOT_ATTENDING_CEREMONY_RB_TAG_VALUE,
			"IS_ATTENDING_RB_TAG_VALUE": RSVPFormView.IS_ATTENDING_RB_TAG_VALUE,
			"IS_ATTENDING_CEREMONY_RB_TAG_VALUE": RSVPFormView.IS_ATTENDING_CEREMONY_RB_TAG_VALUE,
			"TAG_NAME_DELIMETER": RSVPFormView.TAG_NAME_DELIMETER,
			"wedding_date": details.event_start_timestamp.strftime("%b %d, %Y"),
			"wedding_time": details.event_start_timestamp.strftime("%I:%M %p"),
			"venue_name": details.venue_name,
			"invitation_url_id": inv.invitation_url_id

		}
		return render(request, RSVPFormView.FORM_TEMPLATE_PATH, context)

	def render_post_rsvp(self, request, inv):
		"""
		Renders the success page after the RSVP form has been submitted, or the failure page if the form is invalid.

		Args:
			request (Request): Incoming request object.
			inv (models.Invitation): Invitation model object.

		Returns:
			HttpResponse: Render the approprate template.
		"""

		context = {
			"invitation_url_id": inv.invitation_url_id
		}
		return render(request, RSVPFormView.RSVP_SUCCESS_TEMPLATE_PATH, context)


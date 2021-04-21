from django import http
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImportGuestsForm
from django.contrib.auth.decorators import login_required
import logging
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

		Args:
			file_obj (InMemoryUploadedFile): In memory file object handling the CSV input.
		
		"""

		for c in file_obj.chunks():
			logger.info(c)

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

def invitation_endpoint(request, invitation_id):
	return HttpResponse(f"Invitation Endpoint: {invitation_id}")

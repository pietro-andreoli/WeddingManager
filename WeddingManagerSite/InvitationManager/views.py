from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello world! Welcome to the InvitationManager app!")

def invitation_endpoint(request, invitation_id):
	return HttpResponse(f"Invitation Endpoint: {invitation_id}")

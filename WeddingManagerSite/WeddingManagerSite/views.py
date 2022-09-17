from django.shortcuts import render

def index(request):
	return render(request, "WeddingManager/coming_soon.html")
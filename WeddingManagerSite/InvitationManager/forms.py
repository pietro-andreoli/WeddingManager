from django import forms

class ImportGuestsForm(forms.Form):
	file_upload = forms.FileField(label="file_upload")
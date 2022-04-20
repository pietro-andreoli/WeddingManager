from django import forms
from .models import Guest, Group, RSVP, Invitation
from .enums import DisplayStrings

class ImportGuestsForm(forms.Form):
	file_upload = forms.FileField(label="file_upload")
	clear_db = forms.CheckboxInput()

class RSVPForm(forms.ModelForm):


	class Meta:
		model = RSVP
		fields = ["is_attending", "is_vegan"]


class RSVPSubform(forms.ModelForm):
	ATTENDANCE_OPTIONS = [
		(True, DisplayStrings.IS_ATTENDING),
		(False, DisplayStrings.IS_NOT_ATTENDING)
	]
	parent_invitation = None
	is_attending = forms.ChoiceField(choices=ATTENDANCE_OPTIONS, widget=forms.RadioSelect)
	is_vegan = forms.CheckboxInput()

	class Meta:
		model = RSVP
		exclude = ("rsvp_id",)
	
	def get_all_guests(self):
		return Guest.objects.filter(assoc_invitation=self.parent_invitation)

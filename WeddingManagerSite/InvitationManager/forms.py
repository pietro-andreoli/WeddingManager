from django import forms

class ImportGuestsForm(forms.Form):
	file_upload = forms.FileField(label="file_upload")

class RSVPForm(forms.Form):
	# Guest model that is designated this form.
	owner = None

	
	attending_field = forms.ChoiceField(choices=AttendingFieldResponses.responses)
	# States whether the guest has vegan food restrictions.
	# `required` is `false` to allow the user to choose either True OR False as options.
	vegan_field = forms.BooleanField(required=False)

	class AttendingFieldResponses():
		"""
		Enum of options for the field `attending_field`
		"""
		ATTENDING_LABEL = "I will be attending."
		ATTENDING_VALUE = 1

		NOT_ATTENDING_LABEL = "I regretfully will not be attending."
		NOT_ATTENDING_VALUE = 0

		@static_method
		def responses():
			"""
			Returns list of response options for Django selection fields.

			Returns:
				list<tuple<int, str>>: A list of value-label tuples representing options.
			"""
			return [(ATTENDING_VALUE, ATTENDING_LABEL), (NOT_ATTENDING_VALUE, NOT_ATTENDING_LABEL)]
	
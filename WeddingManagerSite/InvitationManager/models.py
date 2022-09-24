from django.db import models
import uuid
from .configs import Food

class Guest_Relation(models.Model):
	relation_en = models.CharField(max_length=32, primary_key=True)
	relation_mk = models.CharField(max_length=32, null=False)
	relation_it = models.CharField(max_length=32, null=False)

	def __str__(self):
		return self.relation_en

class Invitation_Email(models.Model):
	email_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	to_field = models.CharField(max_length=128, null=False)
	# CC will usually be empty, but that isnt null, thats just an empty string.
	cc_field = models.CharField(max_length=256, null=False)
	from_field = models.CharField(max_length=128, null=False)
	subject_field = models.CharField(max_length=256, null=False)
	body_field = models.TextField(null=False)

	def __str__(self):
		return self.email_id

def generate_invitation_url_id():
	"""
	Generates a UUID.

	Returns:
		str: UUID string, truncated to 5 characters.
	"""
	return str(uuid.uuid4())[:5]

class Invitation(models.Model):
	# Uniquely identifies each row
	invitation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	invitation_name = models.CharField(unique=True, max_length=128, default="NO NAME SET")
	# Name of the invitation that can be displayed to users. Ex: "Guido Family"
	# invitation_public_name = models.CharField(max_length=128, default="Guest Group")
	# The ID used in the URL in the invitation email
	invitation_url_id = models.CharField(
		max_length=36,
		null=False,
		unique=True,
		blank=True,
		default=generate_invitation_url_id
	)
	# States whether the invitation has been sent already
	invitation_sent = models.BooleanField(default=False)
	# Date + time sent
	send_date = models.DateTimeField(null=True, blank=True)
	# States whether the invitation link has been clicked already
	invitation_seen = models.BooleanField(default=False)
	# The most recent date the link has been clicked
	seen_date = models.DateTimeField(null=True, blank=True)
	assoc_email = models.ForeignKey(Invitation_Email, null=True, on_delete=models.SET_NULL, blank=True)

	def __str__(self):
		return self.invitation_name

	def get_all_guests(self):
		return Guest.objects.filter(assoc_invitation=self)

	@staticmethod
	def get_invitation_by_url_id(inv_url_id):
		return Invitation.objects.get(invitation_url_id=inv_url_id)

class Group(models.Model):
	group_label = models.CharField(primary_key=True, max_length=64, null=False, unique=True)
	primary_contact = models.ForeignKey("Guest", null=True, on_delete=models.SET_NULL, blank=True)

	def __str__(self):
		return self.group_label

class RSVP(models.Model):
	"""
	Model representing an RSVP response a guest has given.
	One RSVP belongs to One guest.
	A reference to the associated RSVP can be found in the Guest model.
	"""

	FOOD_CHOICES = Food.options

	rsvp_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	is_attending = models.BooleanField(default=False, null=True)
	is_vegan = models.BooleanField(default=False)

class Guest(models.Model):
	# The options for the field whose_guest.
	# It is stored as a dict for easy identification, converted to list for WHOSE_GUEST_OPTIONS constant.
	# The key is for accessing from other parts of the app.
	# Tuple's 0th value is what will be stored in the database. Tuples 1st value is a label for readability.
	WHOSE_GUEST_OPTION_DICT = {
		"PETER": ("peter", "Peter's"),
		"TEA": ("tea", "Teodora's")
	}
	WHOSE_GUEST_OPTIONS = list(WHOSE_GUEST_OPTION_DICT.values())

	guest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(max_length=16)
	last_name = models.CharField(max_length=32)
	relation = models.ForeignKey(Guest_Relation, null=True, on_delete=models.SET_NULL)
	whose_guest = models.CharField(max_length=8, null=True, choices=WHOSE_GUEST_OPTIONS)
	home_address = models.CharField(max_length=128, null=True, blank=True)
	phone_number = models.CharField(max_length=16, null=True, blank=True)
	email = models.CharField(max_length=64, null=True, blank=True)
	fb_link = models.CharField(max_length=256, null=True, blank=True)
	assoc_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
	is_overseas = models.BooleanField(default=False)
	assoc_invitation = models.ForeignKey(Invitation, null=True, on_delete=models.SET_NULL, blank=True)
	is_attending = models.BooleanField(null=True, default=None)
	rsvp = models.ForeignKey(RSVP, null=True, on_delete=models.SET_NULL, blank=True)

	def __str__(self):
		return self.first_name + " " + self.last_name
	
	def has_seen_invitation(self):
		return self.assoc_invitation.invitation_seen
	
	def get_full_name(self):
		return self.first_name + ' ' + self.last_name
	
	def has_rsvpd(self):
		return self.rsvp is not None
	
class Config(models.Model):
	config_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	is_main_config = models.BooleanField(
		default=False,
		help_text="True if this is the config that has all real data. False otherwise."
	)
	event_date = models.DateTimeField(null=True, help_text="In local timezone")
	event_date_tz = models.CharField(null=True, max_length=64)
	event_date_tz_short = models.CharField(null=True, max_length=8, help_text="EST, PST, etc")
	venue_addr = models.CharField(null=True, max_length=512)
	venue_name = models.CharField(null=True, max_length=128)
	venue_google_map_link = models.URLField(
		null=True,
		max_length=512,
		help_text="Link to the address on Google maps."
	)
	venue_google_map_embed_link = models.URLField(
		null=True,
		max_length=512,
		help_text="Embed link that Google provides in its embedded iframe."
	)
	reply_deadline = models.DateTimeField(null=True, help_text="In local timezone")
	contact_help_email = models.EmailField(null=True)
	contact_help_phone = models.CharField(null=True, max_length=16)
	partner_1_first_name = models.CharField(null=True, max_length=32)
	partner_1_last_name = models.CharField(null=True, max_length=32)
	partner_1_full_name = models.CharField(null=True, max_length=64)
	partner_2_first_name = models.CharField(null=True, max_length=32)
	partner_2_last_name = models.CharField(null=True, max_length=32)
	partner_2_full_name = models.CharField(null=True, max_length=64)
	logo_acronym = models.CharField(
		default='',
		max_length=6,
		help_text="Text logo to use on website. Example: P&T"
	)
	ceremony_timestamp = models.DateTimeField(null=True, help_text="In local timezone")
	ceremony_location_name = models.CharField(null=True, max_length=128)
	ceremony_location_addr = models.CharField(null=True, max_length=256)
	reception_timestamp = models.DateTimeField(null=True, help_text="In local timezone")
	reception_location_name = models.CharField(null=True, max_length=128)
	reception_location_addr = models.CharField(null=True, max_length=256)
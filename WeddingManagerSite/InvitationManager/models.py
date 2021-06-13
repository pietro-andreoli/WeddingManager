from django.db import models
import uuid

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

class Invitation(models.Model):
	# Uniquely identifies each row
	invitation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	invitation_name = models.CharField(unique=True, max_length=128, default="NO NAME SET")
	# Name of the invitation that can be displayed to users. Ex: "Guido Family"
	invitation_public_name = models.CharField(unique=True, max_length=128, default="Guest Group")
	# The ID used in the URL in the invitation email
	invitation_url_id = models.CharField(max_length=36, null=False, unique=True, blank=True, default=uuid.uuid4)
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

class Group(models.Model):
	group_label = models.CharField(primary_key=True, max_length=64, null=False, unique=True)
	primary_contact = models.ForeignKey("Guest", null=True, on_delete=models.SET_NULL, blank=True)

	def __str__(self):
		return self.group_label

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

	def __str__(self):
		return self.first_name + " " + self.last_name
	
	def has_seen_invitation(self):
		return self.assoc_invitation.invitation_seen
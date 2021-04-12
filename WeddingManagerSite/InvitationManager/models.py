from django.db import models
import uuid

# CREATE TABLE Guest(
# 	/*Unique Identifier*/
# 	guest_id VARCHAR(32) PRIMARY KEY,
# 	first_name VARCHAR(16) NOT NULL,
# 	last_name VARCHAR(32) NOT NULL,
# 	/*Relationship*/
# 	relation_en VARCHAR(32),
# 	whose_guest VARCHAR(8) NOT NULL,
# 	home_address VARCHAR(128),
# 	phone_number VARCHAR(16),
# 	email VARCHAR(64),
# 	fb_link VARCHAR(256),
# 	/*If invited_as_group is TRUE, this is a reference to the group theyre a part of.*/
# 	group_id VARCHAR (32),
# 	/*States whether this person is overseas*/
# 	is_overseas BOOLEAN DEFAULT FALSE,
# 	/*Invitation this guest is associated with.*/
# 	invitation_id VARCHAR(32),
# 	/*Determines if the user has responded yet. True = Yes, False = No, Null = No response.*/
# 	is_attending BOOLEAN,
# 	FOREIGN KEY (relation_en) REFERENCES Guest_Relation(relation_en),
# 	FOREIGN KEY (group_id) REFERENCES Group(group_id),
# 	FOREIGN KEY (invitation_id) REFERENCES Invitation(invitation_id)
# );

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
	# The ID used in the URL in the invitation email
	invitation_url_id = models.CharField(max_length=32, null=False, unique=True)
	# States whether the invitation has been sent already
	invitation_sent = models.BooleanField(default=False)
	# Date + time sent
	send_date = models.DateTimeField(null=True)
	# States whether the invitation link has been clicked already
	invitation_seen = models.BooleanField(default=False)
	# The most recent date the link has been clicked
	seen_date = models.DateTimeField(null=True)
	assoc_email = models.ForeignKey(Invitation_Email, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.invitation_url_id

class Group(models.Model):
	group_label = models.CharField(primary_key=True, max_length=64, null=False, unique=True)
	primary_contact = models.ForeignKey("Guest", null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.group_label

class Guest(models.Model):
	guest_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(max_length=16)
	last_name = models.CharField(max_length=32)
	relation = models.ForeignKey(Guest_Relation, null=True, on_delete=models.SET_NULL)
	whose_guest = models.CharField(max_length=8, null=True)
	home_address = models.CharField(max_length=128, null=True)
	phone_number = models.CharField(max_length=16, null=True)
	email = models.CharField(max_length=64, null=True)
	fb_link = models.CharField(max_length=256, null=True)
	assoc_group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
	is_overseas = models.BooleanField(default=False)
	assoc_invitation = models.ForeignKey(Invitation, null=True, on_delete=models.SET_NULL)
	is_attending = models.BooleanField(null=True, default=None)

	def __str__(self):
		return self.first_name + " " + self.last_name
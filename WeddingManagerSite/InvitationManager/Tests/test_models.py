from django.test import TestCase
from InvitationManager import models

class GuestTestCases(TestCase):
	"""
	Test that the string representation of this model is as expected.
	"""

	TEST_GUEST_1 = {
		"first_name":"Peter",
		"last_name":"Andreoli",
		"whose_guest":"Peters",
		"home_address":"84 Dean Place",
		"phone_number":"123-456-7890",
		"email":"test@gmail.com",
		"fb_link":"http://....",
		"is_overseas":False,
		"is_attending":None
	}

	TEST_INVITATION_1 = {
		"invitation_url_id": "12345abc",
		"invitation_sent": True,
		"send_date": "2022-09-12 12:00:00",
		"invitation_seen": False,
		"seen_date": None
	}

	def setUp(self):
		inv = models.Invitation.objects.create(**self.TEST_INVITATION_1)
		models.Guest.objects.create(**self.TEST_GUEST_1, assoc_invitation=inv)

	def test_to_str(self):
		guest = models.Guest.objects.get(
			first_name=self.TEST_GUEST_1["first_name"],
			last_name=self.TEST_GUEST_1["last_name"]
		)
		self.assertEquals(
			str(guest),
			self.TEST_GUEST_1["first_name"] + ' ' + self.TEST_GUEST_1["last_name"]
		)
	
	def test_has_seen_from_guest(self):
		guest = models.Guest.objects.get(
			first_name=self.TEST_GUEST_1["first_name"],
			last_name=self.TEST_GUEST_1["last_name"]
		)
		self.assertFalse(guest.has_seen_invitation())


class GroupTestCases(TestCase):
	TEST_GROUP_1 = {
		"group_label": "Test Label",
		"primary_contact": None
	}

	def setUp(self):
		models.Group.objects.create(**self.TEST_GROUP_1)

	def test_to_str(self):
		"""
		Test that the string representation of this model is as expected.
		"""

		group = models.Group.objects.get(group_label="Test Label")
		self.assertEquals(str(group), self.TEST_GROUP_1["group_label"])


class InvitationTestCases(TestCase):
	TEST_INVITATION_1 = {
		"invitation_url_id": "12345",
		"invitation_sent": False,
		"send_date": "2023-01-01 12:00:00",
		"invitation_seen": False,
		"seen_date": "2023-02-02 15:23:00",
		"assoc_email": None
	}

	def setUp(self):
		models.Invitation.objects.create(**self.TEST_INVITATION_1)

	def test_to_str(self):
		"""
		Test that the string representation of this model is as expected.
		"""

		inv = models.Invitation.objects.get(invitation_url_id="12345")
		self.assertEquals(str(inv), self.TEST_INVITATION_1["invitation_url_id"])
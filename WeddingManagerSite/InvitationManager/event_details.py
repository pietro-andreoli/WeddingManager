from datetime import datetime
import pytz
from django.conf import settings
import os
from . import models

def datetime_from_str(date_str, tz_str):
	"""
	Creates the datetime object from a timestamp string and timezone name.

	Args:
		date_str (str): timestamp as a string in the format YYYY-MM-DD hh:mm:ss (24h time).
		tz_str (str): Name of the timezone. See pytz for a list of valid timezone names.

	Returns:
		datetime: Timezone aware date of the string.
	"""

	tz = pytz.timezone(tz_str)
	return tz.localize(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))

def get_main_config() -> models.Config:
	"""
	Gets the main config from the database

	Raises:
		ValueError: Raised if the config could not be found, or if there is more than one config marked as main.

	Returns:
		models.Config: Config model.
	"""

	config_qs = models.Config.objects.filter(is_main_config=True)
	if config_qs.count() != 1:
		raise ValueError(
			"There should only be 1 config flagged with is_main_config. Found " + str(config_qs.count())
		)
	
	return config_qs[0]
	# TODO keep working on getting config out of db, see Config model

class EventDetails():
	
	# Path to the event details file.
	DETAILS_FP = os.path.join(settings.BASE_DIR, "InvitationManager", "configs/event_details_config.json")
	
	def __init__(self):
		import json

		self.config_model: models.Config = get_main_config()

		# Read event details JSON file into memory.
		contents = None
		with open(EventDetails.DETAILS_FP, 'r') as details_f:
			contents = json.load(details_f)
		
		# Load essential information into this object.
		start_timestamp_str = contents["event_date"]["t_stamp"]
		tz_str = contents["event_date"]["tz"]
		self.event_start_timestamp = self.config_model.event_date
		self.venue_name = self.config_model.venue_name
		self.venue_address = self.config_model.venue_addr
		self.venue_google_link = self.config_model.venue_google_map_link
		self.venue_map_embed_link = self.config_model.venue_google_map_embed_link
		self.reply_deadline = self.config_model.reply_deadline
		self.help_phone = self.config_model.contact_help_phone
		self.help_email = self.config_model.contact_help_email
		self.partner_1 = {
			"full_name": self.config_model.partner_1_full_name,
			"first_name": self.config_model.partner_1_first_name,
			"last_name": self.config_model.partner_1_last_name
		}
		self.partner_2 = {
			"full_name": self.config_model.partner_2_full_name,
			"first_name": self.config_model.partner_2_first_name,
			"last_name": self.config_model.partner_2_last_name
		}
	
	@property
	def event_time(self):
		return self.event_start_timestamp.time()
	
	@property
	def event_date(self):
		return self.event_start_timestamp.date()

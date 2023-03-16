from django.contrib import admin

from .models import RSVP, Guest, Group, Invitation, Guest_Relation, Config, LogEvent
from . import event_details
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(Guest)
admin.site.register(Group)
admin.site.register(Guest_Relation)
# @admin.site.register(RSVP)

class InvitationAdmin(admin.ModelAdmin):
	model = Invitation
	list_display = ("invitation_id", "invitation_name", "created_at", 'inv_url')

	def inv_url(self, obj: Invitation):
		config = event_details.get_main_config()
		return format_html(f"<a href='{config.website_url}{reverse('InvitationManager:invitation_endpoint', args=[obj.invitation_url_id])}' target='_blank'>{obj.invitation_url_id}</a>")
	
	inv_url.short_description = "Invitation URL"
	inv_url.admin_order_field = "created_at"



class RSVPAdmin(admin.ModelAdmin):
	model = RSVP
	list_display = ("view_rsvp_owner", "is_attending_ceremony", "is_attending", "is_vegan")
	list_filter = ("is_attending_ceremony", "is_attending", "is_vegan")

	def view_rsvp_owner(self, obj):
		return Guest.objects.get(rsvp=obj)
	
	view_rsvp_owner.short_description = "Owner"
	view_rsvp_owner.admin_order_field = "guest__first_name"

class LogEventAdmin(admin.ModelAdmin):
	model = LogEvent
	list_display = ("timestamp", "category", "related_inv", "message")

	def related_inv(self, obj: LogEvent):
		return obj.related_inv

	related_inv.short_description = "Invitation Group"
	related_inv.admin_order_field = "invitation__invitation_name"

class ConfigAdmin(admin.ModelAdmin):
	model = Config

	list_display = ("config_id", "is_main_config")

admin.site.register(RSVP, RSVPAdmin)
admin.site.register(LogEvent, LogEventAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Config, ConfigAdmin)
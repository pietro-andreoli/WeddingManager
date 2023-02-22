from django.contrib import admin

from .models import RSVP, Guest, Group, Invitation, Guest_Relation, Config

admin.site.register(Guest)
admin.site.register(Group)
admin.site.register(Invitation)
admin.site.register(Guest_Relation)
admin.site.register(Config)
# @admin.site.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
	model = RSVP
	list_display = ("view_rsvp_owner", "is_attending_ceremony", "is_attending", "is_vegan")

	def view_rsvp_owner(self, obj):
		return Guest.objects.get(rsvp=obj)
	
	view_rsvp_owner.short_description = "Owner"
	view_rsvp_owner.admin_order_field = "guest__first_name"

admin.site.register(RSVP, RSVPAdmin)
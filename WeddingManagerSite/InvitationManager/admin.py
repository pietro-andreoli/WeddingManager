from django.contrib import admin

from .models import Guest, Group, Invitation, Guest_Relation

admin.site.register(Guest)
admin.site.register(Group)
admin.site.register(Invitation)
admin.site.register(Guest_Relation)
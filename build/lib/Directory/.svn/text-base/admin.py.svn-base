from Directory.models import *
from django.contrib import admin


class EmailInline(admin.StackedInline):
    model = addEmail
    extra = 0

class TagsInline(admin.StackedInline):
    model = Tags
    extra = 0
	
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    fieldsets = [
        (None, {'fields': ['nickname', 'middle', 'maiden', 'year', 'picture']}),
        ('Meta Information', {'fields': ['international'],
 'classes': ['collapse']}), 
    ]

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline, EmailInline, TagsInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from Directory.models import *
from django.contrib import admin


class EmailInline(admin.StackedInline):
    model = addEmail
    extra = 0

class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 0

class InternationalPhoneInline(admin.StackedInline):
    model = InternationalPhone
    extra = 0

class USAddressInline(admin.StackedInline):
    model = USAddress
    extra = 0

class OtherAddressInline(admin.StackedInline):
    model = OtherAddress
    extra = 0

class CampusAddressInline(admin.StackedInline):
    model = CampusAddress
    extra = 0

class SocialMediaInline(admin.StackedInline):
    model = SocialMedia
    extra = 0
    
class JobInline(admin.StackedInline):
    model = Job
    extra = 0

class TagsInline(admin.StackedInline):
    model = Tags
    extra = 0
	
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 0
    fieldsets = [
        (None, {'fields': ['nickname', 'middle', 'maiden', 'year', 'picture','type',]}),
        ('Meta Information', {'fields': ['international'],
 'classes': ['collapse']}), 
    ]

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline, EmailInline, PhoneInline,
    InternationalPhoneInline, USAddressInline, OtherAddressInline, 
    CampusAddressInline, SocialMediaInline, JobInline, TagsInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

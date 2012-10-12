from django.db import models
from django.forms import ModelForm
from django.contrib.localflavor.us.models import PhoneNumberField, USPostalCodeField
from django.contrib.localflavor.us.forms import USZipCodeField
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from taggit.managers import TaggableManager
from taggit_autocomplete_modified.managers \
    import TaggableManagerAutocomplete as TaggableManager
from sorl.thumbnail import ImageField
#NOTE: this ImageField is not required, but recommended - read sorl doc
import os

def get_upload_path(instance, filename):
    return os.path.join(
      "images", "class_of_%d" % instance.year, 
      "%s" % instance.user.first_name + instance.user.last_name,
      filename)

# Create your models here.
USER_TYPES = (
	('AL', 'Alumni'),
	#don't give option for campus address
	('Current', 'Current Students'),
	('Exchange', 'Exchange Students'),
	#don't give option for graduation year
)

class UserForm(ModelForm):
    #used to extend the UserCreationForm
    first = forms.CharField(max_length=200)
    #first name
    last = forms.CharField(max_length=200)
    #last name
    class Meta:
        model = User
        fields = ["first", "last"]
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first"]
        user.last_name = self.cleaned_data["last"]
        if commit:
            user.save()
        return user

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #user = models.ForeignKey(User)
    type = models.CharField(max_length=10, choices=USER_TYPES)
	#select whether they are alumni, current student, or exchange student
    year = models.IntegerField()
	# graduation year
    middle = models.CharField(max_length=200, null=True, blank=True)
	#middle name - not required
    nickname = models.CharField(max_length=200, null=True, blank=True)
	#nickname - not required
    maiden = models.CharField(max_length=200, null=True, blank=True)
	#maiden name - not required (null = database, blank = admin)
    international = models.BooleanField()
	#select if they live outside the US or not
    # svn checkout http://django-stdimage.googlecode.com/svn/trunk/stdimage
    picture = ImageField(upload_to=get_upload_path,)
    #size is full sized image resized, thumbnail_size creates a smaller thumbnail
    # http://code.google.com/p/django-stdimage/ for documentation

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


class UserProfileForm(ModelForm):
    international = forms.BooleanField(initial=False, required=False)
    #this makes the international boolean work without requiring input
    class Meta:
        model = UserProfile
        exclude = ["user"]


class addEmail(models.Model):
	user = models.ForeignKey(User)
	email = models.EmailField(null=True, blank=True)
	#like charfield, but makes sure it's a valid email address

class Phone(models.Model):
#use either number of nonusnumber depending on whether they selected that they're living in the US
	user = models.ForeignKey(User)
	PHONE_CHOICES = (
	#different types of phone numbers they can add
		('Cell', 'Cell Phone'),
		('Home', 'Home Phone'),
		('Work', 'Work Phone'),
		('Other', 'Other Phone'),
	)
	number = PhoneNumberField(null=True, blank=True)
	#add in phone number (has to be US number)

class InternationalPhone(models.Model):
    user = models.ForeignKey(User)
    PHONE_CHOICES = (
    #different types of phone numbers they can add
	('Cell', 'Cell Phone'),
	('Home', 'Home Phone'),
	('Work', 'Work Phone'),
	('Other', 'Other Phone'),
    )
    nonusnumber = models.IntegerField(null=True, blank=True)
    #for people not in US
    typenum = models.CharField(max_length=5, choices=PHONE_CHOICES, null=True, blank=True)
    #choose which type of phone number it is

class USAddress(models.Model):
#fields to enter US address - lets them select state, makes sure it's a valid zip code
	user = models.ForeignKey(User)
	state = USPostalCodeField(null=True, blank=True)
	city = models.CharField(max_length=200, null=True, blank=True)
	zipcode = models.IntegerField(null=True, blank=True)
	#change this to an actual zipcode checking field
	street1 = models.CharField(max_length=200, null=True, blank=True)
	street2 = models.CharField(max_length=200, null=True, blank=True)
        class Meta:
            verbose_name = "Domestic Address"
            verbose_name_plural = "Domestic Addresses"

class OtherAddress(models.Model):
#fields to enter foreign address - 4 lines of charfields
	user = models.ForeignKey(User)
	line1 = models.CharField(max_length=200, null=True, blank=True)
	line2 = models.CharField(max_length=200, null=True, blank=True)
	line3 = models.CharField(max_length=200, null=True, blank=True)
	line4 = models.CharField(max_length=200, null=True, blank=True)
        class Meta:
            verbose_name = "International Address"
            verbose_name_plural = "International Addresses"

class CampusAddress(models.Model):
#campus address (current / exchange only?) - not required field (some students live off campus)
	user = models.ForeignKey(User)
	mailbox = models.IntegerField(null=True, blank=True)
	#campus mailbox
	DORM_CHOICES = (
	#dorm options
		('EH', 'East Hall'),
		('WH', 'West Hall'),
	)
	dorm = models.CharField(max_length=2, choices=DORM_CHOICES, null=True, blank=True)
	#choose which dorm they live in
	roomnumber = models.IntegerField(null=True, blank=True)
	#room number
        class Meta:
            verbose_name = "Campus Address"
            verbose_name_plural = "Campus Addresses"

class SocialMedia(models.Model):
	user = models.ForeignKey(User)
	SM_CHOICES = (
	#different social media sites
		('Skype', 'Skype'),
		('AIM', 'AIM'),
		('LI', 'LinkedIn'),
		('FB', 'Facebook'),
		('TW', 'Twitter'),
	)
	#choose which service it's for
	service = models.CharField(max_length=5, choices=SM_CHOICES, null=True, blank=True)
	#account username
	account = models.CharField(max_length=200, null=True, blank=True)
        class Meta:
            verbose_name = "Contact Method"


class Job(models.Model):
    user = models.ForeignKey(User)
    employer = models.CharField(max_length=200, null=True, blank=True)
    position = models.CharField(max_length=200, null=True, blank=True)
    #name of job
    jobdescription = models.TextField(blank=True, null=True)
    #place to put description of the job
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)


class Tags(models.Model):
    user = models.ForeignKey(User)
    tags = TaggableManager()
    class Meta:
	verbose_name = "Tag"
	verbose_name_plural = "Tags"
	#Tags is too embedded; cosmetic fix
	#do research before you do Tags forms

"""
Search stuff
From http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
"""
import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

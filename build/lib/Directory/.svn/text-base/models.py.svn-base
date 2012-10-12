from django.db import models
from django.forms import ModelForm
from django.contrib.localflavor.us.models import PhoneNumberField, USPostalCodeField
from django.contrib.localflavor.us.forms import USZipCodeField
from stdimage import StdImageField
#from tagging.fields import TagField
#from tagging.models import Tag
#from tagging_autocomplete_tagit.models import TagAutocompleteTagItField
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from taggit.managers import TaggableManager
from taggit_autocomplete.managers import TaggableManager



# Create your models here.
USER_TYPES = (
	('AL', 'Alumni'),
	#don't give option for campus address
	('CU', 'Current Students'),
	('EX', 'Exchange Students'),
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
    type = models.CharField(max_length=2, choices=USER_TYPES)
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
    picture = StdImageField(upload_to="/images/users/james_nee",
 size=(200, 400), thumbnail_size=(100,100), null=True, blank=True)
#size is full sized image resized, thumbnail_size creates a smaller thumbnail
# http://code.google.com/p/django-stdimage/ for documentation

class UserProfileForm(ModelForm):
    international = forms.BooleanField(initial=False, required=False)
    #this makes the international boolean work without requiring input
    class Meta:
        model = UserProfile
        exclude = ["user"]


class addEmail(models.Model):
	user = models.ForeignKey(User)
	email = models.EmailField()
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
	number = PhoneNumberField()
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
    nonusnumber = models.IntegerField()
    #for people not in US
    type = models.CharField(max_length=5, choices=PHONE_CHOICES)
    #choose which type of phone number it is

class USAddress(models.Model):
#fields to enter US address - lets them select state, makes sure it's a valid zip code
	user = models.ForeignKey(User)
	state = USPostalCodeField()
	city = models.CharField(max_length=200)
	zipcode = USZipCodeField()
	street1 = models.CharField(max_length=200)
	street2 = models.CharField(max_length=200)
        class Meta:
            verbose_name = "Domestic Address"
            verbose_name_plural = "Domestic Addresses"

class OtherAddress(models.Model):
#fields to enter foreign address - 4 lines of charfields
	user = models.ForeignKey(User)
	line1 = models.CharField(max_length=200)
	line2 = models.CharField(max_length=200)
	line3 = models.CharField(max_length=200)
	line4 = models.CharField(max_length=200)
        class Meta:
            verbose_name = "International Address"
            verbose_name_plural = "International Addresses"

class CampusAddress(models.Model):
#campus address (current / exchange only?) - not required field (some students live off campus)
	user = models.ForeignKey(User)
	mailbox = models.IntegerField()
	#campus mailbox
	DORM_CHOICES = (
	#dorm options
		('EH', 'East Hall'),
		('WH', 'West Hall'),
	)
	dorm = models.CharField(max_length=2, choices=DORM_CHOICES)
	#choose which dorm they live in
	roomnumber = models.IntegerField()
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
	account = models.CharField(max_length=200)
	#account username
	service = models.CharField(max_length=5, choices=SM_CHOICES)
	#choose which service it's for
        class Meta:
            verbose_name = "Contact Method"


class Job(models.Model):
    user = models.ForeignKey(User)
    employer = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    #name of job
    jobdescription = models.TextField()
    #place to put description of the job
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)


class Tags(models.Model):
#adding tagging - http://code.google.com/p/django-tagging/
    user = models.ForeignKey(User)
    tags = TaggableManager()
	#tags = TagAutocompleteTagItField(max_tags=False)
"""
	def get_tags(self):
	#function to get the tags for an object
		return Tag.objects.get_for_object(self)
"""

#do more research before you do Tags forms




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

from django.shortcuts import render_to_response, get_object_or_404
from Directory.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.contrib.auth import logout

def home(request):
    return render_to_response('directory/base.html',
 context_instance=RequestContext(request))

def logout_req(request):
    logout(request)
    return HttpResponseRedirect("/")

def contacts(request):
    profiles = UserProfile.objects.all().exclude(
        nickname = "admin"
    )
    return render_to_response('directory/addresscard.html',
 {"profiles":profiles}, context_instance=RequestContext(request))

def create_user(request):
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profileform = UserProfileForm(request.POST, request.FILES)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            """
            NOTE: since the user has just been created the profilefrom
            needs to be attached to this new user
            """
            pf = profileform.save(commit= False)
            #don't commit
            pf.user = request.user
            #define the user
            pf.save()
            #now save
            return HttpResponseRedirect("/second")
    else:
        userform = UserForm()
        profileform = UserProfileForm()
    return render_to_response("directory/manageusers.html",
    {"userform":userform, "profileform":profileform},
     context_instance=RequestContext(request))

def second(request):
    """
    This is the second half of the registration process.
    Most of the forms here are formsets.
    """
    EmailFormSet = modelformset_factory(addEmail, exclude=('user'), max_num=1)
    if request.method == "POST":
        emailformset = EmailFormSet(request.POST, request.FILES,)
        if emailformset.is_valid():
            for form in emailformset.forms:
                e = form.save(commit=False)
                e.user = request.user
                e.save()
            return HttpResponseRedirect('/contacts') # Redirect after POST
    else:
       emailformset = EmailFormSet(queryset=request.user.addemail_set.none())
    return render_to_response("directory/secondmanage.html",
    {"emailformset":emailformset,},
     context_instance=RequestContext(request))

def manage_users(request):
    filler = {"first": request.user.first_name,
    "last" : request.user.last_name,}
    profileobj = request.user.get_profile()
    profilefill = {"type": profileobj.type,
    "year" : profileobj.year,"middle" : profileobj.middle,
    "nickname" : profileobj.nickname,"maiden" : profileobj.maiden,
    "international" : profileobj.international,
    "picture" : profileobj.picture,}
    EmailFormSet = modelformset_factory(addEmail, exclude=('user'), max_num=1)
    TagFormSet = modelformset_factory(Tags, exclude=('user'), max_num=1)
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=request.user)
        profileform = UserProfileForm(request.POST, request.FILES, instance=profileobj)
        emailform = EmailFormSet(request.POST, request.FILES,)
        tagform = TagFormSet(request.POST, request.FILES,)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            pf = profileform.save(commit= False)
            #don't commit
            pf.user = request.user
            #define the user
            pf.save()
            emailform.save()
            tagform.save()
            return HttpResponseRedirect("/contacts")
    else:
        userform = UserForm(initial=filler)
        profileform = UserProfileForm(initial=profilefill)
        emailform = EmailFormSet(initial = request.user.addemail_set.all())
        tagform = TagFormSet(initial = request.user.tags_set.all())

    return render_to_response("directory/manageusers.html",
    {"userform":userform, "profileform":profileform,
    "emailform":emailform, "tagform":tagform,},
     context_instance=RequestContext(request))

"""
Search stuff
From http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
"""

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip(): #pulls search term from form that sends it
        query_string = request.GET['q']
        
	#this is where we would split stuff up depending on whether they used keywords
        entry_query = get_query(query_string, ['year', 'first', 'last',]) #fields to search

	#it also might be worthwhile to implement sorting by multiple different columns....        
        found_entries = User.objects.filter(entry_query).order_by('first') #how to order it

    return render_to_response('search/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))

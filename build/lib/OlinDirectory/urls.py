from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

"""
    This app will be the only app on this site, so with nothing 
    trailing the URL the home view is presented. Decoupling the 
    urls.py proved too difficult to do so it's just stuck here.
"""
    
urlpatterns += patterns('Directory.views', 
    url(r'^logout/', 'logout_req'),
    url(r'^createuser/', 'create_user'),
    url(r'^manageusers/', 'manage_users'),
    url(r'^second/', 'second'),
    url(r'^$', 'home'),
    url(r'^contacts/', 'contacts'),
    url(r'^second', 'second'),
    url(r'^search/', 'search'),
    url(r'^search/results', 'search'),
    (r'^taggit_autocomplete/', include('taggit_autocomplete.urls')),
        #(r'^tagging_autocomplete_tagit/', include('tagging_autocomplete_tagit.urls')),

)
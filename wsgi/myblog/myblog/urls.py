# -*- coding: utf8 -*-
from django.conf.urls import *
from myblog.blog.views import *
from myblog.blog.sitemaps import BlogSitemap
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from myblog.blog.models import Category
from django.conf import settings
admin.autodiscover()
sitemaps = {
    'blog': BlogSitemap,
}
urlpatterns = patterns('', 
    # Example:
     (r'^category_list/?$',category_list),
     (r'^poll_list/?$',poll_list),
     (r'^most_visited/?$',getVisited),
     (r'^feedback/?$',show_feedback_form),
     (r'^thankyou/?$',show_feedback_form),
     (r'^thanks/?$',getThanks),
     (r'^info/?$',getInfo),
     (r'^archive/(?P<monthSlug>\w+)/?$',getPosts),
     (r'polls/(?P<pollSlug>[-a-zA-Z0-9]+)/vote/?$',vote),
     (r'^poll_list/\d{4}/\d{1,2}/(?P<pollSlug>[-a-zA-Z0-9]+)/?$',getChoices),
     (r'\d{4}/\d{1,2}/(?P<postSlug>[-a-zA-Z0-9]+)/profile/?$', getProfile),
     (r'^$', getPosts),
     (r'^(?P<auth>\w+)_posts/?$',getPosts),
     (r'^admin/', include(admin.site.urls)),
     (r'serch/$', search),
     (r'^robots.txt$',robots),
     (r'^(?P<selected_page>\d+)/?$',getPosts),
     (r'^(?P<postSlug>[-a-zA-Z0-9]+)/?$',getPost),
     (r'^\d{4}/\d{1,2}/(?P<postSlug>[-a-zA-Z0-9]+)/?$', getPost),
     (r'^all_of_that_category/(?P<categorySlug>[-a-zA-Z0-9]+)/?$',getCategory),
     (r'^all_of_that_category/(?P<categorySlug>[-a-zA-Z0-9]+)/(?P<selected_page>\d+)/?$',getCategory),
     (r'^comments/', include('django.contrib.comments.urls')),
     (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
     (r'^feeds/posts/$', PostsFeed()),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),)
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)
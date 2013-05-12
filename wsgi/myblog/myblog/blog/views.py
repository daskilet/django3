# -*- coding: utf8 -*-
# Create your views here.
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from myblog.blog.models import *
from django.forms import ModelForm
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.contrib.syndication.views import Feed
from django.contrib.flatpages.models import FlatPage
from haystack.query import SearchQuerySet
from django.core.urlresolvers import reverse,resolve, Resolver404
import simplejson as json
import datetime
import os
import gdata.analytics.service
from myblog.true_settings import *
class Dlya_saita(object):
  def __init__(self,request):
    self.ssilka = request.get_host()
    self.context =  RequestContext(request)
def categories_spisok():
  spisok_categ = [element for element in Category.objects.all()]
  slovar = {'other':0}
  for element in spisok_categ:
    slovar[element]=0
  for element in slovar.keys():
     for unit in Post.objects.all():
        if element in unit.categories.all():
	  slovar[element]+=1
  for element in Post.objects.all():
    if not element.categories.all():
      slovar['other']+=1
  itog_spisok = [(key.title,slovar[key]) for key in slovar.keys()]  
  return itog_spisok
def archive():
  def padezh(n):
    if str(n)[-1]=='1':
      return '%d %s'%(n,'публикация')
    elif str(n)[-1] in ['2','3','4']:
      return '%d %s'%(n,'публикации')
    elif str(n)[-1] in ['0','5','6','7','8','9']:
      return '%d %s'%(n,'публикаций')
  year = datetime.datetime.now().year
  months=[]
  for element in range(0,6):
    car_mon=datetime.datetime.now().month-element
    if car_mon<=0:
      car_mon+=12
      months.append((str(car_mon),year-1))
    else:
      months.append((str(car_mon),year))
  
  imena_month={'1':"Январь",'2':"Февраль", '3':"Март",'4':"Апрель",'5':"Май",
                 '6':"Июнь",'7':"Июль","8":"Август",'9':"Сентябрь",'10':"Октябрь",
                 '11':"Ноябрь",'12':"Декабрь"}
  spisok_publ = [(padezh(len(Post.objects.filter(created__year = element[1],created__month = element[0]))),imena_month[str(element[0])],\
                        element[1],element[0]) for element in months]
  return spisok_publ
def category_list(request):
  ssil=Dlya_saita(request)
  categories=Category.objects.all()
  return render_to_response('blog/category_list.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),\
  "categories":categories,'site': ssil.ssilka},**recent_polls(request)),context_instance=ssil.context)
def poll_list(request):
  ssil=Dlya_saita(request)
  polls = Poll.objects.all()
  return render_to_response('blog/poll_list.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),\
  "polls":polls,'site': ssil.ssilka},**recent_polls(request)),context_instance=ssil.context)
def getPosts(request,selected_page=1,auth=None,monthSlug=None):
    # Get all blog posts
    ssil = Dlya_saita(request)
    if auth:
       posts = Post.objects.filter(author__username=auth).order_by('created')
    elif monthSlug:
      posts = Post.objects.filter(created__month=monthSlug).order_by('created')
    else:
       posts = Post.objects.all().order_by('created')

    # Add pagination
    pages = Paginator(posts, 5)
    try:
       returned_page = pages.page(selected_page)
    except EmptyPage:
       returned_page = pages.page(pages.num_pages)
    # Display all the posts
    return render_to_response('blog/posts.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),'posts':returned_page.object_list,\
                              'page':returned_page,'site': ssil.ssilka},**recent_polls(request)),context_instance = ssil.context)
def getPost(request,postSlug):
  ssil = Dlya_saita(request)
  post = Post.objects.filter(slug=postSlug)
  return render_to_response('blog/single.html',dict({ 'spisok_categ':categories_spisok(),'spisok_publ':archive(),'posts':post,'site': ssil.ssilka},\
                            **recent_polls(request)),context_instance = ssil.context)
def getChoices(request,pollSlug):
  ssil = Dlya_saita(request)
  pollfor = Poll.objects.filter(slug=pollSlug)[0]
  choices = Choice.objects.filter(poll=pollfor)
  mas=[(element.choice,element.votes) for element in choices]
  mas.append(choices[0].poll.question)
  choices_json = json.dumps(mas)
  return render_to_response('blog/choices_for_poll.html',{'spisok_categ':categories_spisok(),'site':ssil.ssilka,'spisok_publ':archive(),'spisok_publ':archive(),'choices':choices,\
                           'choices_json':choices_json},context_instance=ssil.context)  
def getCategory(request,categorySlug,selected_page=1):
  ssil = Dlya_saita(request)
  posts = Post.objects.all().order_by('-created')
  category_posts = []
  for post in posts:
    if categorySlug!='Other':
       if post.categories.filter(slug=categorySlug):
         category_posts.append(post)
    elif categorySlug=='Other':
      if not post.categories.all():
	category_posts.append(post)
  pages = Paginator(category_posts,5)
  if categorySlug!='Other':
     category = Category.objects.filter(slug=categorySlug)[0]
  else:
    category="Other"
  try:
    returned_page = pages.page(selected_page)
  except EmptyPage:
    returned_page = pages.page(pages.num_pages)
  return render_to_response('blog/posts.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),"posts":returned_page.object_list,\
  "page":returned_page,"category":category,'site': ssil.ssilka},**recent_polls(request)),context_instance = ssil.context)
class PostsFeed(Feed):
    title = "My Django Blog posts"
    link = "feeds/posts/"
    description = "Posts from My Django Blog"

    def items(self):
        return Post.objects.order_by('-created')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body
def getInfo(request):
  ssil = Dlya_saita(request)
  return render_to_response('blog/info.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),'site':ssil.ssilka},**recent_polls(request)),context_instance=ssil.context)
def getThanks(request):
  ssil = Dlya_saita(request)
  return render_to_response('blog/thanks.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),'site':ssil.ssilka},**recent_polls(request)),context_instance=ssil.context)
def getProfile(request,postSlug):
  ssil = Dlya_saita(request)
  return render_to_response('blog/profile.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),'user':Post.objects.get(slug=postSlug).author,\
                           'site':ssil.ssilka},**recent_polls(request)),context_instance=ssil.context)
def search(request):
  ssil = Dlya_saita(request)
  if 'serch' in request.GET and request.GET['serch']:
	try:
	   sTerm = request.GET['serch']
	except:
	   return HttpResponseRedirect('/')
	
	results = SearchQuerySet().auto_query(sTerm)
	posts = []
	for r in results:
		posts.append(r.object)
	#videos list contains all the videos those match the search criteria
	return render_to_response('blog/poisk_rezult.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),'text':posts,'site': ssil.ssilka},\
                                  **recent_polls(request)),context_instance=ssil.context)
def recent_polls(request):
    try:
       latest_poll_list = Poll.objects.all()[0]
    except IndexError:
      latest_poll_list=''
    choices = Choice.objects.filter(poll=latest_poll_list)
    return  {'spisok_categ':categories_spisok(),'spisok_publ':archive(),'latest_poll_list':latest_poll_list,'choices':choices}
def vote(request,pollSlug):
    ssil = Dlya_saita(request)
    if not request.session.get('had_voted',False):
       p = get_object_or_404(Poll, slug=pollSlug)
       try:
           selected_choice = p.choice_set.get(pk=request.POST['choice'])
       except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
           return render_to_response('blog/poll_detail.html', {
               'object': p,
               'error_message': "You didn't select a choice.",
           }, context_instance=RequestContext(request))
       else:
           selected_choice.votes += 1
           selected_choice.save()
           request.session['had_voted']=True
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
           return HttpResponseRedirect(reverse(getChoices, args=(pollSlug,)))
    else:
      return HttpResponseRedirect(reverse(getChoices,args=(pollSlug,)))
def popular(request, selected_page=1):
    ssil = Dlya_saita(request)
    client = gdata.analytics.service.AnalyticsDataService()
    client.ClientLogin("daskilet@mail.ru",GOOGLE_PASSWORD)
    client.ssl = True
    now = datetime.datetime.now()
    month=now.month
    month_minus_one = month-1
    if month_minus_one==0:
      month_minus_one=12
    if month<10:
      month = '0'+str(month)
    else:
      month = str(month)
    if month_minus_one<10:
      month_minus_one = '0'+str(month_minus_one)
    else:
      month_minus_one = str(month_minus_one)
    data = client.GetData(ids='ga:'+ga_prifileid,dimensions="ga:pagePath",metrics="ga:pageviews",
    start_date="%d-%s-%d"%(now.year,month_minus_one,now.day),end_date ="%d-%s-%d"%(now.year,
    month,now.day)) 
    dictionary={}
    for de in data.entry:
      view, args, kwargs = resolve(str(de.pagePath))
      if view == getPost:
                e = Post.objects.get(slug = kwargs["postSlug"])
                if e not in dictionary:
                   dictionary[e]=0
                else:
		  dictionary[e]+=1
    posts=[]
    views_count = []
    i=0
    for element in sorted(dictionary.items(),key=lambda(k,v):v, reverse=True):
      if i<5:
          posts.append(element[0])
          views_count.append(element[1])
          i+=1
      else:
	break
    pages = Paginator(posts, 5)
    try:
       returned_page = pages.page(selected_page)
    except EmptyPage:
       returned_page = pages.page(pages.num_pages)
    return render_to_response('blog/posts.html',dict({'spisok_categ':categories_spisok(),'spisok_publ':archive(),'posts':returned_page.object_list,\
                              'page':returned_page,'views_count':views_count,'site': ssil.ssilka},**recent_polls(request)),context_instance = ssil.context)
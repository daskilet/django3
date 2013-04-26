# -*- coding: utf8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from myblog.blog.models import *
from myblog.blog.models import UserProfile
from myblog.blog.models import Poll, Choice
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class PollAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("question",)}
    list_display = ('question', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'
    inlines = [ChoiceInline]

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug":("title",)}
  
class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline,]

class CategoryToPostInline(admin.TabularInline):
  model = CategoryToPost
  extra = 1
  
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}
    exclude = ('author',)
    inlines = [CategoryToPostInline]
    def save_model(self, request, obj, form, change):
      obj.author = request.user
      obj.save()
admin.site.register(Poll, PollAdmin)
admin.site.unregister(User)   
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
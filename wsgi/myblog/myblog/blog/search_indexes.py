# -*- coding: utf8 -*-
from haystack import indexes
from myblog.blog.models import Post
import datetime
class PostIndex(indexes.RealTimeSearchIndex,indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr='body')
    author = indexes.CharField(model_attr='author')
    categories = indexes.CharField(model_attr='categories')
    def index_queryset(self):
        "Used when the entire index for model is updated."
        return Post.objects.filter(created__lte=datetime.datetime.now())
    def get_model(self):
            return Post 

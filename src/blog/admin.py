from django.contrib import admin
from blog.models import BlogPost, Reply

admin.site.register(BlogPost)
admin.site.register(Reply)
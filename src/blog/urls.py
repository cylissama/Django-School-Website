from django.urls import path

from blog.views import(
	create_blog_view,
	detail_blog_view,
	edit_blog_view,
	delete_blog,
	add_reply,
)

#this is for easier reference of the app urls
app_name = 'blog'

urlpatterns = [
	path('create/', create_blog_view, name="create"),
	path('<slug>/', detail_blog_view, name="detail"),
	path('<slug>/edit', edit_blog_view, name="edit"),
	path('<slug>/delete', delete_blog, name="delete"),
	path('<slug>/reply', add_reply, name="reply"),
]
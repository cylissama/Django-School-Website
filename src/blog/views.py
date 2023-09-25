from django.shortcuts import render, redirect, get_object_or_404
from blog.models import BlogPost, Reply
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm, ReplyForm
from account.models import Account
from django.db.models import Q
from hitcount.views import HitCountMixin
from hitcount.models import HitCount

def create_blog_view (request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()
		context['success_message'] = "Posted"

	context['form'] = form

	return render(request, "blog/create_blog.html", context)

def detail_blog_view(request, slug):

	context = {}

	post = get_object_or_404(BlogPost, slug=slug)

	if request.method == 'POST':
		form = ReplyForm(request.POST)

		if form.is_valid():
			obj = form.save(commit=False)
			obj.post = post
			obj.save()

			return redirect('/')

	else:
		form = ReplyForm()

	context['blog_post'] = post
	context['form'] = form

	hit_count = HitCount.objects.get_for_object(post)

	hit_count_response = HitCountMixin.hit_count(request, hit_count)


	return render(request, 'blog/deatil_blog.html', context)


def edit_blog_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(BlogPost, slug=slug)

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance = blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj 

	form = UpdateBlogPostForm(
		initial = {
			"title": blog_post.title,
			"body": blog_post.body,
			"image": blog_post.image,
		}
	)
	context['form'] = form

	return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = BlogPost.objects.filter(
				Q(title__icontains=q) | 
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))	

def delete_blog(request, slug):

    blog_post = get_object_or_404(BlogPost, slug=slug)  # Get your current cat

         # If method is POST,
    blog_post.delete()                     # delete the cat.
    return redirect('/') 

def add_reply(request, slug):

	context = {}

	blog_post = get_object_or_404(BlogPost, slug=slug)

	form = ReplyForm(
		initial = {
			"post": blog_post,
			"name": blog_post.author.username,
		}
	)
	context['form'] = form

	return render(request, 'blog/add_reply.html', context)




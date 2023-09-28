from django import forms
from blog.models import BlogPost, Reply

class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image', 'file',]

class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image', 'file']

	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']
		if self.cleaned_data['file']:
			blog_post.file = self.cleaned_data['file']

		if commit:
			blog_post.save()
		return blog_post

class ReplyForm(forms.ModelForm):

	class Meta:
		model = Reply
		fields = ['post','name','body']
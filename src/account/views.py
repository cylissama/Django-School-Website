from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost
from account.models import *
from quiz.models import *
from account.forms import *
import json

def registration_view(request):
	context={}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else: #get request
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def del_user(request, username):    
    try:
        u = Account.objects.get(username = username)
        u.delete()
        messages.success(request, "The user is deleted")            

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return render(request, '/')

    except Exception as e: 
        return render(request, '/',{'err':e.message})

    return render(request, '/') 

def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):

	context = {}

	user = request.user 
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'account/login.html', context)

def account_view(request):

	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	attempts = SubmissionAttempts.objects.all()
	context['attempts'] = attempts
	accounts = Account.objects.all()
	context['accounts'] = accounts
	quiz_takers = QuizTaker.objects.all()
	context['quiz_takers'] = quiz_takers

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
				"email": request.POST['email'],
				"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(
			initial = {
				"email":request.user.email,
				"username":request.user.username,
			}
		)
	context['account_form'] = form

	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts

	return render(request, 'account/account.html', context)

def view_attempts(request):
	context = {}

	attempts = SubmissionAttempts.objects.all()
	context['attempts'] = attempts
	takers = QuizTaker.objects.all()
	context['takers'] = takers
	quizzes = Quiz.objects.all()
	context['quizzes'] = quizzes

	return render(request, 'view_attempts.html', context)

def search_results(request):
	query = request.GET.get('query')

	if query:
		results = Grade.objects.filter(letter_grade__icontains=query).order_by('letter_grade')
		combined_results = list(results)
		num_results = len(combined_results)
		if query == 'ascending':
			combined_results = Grade.objects.all().order_by('letter_grade')
			num_results = len(combined_results)
		if query == 'descending':
			combined_results = Grade.objects.all().order_by('-letter_grade')
			num_results = len(combined_results)
	else:
		combined_results = Grade.objects.all()
		num_results = 0

	return render(request, 'search_results.html', {'results': combined_results, 'query': query, 'num_results': num_results })

def search_results2(request):
	query2 = request.GET.get('query2')
	grades=Grade.objects.all()
	if query2:
		results = Account.objects.filter(username__icontains=query2)
		
		combined_results = list(results)
		num_results = len(combined_results)
	else:
		combined_results = Account.objects.all()
		num_results = len(combined_results)

	return render(request, 'search_results2.html', {'grades': grades, 'results': combined_results, 'query2': query2, 'num_results': num_results })

def search_results3(request):
	query3 = request.GET.get('query3')

	if query3:
		results = Grade.objects.filter(percent__icontains=query3)
		combined_results = list(results)
		num_results = len(combined_results)
		if query3 == 'ascending':
			combined_results = Grade.objects.all().order_by('percent')
			num_results = len(combined_results)
		if query3 == 'descending':
			combined_results = Grade.objects.all().order_by('-percent')
			num_results = len(combined_results)
	else:
		combined_results = Grade.objects.all()
		num_results = len(combined_results)

	return render(request, 'search_results3.html', {'results': combined_results, 'query3': query3, 'num_results': num_results })


def set_grade(request):
	context = {}

	form = setGrade()
	if request.method == 'POST':
		form = setGrade(request.POST)
		if form.is_valid():
			form.save()
			return redirect(request, 'set_grade.html', context)
	
	context['form'] = form


	return render(request, 'set_grade.html', context)

def scores_view(request):
	context = {}
	quiz_takers=QuizTaker.objects.all()
	context['quiz_takers']=quiz_takers
	grades=Grade.objects.all()
	context['grades']=grades
	subjects=Subject.objects.all()
	context['subjects']=subjects

	scores = []
	names = []

	for grade in grades:
		if grade.student == request.user:
			scores.append(str(grade.percent))
			names.append(grade.subject)
	
	context['names'] = names
	context['scores'] = scores

	data = {
		'labels': names,
		'values': scores,
	}

	context['chart_data'] = json.dumps(data)
	
	mathGrades = []
	lGrades= ['A','B','C','D','F']
	
	#math
	a=0
	b=0
	c=0
	d=0
	f=0
	for grade in grades:
		if grade.subject == 'Math':
			if grade.letter_grade == 'A':
				a += 1
			if grade.letter_grade == 'B':
				b += 1
			if grade.letter_grade == 'C':
				c += 1
			if grade.letter_grade == 'D':
				d += 1
			if grade.letter_grade == 'F':
				f +=1
	mathGrades = [a,b,c,d,f]
	mathPie = {
		'mathGrades': mathGrades,
		'lGrades': lGrades,
	}
	context['mathPie'] = json.dumps(mathPie)

	#CompSci
	a=0
	b=0
	c=0
	d=0
	f=0
	for grade in grades:
		if grade.subject == 'Comp Sci':
			if grade.letter_grade == 'A':
				a += 1
			if grade.letter_grade == 'B':
				b += 1
			if grade.letter_grade == 'C':
				c += 1
			if grade.letter_grade == 'D':
				d += 1
			if grade.letter_grade == 'F':
				f +=1
	csGrades = [a,b,c,d,f]
	csPie = {
		'csGrades': csGrades,
		'lGrades': lGrades,
	}
	context['csPie'] = json.dumps(csPie)

	#Reading
	a=0
	b=0
	c=0
	d=0
	f=0
	for grade in grades:
		if grade.subject == 'Reading':
			if grade.letter_grade == 'A':
				a += 1
			if grade.letter_grade == 'B':
				b += 1
			if grade.letter_grade == 'C':
				c += 1
			if grade.letter_grade == 'D':
				d += 1
			if grade.letter_grade == 'F':
				f +=1
	readingGrades = [a,b,c,d,f]
	readingPie = {
		'readingGrades': readingGrades,
		'lGrades': lGrades,
	}
	context['readingPie'] = json.dumps(readingPie)

	#Writing
	a=0
	b=0
	c=0
	d=0
	f=0
	for grade in grades:
		if grade.subject == 'Writing':
			if grade.letter_grade == 'A':
				a += 1
			if grade.letter_grade == 'B':
				b += 1
			if grade.letter_grade == 'C':
				c += 1
			if grade.letter_grade == 'D':
				d += 1
			if grade.letter_grade == 'F':
				f +=1
	writingGrades = [a,b,c,d,f]
	writingPie = {
		'writingGrades': writingGrades,
		'lGrades': lGrades,
	}
	context['writingPie'] = json.dumps(writingPie)



	
	accounts = Account.objects.all()
	context['accounts']=accounts
	

	form = setGrade()
	if request.method == 'POST':
		form = setGrade(request.POST)
		if form.is_valid():
			form.save()
			form = setGrade()
			context['form'] = form
			return redirect('scores')
	
	context['form'] = form

	
	return render(request, 'account/scores.html', context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})












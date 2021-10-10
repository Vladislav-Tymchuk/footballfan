from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Club, Post, Comment, UserPost
import requests
from bs4 import BeautifulSoup
import numpy as np
from django.contrib.auth.models import Group, User
from .forms import RegistrationForm, CommentForm, UserPostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import datetime


def home(request):

	posts = Post.objects

	url = 'https://premierliga.ru/tournaments/championship/tournament-table/'

	r = requests.get(url)

	# нахожу клубы по порядку
	club = BeautifulSoup(r.text, 'lxml')
	clubs = club.find_all('td', class_='club')

	# нахожу сыгранные матчи

	match = BeautifulSoup(r.text, 'lxml')
	matches = match.find_all('td', class_='dark-blue num')

	# нахожу кол-во побед

	victory = BeautifulSoup(r.text, 'lxml')
	victories = match.find_all('td', class_='dark-blue num')

	# нахожу кол-во ничьих

	draw = BeautifulSoup(r.text, 'lxml')
	draws = match.find_all('td', class_='dark-blue num')

	# нахожу кол-во поражений

	defeat = BeautifulSoup(r.text, 'lxml')
	defeats = match.find_all('td', class_='dark-blue num')

	# нахожу з-п

	goal = BeautifulSoup(r.text, 'lxml')
	goals = goal.find_all('td', class_='dark-blue goals')

	# нахожу очки
	pt = BeautifulSoup(r.text, 'lxml')
	pts = pt.find_all('p', class_='points')

	# фильтр команд
	clubs_list = []
	for club in clubs:
	    clubs_list.append(club.text[1:][:-1])
	clubs_list = clubs_list[1:]

	# фильтр количества матчей
	dirty_list = []
	for match in matches:
	    dirty_list.append(match.text[1:][:-1])
	matches_list = dirty_list[::5]

	# фильтр побед
	dirty_list = []
	for victory in victories:
	    dirty_list.append(victory.text[1:][:-1])
	victories_list = dirty_list[1::5]

	# фильтр ничьих
	dirty_list = []
	for draw in draws:
	    dirty_list.append(draw.text[1:][:-1])
	draws_list = dirty_list[2::5]

	# фильтр поражений
	dirty_list = []
	for defeat in defeats:
	    dirty_list.append(defeat.text[1:][:-1])
	defeats_list = dirty_list[3::5]

	# фильтр голов
	goals_list = []
	for goal in goals:
	    goals_list.append(goal.text[2:-2])

	# фильтр очков
	pts_list = []
	for pt in pts:
	    pts_list.append(pt.text)

	# парсинг бомбардиров

	url = 'https://premierliga.ru/players/scorers'
	r = requests.get(url)

	# ищу игроков и фильтрую
	scorer = BeautifulSoup(r.text, 'lxml')
	scorers = scorer.find_all('tr', class_='player')

	scorers_list = []
	for scorer in scorers:
	    scorers_list.append(scorer.text[7:-35])
	scorers_list = scorers_list[:16]

	# кол-во голов и фильтрую
	scorer_goal = BeautifulSoup(r.text, 'lxml')
	scorer_goals = scorer_goal.find_all('b')

	scorer_goals_list = []
	for i in scorer_goals:
	    scorer_goals_list.append(i.text)
	scorer_goals_list = scorer_goals_list[-20:-4]

	# кол-во голов с пенальти и фильтрую
	scorer_goal_pen = BeautifulSoup(r.text, 'lxml')
	scorer_goals_pen = scorer_goal_pen.find_all('p')

	scorer_goals_pen_list = []
	for i in scorer_goals_pen:
	    scorer_goals_pen_list.append(i.text)
	dirty = scorer_goals_pen_list[21::9]
	scorer_goals_pen_list = dirty[:16]

	# парсинг ассистентов

	url = 'https://premierliga.ru/stats/assist/'

	r = requests.get(url)

	# нахожу ассистентов и фильтрую
	assistant = BeautifulSoup(r.text, 'lxml')
	assistants = assistant.find_all('p', class_='name')

	assistants_list = []
	for assistant in assistants:
	    assistants_list.append(assistant.text)
	assistants_list = assistants_list[:16]

	# нахожу количество ассистов и фильтрую
	assistant_pass = BeautifulSoup(r.text, 'lxml')
	assistants_passes = assistant_pass.find_all('p', class_='score')

	assistants_passes_list = []
	for assistant_pass in assistants_passes:
	    assistants_passes_list.append(assistant_pass.text)
	assistants_passes_list = assistants_passes_list[:16]

	# нахожу сыгранное время и фильтрую
	assistant_minute = BeautifulSoup(r.text, 'lxml')
	assistants_minutes = assistant_minute.find_all('p', class_='time')

	assistants_minutes_list = []
	for assistant_minute in assistants_minutes:
	    assistants_minutes_list.append(assistant_minute.text)
	assistants_minutes_list = assistants_minutes_list[:16]


	keys_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

	values_list = np.reshape(np.dstack((clubs_list, matches_list, victories_list, draws_list, defeats_list, goals_list,
	                                    pts_list, scorers_list, scorer_goals_list, scorer_goals_pen_list,
	                                    assistants_list, assistants_passes_list, assistants_minutes_list)), [-1, 13])

	data = dict(zip(keys_list, values_list))

	data.update({
	    'posts': posts
	})

	return render(request, 'home.html', {'data': data})



def rpl_21(request):

	url = 'https://premierliga.ru/tournaments/championship/tournament-table/'

	r = requests.get(url)

	# нахожу клубы по порядку
	club = BeautifulSoup(r.text, 'lxml')
	clubs = club.find_all('td', class_='club')

	# нахожу сыгранные матчи
	match = BeautifulSoup(r.text, 'lxml')
	matches = match.find_all('td', class_='dark-blue num')

	# нахожу кол-во побед
	victory = BeautifulSoup(r.text, 'lxml')
	victories = match.find_all('td', class_='dark-blue num')

	# нахожу кол-во ничьих
	draw = BeautifulSoup(r.text, 'lxml')
	draws = match.find_all('td', class_='dark-blue num')

	# нахожу кол-во поражений
	defeat = BeautifulSoup(r.text, 'lxml')
	defeats = match.find_all('td', class_='dark-blue num')

	# нахожу з-п
	goal = BeautifulSoup(r.text, 'lxml')
	goals = goal.find_all('td', class_='dark-blue goals')

	# нахожу очки
	pt = BeautifulSoup(r.text, 'lxml')
	pts = pt.find_all('p', class_='points')


	# фильтр команд
	clubs_list = []
	for club in clubs:
	    clubs_list.append(club.text[1:][:-1])
	clubs_list = clubs_list[1:]

	# фильтр количества матчей
	dirty_list = []
	for match in matches:
	    dirty_list.append(match.text[1:][:-1])
	matches_list = dirty_list[::5]

	# фильтр побед
	dirty_list = []
	for victory in victories:
	    dirty_list.append(victory.text[1:][:-1])
	victories_list = dirty_list[1::5]

	# фильтр ничьих
	dirty_list = []
	for draw in draws:
	    dirty_list.append(draw.text[1:][:-1])
	draws_list = dirty_list[2::5]

	# фильтр поражений
	dirty_list = []
	for defeat in defeats:
	    dirty_list.append(defeat.text[1:][:-1])
	defeats_list = dirty_list[3::5]

	# фильтр голов
	goals_list = []
	for goal in goals:
	    goals_list.append(goal.text[2:-2])

	# фильтр очков
	pts_list = []
	for pt in pts:
	    pts_list.append(pt.text)

	keys_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

	values_list = np.reshape(np.dstack((clubs_list, matches_list, victories_list, draws_list, defeats_list, 
										goals_list, pts_list)), [-1, 7])

	data = dict(zip(keys_list, values_list))


	return render(request, 'rpl_21.html', {'data': data})

def scorers(request):

	url = 'https://premierliga.ru/players/scorers/'

	r = requests.get(url)

	scorer = BeautifulSoup(r.text, 'html.parser')
	scorers = scorer.find_all('a')

	scorers_list = []
	for scorer in scorers:
	    scorers_list.append(scorer.text)
	scorers_list = scorers_list[157:177:2]


	goal = BeautifulSoup(r.text, 'html.parser')
	goals = goal.find_all('b')

	goals_list = []
	for goal in goals:
	    goals_list.append(goal.text)
	goals_list = goals_list[-20:-10:]

	pen = BeautifulSoup(r.text, 'html.parser')
	pens = pen.find_all('p')

	pens_list = []
	for pen in pens:
	    pens_list.append(pen.text)
	pens_list = pens_list[21::9][:10]

	match = BeautifulSoup(r.text, 'html.parser')
	matches = match.find_all('p')

	matches_list = []
	for match in matches:
	    matches_list.append(match.text)
	matches_list = matches_list[22::9][:10]


	keys_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

	values_list = np.reshape(np.dstack((scorers_list, goals_list, pens_list, matches_list)), [-1, 4])
	data = dict(zip(keys_list, values_list))

	return render(request, 'scorers.html', {'data': data})

def assistants(request):

	url = 'https://premierliga.ru/stats/assist/'

	r = requests.get(url)

	assistant = BeautifulSoup(r.text, 'lxml')
	assistants = assistant.find_all('p', class_='name')

	assistants_list = []
	for assistant in assistants:
	    assistants_list.append(assistant.text)
	assistants_list = assistants_list[:10]


	assist = BeautifulSoup(r.text, 'lxml')
	assists = assist.find_all('p', class_='score')

	assists_list = []
	for assist in assists:
	    assists_list.append(assist.text)
	assists_list = assists_list[:10]


	minute = BeautifulSoup(r.text, 'lxml')
	minutes = minute.find_all('p', class_='time')

	minutes_list = []
	for minute in minutes:
	    minutes_list.append(minute.text)
	minutes_list = minutes_list[:10]

	keys_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

	values_list = np.reshape(np.dstack((assistants_list, assists_list, minutes_list)), [-1, 3])
	data = dict(zip(keys_list, values_list))


	return render(request, 'assistants.html', {'data': data})


def myclub(request, club_slug):

	club_page = get_object_or_404(Club, club_slug=club_slug)
	posts = Post.objects.filter(post_club=club_page)

	return render(request, 'posts_for_club.html', {'posts': posts, 'club_page': club_page})

def full_post(request, post_slug):

	post = get_object_or_404(Post, post_slug=post_slug)
	comments=Comment.objects.filter(post=post).order_by("-timestamp")
	post_club = post.post_club
	posts_this_club = Post.objects.filter(post_club=post_club)

	posts_to_show = []
	for post_this_club in posts_this_club:
		if post.post_title != post_this_club.post_title:
			posts_to_show.append(post_this_club)

	if request.method == 'POST':
	    form = CommentForm(request.POST)
	    if form.is_valid():
		    content = request.POST.get('content')
		    comment = Comment.objects.create(post = post, user = request.user, content = content)
		    comment.timestamp = datetime.datetime.now()
		    comment.save()
		    return redirect(post.get_absolute_url())
	else:
	    form = CommentForm()

	post = Post.objects.get(post_slug=post_slug)

	num_of_comments = Comment.objects.filter(post = post).count()

	context={
	'comments': comments,
    'form': form,
    'post': post,
    'num_of_comments': num_of_comments,
    'posts_to_show': posts_to_show
    }

	return render(request, 'post.html', context)

def delete_comment(request, pk):
	comment = get_object_or_404(Comment, id=pk)
	post = comment.post

	comment.delete()

	return redirect(reverse('post', args=[post.post_slug]))

def create_post(request):
	error = ''
	if request.method == 'POST':
		form = UserPostForm(request.POST)
		if form.is_valid():
			userpost_title = request.POST.get('userpost_title')
			userpost_content = request.POST.get('userpost_content')
			userpost_image = request.POST.get('userpost_image')
			userpost = UserPost.objects.create(userpost_title = userpost_title, userpost_content = userpost_content,
				userpost_image =userpost_image)
			userpost.timestamp = datetime.datetime.now()
			return redirect('home')
		else:
			messages.error(request,'Имя пользователя или пароль неверны')
	else:
		form = UserPostForm()

	return render(request, 'userpost.html', {'form': form, 'error': error})


def registrationView(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username=username)
			user_group = Group.objects.get(name='User')
			user_group.user_set.add(signup_user)
	else:
		form = RegistrationForm()

	return render(request, 'registration.html', {'form': form})


def loginView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.error(request,'Имя пользователя или пароль неверны')
				return redirect('login')
	else:
		form = AuthenticationForm()

	return render(request, 'login.html', {'form': form})


def logoutView(request):
	logout(request)
	return redirect('home')

def accountView(request):

	return render(request, 'account.html')

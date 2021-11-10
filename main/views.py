from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Club, Post, Comment
import requests
from bs4 import BeautifulSoup
import numpy as np
from django.contrib.auth.models import Group, User
from .forms import RegistrationForm, CommentForm
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
	clubsList = []
	for club in clubs:
	    clubsList.append(club.text[1:][:-1])
	clubsList = clubsList[1:]

	# фильтр количества матчей
	dirtyList = []
	for match in matches:
	    dirtyList.append(match.text[1:][:-1])
	matchesList = dirtyList[::5]

	# фильтр побед
	dirtyList = []
	for victory in victories:
	    dirtyList.append(victory.text[1:][:-1])
	victoriesList = dirtyList[1::5]

	# фильтр ничьих
	dirtyList = []
	for draw in draws:
	    dirtyList.append(draw.text[1:][:-1])
	drawsList = dirtyList[2::5]

	# фильтр поражений
	dirtyList = []
	for defeat in defeats:
	    dirtyList.append(defeat.text[1:][:-1])
	defeatsList = dirtyList[3::5]

	# фильтр голов
	goalsList = []
	for goal in goals:
	    goalsList.append(goal.text[2:-2])

	# фильтр очков
	ptsList = []
	for pt in pts:
	    ptsList.append(pt.text)

	# парсинг бомбардиров
	url = 'https://premierliga.ru/players/scorers'
	r = requests.get(url)

	# ищу игроков и фильтрую
	scorer = BeautifulSoup(r.text, 'lxml')
	scorers = scorer.find_all('tr', class_='player')

	scorersList = []
	for scorer in scorers:
	    scorersList.append(scorer.text[7:-35])
	scorersList = scorersList[:16]

	# кол-во голов и фильтрую
	scorerGoal = BeautifulSoup(r.text, 'lxml')
	scorerGoals = scorerGoal.find_all('b')

	scorerGoalsList = []
	for i in scorerGoals:
	    scorerGoalsList.append(i.text)
	scorerGoalsList = scorerGoalsList[-20:-4]

	# кол-во голов с пенальти и фильтрую
	scorerGoalPen = BeautifulSoup(r.text, 'lxml')
	scorerGoalsPen = scorerGoalPen.find_all('p')

	scorerGoalsPenList = []
	for i in scorerGoalsPen:
	    scorerGoalsPenList.append(i.text)
	dirty = scorerGoalsPenList[21::9]
	scorerGoalsPenList = dirty[:16]

	# парсинг ассистентов
	url = 'https://premierliga.ru/stats/assist/'

	r = requests.get(url)

	# нахожу ассистентов и фильтрую
	assistant = BeautifulSoup(r.text, 'lxml')
	assistants = assistant.find_all('p', class_='name')

	assistantsList = []
	for assistant in assistants:
	    assistantsList.append(assistant.text)
	assistantsList = assistantsList[:16]

	# нахожу количество ассистов и фильтрую
	assistantPass = BeautifulSoup(r.text, 'lxml')
	assistantsPasses = assistantPass.find_all('p', class_='score')

	assistantsPassesList = []
	for assistantPass in assistantsPasses:
	    assistantsPassesList.append(assistantPass.text)
	assistantsPassesList = assistantsPassesList[:16]

	# нахожу сыгранное время и фильтрую
	assistantMinute = BeautifulSoup(r.text, 'lxml')
	assistantsMinutes = assistantMinute.find_all('p', class_='time')

	assistantsMinutesList = []
	for assistantMinute in assistantsMinutes:
	    assistantsMinutesList.append(assistantMinute.text)
	assistantsMinutesList = assistantsMinutesList[:16]

	keysList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

	valuesList = np.reshape(np.dstack((clubsList, matchesList, victoriesList, drawsList, defeatsList, goalsList,
	                                    ptsList, scorersList, scorerGoalsList, scorerGoalsPenList,
	                                    assistantsList, assistantsPassesList, assistantsMinutesList)), [-1, 13])

	data = dict(zip(keysList, valuesList))

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
	clubsList = []
	for club in clubs:
	    clubsList.append(club.text[1:][:-1])
	clubsList = clubsList[1:]

	# фильтр количества матчей
	dirtyList = []
	for match in matches:
	    dirtyList.append(match.text[1:][:-1])
	matchesList = dirtyList[::5]

	# фильтр побед
	dirtyList = []
	for victory in victories:
	    dirtyList.append(victory.text[1:][:-1])
	victoriesList = dirtyList[1::5]

	# фильтр ничьих
	dirtyList = []
	for draw in draws:
	    dirtyList.append(draw.text[1:][:-1])
	drawsList = dirtyList[2::5]

	# фильтр поражений
	dirtyList = []
	for defeat in defeats:
	    dirtyList.append(defeat.text[1:][:-1])
	defeatsList = dirtyList[3::5]

	# фильтр голов
	goalsList = []
	for goal in goals:
	    goalsList.append(goal.text[2:-2])

	# фильтр очков
	ptsList = []
	for pt in pts:
	    ptsList.append(pt.text)

	keysList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

	valuesList = np.reshape(np.dstack((clubsList, matchesList, victoriesList, drawsList, defeatsList, 
										goalsList, ptsList)), [-1, 7])

	data = dict(zip(keysList, valuesList))

	return render(request, 'rpl_21.html', {'data': data})

def scorers(request):

	url = 'https://premierliga.ru/players/scorers/'

	r = requests.get(url)

	# нахожу бомбардиров и фильтрую
	scorer = BeautifulSoup(r.text, 'html.parser')
	scorers = scorer.find_all('a')

	scorersList = []
	for scorer in scorers:
	    scorersList.append(scorer.text)
	scorersList = scorersList[157:177:2]

	# кол-во голов и фильтрую
	goal = BeautifulSoup(r.text, 'html.parser')
	goals = goal.find_all('b')

	goalsList = []
	for goal in goals:
	    goalsList.append(goal.text)
	goalsList = goalsList[-20:-10:]

	# кол-во голов с пенальти и фильтрую
	pen = BeautifulSoup(r.text, 'html.parser')
	pens = pen.find_all('p')

	pensList = []
	for pen in pens:
	    pensList.append(pen.text)
	pensList = pensList[21::9][:10]

	# сыгранные матчи и фильтрую
	match = BeautifulSoup(r.text, 'html.parser')
	matches = match.find_all('p')

	matchesList = []
	for match in matches:
	    matchesList.append(match.text)
	matchesList = matchesList[22::9][:10]

	keysList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

	valuesList = np.reshape(np.dstack((scorersList, goalsList, pensList, matchesList)), [-1, 4])

	data = dict(zip(keysList, valuesList))

	return render(request, 'scorers.html', {'data': data})

def assistants(request):

	url = 'https://premierliga.ru/stats/assist/'

	r = requests.get(url)

	# нахожу ассистентов и фильтрую
	assistant = BeautifulSoup(r.text, 'lxml')
	assistants = assistant.find_all('p', class_='name')

	assistantsList = []
	for assistant in assistants:
	    assistantsList.append(assistant.text)
	assistantsList = assistantsList[:10]

	# кол-во ассистов и фильтрую
	assist = BeautifulSoup(r.text, 'lxml')
	assists = assist.find_all('p', class_='score')

	assistsList = []
	for assist in assists:
	    assistsList.append(assist.text)
	assistsList = assistsList[:10]

	# сыгранные минуты и фильтрую
	minute = BeautifulSoup(r.text, 'lxml')
	minutes = minute.find_all('p', class_='time')

	minutesList = []
	for minute in minutes:
	    minutesList.append(minute.text)
	minutesList = minutesList[:10]

	keysList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

	valuesList = np.reshape(np.dstack((assistantsList, assistsList, minutesList)), [-1, 3])

	data = dict(zip(keysList, valuesList))

	return render(request, 'assistants.html', {'data': data})


def chooseClub(request):

	return render(request, 'choose_club.html')

def myClub(request, club_slug):

	clubPage = get_object_or_404(Club, club_slug=club_slug)
	posts = Post.objects.filter(post_club=clubPage)

	return render(request, 'posts_for_club.html', {'posts': posts, 'clubPage': clubPage})


def fullPost(request, post_slug):

	post = get_object_or_404(Post, post_slug=post_slug)
	comments = Comment.objects.filter(post=post).order_by("-timestamp")
	postClub = post.post_club
	postsThisClub = Post.objects.filter(post_club=postClub)

	postsToShow = []
	for postThisClub in postsThisClub:
		if post.post_title != postThisClub.post_title:
			postsToShow.append(postThisClub)

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

	numOfComments = Comment.objects.filter(post = post).count()

	context = {
	'comments': comments,
    'form': form,
    'post': post,
    'numOfComments': numOfComments,
    'postsToShow': postsToShow
    }

	return render(request, 'post.html', context)

def deleteComment(request, pk):
	comment = get_object_or_404(Comment, id=pk)
	post = comment.post

	comment.delete()

	return redirect(reverse('post', args=[post.post_slug]))


def registrationView(request):

	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signupUser = User.objects.get(username=username)
			userGroup = Group.objects.get(name='User')
			userGroup.user_set.add(signupUser)
			return redirect('login')
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


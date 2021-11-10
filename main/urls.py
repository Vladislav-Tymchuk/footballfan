from django.urls import path, include
from . import views


urlpatterns = [ 
    path('', views.home, name='home'),
    path('table/rpl/21-22', views.rpl_21, name='rpl_21'),
    path('registration', views.registrationView, name='registration'),
    path('club', views.chooseClub, name='club'),
    path('club/<slug:club_slug>/news', views.myClub, name='myClub'), 
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('rpl/scorers', views.scorers, name='scorers'),
    path('rpl/assistants', views.assistants, name='assistants'),
    path('posts/<slug:post_slug>', views.fullPost, name='post'),
    path('comment/<int:pk>/delete', views.deleteComment, name='deleteComment'),
]
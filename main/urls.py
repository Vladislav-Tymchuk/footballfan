from django.urls import path, include
from . import views


urlpatterns = [ 
    path('', views.home, name='home'),
    path('table/rpl/21-22', views.rpl_21, name='rpl_21'),
    path('registration', views.registrationView, name='registration'), 
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('account', views.accountView, name='account'),
    path('rpl/scorers', views.scorers, name='scorers'),
    path('rpl/assistants', views.assistants, name='assistants'),
    path('club/<slug:club_slug>/news', views.myclub, name='myclub'),
    path('posts/<slug:post_slug>', views.full_post, name='post'),
    path('comment/<int:pk>/delete', views.delete_comment, name='delete_comment'),
    path('account/create/post', views.create_post, name='create_post')
]
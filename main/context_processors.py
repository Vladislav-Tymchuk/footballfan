from .models import Club

def menu_clubs(request):
	clubs = Club.objects.all()
	return dict(clubs=clubs)
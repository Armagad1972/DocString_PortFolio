from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def home(request):
    """
    This is the home view.
    """
    return render(request, 'home.html')
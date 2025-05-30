from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView
from accounts.forms import UserRegistrationForm
from accounts.models import Societe


# Create your views here.

@login_required
def home(request):
    """
    This is the home view.
    """
    return render(request, 'home.html')


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, 'home')
        else:
            context['errors'] = form.errors
    else:
        form = UserRegistrationForm()

    return render(request, 'signup.html', context={"form": form})


class SocieteListView(LoginRequiredMixin, ListView):
    model = Societe
    template_name = 'societe.html'
    context_object_name = 'societes'
    ordering = ['nom']
    paginate_by = 10

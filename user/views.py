from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['title'] = "Online Learning"
        return context



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.tutor_user.description = form.cleaned_data.get('description')
            user.tutor_user.degree = form.cleaned_data.get('degree')
            user.save()
            raw_password = form.cleaned_data.get('password')
            # user = authenticate(request=request, username=user.email, password=raw_password)
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = SignUpForm()
    return render(request, '', {'form': form})
import hashlib
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LogoutView as LogOutView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import FormView, View

from .models import Hash
from .forms import HashForm

User = get_user_model()


class IndexView(FormView):
    template_name = 'sha256/index.html'
    form_class = HashForm


class HashGenerator(View):
    def post(self, request, *args, **kwargs):
        """generating hashing from text"""
        form = HashForm(request.POST or None)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
            return JsonResponse({'hash': hash})
        return JsonResponse({'msg': 'invalid text'}, status=400)


class LoginView(FormView):
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = authenticate(request=self.request, **form.cleaned_data)
        if user:
            login(self.request, user)
            return JsonResponse({'msg': 'authentication successful'})
        form.add_error(None, 'Wrong username/password please try again')
        return self.form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        if context['form'].errors:
            status = 400
        else:
            status = 200
        rendered_form = render_to_string('sha256/form.html', context, request=self.request)
        return JsonResponse({'form': rendered_form}, status=status)


class RegisterView(LoginView):
    form_class = UserCreationForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        User.objects.create_user(
            username=username,
            password=password
        )
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return JsonResponse({'msg': 'user created'})


class LogoutView(LogOutView):
    def render_to_response(self, context, **response_kwargs):
        return JsonResponse({'msg': 'logged out'})

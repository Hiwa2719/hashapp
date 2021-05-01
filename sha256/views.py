import hashlib
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as LogOutView, PasswordChangeView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
# from django.contrib.auth.urls import
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.views.generic import FormView, View, ListView, CreateView
from django.views.generic import TemplateView, DeleteView

from .models import Hash
from .forms import HashForm

User = get_user_model()


def hash_generator(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class IndexView(FormView):
    template_name = 'sha256/index.html'
    form_class = HashForm


class HashGenerator(View):
    def post(self, request, *args, **kwargs):
        """generating hashing from text"""
        form = HashForm(request.POST or None)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            hash = hash_generator(text)
            return JsonResponse({'hash': hash})
        return JsonResponse({'msg': 'invalid text'}, status=400)


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        user = authenticate(request=self.request, **form.cleaned_data)
        if user:
            login(self.request, user)
            if self.request.is_ajax():
                return JsonResponse({'msg': 'authentication successful'})
            return HttpResponseRedirect(self.get_success_url())
        form.add_error(None, 'Wrong username/password please try again')
        return self.form_invalid(form)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url if url else self.success_url

    def render_to_response(self, context, **response_kwargs):
        if context['form'].errors:
            status = 400
        else:
            status = 200
        if self.request.is_ajax():
            rendered_form = render_to_string('sha256/form.html', context, request=self.request)
            return JsonResponse({'form': rendered_form}, status=status)
        return super().render_to_response(context, **response_kwargs)


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        User.objects.create_user(
            username=username,
            password=password
        )
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        if self.request.is_ajax():
            return JsonResponse({'msg': 'user created'})
        return HttpResponseRedirect(reverse('account'))

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            rendered_form = render_to_string('sha256/form.html', context, request=self.request)
            return JsonResponse({'form': rendered_form},
                                status=400 if context['form'].errors else 200)
        return super().render_to_response(context, **response_kwargs)


class LogoutView(LogOutView):
    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return JsonResponse({'msg': 'logged out'})
        return HttpResponseRedirect(reverse('index'))


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'sha256/account.html'


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            render_modal_body = render_to_string('sha256/delete_account.html', context={'user': self.request.user},
                                                 request=self.request)
            return JsonResponse({'modal-body': render_modal_body})


class PasswordChange(PasswordChangeView):

    def render_to_response(self, context, **response_kwargs):
        if context['form'].errors:
            status = 400
        else:
            status = 200
        render_form = render_to_string('sha256/form.html', context=context, request=self.request)
        return JsonResponse({'form': render_form}, status=status)

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return JsonResponse({'msg': 'password successfully changed'})


class HashListView(LoginRequiredMixin, ListView):
    def render_to_response(self, context, **response_kwargs):
        render_list = render_to_string('sha256/saved_hashes.html', context=context)
        return JsonResponse({'list': render_list})

    def get_queryset(self):
        queryset = Hash.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(text=query) | Q(hash=query))
        return queryset


class SaveHash(LoginRequiredMixin, CreateView):
    form_class = HashForm
    model = Hash

    def form_valid(self, form):
        text = form.cleaned_data.get('text')
        hash = form.save(user=self.request.user, hash=hash_generator(text))
        return JsonResponse({hash.text: hash.hash}, status=201)

    def render_to_response(self, context, **response_kwargs):
        render_form = render_to_string('sha256/form.html', context=context, request=self.request)
        return JsonResponse({'form': render_form})

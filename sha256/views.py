import hashlib
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import FormView, View

from .models import Hash
from .forms import HashForm


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
        user = authenticate(self.request, **form.cleaned_data)
        if user:
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

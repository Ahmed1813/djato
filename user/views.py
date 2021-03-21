from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import UserLoginForm, UserRegistrationForm


# Create your views here.
class UserRegistraionView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'user/register.html'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        else:
            return super().dispatch(request, *args, **kwargs)
    

    def get_form(self):
        form = self.form_class(**self.get_form_kwargs())
        redirect_url = self.get_redirect_url()
        if redirect_url is not None:
            form.helper.form_action = reverse(
                'user:register') + '?next=' + str(redirect_url)
            return form
        return form

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, None)
        )
        return redirect_to

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('user:login')

    def get_success_message(self, cleaned_data):
        return f"User {cleaned_data.get('username')} has been created successfuly."


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def get_form(self):
        form = self.form_class(**self.get_form_kwargs())
        redirect_url = self.get_redirect_url()
        if redirect_url is not None:
            form.helper.form_action = reverse(
                'user:login') + '?next=' + str(redirect_url)
            return form
        return form

    def form_invalid(self, form):
        messages.error(self.request, "Invalid Credentials")
        return super().form_invalid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('todo:home')

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data.get('username')} successfully logged in."


# class UserLoginView(FormView):
#     form_class = AuthenticationForm
#     success_message = "%s has successfuly logged in."
#     template_name = 'user/login.html'


#     def get_success_url(self):
#         username = self.request.POST.get("username")
#         password = self.request.POST.get("password")
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(self.request, user)
#             to = self.request.GET.get('next')
#             if to:
#                 return to
#             return reverse("todo:home")
#         return reverse("user:login")


@login_required(login_url="user:login")
def logout_view(request):
    logout(request)
    messages.warning(request, "User successfully logged out")
    return redirect("todo:home")

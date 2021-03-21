from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = "user:register"
        self.helper.layout = Layout(
            PrependedText(
                'username', "<i class='fa fa-envelope-square'></i>", placeholder="Username"),
            PrependedText(
                'password1', "<i class='fa fa-key'></i>", placeholder="Password"),
            PrependedText(
                'password2', "<i class='fa fa-key'></i>", placeholder="Retype Password"),
            Submit("register", "Register", css_class="btn btn-primary btn-block p-2")
        )


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = "user:login"
        self.helper.layout = Layout(
            PrependedText(
                'username', "<i class='fa fa-envelope-square'></i>", placeholder="Username"),
            PrependedText(
                'password', "<i class='fa fa-key'></i>", placeholder="Password"),
            Submit("login", "Login", css_class="btn btn-primary btn-block p-2")
        )

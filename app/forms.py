from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Pet, Supervisor


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',  'password1', 'password2', 'email',
        ]
        field_classes = {'username': UsernameField}

        #widgets = {
            #'username' : forms.TextInput(attrs={'placeholder' : 'Username'}),
            #'password1' : forms.PasswordInput(attrs={'placeholder' : 'Password'}),
            #'password2' : forms.PasswordInput(attrs={'placeholder' : 'ConfirmPassword'}),
            #'email' : forms.EmailInput(attrs={'placeholder' : 'Email'})
        #}

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2', 'email']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ""
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder' : 'Username'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder' : 'Email'})

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        #user.username = self.cleaned_data['username']
        #user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = [
            'username',  'password'
        ]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ""
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})


class PetEditForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['name','animaltype', 'location','age','color','gender',
        'spayed','vaccinated','housetrained','specialcare','size','breed','photo','description']

    def __init__(self, *args, **kwargs):
        super(PetEditForm, self).__init__(*args, **kwargs)

        self.fields['description'].widget = forms.Textarea(attrs={'placeholder' : 'Write short description of pet'})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)


class SupervisorEditForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['city', 'country', 'telephone', 'photo', 'description']

    def __init__(self, *args, **kwargs):
        super(SupervisorEditForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder' : 'Write about yourself'})

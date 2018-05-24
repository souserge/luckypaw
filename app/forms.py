from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Pet, Supervisor, Photo


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',  'password1', 'password2', 'email',
        ]
        field_classes = {'username': UsernameField}

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


class PetForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['name','animaltype', 'location','age','color','gender',
        'spayed','vaccinated','housetrained','specialcare','adopted','size','breed','description']

    def __init__(self, *args, **kwargs):
        super(PetForm, self).__init__(*args, **kwargs)

        self.fields['description'].widget = forms.Textarea(attrs={'placeholder' : 'Write short description of pet'})
        self.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Write pet\'s name'})

class PetAddForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['name','animaltype', 'location' ]

    def __init__(self, *args, **kwargs):
        super(PetAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Write pet\'s name'})

class PetAddInfoForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = ['age','color','gender','spayed','vaccinated','housetrained','specialcare','size','breed','description']

    def __init__(self, *args, **kwargs):
        super(PetAddInfoForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder' : 'Write short description of pet'})



class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)


class SupervisorForm(forms.ModelForm):
    
    class Meta:
        model = Supervisor
        fields = ['city', 'country', 'telephone', 'photo', 'description']

    def __init__(self, *args, **kwargs):
        super(SupervisorForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'placeholder' : 'Write about yourself'})


class PhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['image', ]

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        
class ContactForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    from_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    #mobile_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Mob. Number'}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}), required=True)

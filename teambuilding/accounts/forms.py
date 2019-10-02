from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from .models import MyProject, Profile, Skill


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
        )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
        )

    class Meta:
        fields = ("email", "password1", "password2")
        model = get_user_model()

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'description',
            'profile_picture'
        ]


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            'skills'
        ]


class MyProjectForm(forms.ModelForm):
    class Meta:
        model = MyProject
        fields = [
            'title',
            'url'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project Name'}),
            'url': forms.URLInput(attrs={'placeholder': 'Project Url'})
        }

SkillInlineFormSet = inlineformset_factory(
    Profile, 
    Skill,
    extra=2,
    fields=('skills',),
    form=SkillForm,
    min_num=1,
    )

MyProjectInlineFormSet = inlineformset_factory(
    Profile,
    MyProject,
    extra=2,
    fields=('title', 'url'),
    form=MyProjectForm
)

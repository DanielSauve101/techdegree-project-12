from django import forms
from django.forms import inlineformset_factory

from .models import Project, Position


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'timeline',
            'applicant_requirements'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Project title',
                'class': 'circle--input--h1'
                }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Project Description',
                'rows': 5
            }),
            'timeline': forms.Textarea(attrs={
                'placeholder': 'Time Estimate',
                'class': 'circle--textarea--input',
                'rows': 5
            }),
            'applicant_requirements': forms.Textarea(attrs={
                'placeholder': 'Any additional requirements',
                'class': 'circle--textarea--input',
                'rows': 5
            })
        }
        

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = [
            'title',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Position Description', 
                'rows': 5
                })
        }
        

PositionInlineFormSet = inlineformset_factory(
    Project,
    Position,
    form=PositionForm,
    fields=('title', 'description'),
)
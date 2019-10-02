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
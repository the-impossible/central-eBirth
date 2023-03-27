# My django imports
from django import forms

# My app imports
from eBirth_reg.models import (
    BirthRegistration,
    Gender,
)

class BirthRegistrationForm(forms.ModelForm):

    child_name = forms.CharField(help_text='Enter Child name',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    father_name = forms.CharField(help_text='Enter Father name',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    mother_name = forms.CharField(help_text='Enter Mother name',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    weight = forms.CharField(help_text='Enter child birth weight',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    date_time = forms.CharField(help_text='Birth date and time',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'datetime-local',
        }
    ))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), empty_label="Select Child Gender", required=True, help_text="Select child's gender", widget=forms.Select(
        attrs={
            'class':'form-control select form-select',
        }
    ))

    class Meta:
        model = BirthRegistration
        fields = ('child_name', 'father_name', 'mother_name', 'date_time', 'weight', 'gender')

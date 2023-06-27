# My django imports
from django import forms

# My app imports
from eBirth_reg.models import (
    BirthRegistration,
    Gender,
    HospitalProfile,

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
            'type':'number',
            'step':'any',
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

class HospitalProfileForm(forms.ModelForm):

    hospital_name = forms.CharField(help_text='Enter Hospital Name',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    hospital_address = forms.CharField(help_text='Enter Hospital Address',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    pic = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
                'class':'form-control',
                'type':'file',
                'accept':'image/png, image/jpeg'
            }
        ))

    class Meta:
        model = HospitalProfile
        fields = ('hospital_name', 'hospital_address', 'pic')

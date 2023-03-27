from django import forms

from eBirth_auth.models import User

class UserRegistrationForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email',
        }
    ))

    password = forms.CharField(help_text='Enter Password',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'password',
        }
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != None:
            if User.objects.filter(email=email.lower().strip()).exists():
                raise forms.ValidationError('Email Already taken!')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError("Password is too short!")

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user


    class Meta:
        model = User
        fields = ('email', 'password',)

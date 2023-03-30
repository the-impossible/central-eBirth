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

    pic = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
                'class':'form-control',
                'type':'file',
                'accept':'image/png, image/jpeg'
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
        fields = ('email', 'password', 'pic')

class EditAdminForm(forms.ModelForm):

    email = forms.CharField(help_text='Enter email',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email',
        }
    ))

    pic = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
                'class':'form-control',
                'type':'file',
                'accept':'image/png, image/jpeg'
            }
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        check = User.objects.filter(email=email)
        if self.instance:
            check = check.exclude(pk=self.instance.pk)
        if check.exists():
            raise forms.ValidationError('Email Already taken!')

        return email

    class Meta:
        model = User
        fields = ('email', 'pic')

class ChangePassForm(forms.ModelForm):

    old_pass = forms.CharField(help_text='Enter Current Password',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'password',
            'name':'old_pass',
        }
    ))

    new_pass = forms.CharField(help_text='Enter New Password',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'password',
            'name':'new_pass',
        }
    ))

    confirm_pass = forms.CharField(help_text='Confirm New Password',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'password',
            'name':'confirm_pass',
        }
    ))

    password = forms.CharField(help_text='Password', required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'password',
            'name':'confirm_pass',
        }
    ))


    def clean_confirm_pass(self):
        new_pass = self.cleaned_data.get('new_pass')
        confirm_pass = self.cleaned_data.get('confirm_pass')
        if new_pass != confirm_pass:
            raise forms.ValidationError("new_pass and confirm password doesn't match!")

        if len(new_pass) < 6 :
            raise forms.ValidationError("Password should be at least 6 characters")

        return confirm_pass

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('new_pass'))

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('password',)

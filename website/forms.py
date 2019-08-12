from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['company_name'].widget.attrs.update({'placeholder': 'Company Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})

    class Meta:
        model = Company
        fields = '__all__'


class NewPasswordForm(forms.Form):
    password = forms.CharField(label= ("Password"),
                            widget=forms.PasswordInput)
    password_confirm = forms.CharField(label= ("Password Confirmation"),
                            widget=forms.PasswordInput)

    def clean(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

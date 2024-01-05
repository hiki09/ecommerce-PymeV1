from django import forms
from .models import Cuenta, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese contraseña',
        'class' : 'form-control',  
    }))
    #Me permite ocuparlo como cualquier elemento html para que django lo procese
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar contraseña',
        'class' : 'form-control',   
    }))

    class Meta:
        model = Cuenta
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingrese nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ingrese telefono'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese email'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Las contraseñas no coinciden!"
            )
        


class UserForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
            super(UserForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class']='form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages= {'invalid': ('Solo archivos de imagen')}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('direccion', 'comuna', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
                
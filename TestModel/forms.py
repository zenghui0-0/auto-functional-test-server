from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))


class RegisterForm(forms.Form):
    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    """
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="confirm password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    #sex = forms.ChoiceField(label='性别', choices=gender)
    #captcha = CaptchaField(label='验证码')



class DevicesForm(forms.Form):
    asset_status = (
        (0, 'Online'),
        (1, 'Offline'),
        (2, 'Unknow'),
        (3, 'Busy'),
        )
    host_name = forms.CharField(label="Host name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    DUT_IP    = forms.GenericIPAddressField(label="DUT IP", widget=forms.TextInput(attrs={'class': 'form-control'}))
    HDT_IP    = forms.GenericIPAddressField(label="HDT IP", widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag       = forms.CharField(label="Tag", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email     = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    status    = forms.ChoiceField(label='Status', choices=asset_status)

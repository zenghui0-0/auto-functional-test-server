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
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    #sex = forms.ChoiceField(label='性别', choices=gender)
    #captcha = CaptchaField(label='验证码')

class DevicesForm(forms.Form):
    asset_status = (
        (0, 'Online'),
        (1, 'Offline'),
        (2, 'Unknow'),
        (3, 'Busy'),
        )
    host_name = forms.CharField(label="主机名", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    DUT_IP    = forms.GenericIPAddressField(label="测试机IP", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    HDT_IP    = forms.GenericIPAddressField(label="wombat IP", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag       = forms.SlugField(label="Tag", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email     = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    status    = forms.ChoiceField(label="device state", choices=asset_status)
    """
    user_name = models.SlugField(max_length=100,null=True, blank=True)
    
    password  = models.SlugField(max_length=100, null=True, blank=True)
    tag       = models.SlugField(max_length=100, null=True, blank=True, help_text='For example: John_3dmark_11_12')
    email     = models.EmailField(max_length=100, null=True, blank=True, verbose_name='email_address', help_text='email address')
    status    = models.SmallIntegerField(choices=asset_status, default=0, verbose_name='device status')
    Owner     = models.SlugField(max_length=100, default="Admin")
    m_time = models.DateTimeField(auto_now=True, verbose_name='update time')
    """
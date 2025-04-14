from django import forms


# from .models import Profile

class UserCreationForm(forms.Form):
    username = forms.CharField(label='اسم المستخدم', max_length=30, help_text= 'اسم المستخدم لايجب أن يحتوي على مسافات')
    email = forms.EmailField(label='البريد الإلكتروني')
    first_name = forms.CharField(label='الأسم الأول')
    last_name = forms.CharField(label='الأسم الأخير')
    password1 = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput(), min_length= 8)
    password2 = forms.CharField(label='تأكيد كلمة المرور', widget=forms.PasswordInput(), min_length= 8)
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2'] or cd['password2'] != cd['password1']:
            raise forms.ValidationError('كلمة المرور غير متطابقه')
        return cd['password2']
    
#     def clean_username(self):
#         cd = self.cleaned_data
#         if User.objects.filter(username=cd['username']).exists():
#             raise forms.ValidationError('يوجد مستخدم بهذا الأسم')
#         return cd['username']
            
class LoginForm(forms.Form):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput())



class PostCreateForm(forms.Form):
    title = forms.CharField(label='العنوان')
    content = forms.CharField(label='نص التدوينة', widget=forms.Textarea())
   



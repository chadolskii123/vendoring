from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, user_logged_in
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accountapp.models import Company, Department

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """
    필수값 모두 포함
    비밀번호 확인 필요
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id', 'email',)

    def clean_password(self):
        # 비밀번호 / 비밀번호 확인이 일치하는지 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        # 장고에서 제공하는 비밀번호 암호화 저장을 함
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('user_id',)


class LoginForm(forms.Form):
    """
    로그인 양식, id와 비밀번호를 입력해야 함
    """
    user_id = forms.CharField(label='ID')
    password = forms.CharField(label="PASSWORD", widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        입력된 user_id가 존재하는지, 존재한다면 password는 일치하는지 확인
        """
        request = self.request
        data = self.cleaned_data
        user_id = data.get("user_id")
        password = data.get("password")
        qs = User.objects.filter(user_id=user_id)

        # 사용자에게 아이디 존재여부 비공개
        if qs.exists():
            # 사용자 인증
            user = authenticate(request, username=user_id, password=password)

            if user is None:
                messages.success(request, "아이디가 유효하지 않거나, 비밀번호가 잘못되었습니다.")
                raise forms.ValidationError("비밀번호 불일치.")
        else:
            messages.success(request, "아이디가 유효하지 않거나, 비밀번호가 잘못되었습니다.")
            raise forms.ValidationError("가입된 ID 없음.")

        login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, user=user, request=request)

        return data


class RegisterForm(forms.ModelForm):
    """
    필수값 모두 포함
    비밀번호 확인 필요
    """

    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id', 'email',)

        labels = {
            'user_id': '아이디',
            'email': '이메일',
            'password1': '비밀번호',
            'password2': '비밀번호 확인'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountUpdateForm(forms.ModelForm):
    company_cd = forms.ModelChoiceField(queryset=Company.objects.all(), required=False, label="회사명")
    dept_cd = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, label="부서명")

    class Meta:
        model = User
        fields = ('email', 'profile', 'company_cd', 'dept_cd')

        labels = {
            'profile': '프로필 사진',
            'email': '이메일',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True


class PasswordUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_id', 'email')
        labels = {
            'user_id': '아이디',
            'email': ' 이메일',
            'password1': '비밀번호',
            'password2': '비밀번호 확인'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].disabled = True
        self.fields['email'].disabled = True

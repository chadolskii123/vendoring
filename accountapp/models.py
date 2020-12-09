from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class Company(models.Model):
    company_cd = models.CharField(max_length=2, unique=True, null=False)
    company_nm = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.company_nm

# 부서
class Department(models.Model):
    company_cd = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True)
    dept_cd = models.CharField(max_length=2, unique=True, null=False, blank=False)
    dept_nm = models.CharField(max_length=50, null=False, blank=False)
    dept_grade = models.IntegerField()
    parent_dept_cd = models.CharField(max_length=2, unique=True, null=True, blank=True)

    def __str__(self):
        return self.dept_nm


# 직급
class Position(models.Model):
    position_cd = models.CharField(max_length=2, unique=True, null=False, blank=False)
    position_nm = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.position_nm


class UserManager(BaseUserManager):
    def create_user(self, user_id, password, email=None, is_active=True, is_staff=False, is_admin=False,
                    company_cd=None, dept_cd=None,
                    position_cd=None,
                    perm_grade=5):
        if not user_id:
            raise ValueError("ID를 입력하세요.")
        if not password:
            raise ValueError("Password를 입력하세요")

        user_obj = self.model(
            user_id=user_id
        )
        user_obj.set_password(password)  # change user password
        user_obj.email = email
        user_obj.company_cd = company_cd
        user_obj.dept_cd = dept_cd
        user_obj.position_cd = position_cd
        user_obj.is_active = is_active
        user_obj.perm_grade = perm_grade
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, user_id, email, full_name=None, password=None):
        user = self.create_user(
            user_id=user_id,
            email=email,
            password=password,
            is_staff=True,
            is_admin=False
        )
        return user

    def create_superuser(self, user_id, email, password=None):
        user = self.create_user(
            user_id=user_id,
            email=email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


# 사용자
class User(AbstractBaseUser):
    user_id = models.CharField(max_length=255, unique=True, verbose_name="ID")
    email = models.CharField(max_length=255, unique=True, verbose_name="이메일")
    profile = models.ImageField(upload_to='profile/', null=True)
    company_cd = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    dept_cd = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position_cd = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    # 권한 설정, 낮을 수록 접근권한 높음
    # 개발자 / 관리자 / 팀장 / 소팀장 / 팀원 5단계 구분 - 기본은 5단계로 시작, 별도 관리자이상급의 설정이 필요함
    perm_grade = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.user_id

    def perm_level(self):
        pg = self.perm_grade
        if pg == 1:
            return "모든 권한"
        elif pg == 2:
            return "관리자 권한"
        elif pg == 3:
            return "팀장 권한"
        elif pg == 4:
            return "소팀장 권한"
        else:
            return "기본 권한"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

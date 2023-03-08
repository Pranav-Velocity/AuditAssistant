from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None,mobile=None, first_name=None, last_name=None,is_super_admin=None, is_main_client=None ,is_partner=None,
                    is_manager=None, is_auditorclerk=None, is_articleholder=None,is_developer_admin=None):
        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_main_client=is_main_client,
            is_super_admin=is_super_admin,
            is_partner=is_partner,
            is_manager=is_manager,
            is_auditorclerk=is_auditorclerk,
            is_articleholder=is_articleholder,
            is_developer_admin=is_developer_admin
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, email=None, mobile=None, first_name=None, last_name=None,is_super_admin=True, is_main_client=False, is_partner=False,
                    is_manager=False, is_auditorclerk=False, is_articleholder=False,is_developer_admin=False):
        user = self.create_user(username=username,password=password,email=None,mobile=None, first_name=None, last_name=None, is_main_client=False,
         is_partner=False, is_manager=False,is_super_admin=True, is_auditorclerk=False, is_articleholder=False,is_developer_admin=False)
        user.is_admin = True
        user.is_super_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    mobile = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_super_admin = models.BooleanField(default=False, null=False, blank=False)
    is_main_client = models.BooleanField(default=False, null=False, blank=False)
    is_admin = models.BooleanField(default=False, null=False, blank=False)
    is_partner = models.BooleanField(default=False, null=False, blank=False)
    is_manager = models.BooleanField(default=False, null=False, blank=False)
    is_auditorclerk = models.BooleanField(default=False, null=False, blank=False)
    is_articleholder = models.BooleanField(default=False, null=False, blank=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    is_developer_admin =  models.BooleanField(default=False, null=False, blank=False)
    objects = UserManager()
    linked_employee = models.CharField(max_length=20,null=True,blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # @property
    # def is_admin(self):
    #     # Admin permissions
    #     return self.is_admin

    # @property
    # def is_partner(self):
    #     # CA permissions
    #     return self.is_partner

    # @property
    # def is_manager(self):
    #     # Manager permissions
    #     return self.is_manager

    # @property
    # def is_auditorclerk(self):
    #     # Manager permissions
    #     return self.is_auditorclerk

    # @property
    # def is_articleholder(self):
    #     # Manager permissions
    #     return self.is_articleholder

    # @property
    # def is_staff(self):
    #     return self.is_admin


# Create your models here.

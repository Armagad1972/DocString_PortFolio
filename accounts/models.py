from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models




class JadUserManager(BaseUserManager):
    def create_user(self, email, fname, lname, password=None,**kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            fname=fname,
            lname=lname,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            fname=fname,
            lname=lname,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class JadUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Adresse Mail",
        max_length=255,
        unique=True,
    )
    fname = models.CharField(verbose_name="Prénom", max_length=255)
    lname = models.CharField(verbose_name="Nom", max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Utilisateur"

    objects = JadUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fname', 'lname']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.is_admin  # Les administrateurs sont considérés comme du personnel

User = get_user_model()
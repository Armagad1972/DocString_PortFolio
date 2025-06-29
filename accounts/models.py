from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django_countries.fields import CountryField


class JadUserManager(BaseUserManager):
    def create_user(self, email, fname, lname, password=None, **kwargs):
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


class JadUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Adresse Mail",
        max_length=255,
        unique=True,
    )
    fname = models.CharField(verbose_name="Prénom", max_length=255)
    lname = models.CharField(verbose_name="Nom", max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        verbose_name="Statut staff",
        default=False,
        help_text="Détermine si l'utilisateur peut se connecter à l'interface d'administration."
    )
    is_assign = models.BooleanField(
        verbose_name="Magasins / Sociétés assignés",
        default=False,
    )

    class Meta:
        verbose_name = "Utilisateur"

    objects = JadUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fname', 'lname']

    User = settings.AUTH_USER_MODEL

    def __str__(self):
        return f"{self.fname} {self.lname}"

    def create_user(self, email, fname, lname, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            fname=fname,
            lname=lname,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.is_assign = False
        super.save(using=self, **kwargs)
        return user


class Societe(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    pays = CountryField(blank_label='(select country)')
    users = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name="utilisateurs", on_delete=models.CASCADE,
                              related_name="societes")

    class Meta:
        verbose_name = "Société"
        verbose_name_plural = "Sociétés"

    def __str__(self):
        return f"{self.nom} {self.ville}"


class Magasin(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    pays = CountryField(blank_label='(select country)')
    societe = models.ForeignKey(to=Societe, verbose_name="société", on_delete=models.CASCADE, related_name="magasins")
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="utilisateurs", related_name="magasins",
                                   blank=True)

    class Meta:
        verbose_name = "Magasin"
        verbose_name_plural = "Magasins"

    def __str__(self):
        return self.nom

    def get_societe(self):
        return self.societe

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Produit(models.Model):
    nom = models.CharField(max_length=255, help_text="Nom du produit")
    slug = models.SlugField(max_length=255, blank=True, null=True)
    ean = models.CharField(max_length=255, blank=True, null=True)
    societe = models.ForeignKey(to=Societe, verbose_name="société", on_delete=models.CASCADE, related_name="produits")
    CreationDate = models.DateTimeField(auto_now_add=True)
    UpdateDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Stock(models.Model):
    produit = models.ForeignKey(to=Produit, verbose_name="produit", on_delete=models.RESTRICT, related_name="stock")
    magasin = models.ForeignKey(to=Magasin, verbose_name="magasin", on_delete=models.RESTRICT, related_name="stock")
    quantite = models.IntegerField(
        verbose_name="quantité",
    )
    seuil = models.IntegerField(
        verbose_name="seuil",
    )
    alerte = models.BooleanField(
        verbose_name="alerte",
        default=False
    )
    date = models.DateTimeField(auto_now=True)
    obsolete = models.BooleanField(
        verbose_name="obsolete",
        default=False,
        help_text="Cette option permet de retirer un produit du stock."
    )

    def __str__(self):
        return f"{self.produit} - {self.magasin}-{self.quantite}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ['produit', 'magasin']

    def per_alerte(self):
        if self.obsolete:
            return 0
        else:
            return (self.quantite - self.seuil) / self.seuil * 100

    def save(self, *args, **kwargs):
        if self.quantite < self.seuil:
            self.alerte = True
        else:
            self.alerte = False
        if self.seuil == int(0):
            self.obsolete = True
        else:
            self.obsolete = False
        super().save(*args, **kwargs)


class Mouvements(models.Model):
    produit = models.ForeignKey(to=Produit, verbose_name="produit", on_delete=models.RESTRICT,
                                related_name="mouvements")
    magasin_in = models.ForeignKey(to=Magasin, verbose_name="magasin", on_delete=models.RESTRICT,
                                   related_name="mouvements", null=True, blank=True)
    magasin_out = models.ForeignKey(to=Magasin, verbose_name="magasin", on_delete=models.RESTRICT,
                                    related_name="mouvements_out", null=True, blank=True)
    quantite = models.IntegerField(
        verbose_name="quantité",
        validators=[MinValueValidator(0)]
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mouvement"
        verbose_name_plural = "Mouvements"

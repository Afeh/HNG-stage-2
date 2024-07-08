from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
import uuid

class UserManager(BaseUserManager):
	def create_user(self, email, password, first_name, last_name, phone=None):
		if not email:
			raise ValueError('User must have an email address')
		
		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
			phone=phone
		)

		user.set_password(password)
		user.save(using=self._db)

		org_name = f"{first_name}'s Organisation"
		organisation = Organisation.objects.create(name=org_name, owner=user)
		organisation.users.add(user)
		return user
	
	def create_superuser(self, userId, email, password, first_name, last_name, phone=None):
		user = self.create_user(email, userId, password, first_name, last_name, phone)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class CustomUser(AbstractBaseUser):
	userId = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(max_length=255, null=False)
	last_name = models.CharField(max_length=255, null=False)
	email = models.EmailField(unique=True, null=False)
	phone = models.CharField(max_length=20, blank=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	objects = UserManager()

	def __str__(self):
		return self.first_name
	
	def has_perm(self, perm, obj=None):
		return self.is_staff
	
	def has_module_perms(self, app_label):
		return self.is_staff


class Organisation(models.Model):
	orgId = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4)
	name = models.CharField(max_length=255, null=False)
	description = models.TextField()
	owner= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organisations')
	users = models.ManyToManyField(CustomUser)

	def __str__(self):
		return self.name
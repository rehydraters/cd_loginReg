from __future__ import unicode_literals

from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator_reg(self, postData):
        errors = {}
        if User.objects.filter(email = postData['email']):
            errors['email_present'] = "There is an account already with that email address."
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors['first_name'] = "First name must be no fewer than 2 characters long, and must be alphanumeric."
        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            errors['last_name'] = "Last name must be no fewer than 2 characters long, and must be alphanumeric."
        if EMAIL_REGEX.match(postData['email']) == None:
            errors['email_format'] = "Email address must be in valid email format."
        if len(postData['pword']) < 8:
            errors['pword_length'] = "Password must be at least 8 characters long."
        if postData['pword'] != postData['pwconf']:
            errors['pwconf'] = "Passwords must match."
        return errors

    def basic_validator_login(self, postData):
        errors = {}
        try:
            user = User.objects.get(email = postData['email'])
        except User.DoesNotExist:
            errors['email_mismatch'] = "Email not found."
        else:
            if not bcrypt.checkpw(postData['pword'].encode('utf8'), user[0].password.encode('utf8')):
                errors['pword'] = "Password invalid."
        finally:
            return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at= models.DateTimeField(auto_now = True)

    objects = UserManager()

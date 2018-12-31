from django.db import models
from django.contrib import messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager): 
  def validate(self, request): #self is refering to the manager
     # request.POST is a dictionary
    if request.method =="POST": #making sure that POST is being used
      #basic check to ensure something is entered into field
      valid = True
      for key in request.POST:
        if request.POST[key] == '': #if the form field is blank
          valid = False
          messages.error(request, '{} field must not be blank '.format(key)) #.error() is build into messages automatically
      if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, "Email must be valid")
      if len(request.POST["password"]) < 8:
        valid = False
        messages.error(request, "Password must be at least 8 characters long")
      # checking to ensure password matches
      if request.POST["confirm password"] != request.POST["password"]:
        valid = False
        messages.error(request, "Password must match confirmation")
      if valid == True:
        #create and send to database
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create( #can also be written as self.objects.create( .... 
          first_name=request.POST["first_name"], 
          last_name=request.POST["last_name"],
          email=request.POST["email"], 
          password=pw_hash
          )
        print(User.objects.all())
        messages.success(request, "Created User, please log in.")

class JobManager(models.Manager):
  def validator(self, user_data):
      errors = {}
      if len(user_data["title"]) < 3:
          errors["title"] = "Title must be longer than 3 characters"
      if len(user_data["description"]) < 10:
          errors["description"] = "Description must be longer than 10 characters"
      if len(user_data["location"]) < 1:
          errors["location"] = "Location must not be blank"

      return errors 
  def create_job(self, user_data):
    # print(user_data["id"])
    user=User.objects.get(id=user_data["id"])
    # print(user)
    return self.create( 
      title=user_data["title"], 
      description=user_data["description"],
      location=user_data["location"],
      user=user
      )
    # print(Job.objects.all())
    # messages.success(request, "Created Job")
  def delete_job(self, user_data):
    job = Job.objects.get(id=user_data)
    job.delete()  

class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  objects = UserManager()

class Job(models.Model): 
  title = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  description = models.TextField()
  user = models.ForeignKey(User, related_name="has_jobs") 
  created_at = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  objects = JobManager()

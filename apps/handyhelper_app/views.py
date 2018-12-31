from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Job
import bcrypt

# Create your views here.
def index(request):

 #if user is already logged in
  if "id" in request.session:
    return render(request, "handyhelper_app/index.html")
  # print(Job.objects.all())
  return render(request, "handyhelper_app/index.html")

#User Registration
def register(request):
  User.objects.validate(request)
  return redirect('/')

#User Login
def login(request):
  users = User.objects.filter(email=request.POST["email"]) #retrieve record in database to see if that email exists. #if i use .get, ill need to use try/except (errors with duplicates/or null data)
  if len(users) > 0 : #if i found a user
    user = users[0]
   #checking to make sure they have the right password
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
      request.session['id'] = user.id
      # return HttpResponse("logged in!!")   #test page to prove it is working
      return redirect("/dashboard")
  messages.error(request, 'Invalid Email and Password Combination')#if either of the above if's fail
  return redirect('/')

#User Logout
def logout(request):
  request.session.clear()
  return redirect("/")

#Route that loads the dashboard
def dashboard(request):
  if 'id' not in request.session:	
	  return redirect('/')
  context = {
  "user":User.objects.get(id=request.session["id"]), #This is the current user, used for the "Welcome, USER" portion of the page. used as user.name in the dashboard.
  "jobs" : Job.objects.all(), 
  "user_jobs": Job.objects.filter(user=request.session["id"])#gets the jobs assigned to the user in session
  }
  return render(request, "handyhelper_app/dashboard.html", context)

#Route adding a new job
def add(request):
  if 'id' not in request.session:	
	  return redirect('/')
  context = {
  "user":User.objects.get(id=request.session["id"]), #This is the current user
  "jobs" : Job.objects.all()
  }
  return render(request, "handyhelper_app/add.html", context)

#Creates the job
def create(request):
  if 'id' not in request.session:	
	  return redirect('/')
  if request.method != "POST": #redirect out of application if method used is not post
    return redirect('/')
  # valiadate data for errors
  errors = Job.objects.validator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect("/addjob")
  #Creates job  
  Job.objects.create_job(request.POST)
  return redirect("/dashboard")

#Shows the job
def show(request, job_id):
  if 'id' not in request.session:	
	  return redirect('/')
  context = {
    "job": Job.objects.get(id=job_id)
  }
  return render(request, "handyhelper_app/showjob.html", context)

#Route for loading the edit job page
def edit(request, job_id):
  if 'id' not in request.session:	
	  return redirect('/')
  context = {
    "job" : Job.objects.get(id=job_id)
  }
  return render(request, "handyhelper_app/editjob.html", context)

#Edits the job
def editjob(request, job_id):
  if 'id' not in request.session:	
	  return redirect('/')
  if request.method != "POST": #redirect out of application if method used is not post
    return redirect('/')
  # print(request.POST)
  job = Job.objects.get(id=job_id)
  #Run Validations
  errors = Job.objects.validator(request.POST)
  if len(errors):
    for key, value in errors.items():
      messages.error(request, value)
    return redirect("/edit/"+job_id)
  else: #there is a better way to do this, however, I cannot figure that out at this time.
    job.title=request.POST["title"]
    job.description=request.POST["description"]
    job.location=request.POST["location"]
    job.save()
    return redirect("/dashboard")

#Delete a Job
def delete(request, job_id):
  if 'id' not in request.session:	
	  return redirect('/')
  Job.objects.delete_job(job_id)
  return redirect("/dashboard")

#Users function to reassign the job to their jobs
def addtomyjobs(request, job_id):
  if 'id' not in request.session:	
	  return redirect('/')
  job = Job.objects.get(id=job_id) #get current job id
  currentUserID = request.session['id']#This is the current user
  # print("The current user is", currentUserID)
  # print("Title is",  job.title, "| Job ID is", job.id, " | Job User ID is", job.user_id)
  job.user_id = currentUserID
  # print("The updated job userid is", job.user_id)
  job.save()
  # print("Now, Title is",  job.title, "| Job ID is", job.id, " | Job User ID is", job.user_id)
  return redirect("/dashboard")
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
from quiz.models import UserRank, Quiz, QuizSubmission, Question
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from .models import Message,Blog,Resource
from django.db.models import Count, Q
import math
from django.db.models.functions import ExtractYear
from .forms import BlogForm

# Create your views here.
def home(request):
  leaderboard_users = UserRank.objects.order_by('rank')[:4]
  if request.user.is_authenticated:
    #request user
    user_object= User.objects.get(username= request.user)
    user_profile = Profile.objects.get_or_create(user=user_object)
    context={"user_profile":user_profile,"leaderboard_users":leaderboard_users}
  else: 
    context ={"leaderboard_users":leaderboard_users}
  return render(request,'welcome.html', context)

@login_required(login_url="login")
def leaderboard_view(request):
  user_object= User.objects.get(username= request.user)
  user_profile = Profile.objects.get(user=user_object)
  leaderboard_users = UserRank.objects.order_by('rank')
  context={"leaderboard_users":leaderboard_users,"user_profile":user_profile}
  return render(request,'leaderboard.html',context)

def is_superuser(user):
  return user.is_superuser

@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashboard_view(request):
  user_object = User.objects.get(username=request.user)
  user_profile = Profile.objects.get(user=user_object)
  #total number
  total_users =User.objects.all().count()
  total_quizzes = Quiz.objects.all().count()
  total_quiz_submit = QuizSubmission.objects.all().count()
  total_questions = Question.objects.all().count()

  #today  numbers
  today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
  today_quizzes_objs = Quiz.objects.filter(created_at__date= datetime.date.today())
  today_quizzes =  Quiz.objects.filter(created_at__date= datetime.date.today()).count()
 
  today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
  today_questions = 0

  for quiz in today_quizzes_objs:
    today_questions += quiz.question_set.count()

  #gain % 
  gain_users = gain_percentage(total_users, today_users)
  gain_quizzes = gain_percentage(total_quizzes, today_quizzes)
  gain_quiz_submit = gain_percentage(total_quiz_submit, today_quiz_submit)
  gain_questions = gain_percentage(total_questions, today_questions)

  #inbox Message
  messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')
  context={'user_profile':user_profile,'total_users':total_users,'total_quizzes':total_quizzes,
  'total_quiz_submit':total_quiz_submit,'total_questions':total_questions,
  'today_users':today_users,'today_quizzes':today_quizzes,'today_quiz_submit':today_quiz_submit,
  'today_questions':today_questions,
  "gain_users": gain_users,"gain_quizzes": gain_quizzes,
  "gain_quiz_submit": gain_quiz_submit,
    "gain_questions": gain_questions,
    'messages':messages,
  }
  return render(request,'dashboard.html',context)

def gain_percentage(total,today):
  if total > 0 and today > 0:
    gain =math.floor((today*100)/total)
    return gain




def message_view(request,id):
  message = get_object_or_404(Message, pk=id)
  if not message.is_read:
      message.is_read = True
      message.save()

  context = {"message": message}
  return render(request, "message.html", context)
  
  
def about_view(request):
  if request.user.is_authenticated:
    #request user
    user_object= User.objects.get(username= request.user)
    user_profile = Profile.objects.get_or_create(user=user_object)
    context={"user_profile":user_profile}
  else: 
    context ={}
  
  return render(request,'about.html',context)



def blogs_view(request):

    year_blog_count = Blog.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).order_by('-year').filter(status='public')

    blogs = Blog.objects.filter(status='public').order_by('-created_at')

    context = {"year_blog_count": year_blog_count, "blogs": blogs}
    return render(request, "blogs.html", context)

@login_required(login_url='login')
def blog_view(request, blog_id):

    blog = get_object_or_404(Blog, pk=blog_id)
    
    context = {"blog": blog}
    return render(request, "blog.html", context)

  
  
def terms_conditions_view(request):
  if request.user.is_authenticated:
    user_object= User.objects.get(username= request.user)
    user_profile = Profile.objects.get_or_create(user=user_object)
    context={"user_profile":user_profile}
  else:
    context={}

  return render(request,'terms-conditions.html',context)


@login_required(login_url='login')   
def downloads_view(request):
  if request.user.is_authenticated:
    user_object= User.objects.get(username= request.user)
    user_profile = Profile.objects.get_or_create(user=user_object)
    context={"user_profile":user_profile}
  else:
    context={}

  
  return render(request,'downloads.html',context)


def search_users_view(request):
  context={}
  return render(request,'search-users.html',context)
@login_required(login_url='login')
def contact_view(request):

    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject is not None and message is not None:
            form = Message.objects.create(user=request.user, subject=subject, message=message)
            form.save()
            messages.success(request, "We got your message. We will resolve your query soon.")
            return redirect('profile', request.user.username)
        
        else:
            return redirect('contact')

    return render(request, "contact.html")

def search_users_view(request):
    query = request.GET.get('q')

    if query:
        users = User.objects.filter(
            (Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)) & 
            Q(is_superuser=False)  # Exclude superuser accounts
        ).order_by('date_joined')
    else:
        users = []

    context = {"query": query, "users": users}
    return render(request, "search-users.html", context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def resources_view(request):
    resources = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resources})


def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.status = 'public'
            blog.save()
            return redirect('blogs')
    else:
        form = BlogForm()
    return render(request, 'add_blog.html', {'form': form})

def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        blog.delete()
        return redirect('blogs')
    return render(request, 'confirm_delete.html', {'blog': blog})
    
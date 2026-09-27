from django.shortcuts import render, redirect
from .models import Course, Application
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):
    courses = Course.objects.all()
    return render(
        request,
        'courses/index.html',
        {
            'courses': courses
        }
    )

def apply_course(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return render(
            request,
            'courses/error.html',
            {
                'message': 'Course Not Found'
            }
        )

    if request.method == 'POST':

        phone = request.POST.get('phone')
        age = request.POST.get('age')
        address = request.POST.get('address')
        qualification = request.POST.get('qualification')

        Application.objects.create(
            user=request.user,
            course=course,
            phone=phone,
            age=age,
            address=address,
            qualification=qualification
        )

        return redirect('success')

    return render(
        request,
        'courses/apply.html',
        {
            'course': course
        }
    )

def register_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not username or not password:
            return render(
                request,
                'courses/signin.html',
                {
                    'error': 'Username and Password are required'
                }
            )


        if User.objects.filter(username=username).exists():
            return render(
                request,
                'courses/signin.html',
                {
                    'error': 'Username Already Exists'
                }
            )


        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return redirect('login')
    
    return render(
        request,
        'courses/signin.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:
            login(request, user)
            return redirect('home')
        
        return render(
            request,
            'courses/login.html',
            {
                'error': 'Invalid Username or Password'
            }
        )
    return render(
        request,
        'courses/login.html'
    )


def logout_user(request):
    logout(request)
    return redirect('login')


def success_page(request):

    return render(
        request,
        'courses/success.html'
    )
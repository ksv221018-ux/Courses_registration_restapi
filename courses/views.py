from django.shortcuts import render
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({
        "message": "CSRF cookie set"
    })


@api_view(['GET'])
def get_course(request):
    courses=Course.objects.all()
    serializer=CourseSerializer(
        courses,
        many=True
    )
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def apply_course(request, id):

    if not request.user.is_authenticated:
        return Response(
            {
                "error": "Please Login First"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        course = Course.objects.get(id=id)

    except Course.DoesNotExist:
        return Response(
            {
                "error": "Course Not Found"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ApplicationSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save(
            user=request.user,
            course=course
        )

        return Response(
            {
                "Message": "Application Submitted Successfully"
            },
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['POST'])
def register_user(request):

    username=request.data.get('username')
    email=request.data.get('email')
    password=request.data.get('password')

    if not username or not password:
        return Response(
            {
                "error":"The Username and Password Fields are Required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {
                "error":"Username Already Exists"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    user=User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    return Response(
        {
            "Message":"User Register Successfully.."
        },
        status=status.HTTP_201_CREATED
    )

@csrf_exempt
@api_view(['POST'])
def user_login(request):

    username=request.data.get('username')
    password=request.data.get('password')

    user=authenticate(
        username=username,
        password=password
    )

    if user is not None:
        login(request,user)
        return Response(
            {
                "Message":"Login Successfully.."
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "error":"Invalid Username or Password"
        },
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
def logout_user(request):
    logout(request)

    return Response(
        {
            'message': 'Logout successful'
        }
    )

def success_page(request):
    return render(request, 'courses/success.html')
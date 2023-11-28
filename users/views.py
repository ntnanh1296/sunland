# users/views.py
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework_simplejwt.tokens import RefreshToken
import json

from .models import User

@csrf_exempt
@require_POST
def register_user(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    username = data['username']
    password = data['password']

    user = User.objects.create_user(email=email, username=username, password=password)

    response_data = {'user_id': user.id, 'username': user.username, 'email': user.email}
    return JsonResponse(response_data)

@csrf_exempt
@require_POST
def login_user(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'access_token': access_token,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


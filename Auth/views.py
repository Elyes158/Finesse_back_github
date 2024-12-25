from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json
from .models import AuthToken, UserProfile
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken


@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            phone_number = data.get('phone_number')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            user = User.objects.create_user(username=username, password=password, email=email)
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                last_name = last_name,
                first_name = first_name
            )
            return JsonResponse({'message': 'Utilisateur créé avec succès', 'user_id': user.id}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse({'message': 'Méthode non autorisée'}, status=405)
@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                token_instance, created = AuthToken.objects.get_or_create(user=user)
                token_instance.token = access_token
                token_instance.save()
                return JsonResponse({
                    'message': 'Connexion réussie',
                    'user_id': user.id,
                    'access_token': access_token,
                    'refresh_token': str(refresh)
                }, status=200)
            else:
                return JsonResponse({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse({'message': 'Méthode non autorisée'}, status=405)

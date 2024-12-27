from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json
from .models import AuthToken, UserProfile
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail



@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            # Récupération des données envoyées par le client
            data = json.loads(request.body)
            username = data.get('username',None)
            password = data.get('password')
            email = data.get('email')
            phone_number = data.get('phone_number')
            full_name = data.get('full_name')

            user = User.objects.create_user(username=username, password=password, email=email)
            
            user_profile = UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                full_name=full_name
            )
            user_profile.generate_verification_code()
            user_profile.send_verification_email()
            return JsonResponse({
                'id': user.id
            }, status=201)

        except Exception as e:
            # En cas d'erreur, retourne un message d'erreur
            return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse({'message': 'Méthode non autorisée'}, status=405)


# Vue pour la vérification du code de vérification
@csrf_exempt
def verify_code(request):
    if request.method == "POST":
        try:
            # Récupération des données envoyées par le client
            data = json.loads(request.body)
            user_id = data.get('user_id')
            verification_code = data.get('verification_code')

            # Recherche de l'utilisateur
            user = User.objects.get(id=user_id)
            profile = user.profile

            # Vérification du code
            if profile.verification_code == verification_code:
                profile.is_email_verified = True
                profile.save()

                # Réponse avec un message de succès
                return JsonResponse({'message': 'Votre email a été vérifié avec succès.'}, status=200)
            else:
                return JsonResponse({'message': 'Code de vérification incorrect'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Utilisateur non trouvé'}, status=404)
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

@csrf_exempt
def register_profile(request, userId):
    if request.method == "POST":
        try:
            # Utilisez request.POST pour récupérer les champs de texte
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            description = request.POST.get('description')

            # Utilisez request.FILES pour récupérer le fichier image
            avatar = request.FILES.get('avatar')
            
            # Récupérer l'utilisateur et son profil
            user = User.objects.get(id=userId)
            profile = user.profile
            profile.full_name = full_name
            profile.phone_number = phone_number
            profile.address = address
            profile.description = description
            
            # Si l'image est présente, on l'ajoute au profil
            if avatar:
                profile.avatar = avatar
            
            profile.save()

            return JsonResponse({'message': 'Profile updated successfully.'}, status=200)

        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e)}, status=400)
# @csrf_exempt
# def create_username(request , )

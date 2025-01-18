import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import json

import requests
from .models import AdminUser, AuthToken, PasswordResetToken, UserGoogle, UserProfile
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from allauth.socialaccount.models import SocialAccount, SocialToken
import traceback
import uuid
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

@csrf_exempt
def login_view_admin(request):
    print("marahab")
    if request.method == 'POST':
        print("marahab")
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        print(identifier,password)
        try:
            user = AdminUser.objects.get(identifier=identifier)

            # Vérification du mot de passe
            if (password ==user.password):
                # Si authentification réussie, retourner une réponse JSON
                return JsonResponse({'message': 'Connexion réussie', 'status': 'success'}, status=200)
            else:
                # Si mot de passe incorrect
                return JsonResponse({'message': 'Mot de passe incorrect', 'status': 'error'}, status=400)
        except AdminUser.DoesNotExist:
            # Si l'identifiant n'existe pas
            return JsonResponse({'message': 'Identifiant non trouvé', 'status': 'error'}, status=404)

    # Si ce n'est pas une requête POST, retourner une erreur
    return JsonResponse({'message': 'Méthode non autorisée', 'status': 'error'}, status=405)



@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            # Récupération des données envoyées par le client
            data = json.loads(request.body)
            username = data.get('username', None)
            password = data.get('password')
            email = data.get('email')
            phone_number = data.get('phone_number')
            full_name = data.get('full_name')

            # Vérification si l'e-mail existe déjà
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'message': 'An account with this email already exists. Please log in.'
                }, status=400)

            # Vérification si le nom d'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'message': 'This username is already taken. Please choose another one.'
                }, status=400)

            # Création de l'utilisateur et du profil utilisateur
            user = User.objects.create_user(username=username, password=password, email=email)
            user_profile = UserProfile.objects.create(
                user=user,
                phone_number=phone_number,
                full_name=full_name
            )
            user_profile.generate_verification_code()
            user_profile.send_verification_email()

            return JsonResponse({
                'id': user.id,
                'message': 'User successfully created. Please verify your email.'
            }, status=201)

        except Exception as e:
            # En cas d'erreur, retourne un message d'erreur
            return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse({'message': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def send_email_to_reset_password(request,email) :
    if request.method == "POST": 
        try:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'message': 'User with this email does not exist.'}, status=400)
            
            profile = user.profile
            profile.generate_verification_code()
            profile.send_verification_email()
            
            return JsonResponse({
                'message': 'Mail sent successfully',
                  # Expiration time in ISO format
            }, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
        
@csrf_exempt
def change_password(request, reset_token):
    if request.method == "POST":
        try:
            try:
                valid_token = PasswordResetToken.objects.get(token=reset_token)
            except PasswordResetToken.DoesNotExist:
                return JsonResponse({'message': 'Invalid token.'}, status=400)

            if valid_token.is_expired():
                return JsonResponse({'message': 'Token has expired.'}, status=400)

            user = valid_token.user

            # Charger le mot de passe depuis le corps JSON
            try:
                data = json.loads(request.body)
                new_password = data.get('new_password')
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON format.'}, status=400)

            if not new_password:
                return JsonResponse({'message': 'New password is required.'}, status=400)

            user.password = make_password(new_password)  # Hash the new password
            user.save()

            valid_token.delete()

            return JsonResponse({'message': 'Password updated successfully.'}, status=200)

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


@csrf_exempt
def verify_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            verification_code = data.get('verification_code')

            user = User.objects.get(id=user_id)
            profile = user.profile
            if profile.verification_code == verification_code:
                profile.is_email_verified = True
                profile.save()
                return JsonResponse({'message': 'Votre email a été vérifié avec succès.'}, status=200)
            else:
                return JsonResponse({'message': 'Code de vérification incorrect'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Utilisateur non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse({'message': 'Méthode non autorisée'}, status=405)

@csrf_exempt
def verify_code_for_reset(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            verification_code = data.get('verification_code')

            user = User.objects.get(email=email)
            profile = user.profile
            if profile.verification_code == verification_code:
                profile.is_email_verified = True
                profile.save()
                reset_token = str(uuid.uuid4())
                token_obj = PasswordResetToken.objects.create(
                user=user,
                token=reset_token,
                created_at=timezone.now(),
                expires_at=timezone.now() + timezone.timedelta(hours=1)  # Token expires in 1 hour
            )
                return JsonResponse({'message': 'Votre email a été vérifié avec succès.',"token":reset_token}, status=200)
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
            userr = User.objects.get(username = username)
            mail_verfied = userr.profile.is_email_verified
            if user is not None and mail_verfied:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                token_instance, created = AuthToken.objects.get_or_create(user=user)
                token_instance.token = access_token
                token_instance.save()
                user_profile = user.profile
                return JsonResponse({
                    'message': 'Connexion réussie',
                    'user_id': user.id,
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_profile': {
                        'hasStory':user.profile.hasStory,
                        'email':user.email,
                        'username':user.username,
                        'avatar': user_profile.avatar.url if user_profile.avatar else None,
                        'phone_number': user_profile.phone_number,
                        'full_name': user_profile.full_name,
                        'address': user_profile.address,
                        'is_email_verified': user_profile.is_email_verified,
                        'verification_code': user_profile.verification_code,
                        'description': user_profile.description,
                    }
                },status=200)
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
            avatar = request.FILES.get('avatar')
            
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
        

@csrf_exempt
def register_profile_google(request, userId):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            full_name = data.get('full_name')
            phone_number = data.get('phone_number')
            address = data.get('address')
            description = data.get('description')

            if not full_name or not phone_number or not address or not description:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            user = User.objects.get(id=userId)

            profile = user.googleProfile
            profile.full_name = full_name
            profile.phone_number = phone_number
            profile.address = address
            profile.description = description

            profile.save()

            return JsonResponse({'message': 'Profile updated successfully.'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'message': f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
@csrf_exempt
def create_username(request, userId):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            isPolicy = data.get('policy')
            isMail = data.get('mail')
            
            # Vérification que policy est True
            if not isPolicy:
                return JsonResponse({'message': 'You must accept the privacy policy.'}, status=400)
            
            user = User.objects.get(id=userId)
            profile = user.profile
            
            # Mise à jour des données
            profile.isPrivacyChecked = isPolicy
            profile.isSendMailChacked = isMail
            user.username = username
            user.save()
            profile.save()
            
            return JsonResponse({'message': 'Profile updated successfully.'}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e)}, status=400)
        

@csrf_exempt
def create_username_google(request, userId):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            isPolicy = data.get('policy')
            isMail = data.get('mail')
            
            # Vérification que policy est True
            if not isPolicy:
                return JsonResponse({'message': 'You must accept the privacy policy.'}, status=400)
            
            user = User.objects.get(id=userId)
            profile = user.googleProfile
            
            # Mise à jour des données
            profile.isPrivacyChecked = isPolicy
            profile.isSendMailChacked = isMail
            user.username = username
            user.save()
            profile.save()
            
            return JsonResponse({'message': 'Profile updated successfully.'}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e)}, status=400)

@csrf_exempt
def google_register(request):
    print("i'm used")
    if request.method == "POST":
        try:
            # Vérifier le type de contenu
            if request.content_type == "application/x-www-form-urlencoded":
                data = request.POST  # Utiliser QueryDict pour extraire les données
            elif request.content_type == "application/json":
                data = json.loads(request.body)  # Traiter les requêtes JSON
            else:
                return JsonResponse({"message": "Unsupported content type"}, status=400)

            print(f"Parsed data: {data}")

            id_token = data.get('id_token')
            if id_token:
                # Vérifier le jeton via l'API de Google
                url = f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}'
                response = requests.get(url)
                print(f"Google response: {response.status_code}, {response.text}")
                user_info = response.json()

                if response.status_code == 200:
                    user_email = user_info.get('email')
                    user_first_name = user_info.get('given_name')
                    user_last_name = user_info.get('family_name')
                    user_full_name = f"{user_first_name} {user_last_name}"  # Concaténation
                    user_avatar = user_info.get('picture')  # URL directe de l'avatar

                    # Vérifier si un utilisateur avec cet e-mail existe déjà
                    if User.objects.filter(email=user_email).exists():
                        return JsonResponse({
                            "message": "Email already exists. Login instead.",
                            "user": {
                                "email": user_email
                            }
                        }, status=400)

                    # Créer ou mettre à jour l'utilisateur dans le modèle User
                    user, created = User.objects.get_or_create(
                        username=user_email,
                        defaults={'email': user_email}
                    )

                    # Créer ou mettre à jour l'utilisateur dans le modèle UserGoogle
                    user_google, google_created = UserGoogle.objects.update_or_create(
                        user=user,
                        defaults={
                            'full_name': user_full_name,  # Stocker le nom complet
                            'avatar': user_avatar
                        }
                    )

                    message = "User created" if created or google_created else "User updated"

                    return JsonResponse({
                        "message": f"Login successful: {message}",
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "username": user.username,
                            "first_name": user_first_name,  # Envoyer séparément
                            "last_name": user_last_name,    # Envoyer séparément
                            "full_name": user_google.full_name,  # Si besoin
                            "avatar": user_google.avatar  # URL directement serialisée
                        }
                    })
                else:
                    return JsonResponse({"message": "Invalid token"}, status=400)
            else:
                return JsonResponse({"message": "No token provided"}, status=400)
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error during token verification: {error_details}")
            return JsonResponse({"message": "Error verifying token", "error": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Invalid method"}, status=405)




@csrf_exempt
def google_login(request):
    print("I'm used")
    if request.method == "POST":
        try:
            if request.content_type == "application/x-www-form-urlencoded":
                data = request.POST 
            elif request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                return JsonResponse({"message": "Unsupported content type"}, status=400)
            print(f"Parsed data: {data}")

            id_token = data.get('id_token')
            if id_token:
                # Vérifier le jeton via l'API de Google
                url = f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}'
                response = requests.get(url)
                print(f"Google response: {response.status_code}, {response.text}")
                user_info = response.json()

                if response.status_code == 200:
                    user_email = user_info.get('email')

                    # Vérifier si l'email existe déjà dans la base de données
                    try:
                        user = User.objects.get(email=user_email)
                    except User.DoesNotExist:
                        # Retourner une erreur si l'utilisateur n'existe pas
                        return JsonResponse({"message": "Email does not exist in the database"}, status=400)

                    user_first_name = user_info.get('given_name')
                    user_last_name = user_info.get('family_name')
                    user_full_name = f"{user_first_name} {user_last_name}"  # Concaténation
                    user_avatar = user_info.get('picture')  # URL directe de l'avatar

                    # Créer ou mettre à jour l'utilisateur dans le modèle UserGoogle
                    user_google, google_created = UserGoogle.objects.update_or_create(
                        user=user,
                        defaults={
                            'full_name': user_full_name,  # Stocker le nom complet
                            'avatar': user_avatar
                        }
                    )
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    token_instance, created = AuthToken.objects.get_or_create(user=user)
                    token_instance.token = access_token
                    token_instance.save()
                    message = "User updated" if google_created else "User already updated"
                    return JsonResponse({
                    'message': 'Connexion réussie',
                    'user_id': user.id,
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_profile': {
                        'email':user.email,
                        'username':user.username,
                        'avatar': user_google.avatar if user_google.avatar else None,
                        'phone_number': user_google.phone_number,
                        'full_name': user_google.full_name,
                        'address': user_google.address,
                        'description': user_google.description,
                        'hasStory':user_google.hasStory,
                       
                    }
                }, status=200)
                else:
                    return JsonResponse({"message": "Invalid token"}, status=400)
            else:
                return JsonResponse({"message": "No token provided"}, status=400)
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error during token verification: {error_details}")
            return JsonResponse({"message": "Error verifying token", "error": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Invalid method"}, status=405)
################################################################################
import json
import requests
import traceback
from django.http import JsonResponse
from .models import User, UserFacebook  # Assurez-vous d'avoir un modèle UserFacebook pour lier les informations Facebook

@csrf_exempt
def facebook_register(request):
    print("i'm used for Facebook")
    if request.method == "POST":
        try:
            # Vérifier le type de contenu
            if request.content_type == "application/x-www-form-urlencoded":
                data = request.POST  # Utiliser QueryDict pour extraire les données
            elif request.content_type == "application/json":
                data = json.loads(request.body)  # Traiter les requêtes JSON
            else:
                return JsonResponse({"message": "Unsupported content type"}, status=400)

            print(f"Parsed data: {data}")

            access_token = data.get('access_token')
            if access_token:
                # Vérifier le jeton via l'API de Facebook
                url = f'https://graph.facebook.com/v11.0/me?fields=email,first_name,last_name,picture&access_token={access_token}'
                response = requests.get(url)
                print(f"Facebook response: {response.status_code}, {response.text}")
                user_info = response.json()

                if response.status_code == 200:
                    user_email = user_info.get('email')
                    user_first_name = user_info.get('first_name')
                    user_last_name = user_info.get('last_name')
                    user_full_name = f"{user_first_name} {user_last_name}"  # Concaténation
                    user_avatar = user_info.get('picture', {}).get('data', {}).get('url')  # URL de l'avatar

                    # Vérifier si un utilisateur avec cet e-mail existe déjà
                    if User.objects.filter(email=user_email).exists():
                        return JsonResponse({
                            "message": "Email already exists. Login instead.",
                            "user": {
                                "email": user_email
                            }
                        }, status=400)

                    # Créer ou mettre à jour l'utilisateur dans le modèle User
                    user, created = User.objects.get_or_create(
                        username=user_email,
                        defaults={'email': user_email}
                    )

                    # Créer ou mettre à jour l'utilisateur dans le modèle UserFacebook
                    user_facebook, facebook_created = UserFacebook.objects.update_or_create(
                        user=user,
                        defaults={
                            'full_name': user_full_name,  # Stocker le nom complet
                            'avatar': user_avatar
                        }
                    )

                    message = "User created" if created or facebook_created else "User updated"

                    return JsonResponse({
                        "message": f"Login successful: {message}",
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "username": user.username,
                            "first_name": user_first_name,  # Envoyer séparément
                            "last_name": user_last_name,    # Envoyer séparément
                            "full_name": user_facebook.full_name,  # Si besoin
                            "avatar": user_facebook.avatar  # URL directement serialisée
                        }
                    })
                else:
                    return JsonResponse({"message": "Invalid token"}, status=400)
            else:
                return JsonResponse({"message": "No token provided"}, status=400)
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error during token verification: {error_details}")
            return JsonResponse({"message": "Error verifying token", "error": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Invalid method"}, status=405)

@csrf_exempt
def register_profile_facebook(request, userId):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            full_name = data.get('full_name')
            phone_number = data.get('phone_number')
            address = data.get('address')
            description = data.get('description')

            if not full_name or not phone_number or not address or not description:
                return JsonResponse({'message': 'All fields are required.'}, status=400)

            user = User.objects.get(id=userId)

            profile = user.facebookProfile
            profile.full_name = full_name
            profile.phone_number = phone_number
            profile.address = address
            profile.description = description

            profile.save()

            return JsonResponse({'message': 'Profile updated successfully.'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'message': f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


@csrf_exempt
def create_username_facebook(request, userId):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            isPolicy = data.get('policy')
            isMail = data.get('mail')
            
            # Vérification que policy est True
            if not isPolicy:
                return JsonResponse({'message': 'You must accept the privacy policy.'}, status=400)
            
            user = User.objects.get(id=userId)
            profile = user.facebookProfile
            
            # Mise à jour des données
            profile.isPrivacyChecked = isPolicy
            profile.isSendMailChacked = isMail
            user.username = username
            user.save()
            profile.save()
            
            return JsonResponse({'message': 'Profile updated successfully.'}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e)}, status=400)

@csrf_exempt
def facebook_login(request):
    print("I'm used")
    if request.method == "POST":
        try:
            if request.content_type == "application/x-www-form-urlencoded":
                data = request.POST 
            elif request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                return JsonResponse({"message": "Unsupported content type"}, status=400)
            print(f"Parsed data: {data}")

            id_token = data.get('id_token')
            if id_token:
                url = f'https://graph.facebook.com/v11.0/me?fields=email,first_name,last_name,picture&access_token={id_token}'
                response = requests.get(url)
                print(f"facebook response: {response.status_code}, {response.text}")
                user_info = response.json()
                if response.status_code == 200:
                    user_email = user_info.get('email')
                    try:
                        user = User.objects.get(email=user_email)
                    except User.DoesNotExist:
                        return JsonResponse({"message": "Email does not exist in the database"}, status=400)
                    user_first_name = user_info.get('given_name')
                    user_last_name = user_info.get('family_name')
                    user_full_name = f"{user_first_name} {user_last_name}"  
                    user_avatar = user_info.get('picture') 

                    user_google, google_created = UserFacebook.objects.update_or_create(
                        user=user,
                        defaults={
                            'full_name': user_full_name,  # Stocker le nom complet
                            'avatar': user_avatar
                        }
                    )
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    token_instance, created = AuthToken.objects.get_or_create(user=user)
                    token_instance.token = access_token
                    token_instance.save()
                    message = "User updated" if google_created else "User already updated"
                    return JsonResponse({
                    'message': 'Connexion réussie',
                    'user_id': user.id,
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'user_profile': {
                        'email':user.email,
                        'username':user.username,
                        'avatar': user_google.avatar["data"]["url"] if user_google.avatar else None,
                        'phone_number': user_google.phone_number,
                        'full_name': user_google.full_name,
                        'address': user_google.address,
                        'description': user_google.description,
                        'hasStory':user_google.hasStory,
                        'is_email_verified':True,
                        'verification_code':"",

                        
                       
                    }
                }, status=200)
                else:
                    return JsonResponse({"message": "Invalid token"}, status=400)
            else:
                return JsonResponse({"message": "No token provided"}, status=400)
        except Exception as e:
            error_details = traceback.format_exc()
            print(f"Error during token verification: {error_details}")
            return JsonResponse({"message": "Error verifying token", "error": str(e)}, status=500)
    else:
        return JsonResponse({"message": "Invalid method"}, status=405)
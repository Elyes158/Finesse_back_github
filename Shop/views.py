from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Order, Payment, Product, Category, ProductImage,Comment, SubCategory
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, ProductImage, User, Category
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Product, ProductImage, User, SubCategory

@csrf_exempt
def create_product_with_images(request):
    if request.method == 'POST':
        try:
            print("Début de la requête POST")  # Premier print pour indiquer que la requête a commencé

            # Récupérer les données JSON
            data = request.POST
            print("Données reçues:", data)  # Print les données reçues

            owner_id = data.get('owner_id')
            category_id = data.get('category_id')
            title = data.get('title')
            description = data.get('description')
            price = data.get('price')
            etat = data.get('etat'),
            is_available = data.get('is_available', 'true') == 'true'

            if not owner_id or not title or not price:
                return JsonResponse({'error': 'Les champs obligatoires sont manquants.'}, status=400)

            print("Données validées pour owner_id:", owner_id, "title:", title, "price:", price)

            owner = get_object_or_404(User, id=owner_id)
            print("Utilisateur récupéré:", owner)

            Subcategory = get_object_or_404(SubCategory, name=category_id) if category_id else None
            print("Sous-catégorie récupérée:", Subcategory)

            product = Product.objects.create(
                owner=owner,
                subcategory=Subcategory,
                title=title,
                description=description,
                price=price,
                is_available=is_available,
                etat = etat
            )
            print(f"Produit '{product.title}' créé avec succès!")

            images = request.FILES.getlist('images')
            print("Images reçues:", images)  # Vérifie les images reçues

            for image in images:
                print(f"Enregistrement de l'image: {image}")
                ProductImage.objects.create(product=product, image=image)

            return JsonResponse({'message': f'Produit "{product.title}" avec images créé avec succès!'}, status=201)

        except Exception as e:
            print("Erreur rencontrée:", str(e))  # Affiche l'erreur rencontrée
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Seules les requêtes POST sont autorisées.'}, status=405)


@csrf_exempt
def get_products_by_user(request, userId):
    print("La fonction a été appelée.")  # Vérifier si la fonction est appelée
    if request.method == 'GET':
        try:
            print(f"Requête pour récupérer les produits de l'utilisateur avec ID: {userId}")
            user = get_object_or_404(User, id=userId)
            print(f"Utilisateur récupéré : {user}")
            products = Product.objects.filter(owner=user, validated=True)
            print(f"Produits trouvés : {products.count()}")
            products_data = []
            for product in products:
                images = ProductImage.objects.filter(product=product)
                images_urls = [image.image.url for image in images]
                print("heeeeeeeeeeeeeeey")
                product_data = {
                    'id': product.id,
                    'title': product.title,
                    'description': product.description,
                    'price': product.price,
                    'is_available': product.is_available,
                    'subcategory': product.subcategory.name if product.subcategory else None,
                    'images': images_urls,
                }
                products_data.append(product_data)
            return JsonResponse({'products': products_data}, status=200)

        except Exception as e:
            print(f"Erreur rencontrée lors de la récupération des produits : {str(e)}")
            return JsonResponse({'error': f"Erreur : {str(e)}"}, status=500)

    return JsonResponse({'error': 'Seules les requêtes GET sont autorisées.'}, status=405)



@csrf_exempt
def get_products(request):
    print("La fonction a été appelée.")  # Vérifier si la fonction est appelée
    if request.method == 'GET':
        try:
            products = Product.objects.filter(validated=True)
            print(f"Produits trouvés : {products.count()}")
            products_data = []
            for product in products:
                images = ProductImage.objects.filter(product=product)
                images_urls = [image.image.url for image in images]
                print("heeeeeeeeeeeeeeey")
                product_data = {
                    'id': product.id,
                    'title': product.title,
                    'description': product.description,
                    'price': product.price,
                    'is_available': product.is_available,
                    'subcategory': product.subcategory.name if product.subcategory else None,
                    'images': images_urls,
                }
                products_data.append(product_data)
            return JsonResponse({'products': products_data}, status=200)

        except Exception as e:
            print(f"Erreur rencontrée lors de la récupération des produits : {str(e)}")
            return JsonResponse({'error': f"Erreur : {str(e)}"}, status=500)

    return JsonResponse({'error': 'Seules les requêtes GET sont autorisées.'}, status=405)


################################################################
def create_order(request):
    if request.method == 'POST':
        buyer_id = request.POST.get('buyer_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1)) 

        if not buyer_id or not product_id:
            return JsonResponse({'error': 'Les champs obligatoires sont manquants.'}, status=400)
        try:
            buyer = get_object_or_404(User, id=buyer_id)
            product = get_object_or_404(Product, id=product_id)

            total_price = product.price * quantity

            order = Order.objects.create(
                buyer=buyer,
                product=product,
                total_price=total_price
            )
            return JsonResponse({'message': f'Commande #{order.id} créée avec succès!', 'order_id': order.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Seules les requêtes POST sont autorisées.'}, status=405)

def create_payment(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        order_id = request.POST.get('order_id')
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')

        if not user_id or not order_id or not payment_method or not amount:
            return JsonResponse({'error': 'Les champs obligatoires sont manquants.'}, status=400)

        try:
            user = get_object_or_404(User, id=user_id)
            order = get_object_or_404(Order, id=order_id)

            if float(amount) != float(order.total_price):
                return JsonResponse({'error': 'Le montant du paiement ne correspond pas au total de la commande.'}, status=400)

            payment = Payment.objects.create(
                user=user,
                order=order,
                amount=amount,
                payment_method=payment_method,
                status='Completed' 
            )

            order.status = 'Paid'
            order.save()

            return JsonResponse({
                'message': f'Paiement pour la commande #{order.id} effectué avec succès!',
                'payment_id': payment.id,
                'payment_method': payment.payment_method,
                'status': payment.status
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Seules les requêtes POST sont autorisées.'}, status=405)

##################################################################""

def get_product_comments(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    comments = product.comments.all().values('user__username', 'content', 'created_at')
    
    if comments:
        return JsonResponse(list(comments), safe=False, status=200)
    else:
        return JsonResponse({'message': 'Aucun commentaire trouvé pour ce produit.'}, status=404)
    
@csrf_exempt  
def create_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        content = request.POST.get('content')
        if not content:
            return JsonResponse({'error': 'Le contenu du commentaire est requis.'}, status=400)
        
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Vous devez être connecté pour ajouter un commentaire.'}, status=401)

        comment = Comment.objects.create(
            product=product,
            user=request.user,
            content=content
        )
        return JsonResponse({'message': 'Commentaire créé avec succès!', 'comment_id': comment.id}, status=201)
    return JsonResponse({'error': 'Seules les requêtes POST sont autorisées.'}, status=405)

###################################################
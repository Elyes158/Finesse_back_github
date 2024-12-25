from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Order, Payment, Product, Category, ProductImage,Comment
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def create_product_with_images(request):
    if request.method == 'POST':
        # Récupérer les données de la requête
        owner_id = request.POST.get('owner_id')
        category_id = request.POST.get('category_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available', 'true') == 'true'

        if not owner_id or not title or not price:
            return JsonResponse({'error': 'Les champs obligatoires sont manquants.'}, status=400)

        try:
            owner = get_object_or_404(User, id=owner_id)
            category = get_object_or_404(Category, id=category_id) if category_id else None

            # Créer le produit
            product = Product.objects.create(
                owner=owner,
                category=category,
                title=title,
                description=description,
                price=price,
                is_available=is_available
            )

            # Gérer les images
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return JsonResponse({'message': f'Produit "{product.title}" avec images créé avec succès!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Seules les requêtes POST sont autorisées.'}, status=405)

################################################################
def create_order(request):
    if request.method == 'POST':
        # Récupérer les données de la requête
        buyer_id = request.POST.get('buyer_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Par défaut, la quantité est 1

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
        # Récupérer les données de la requête
        user_id = request.POST.get('user_id')
        order_id = request.POST.get('order_id')
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')

        if not user_id or not order_id or not payment_method or not amount:
            return JsonResponse({'error': 'Les champs obligatoires sont manquants.'}, status=400)

        try:
            user = get_object_or_404(User, id=user_id)
            order = get_object_or_404(Order, id=order_id)

            # Vérifier que le montant correspond au total de la commande
            if float(amount) != float(order.total_price):
                return JsonResponse({'error': 'Le montant du paiement ne correspond pas au total de la commande.'}, status=400)

            # Créer le paiement
            payment = Payment.objects.create(
                user=user,
                order=order,
                amount=amount,
                payment_method=payment_method,
                status='Completed'  # Mise à jour automatique du statut en "Complété" lors de la création du paiement
            )

            # Mettre à jour le statut de l'ordre à "Paid"
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
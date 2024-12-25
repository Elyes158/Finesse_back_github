from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Order, Product, Category, ProductImage
from django.contrib.auth.models import User
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


def create_order(request):
    if request.method == 'POST':
        # Récupérer les données de la requête
        buyer_id = request.POST.get('buyer_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Par défaut, la quantité est 1

        # Validation des données
        if not buyer_id or not product_id:
            return JsonResponse({'error': 'Les champs obligatoires sont manquants.'}, status=400)

        try:
            # Récupérer l'utilisateur et le produit
            buyer = get_object_or_404(User, id=buyer_id)
            product = get_object_or_404(Product, id=product_id)

            # Calculer le prix total
            total_price = product.price * quantity

            # Créer la commande
            order = Order.objects.create(
                buyer=buyer,
                product=product,
                total_price=total_price
            )

            return JsonResponse({'message': f'Commande #{order.id} créée avec succès!', 'order_id': order.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Seules les requêtes POST sont autorisées.'}, status=405)
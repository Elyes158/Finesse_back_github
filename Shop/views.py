from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category, ProductImage
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

        # Validation des données
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
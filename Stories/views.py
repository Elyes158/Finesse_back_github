from .models import Story
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def create_story(request,userId):
    if request.method == 'POST':
        user = User.objects.get(id = userId)
        story_image = request.FILES.get('story_image')
        if not story_image:
            return JsonResponse({'error': 'Story image is required.'}, status=400)
        
        try:
            story = Story.objects.create(
                user=user,
                story_image=story_image,
                created_at=now(),
                expires_at=now() + timedelta(hours=24)  
            )
            user.profile.hasStory = True
            user.profile.save()
            return JsonResponse({
                'message': 'Story created successfully!',
                'story_id': story.id,
                'created_at': story.created_at.isoformat(),
                'expires_at': story.expires_at.isoformat()
            }, status=201)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
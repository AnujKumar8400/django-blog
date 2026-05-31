from .models import Category
from assignments.models import SocialMedia

def get_category(request):
    categories = Category.objects.all()
    return dict(categories = categories)


def get_social_media(request):
    social_media = SocialMedia.objects.all()
    return dict(social_media = social_media)
from django.db import models



class About(models.Model):
    about_name = models.CharField(max_length=50)
    about_description = models.TextField()
    
    def __str__(self):
        return self.about_name
    
class SocialMedia(models.Model):
    plateform = models.CharField(max_length=50)
    link = models.URLField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plateform

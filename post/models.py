from django.db import models

# Create your models here.

class Post(models.Model):

  title = models.CharField(max_length=255)
  context = models.TextField()
  user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='posts')
  likes = models.ManyToManyField("user.User", related_name='like_posts')
  hash_tags = models.ManyToManyField("post.HashTag", related_name='posts')
  delete_flag= models.BooleanField(default=False)

  @classmethod
  def active(self):
    return self.objects.filter(delete_flag=False)    

  def pagenation(self, page, page_per=10):
    return self[page * page_per: (page+1) * page_per]

class HashTag(models.Model):
  name = models.CharField(max_length=255, unique=True)
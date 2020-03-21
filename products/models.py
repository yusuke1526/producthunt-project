from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
  title = models.CharField(max_length=255)
  url = models.TextField()
  pub_date = models.DateTimeField()
  votes_total = models.IntegerField(default=0)
  image = models.ImageField(upload_to='images/')
  icon = models.ImageField(upload_to='images/')
  body = models.TextField()
  hunter = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

  def summary(self):
    if len(self.body) > 120:
      return self.body[:120] + '...'
    else:
      return self.body

  def pub_date_pretty(self):
    return self.pub_date.strftime('%b %e %Y')

class Vote(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  @classmethod
  def exists(cls, product_id, user_id):
    try:
      Vote.objects.get(product_id=product_id, user_id=user_id)
      return True
    except Vote.DoesNotExist:
      return False
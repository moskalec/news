from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    creation_date = models.DateField()
    amount_of_upvotes = models.IntegerField()
    # author_name

    def __str__(self):
        return self.title
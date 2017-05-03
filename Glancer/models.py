from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


#Review
class Review(models.Model):
    date = models.DateField('Date Sent')
    description = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return str(self.date)

    @classmethod
    def create(cls, Date, Description):
        review = cls(date=Date, description=Description)
        review.save()
        return review

#Company
class Company(models.Model):
    name = models.CharField(blank="False", max_length=100)
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return str(self.name)

#User profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    glance_number = models.PositiveIntegerField(blank='false', default=0)
    glance_giveaway = models.PositiveIntegerField(blank='false', default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)

    #Profile automatically created/updated when we create/update User instances
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

#Glance model. Defines Glance (Point) class
class Glance(models.Model):
    value = 1
    date = models.DateField('Date Sent')
    description = models.TextField(max_length=200, blank=True)
    receiver = models.ForeignKey(Profile, related_name="glance_receiver", on_delete=models.CASCADE)


    def __str__(self):
        return str(self.receiver.user.first_name + " | " + str(self.date))

    #Create a new instance of Glance (used in views.create_glance)
    @classmethod
    def create(cls, Date, Description, Receiver):
        glance = cls(date = Date, description=Description, receiver=Receiver)
        glance.save()
        return glance


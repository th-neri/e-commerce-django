from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Customer

# creating a post_save signal of the user model so the store app gets notified an user was created and 
# it creates a customer record. basically django will know that it should call this signal everytime an user model is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_the_user(sender, **kwargs):
    # the boolean checks if a new instance was created and if yes, it creates a customer record
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])
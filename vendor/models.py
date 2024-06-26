from collections.abc import Iterable
from django.db import models
from accounts.models import User, userProfile
from accounts.utils import send_notification
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name = 'user', on_delete=models.CASCADE)
    vendor_profile = models.OneToOneField(
        userProfile, related_name = 'userProfile', on_delete=models.CASCADE
    )
    vendor_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            previous_record = Vendor.objects.get(pk=self.pk)
            if previous_record.is_approved != self.is_approved:
                email_template = 'emails/email_approval_notification.html'
                context = {
                    "user" : self.user,
                    "is_approved" : self.is_approved,
                }
                if self.is_approved == True:
                    mail_subject = "Your restaurant has been approved"
                    send_notification(mail_subject, email_template, context)
                else:
                    mail_subject = "Your restaurant has been suspended"
                    send_notification(mail_subject, email_template, context)
        return super(Vendor, self).save(*args, **kwargs)

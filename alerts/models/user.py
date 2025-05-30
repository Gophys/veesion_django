
from django.db import models
from django.db.models.constraints import UniqueConstraint

class User(models.Model):
    # Fields for user information used by notifications
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    api_uid = models.CharField(max_length=100, blank=True, null=True)

    # Constraints to ensure uniqueness of api_uid and phone, but allow nulls
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["api_uid"],
                name="unique_api_uid_constraint",
                condition=(
                    models.Q(api_uid__isnull=False) & ~models.Q(api_uid__exact="")
                ),
            ),
            UniqueConstraint(
                fields=["phone"],
                name="unique_phone_constraint",
                condition=(models.Q(phone__isnull=False) & ~models.Q(phone__exact="")),
            ),
        ]

    def __str__(self):
        return self.email

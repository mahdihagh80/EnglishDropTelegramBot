from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

   
class Media(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True


class TelegramChannel(Media):
    title = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class InstagramPage(Media):
    title = models.CharField(max_length=255)
    instagram_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=255, primary_key=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    instagram_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.full_name


class Package(models.Model):
    title = models.CharField(max_length=255)
    voice = models.FileField(upload_to='packages/voices/', )
    description = models.TextField()
    price = models.CharField(max_length=255)
    telegram_channels = models.ManyToManyField(TelegramChannel)
    instagram_pages = models.ManyToManyField(InstagramPage)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class BankAccount(models.Model):
    title = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    owner_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Transaction(models.Model):
    class TransactionState(models.TextChoices):
        ACCEPTED = "AC", _("Accepted")
        REJECTED = "RE", _("Rejected")
        PENDING = "PE", _("Pending")

    user = models.ForeignKey(TelegramUser, on_delete=models.RESTRICT)
    package = models.ForeignKey(Package, on_delete=models.RESTRICT)
    package_price = models.CharField(max_length=255)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.RESTRICT)
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    state = models.CharField(max_length=2, choices=TransactionState.choices, default=TransactionState.PENDING)
    links_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.user.full_name




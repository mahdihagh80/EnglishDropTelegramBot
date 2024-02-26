from rest_framework import serializers
from .models import Package, Transaction, TelegramUser, BankAccount
from rest_framework.parsers import FileUploadParser


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        exclude = ['telegram_channels', 'instagram_pages', 'active']


class TransactionSerializer(serializers.ModelSerializer):
    parser_classes = (FileUploadParser,)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'package', 'receipt', 'bank_account', 'package_price']

    
class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        exclude = ['created_at']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        exclude = ['title', 'active']
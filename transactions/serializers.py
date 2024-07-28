from rest_framework import serializers 
from .models import Transaction
from products.models import ProductCategory
from users.serializers import WalletSerializer
class TransactionSerializer(serializers.ModelSerializer):
  status_display = serializers.SerializerMethodField()
  transaction_type = serializers.SerializerMethodField()
  wallet = WalletSerializer()

  def get_status_display(self, obj):
    return obj.get_status_display()

  def get_transaction_type(self, obj):
    return obj.transaction_type.category 

  class Meta:
    model = Transaction
    fields = (
        'transaction_ref_no', 
        'wallet',
        'transaction_type',
        'product',
        'price',
        'status_display',
        'date_create'
    )
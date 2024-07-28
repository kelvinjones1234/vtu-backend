from django.db import models
from users.models import Wallet, User
import uuid
from products.models import ProductCategory

class Transaction(models.Model):
    STATUS = (
        ('S', 'Success'),
        ('P', 'Pending'),
        ('F', 'Failed')
    )
    transaction_ref_no = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Transaction ID")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product



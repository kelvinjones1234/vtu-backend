# Generated by Django 5.0.3 on 2024-08-06 15:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0003_remove_electricitysettings_disco_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_ref_no', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Transaction ID')),
                ('product', models.CharField(max_length=100)),
                ('price', models.PositiveBigIntegerField()),
                ('status', models.CharField(choices=[('S', 'Success'), ('P', 'Pending'), ('F', 'Failed')], default='P', max_length=1)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productcategory')),
            ],
        ),
    ]

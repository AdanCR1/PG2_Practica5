# Generated by Django 5.2 on 2025-07-06 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos_cafe', '0002_remove_pedidocafe_precio_pedidocafe_cliente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidocafe',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

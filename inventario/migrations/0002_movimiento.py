# Generated by Django 5.1 on 2025-06-17 18:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=10)),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto')),
                ('realizado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

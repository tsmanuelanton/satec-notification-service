# Generated by Django 4.2.2 on 2023-06-24 21:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_subscription_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriptiongroup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='conector',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=45),
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-26 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WM_pp', '0004_alter_filter_price_price_alter_product_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=50)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

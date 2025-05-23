# Generated by Django 5.2.1 on 2025-05-12 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productname', models.CharField(max_length=100, null=True)),
                ('size', models.IntegerField()),
                ('item_photo', models.ImageField(blank=True, null=True, upload_to='menu_photo/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminuser.category_gender')),
            ],
        ),
    ]

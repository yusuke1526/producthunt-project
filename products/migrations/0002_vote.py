# Generated by Django 2.2.11 on 2020-03-21 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
            ],
        ),
    ]

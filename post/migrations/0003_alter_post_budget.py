# Generated by Django 4.2.3 on 2023-07-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_remove_post_text_post_actors_post_budget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='budget',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True, verbose_name='Цена'),
        ),
    ]

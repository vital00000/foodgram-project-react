# Generated by Django 3.2.18 on 2023-03-30 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recopes', '0008_auto_20230330_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('created_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='pub_date',
            new_name='created_date',
        ),
    ]

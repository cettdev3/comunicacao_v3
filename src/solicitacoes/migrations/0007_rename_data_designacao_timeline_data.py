# Generated by Django 4.0.6 on 2023-12-07 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0006_timeline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeline',
            old_name='data_designacao',
            new_name='data',
        ),
    ]

# Generated by Django 4.0.6 on 2023-12-15 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitacoes', '0009_demandas_descricao_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitacoes',
            name='prioridade',
            field=models.IntegerField(choices=[(1, 'Normal'), (2, 'Urgente')], default=1),
        ),
    ]

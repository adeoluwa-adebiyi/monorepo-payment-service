# Generated by Django 3.1.5 on 2021-02-04 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordertransaction',
            old_name='order_id',
            new_name='trxjob_id',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='charge_response',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='validate_response',
            field=models.JSONField(null=True),
        ),
    ]

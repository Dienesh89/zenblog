# Generated by Django 4.1.7 on 2023-04-20 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_postinfo_date_alter_postinfo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postinfo',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

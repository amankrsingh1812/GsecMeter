# Generated by Django 2.0.3 on 2020-01-14 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsecWorkStatus', '0020_auto_20200109_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='votes',
            fields=[
                ('vote_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_id', models.IntegerField(null=True)),
                ('user_id', models.CharField(max_length=1000)),
            ],
        ),
    ]

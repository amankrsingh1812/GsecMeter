# Generated by Django 2.0.5 on 2018-06-06 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gsecWorkStatus', '0009_auto_20180606_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='status',
            field=models.CharField(choices=[('Completed', 'COMPLETED'), ('Ongoing-Long-Term', 'ONGOING-LONG-TERM'), ('Ongoing-Short-term', 'ONGOING-SHORT-TERM'), ('Not-Started', 'NOT_STARTED'), ('Broken', 'BROKEN'), ('Not-Evaluated', 'NOT-EVALUATED'), ('Not-Evaluated-Subjective', 'NOT-EVALUATED-SUBJECTIVE')], default='Select', max_length=100),
        ),
    ]

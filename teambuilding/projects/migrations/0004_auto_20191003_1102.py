# Generated by Django 2.2.5 on 2019-10-03 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20191002_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='applicant_requirements',
            field=models.TextField(blank=True),
        ),
    ]

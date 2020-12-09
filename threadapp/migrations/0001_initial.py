# Generated by Django 3.1.4 on 2020-12-09 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accountapp', '0002_user_company_cd'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, null=True)),
                ('thread_cd', models.CharField(max_length=50, unique=True)),
                ('thread_nm', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=200, null=True)),
                ('image', models.ImageField(null=True, upload_to='thread/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='company', to='accountapp.company')),
            ],
        ),
    ]

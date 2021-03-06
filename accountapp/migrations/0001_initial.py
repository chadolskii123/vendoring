# Generated by Django 3.1.4 on 2020-12-08 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_cd', models.CharField(max_length=2, unique=True)),
                ('company_nm', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_cd', models.CharField(max_length=2, unique=True)),
                ('position_nm', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_cd', models.CharField(max_length=2, unique=True)),
                ('dept_nm', models.CharField(max_length=50)),
                ('dept_grade', models.IntegerField()),
                ('parent_dept_cd', models.CharField(blank=True, max_length=2, null=True, unique=True)),
                ('company_cd', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accountapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.CharField(max_length=255, unique=True, verbose_name='ID')),
                ('email', models.CharField(max_length=255, unique=True, verbose_name='이메일')),
                ('is_active', models.BooleanField(default=True)),
                ('perm_grade', models.IntegerField(default=5)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('dept_cd', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accountapp.department')),
                ('position_cd', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accountapp.position')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

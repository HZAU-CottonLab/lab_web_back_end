# Generated by Django 3.2.8 on 2022-06-16 14:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(default='None', max_length=30)),
                ('sex', models.IntegerField(blank=True, choices=[(0, '男'), (1, '女')], null='NULL')),
                ('img_url', models.CharField(blank=True, max_length=30, null='NULL')),
                ('people_type', models.IntegerField(blank=True, choices=[(0, '老师'), (1, '博士后'), (2, '博士'), (3, '硕士'), (4, '访问学者')], null='NULL')),
                ('contact', models.CharField(blank=True, max_length=50, null='NULL')),
                ('office_site', models.CharField(blank=True, max_length=100, null='NULL')),
                ('info_detail', models.CharField(blank=True, max_length=100, null='NULL')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
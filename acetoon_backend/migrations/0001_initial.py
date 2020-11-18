# Generated by Django 3.1.1 on 2020-11-18 03:29

import acetoon_backend.models.submission
import acetoon_backend.models.user
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('M', 'male'), ('F', 'female'), ('O', 'other')], max_length=1)),
                ('designation', models.CharField(blank=True, max_length=255)),
                ('bio', models.TextField(blank=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to=acetoon_backend.models.user.upload_path)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('PT', 'Painting'), ('SI', 'Singing'), ('HT', 'Hackathon'), ('DN', 'Dancing'), ('PT', 'Photography'), ('OT', 'Other')], max_length=2)),
                ('start_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('eligibility', models.TextField(blank=True)),
                ('rules', models.TextField()),
                ('prizes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('token', models.CharField(blank=True, max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='acetoon_backend.contest')),
                ('members', models.ManyToManyField(blank=True, related_name='teams', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'unique_together': {('name', 'contest')},
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField(blank=True)),
                ('rating', models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('link', models.URLField(blank=True)),
                ('file', models.FileField(blank=True, upload_to=acetoon_backend.models.submission.upload_path)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='acetoon_backend.contest')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_submissions', to='acetoon_backend.team')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_no', models.CharField(max_length=12)),
                ('email_id', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('is_organizer', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contest',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contests', to='acetoon_backend.organizer'),
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='acetoon_backend.contest')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]

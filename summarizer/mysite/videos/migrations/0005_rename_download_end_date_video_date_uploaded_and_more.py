# Generated by Django 5.1.1 on 2024-10-08 13:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_alter_summary_date_alter_summary_summary_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='download_end_date',
            new_name='date_uploaded',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='download_start_date',
            new_name='download_end_datetime',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='pub_date',
            new_name='upload_date_youtube',
        ),
        migrations.RemoveField(
            model_name='summary',
            name='date',
        ),
        migrations.RemoveField(
            model_name='video',
            name='audio',
        ),
        migrations.RemoveField(
            model_name='video',
            name='channel',
        ),
        migrations.AddField(
            model_name='summary',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='summary',
            name='gpt_information',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='summary_path',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='title',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='summary',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='video',
            name='audio_path',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='categories',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='channel_name',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='channel_url',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='video',
            name='download_start_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='ext',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='is_transcribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='like_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='title_with_ext',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='transcribing_end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='transcribing_start_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='transcribing_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='transcript_path',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='video',
            name='view_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='summary',
            name='summary_text',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='is_summarized',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(default='Pending'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='transcript',
            field=models.CharField(null=True),
        ),
    ]
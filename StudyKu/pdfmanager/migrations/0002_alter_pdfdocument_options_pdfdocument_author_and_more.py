from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
        ('pdfmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfdocument',
            name='author',
            field=models.ForeignKey(null=True, blank=True, on_delete=models.CASCADE, to='auth.user'),
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='updated_at',
            field=models.DateTimeField(null=True, blank=True, default=django.utils.timezone.now),
        ),
    ]
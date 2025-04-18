# Generated by Django 5.0.1 on 2024-02-14 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_management', '0023_alter_bookrequest_status_alter_books_geners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrequest',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('return', 'Returned'), ('denied', 'Denied'), ('requested', 'Requested')], default='requested', max_length=30),
        ),
        migrations.AlterField(
            model_name='books',
            name='Geners',
            field=models.CharField(choices=[('action', 'Action'), ('adventure', 'Adventure'), ('crime', 'Crime'), ('suspense', 'Suspense')], default='action', max_length=30),
        ),
    ]

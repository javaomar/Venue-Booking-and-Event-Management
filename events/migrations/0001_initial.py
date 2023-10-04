# Generated by Django 4.2.5 on 2023-09-30 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Event Name')),
                ('speaker', models.CharField(blank=True, max_length=250, null=True, verbose_name='Speaker')),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
                ('description', models.TextField(blank=True, default='')),
                ('description_html', models.TextField(blank=True, default='', editable=False)),
                ('total_tickets', models.PositiveIntegerField(default=0)),
                ('available_tickets', models.PositiveIntegerField(default=0)),
                ('ticket_price', models.PositiveIntegerField(default=0)),
                ('payment', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_reservation', to='reservation.reservation')),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='venue.venue')),
            ],
            options={
                'ordering': ['-event_date'],
            },
        ),
        migrations.CreateModel(
            name='MyClubUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=40, verbose_name='User Email')),
                ('event', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='myclub', to='events.event')),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.CharField(default='', max_length=20, unique=True)),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myclub', to='events.myclubuser')),
            ],
            options={
                'ordering': ['ticket_number'],
            },
        ),
        migrations.CreateModel(
            name='BuyTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=250, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=40, verbose_name='User Email')),
                ('card_type', models.CharField(choices=[('mastercard', 'MasterCard'), ('visacard', 'VisaCard')], max_length=20)),
                ('card_name', models.CharField(max_length=250)),
                ('card_number', models.CharField(max_length=450)),
                ('card_date', models.CharField(max_length=250)),
                ('card_security', models.CharField(max_length=100)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.ticket')),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('card_type', models.CharField(choices=[('mastercard', 'MasterCard'), ('visacard', 'VisaCard')], max_length=20)),
                ('card_name', models.CharField(max_length=250)),
                ('card_number', models.CharField(max_length=450)),
                ('card_date', models.CharField(max_length=250)),
                ('card_security', models.CharField(max_length=100)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('reservation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='reservation.reservation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='venue.venue')),
            ],
            options={
                'unique_together': {('venue', 'user')},
            },
        ),
    ]
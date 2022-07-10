# Generated by Django 4.0.1 on 2022-06-12 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=50)),
                ('mnemonic', models.CharField(max_length=100)),
                ('created', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'crypto_accounts',
            },
        ),
        migrations.CreateModel(
            name='NFTPrepared',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=100)),
                ('data', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nft_prepared',
            },
        ),
        migrations.CreateModel(
            name='NFTMinted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('location', models.CharField(max_length=250)),
                ('url', models.CharField(max_length=150)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='home.cryptoaccount')),
                ('prepared', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='home.nftprepared')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nft_final',
            },
        ),
    ]

# Generated by Django 3.1.7 on 2021-04-24 08:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
        migrations.AlterField(
            model_name='item',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.brand'),
        ),
        migrations.CreateModel(
            name='CheckoutCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=None, max_length=200)),
                ('last_name', models.CharField(default=None, max_length=200)),
                ('username', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('shipping_add', models.CharField(max_length=200)),
                ('mobile_no', models.IntegerField()),
                ('zip_code', models.CharField(default=None, max_length=20)),
                ('date_checked', models.DateTimeField(default=django.utils.timezone.now)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.cart')),
                ('items', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.item')),
            ],
        ),
        migrations.CreateModel(
            name='CartTotal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default=None, max_length=200)),
                ('net_total', models.IntegerField(default=0)),
                ('slug', models.CharField(default=None, max_length=100, unique=True)),
                ('shipping_cost', models.IntegerField(default=0)),
                ('grand_total', models.IntegerField(default=0)),
                ('checkout', models.BooleanField(default=False)),
                ('cart', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.cart')),
            ],
        ),
    ]

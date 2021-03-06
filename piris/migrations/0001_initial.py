# Generated by Django 3.0 on 2021-02-23 18:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('father_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('place_of_birth', models.CharField(max_length=50)),
                ('place_of_living', models.CharField(choices=[('MSQ', 'Minsk'), ('BRS', 'Brest'), ('GML', 'Gomel'), ('VTB', 'Vitebsk'), ('MZ', 'Mozyr'), ('GRD', 'Grodno')], max_length=50)),
                ('sex', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=7)),
                ('passport_series', models.CharField(max_length=2)),
                ('passport_id', models.CharField(max_length=7, unique=True)),
                ('goverment', models.CharField(max_length=50)),
                ('passport_date', models.DateField()),
                ('passport_uuid', models.CharField(max_length=14, unique=True)),
                ('address', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('mobile_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('relationship_status', models.CharField(choices=[('H', 'HOLOST'), ('Z', 'ZAMYZEM'), ('ZH', 'ZHENAT')], max_length=10)),
                ('citizenship', models.CharField(choices=[('BLR', 'Беларусь'), ('EU', 'Евросоюз'), ('USA', 'США')], max_length=20)),
                ('disability', models.CharField(choices=[('N', 'НЕТ'), ('I', 'I группа'), ('II', 'II группа'), ('III', 'III группа')], max_length=20)),
                ('pensioner', models.BooleanField(default=False)),
                ('salary', models.CharField(blank=True, max_length=15)),
                ('liable_for_military_service', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PlanOfBaseAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4, unique=True)),
                ('name', models.CharField(max_length=70)),
                ('activity', models.CharField(choices=[('A', 'active'), ('P', 'passive')], max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='BankPersonalContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_in_months', models.IntegerField(default=0)),
                ('date_of_creating', models.DateField(default=django.utils.timezone.now)),
                ('date_of_ending', models.DateField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('UD', 'До восстребования'), ('URG', 'Срочный')], max_length=35)),
                ('percents', models.CharField(default='', max_length=35)),
                ('capitalization', models.BooleanField(default=False)),
                ('currency', models.CharField(choices=[('EUR', 'EUR'), ('USD', 'USD'), ('BYN', 'BYN')], default='BYN', max_length=3)),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person', to='piris.Person')),
            ],
        ),
        migrations.CreateModel(
            name='BankCreditContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_in_months', models.IntegerField(default=0)),
                ('date_of_creating', models.DateField(default=django.utils.timezone.now)),
                ('date_of_ending', models.DateField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('DIF', 'differentiated'), ('ANN', 'annuity')], max_length=35)),
                ('percents', models.CharField(default='', max_length=35)),
                ('currency', models.CharField(choices=[('EUR', 'EUR'), ('USD', 'USD'), ('BYN', 'BYN')], default='BYN', max_length=3)),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_credit', to='piris.Person')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=14)),
                ('initial_price', models.CharField(max_length=35)),
                ('current_price', models.CharField(max_length=35)),
                ('final_price', models.CharField(max_length=35)),
                ('income', models.CharField(max_length=35)),
                ('account_type', models.CharField(choices=[('DEP', 'deposit'), ('ACT', 'active_card'), ('PRC', 'percentages')], max_length=35)),
                ('base_account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_type', to='piris.PlanOfBaseAccounts')),
                ('contract_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='piris.BankPersonalContract')),
            ],
        ),
    ]

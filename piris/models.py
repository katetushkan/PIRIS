from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from piris.constants import SEX_CHOICES, CITY_CHOICES, RELATION_STATUS_CHOICES, CITIZENSHIP_CHOICES, DISABILITY_CHOICES, \
    ACTIVITY_CHOICES, DEPOSIT_CHOICES, BANK_ACCOUNT_TYPE, CURRENCY_CHOICES, CREDIT_CHOICES


class Person(models.Model):

    second_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(default=timezone.now)
    place_of_birth = models.CharField(max_length=50)
    place_of_living = models.CharField(max_length=50, choices=CITY_CHOICES)
    sex = models.CharField(max_length=7, choices=SEX_CHOICES)
    passport_series = models.CharField(max_length=2)
    passport_id = models.CharField(max_length=7, unique=True)
    goverment = models.CharField(max_length=50)
    passport_date = models.DateField()
    passport_uuid = models.CharField(max_length=14, unique=True)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True, unique=True)
    email = models.EmailField(blank=True)
    relationship_status = models.CharField(max_length=10, choices=RELATION_STATUS_CHOICES)
    citizenship = models.CharField(max_length=20, choices=CITIZENSHIP_CHOICES)
    disability = models.CharField(max_length=20, choices=DISABILITY_CHOICES)
    pensioner = models.BooleanField(default=False)
    salary = models.CharField(max_length=15, blank=True)
    liable_for_military_service = models.BooleanField(default=False)


class PlanOfBaseAccounts(models.Model):

    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=70)
    activity = models.CharField(max_length=35, choices=ACTIVITY_CHOICES)


class BankPersonalContract(models.Model):

    person_id = models.ForeignKey(Person, related_name='person', on_delete=models.CASCADE)
    period_in_months = models.IntegerField(default=0)
    date_of_creating = models.DateField(default=timezone.now)
    date_of_ending = models.DateField(default=timezone.now)
    type = models.CharField(max_length=35, choices=DEPOSIT_CHOICES)
    percents = models.CharField(max_length=35, default='')
    capitalization = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='BYN')


class BankAccount(models.Model):

    contract_id = models.ForeignKey(BankPersonalContract, related_name='contract', on_delete=models.CASCADE)
    base_account_id = models.ForeignKey(PlanOfBaseAccounts, related_name='account_type', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=14)
    initial_price = models.CharField(max_length=35)
    current_price = models.CharField(max_length=35)
    final_price = models.CharField(max_length=35)
    income = models.CharField(max_length=35)  # saldo - delta between final and initial price
    account_type = models.CharField(max_length=35, choices=BANK_ACCOUNT_TYPE)


class BankCreditContract(models.Model):

    person_id = models.ForeignKey(Person, related_name='person_credit', on_delete=models.CASCADE)
    period_in_months = models.IntegerField(default=0)
    date_of_creating = models.DateField(default=timezone.now)
    date_of_ending = models.DateField(default=timezone.now)
    type = models.CharField(max_length=35, choices=CREDIT_CHOICES)
    percents = models.CharField(max_length=35, default='')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='BYN')


class CreditAccount(models.Model):

    contract_id = models.ForeignKey(BankCreditContract, related_name='credit_contract', on_delete=models.CASCADE)
    base_account_id = models.ForeignKey(PlanOfBaseAccounts, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=14)
    initial_price = models.CharField(max_length=35)
    current_price = models.CharField(max_length=35)
    final_price = models.CharField(max_length=35)
    income = models.CharField(max_length=35)
    account_type = models.CharField(max_length=35, choices=BANK_ACCOUNT_TYPE)
    payments = ArrayField(ArrayField(models.IntegerField(), size=1), blank=True, default=list())
    closed = models.BooleanField(default=True)



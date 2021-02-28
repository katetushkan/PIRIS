import datetime

from django import forms
from django.forms import SelectDateWidget, RadioSelect, Select

from piris.constants import RELATION_STATUS_CHOICES, CITIZENSHIP_CHOICES, DISABILITY_CHOICES, SEX_CHOICES, CITY_CHOICES, \
    DEPOSIT_CHOICES, CURRENCY_CHOICES, NON_REVOCABLE, R_DEPOSIT_CHOICES, REVOCABLE, CREDIT_CHOICES, CREDIT
from piris.models import Person, BankPersonalContract, BankCreditContract


class CreateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    years = [year for year in range(1900, 2022)]

    second_name = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    father_name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=years),
                                    required=True)
    place_of_birth = forms.CharField(max_length=50, required=True)
    place_of_living = forms.ChoiceField(widget=Select(), choices=CITY_CHOICES, required=True)
    sex = forms.ChoiceField(widget=RadioSelect(), choices=SEX_CHOICES, required=True)
    passport_series = forms.CharField(max_length=2, required=True)
    passport_id = forms.CharField(max_length=7, required=True)
    goverment = forms.CharField(max_length=50, required=True)
    passport_date = forms.DateField(widget=SelectDateWidget(years=years), required=True)
    passport_uuid = forms.CharField(max_length=13, required=True)
    address = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    mobile_number = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    relationship_status = forms.ChoiceField(widget=Select(), choices=RELATION_STATUS_CHOICES, required=True)
    citizenship = forms.ChoiceField(widget=Select(), choices=CITIZENSHIP_CHOICES, required=True)
    disability = forms.ChoiceField(widget=Select(), choices=DISABILITY_CHOICES, required=True)
    pensioner = forms.BooleanField(required=False)
    salary = forms.CharField(max_length=15, label_suffix=' Br ', required=False)
    liable_for_military_service = forms.BooleanField(required=False)


class CreateANoNRevocableContractForm(forms.ModelForm):
    class Meta:
        model = BankPersonalContract
        fields = [
            'period_in_months',
            'date_of_creating',
            'date_of_ending',
            'type',
            'currency',
            'capitalization'
        ]

    years = [year for year in range(1900, 2050)]

    contract_number = forms.CharField(max_length=20, disabled=True)

    second_name = forms.CharField(max_length=50, required=True, disabled=True)
    first_name = forms.CharField(max_length=50, required=True, disabled=True)
    father_name = forms.CharField(max_length=50, required=True, disabled=True)
    date_of_birth = forms.CharField(required=True, disabled=True)
    passport_uuid = forms.CharField(max_length=13, required=True, disabled=True)

    date_of_creating = forms.DateField(widget=SelectDateWidget(years=years), required=True)
    date_of_ending = forms.DateField(widget=SelectDateWidget(years=years), required=True)
    period_in_months = forms.ChoiceField(widget=Select(), choices=NON_REVOCABLE)
    currency = forms.ChoiceField(widget=Select(), choices=CURRENCY_CHOICES)
    total_amount = forms.CharField(max_length=20)


class CreateARevocableContractForm(forms.ModelForm):

    class Meta:
        model = BankPersonalContract
        fields = [
            'period_in_months',
            'date_of_creating',
            'currency',
            'capitalization'
        ]

    years = [year for year in range(1900, 2050)]

    contract_number = forms.CharField(max_length=20, disabled=True)
    type = forms.ChoiceField(widget=Select(), choices=R_DEPOSIT_CHOICES)
    second_name = forms.CharField(max_length=50, required=True, disabled=True)
    first_name = forms.CharField(max_length=50, required=True, disabled=True)
    father_name = forms.CharField(max_length=50, required=True, disabled=True)
    date_of_birth = forms.CharField(required=True, disabled=True)
    passport_uuid = forms.CharField(max_length=13, required=True, disabled=True)

    date_of_creating = forms.DateField(widget=SelectDateWidget(years=years), required=True)
    period_in_months = forms.ChoiceField(widget=Select(), choices=REVOCABLE)
    currency = forms.ChoiceField(widget=Select(), choices=CURRENCY_CHOICES)
    total_amount = forms.CharField(max_length=20)


class CreditContractForm(forms.ModelForm):

    class Meta:
        model = BankCreditContract
        fields = [
            'period_in_months',
            'date_of_creating',
            'currency'
        ]

    years = [year for year in range(1900, 2050)]

    contract_number = forms.CharField(max_length=20, disabled=True)
    type = forms.ChoiceField(widget=Select(), choices=CREDIT_CHOICES)
    second_name = forms.CharField(max_length=50, required=True, disabled=True)
    first_name = forms.CharField(max_length=50, required=True, disabled=True)
    father_name = forms.CharField(max_length=50, required=True, disabled=True)
    date_of_birth = forms.CharField(required=True, disabled=True)
    passport_uuid = forms.CharField(max_length=13, required=True, disabled=True)

    date_of_creating = forms.DateField(widget=SelectDateWidget(years=years), required=True)
    period_in_months = forms.ChoiceField(widget=Select(), choices=CREDIT)
    currency = forms.ChoiceField(widget=Select(), choices=CURRENCY_CHOICES)
    total_amount = forms.CharField(max_length=20)

SEX_CHOICES = (
    ('F', 'Female'),
    ('M', 'Male')
)

CITY_CHOICES = (
    ('MSQ', 'Minsk'),
    ('BRS', 'Brest'),
    ('GML', 'Gomel'),
    ('VTB', 'Vitebsk'),
    ('MZ', 'Mozyr'),
    ('GRD', 'Grodno')
)

RELATION_STATUS_CHOICES = (
    ('H', 'HOLOST'),
    ('Z', 'ZAMYZEM'),
    ('ZH', 'ZHENAT')
)

CITIZENSHIP_CHOICES = (
    ('BLR', 'Беларусь'),
    ('EU', 'Евросоюз'),
    ('USA', 'США')
)

DISABILITY_CHOICES = (
    ('N', 'НЕТ'),
    ('I', 'I группа'),
    ('II', 'II группа'),
    ('III', 'III группа')
)

DEPOSIT_CHOICES = {
    ('UD', 'До восстребования'),
    ('URG', 'Срочный')
}

R_DEPOSIT_CHOICES = {
    ('UD', 'До восстребования')
}

NON_REVOCABLE = {
    ('2', '2 месяца - 18.5%'),
    ('5', '5 месяцев - 15.5%'),
    ('7', '7 месяцев - 15%'),
    ('13', '13 месяцев - 14%'),
    ('26', '26 месцев - 13%')
}


REVOCABLE = {
    ('6', '6 месяцев - 13.5%'),
    ('18', '18 месяцев - 12%'),
}

ACTIVITY_CHOICES = {
    ('A', 'active'),
    ('P', 'passive')
}

BANK_ACCOUNT_TYPE = {
    ('PRC', 'percentages'),
    ('DEP', 'deposit'),
    ('ACT', 'active_card')
}

CURRENCY_CHOICES = {
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('BYN', 'BYN')
}

CREDIT_CHOICES = {
    ('ANN', 'annuity'),
    ('DIF', 'differentiated'),
}

CREDIT = {
    ('48', '48 месяцев - 28.9%'),
    ('60', '60 месяцев - 28.9%'),
}
import datetime
from calendar import monthrange

from django import views
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from piris.constants import NON_REVOCABLE, REVOCABLE, CREDIT
from piris.forms import CreateForm, CreateANoNRevocableContractForm, CreateARevocableContractForm, CreditContractForm
from piris.models import Person, BankPersonalContract, BankAccount, PlanOfBaseAccounts, BankCreditContract, \
    CreditAccount


class MainView(views.View):
    def get(self, request):
        person_list = Person.objects.exclude(second_name='Bank').order_by('second_name')

        return render(
            request,
            'main.html',
            context={'list': person_list}
        )


class PersonCreateView(CreateView):
    model = Person
    # fields = '__all__'
    template_name = 'create_obj.html'
    form_class = CreateForm

    def form_valid(self, form):
        self.object = Person(**form.cleaned_data)

        self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('main')


class PersonUpdateView(UpdateView):
    model = Person
    form_class = CreateForm
    template_name = 'update_obj.html'

    def get_context_data(self, **kwargs):
        context = super(PersonUpdateView, self).get_context_data(**kwargs)
        if 'form' in kwargs and kwargs['form'].errors:
            return context
        else:
            # id = context['person']
            # if BankCreditContract.objects.filter(person_id=id).first() is not None:
            #     closed_contract = BankCreditContract.objects.get(person_id=id)
            #     if closed_contract:
            #         closed_account = CreditAccount.objects.get(contract_id=closed_contract, account_type="PRC")
            #         context['credits'] = closed_account.closed
            return context

    def get_success_url(self):
        return reverse_lazy('main')


class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'delete_obj.html'

    def get_success_url(self):
        return reverse_lazy('main')


class CreateAContract(views.View):

    def get(self, request, **kwargs):
        person = Person.objects.filter(id=kwargs['id']).first()
        form = CreateANoNRevocableContractForm(initial={'second_name': person.second_name,
                                                        'first_name': person.first_name,
                                                        'father_name': person.father_name,
                                                        'date_of_birth': person.date_of_birth,
                                                        'passport_uuid': person.passport_uuid,
                                                        'contract_number': str(datetime.datetime.now().date()).replace(
                                                            '-', '') +
                                                                           str(datetime.datetime.now().time()).replace(
                                                                               ':', '').replace('.', '')
                                                        })
        return render(
            request,
            'create_contract.html',
            context={'form': form, 'person': person}
        )

    def post(self, request, id):

        person = Person.objects.filter(id=id).first()
        date_of_creating = str(datetime.date(int(request.POST['date_of_creating_year']), int(request.POST['date_of_creating_month']), int(request.POST['date_of_creating_day'])))
        date_of_ending = str(datetime.date(int(request.POST['date_of_creating_year']), int(request.POST['date_of_creating_month']), int(request.POST['date_of_creating_day'])))
        for items in NON_REVOCABLE:
            if items[0] == request.POST['period_in_months']:
                percents = items[1]

        if request.POST.get('capitalization'):
            capitalization = True
        else:
            capitalization = False

        bank_personal_contract = BankPersonalContract(person_id=person, period_in_months=request.POST['period_in_months'],
                                                      date_of_creating=date_of_creating,
                                                      date_of_ending=date_of_ending,
                                                      type=request.POST['type'],
                                                      percents=percents.replace('%', '').split(' ')[-1],
                                                      currency=str(request.POST['currency']),
                                                      capitalization=capitalization)

        bank_personal_contract.save()
        now = str(datetime.datetime.now().hour) + str(datetime.datetime.now().second)
        if datetime.datetime.now().hour <= 9:
            passport = person.passport_id[0:4]
        else:
            passport = person.passport_id[0:3]
        if request.POST['type'] == 'URG':
            base_account_deposit = PlanOfBaseAccounts.objects.get(code='3414')
            base_account_percent = PlanOfBaseAccounts.objects.get(code='3471')
            account_number_deposit = '3414' + passport + now + '03'
            account_number_percent = '3471' + passport + now + '04'
        else:
            base_account_deposit = PlanOfBaseAccounts.objects.get(code='3404')
            base_account_percent = PlanOfBaseAccounts.objects.get(code='3470')
            account_number_deposit = '3404' + passport + now + '03'
            account_number_percent = '3470' + passport + now + '04'

        bank_account_deposit = BankAccount(contract_id=bank_personal_contract,
                                           base_account_id=base_account_deposit,
                                           account_number=account_number_deposit,
                                           initial_price=request.POST['total_amount'],
                                           current_price='0',
                                           final_price ='0',
                                           income='0',
                                           account_type='DEP'
                                           )

        bank_account_percent = BankAccount(contract_id=bank_personal_contract,
                                           base_account_id=base_account_percent,
                                           account_number=account_number_percent,
                                           initial_price='0',
                                           current_price='0',
                                           final_price='0',
                                           income='0',
                                           account_type='PRC'
                                           )

        bank = BankAccount.objects.filter(base_account_id=5).first()
        c_p = float(bank.current_price) + float(request.POST['total_amount'])
        BankAccount.objects.filter(base_account_id=5).update(current_price=c_p)
        bank_account_deposit.save()
        bank_account_percent.save()

        response = redirect('/')
        return response


class CreateAContractRevoc(views.View):

    def get(self, request, **kwargs):

        person = Person.objects.filter(id=kwargs['id']).first()
        form = CreateARevocableContractForm(initial={'second_name': person.second_name,
                                                        'first_name': person.first_name,
                                                        'father_name': person.father_name,
                                                        'date_of_birth': person.date_of_birth,
                                                        'passport_uuid': person.passport_uuid,
                                                        'contract_number': str(datetime.datetime.now().date()).replace(
                                                            '-', '') + str(datetime.datetime.now().time()).replace(
                                                                               ':', '').replace('.', '')
                                                        })

        return render(
            request,
            'create_r_contract.html',
            context={'form': form, 'person': person}
        )


    def post(self, request, id):

        person = Person.objects.filter(id=id).first()
        date_of_creating = str(datetime.date(int(request.POST['date_of_creating_year']), int(request.POST['date_of_creating_month']), int(request.POST['date_of_creating_day'])))
        date_of_ending =  str(datetime.date(int(request.POST['date_of_creating_year']), int(request.POST['date_of_creating_month']), int(request.POST['date_of_creating_day'])))
        percents_r = '123'
        for items in REVOCABLE:
            if items[0] == request.POST['period_in_months']:
                percents_r = items[1].replace('%', '').split(' ')[-1]

        if request.POST.get('capitalization'):
            capitalization = True
        else:
            capitalization = False

        bank_personal_contract = BankPersonalContract(person_id=person, period_in_months=request.POST['period_in_months'],
                                                      date_of_creating=date_of_creating,
                                                      date_of_ending=date_of_ending,
                                                      type=request.POST['type'],
                                                      percents=percents_r,
                                                      currency=str(request.POST['currency']),
                                                      capitalization=capitalization)

        bank_personal_contract.save()

        base_account_deposit = PlanOfBaseAccounts.objects.get(code='3404')
        base_account_percent = PlanOfBaseAccounts.objects.get(code='3470')
        now = str(datetime.datetime.now().hour) + str(datetime.datetime.now().second)
        passport = person.passport_id[0:4]
        account_number_deposit = '3404' + passport + now + '03'
        account_number_percent = '3470' + passport + now + '04'

        bank_account_deposit = BankAccount(contract_id=bank_personal_contract,
                                           base_account_id=base_account_deposit,
                                           account_number=account_number_deposit,
                                           initial_price=request.POST['total_amount'],
                                           current_price=request.POST['total_amount'],
                                           final_price ='0',
                                           income='0',
                                           account_type='DEP'
                                           )

        bank_account_percent = BankAccount(contract_id=bank_personal_contract,
                                           base_account_id=base_account_percent,
                                           account_number=account_number_percent,
                                           initial_price='0',
                                           current_price='0',
                                           final_price='0',
                                           income='0',
                                           account_type='PRC'
                                           )
        bank = BankAccount.objects.filter(base_account_id=5).first()
        c_p = float(bank.current_price) + float(request.POST['total_amount'])
        BankAccount.objects.filter(base_account_id=5).update(current_price=c_p)
        bank_account_deposit.save()
        bank_account_percent.save()


        response = redirect('/')
        return response


class FinishingBankDay(views.View):

    def get(self, request):

        accounts = BankAccount.objects.filter(account_type='DEP')
        for account in accounts:
            if account.contract_id.capitalization:
                if account.contract_id.period_in_months > 0:
                    delta = BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').first()
                    p = float(account.initial_price)
                    pr = float(account.contract_id.percents)
                    if float(delta.current_price) == 0:
                        price = p
                    else:
                        price = p + float(delta.current_price)
                    day = monthrange(account.contract_id.date_of_creating.year, account.contract_id.date_of_ending.month)[1]
                    s = (price * pr * day) / (100 * 365)

                    if account.contract_id.type == "UD":
                        bank = BankAccount.objects.filter(base_account_id=5).first()
                        current_price = float(bank.current_price) - s
                        BankAccount.objects.filter(base_account_id=5).update(current_price=current_price)
                        percents = BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').first()
                        if float(percents.income) == 0:
                            income = s
                        else:
                            income = s + float(percents.income)
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC') \
                            .update(current_price=income, income=income)
                    else:
                        percents = BankAccount.objects.filter(contract_id=account.contract_id,
                                                              account_type='PRC').first()
                        if float(percents.current_price) == 0:
                            income = s
                        else:
                            income = s + float(percents.current_price)
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC') \
                            .update(current_price=income)

                    m = str(int(account.contract_id.period_in_months))
                    if int(account.contract_id.period_in_months) > 0:
                        m = str(int(account.contract_id.period_in_months) - 1)

                    if account.contract_id.date_of_ending.month == 12:
                        ending_date = 1
                        ending_year = account.contract_id.date_of_ending.year + 1
                    else:
                        ending_date = account.contract_id.date_of_ending.month + 1
                        ending_year = account.contract_id.date_of_ending.year
                    final_date = str(datetime.date(int(ending_year), int(ending_date),
                                                   int(account.contract_id.date_of_ending.day)))
                    if int(m) == 0:
                        income = BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').first()
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='DEP') \
                            .update(income=account.initial_price, current_price=F('initial_price'))
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC') \
                            .update(income=income.current_price)
                        BankPersonalContract.objects.filter(contract=account).update(period_in_months=0,
                                                                                     date_of_ending=final_date)
                        if account.contract_id.type == "UD":

                            acc = BankAccount.objects.filter(base_account_id=5).first()
                            c_p = float(acc.current_price) - float(account.initial_price) - float(income.current_price)
                            BankAccount.objects.filter(base_account_id=5).update(
                                current_price=c_p)
                        else:
                            acc = BankAccount.objects.filter(base_account_id=5).first()
                            c_p = float(acc.current_price) - float(account.initial_price)
                            BankAccount.objects.filter(base_account_id=5).update(
                                current_price=c_p)
                        # BankAccount.objects.get(contract_id=account.contract_id, account_type='').update()
                    else:
                        BankPersonalContract.objects.filter(contract=account).update(period_in_months=m, date_of_ending=final_date)

            else:
                if account.contract_id.period_in_months > 0:
                    p = float(account.initial_price)
                    pr = float(account.contract_id.percents)
                    # total = 0
                    # m = account.contract_id.date_of_creating.month
                    # for i in range(0, account.contract_id.period_in_months):
                    #     day = monthrange(account.contract_id.date_of_creating.year,
                    #                      m + i)[1]
                    #     total += day
                    day = monthrange(account.contract_id.date_of_creating.year,
                                     account.contract_id.date_of_ending.month)[1]
                    s = (p * pr * day) / (100 * 365)

                    # BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC')\
                    #     .update(current_price=s)

                    if account.contract_id.type == "UD":
                        bank = BankAccount.objects.filter(base_account_id=5).first()
                        current_price = float(bank.current_price) - s
                        BankAccount.objects.filter(base_account_id=5).update(current_price=current_price)
                        percents = BankAccount.objects.filter(contract_id=account.contract_id,
                                                              account_type='PRC').first()
                        if float(percents.income) == 0:
                            income = s
                        else:
                            income = s + float(percents.income)
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC') \
                            .update(current_price=income, income=income)
                    else:
                        percents = BankAccount.objects.filter(contract_id=account.contract_id,
                                                              account_type='PRC').first()
                        if float(percents.current_price) == 0:
                            income = s
                        else:
                            income = s + float(percents.current_price)
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC') \
                            .update(current_price=income)

                    if account.contract_id.date_of_ending.month == 12:
                        ending_date = 1
                        ending_year = account.contract_id.date_of_ending.year + 1
                    else:
                        ending_date = account.contract_id.date_of_ending.month + 1
                        ending_year = account.contract_id.date_of_ending.year
                    final_date = str(datetime.date(int(ending_year), int(ending_date),
                                                   int(account.contract_id.date_of_ending.day)))
                    m = str(int(account.contract_id.period_in_months))
                    if int(account.contract_id.period_in_months) > 0:
                        m = str(int(account.contract_id.period_in_months) - 1)
                    if int(m) == 0:
                        income = BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').first()
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='DEP') \
                            .update(income=account.initial_price, current_price=F('initial_price'))
                        BankAccount.objects.filter(contract_id=account.contract_id, account_type='PRC') \
                            .update(income=income.current_price)
                        BankPersonalContract.objects.filter(contract=account).update(period_in_months=0,
                                                                                     date_of_ending=final_date)
                        if account.contract_id.type == "UD":
                            acc = BankAccount.objects.filter(base_account_id=5).first()
                            c_p = float(acc.current_price) - float(account.initial_price) - float(income.current_price)
                            BankAccount.objects.filter(base_account_id=5).update(
                                current_price=c_p)
                        else:
                            acc = BankAccount.objects.filter(base_account_id=5).first()
                            c_p = float(acc.current_price) - float(account.initial_price)
                            BankAccount.objects.filter(base_account_id=5).update(
                                current_price=c_p)
                        # BankAccount.objects.get(contract_id=account.contract_id, account_type='').update()
                    else:
                        BankPersonalContract.objects.filter(contract=account).update(period_in_months=m,
                                                                                     date_of_ending=final_date)

        accounts_list = BankAccount.objects.all().order_by('contract_id')
        return render(
            request,
            'accounts.html',
            context={'list': accounts_list}
        )


class AccountsListView(views.View):

    def get(self, request):
        accounts_list = BankAccount.objects.all().order_by('contract_id')

        return render(
            request,
            'accounts.html',
            context={'list': accounts_list}
        )


class CreditContract(views.View):

    def get(self, request, **kwargs):

        person = Person.objects.filter(id=kwargs['id']).first()
        form = CreditContractForm(initial={'second_name': person.second_name,
                                                        'first_name': person.first_name,
                                                        'father_name': person.father_name,
                                                        'date_of_birth': person.date_of_birth,
                                                        'passport_uuid': person.passport_uuid,
                                                        'date_of_creating': datetime.date.today(),
                                                        'contract_number': str(datetime.datetime.now().date()).replace(
                                                            '-', '') + str(datetime.datetime.now().time()).replace(
                                                                               ':', '').replace('.', '')
                                                        })

        return render(
            request,
            'credit_contract.html',
            context={'form': form, 'person': person}
        )

    def post(self, request, id):

        person = Person.objects.filter(id=id).first()
        date_of_creating = str(datetime.date(int(request.POST['date_of_creating_year']), int(request.POST['date_of_creating_month']), int(request.POST['date_of_creating_day'])))
        date_of_ending = str(datetime.date(int(request.POST['date_of_creating_year']), int(request.POST['date_of_creating_month']), int(request.POST['date_of_creating_day'])))

        percents_r = '123'
        for items in CREDIT:
            if items[0] == request.POST['period_in_months']:
                percents_r = items[1].replace('%', '').split(' ')[-1]

        if request.POST['type'] == 'ANN':
            count = '0'
        else:
            count = request.POST['total_amount']

        bank_credit_contract = BankCreditContract(person_id=person, period_in_months=request.POST['period_in_months'],
                                                      date_of_creating=date_of_creating,
                                                      date_of_ending=date_of_ending,
                                                      type=request.POST['type'],
                                                      percents=percents_r,
                                                      currency=str(request.POST['currency']))

        bank_credit_contract.save()

        base_credit_deposit = PlanOfBaseAccounts.objects.get(code='2400')
        base_credit_percent = PlanOfBaseAccounts.objects.get(code='2470')
        now = str(datetime.datetime.now().hour) + str(datetime.datetime.now().second)
        passport = person.passport_id[0:4]
        account_credit_deposit = '2400' + passport + now + '03'
        account_credit_percent = '2470' + passport + now + '04'

        bank_credit_deposit = CreditAccount(contract_id=bank_credit_contract,
                                           base_account_id=base_credit_deposit,
                                           account_number=account_credit_deposit,
                                           initial_price=request.POST['total_amount'],
                                           current_price=request.POST['total_amount'],
                                           final_price ='0',
                                           income=request.POST['total_amount'],
                                           account_type='DEP'
                                           )

        bank_credit_percent = CreditAccount(contract_id=bank_credit_contract,
                                           base_account_id=base_credit_percent,
                                           account_number=account_credit_percent,
                                           initial_price=request.POST['total_amount'],
                                           current_price=count,
                                           final_price='0',
                                           income='0',
                                           account_type='PRC'
                                           )
        bank = CreditAccount.objects.filter(base_account_id=5).first()
        c_p = float(bank.current_price) - float(request.POST['total_amount'])
        CreditAccount.objects.filter(base_account_id=5).update(current_price=c_p)
        bank_credit_deposit.save()
        bank_credit_percent.save()

        response = redirect('/')
        return response


class CreditListView(views.View):

    def get(self, request):
        accounts_list = CreditAccount.objects.all().order_by('contract_id')

        return render(
            request,
            'credits.html',
            context={'list': accounts_list}
        )


class FinishingCreditBankDay(views.View):
    def get(self, request, **kwargs):
        bank = CreditAccount.objects.filter(account_type='BANk').get()
        accounts = CreditAccount.objects.filter(account_type='DEP')
        for account in accounts:
            if (account.contract_id.date_of_ending - account.contract_id.date_of_creating).days < (account.contract_id.period_in_months*30):
                if account.contract_id.type == "DIF":
                    credit_body = float(account.initial_price) / float(account.contract_id.period_in_months)
                    day = monthrange(account.contract_id.date_of_creating.year,
                                     account.contract_id.date_of_ending.month)[1]
                    percent = CreditAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').get()
                    monthly_payment = (float(percent.current_price) - credit_body) * float(account.contract_id
                                                                                           .percents) * day / (100 * 365)
                    percent = CreditAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').get()
                    percent.payments.append(monthly_payment)
                    percent_current_price = float(percent.current_price) - credit_body
                    percent.income = monthly_payment
                    percent.current_price = str(percent_current_price)
                    percent.save()
                    if account.contract_id.date_of_ending.month == 12:
                        ending_date = 1
                        ending_year = account.contract_id.date_of_ending.year + 1
                    else:
                        ending_date = account.contract_id.date_of_ending.month + 1
                        ending_year = account.contract_id.date_of_ending.year
                    account_ending_date = datetime.date(int(ending_year), int(ending_date),
                                                   int(account.contract_id.date_of_ending.day))
                    account.contract_id.date_of_ending = account_ending_date
                    account.contract_id.save()
                    bank_price = float(bank.current_price) + monthly_payment
                    bank.current_price = bank_price
                    bank.save()
                else:
                    i = float(account.contract_id.percents) / 12 / 100
                    credit_coefficient = (i * (1 + i)**int(account.contract_id.period_in_months)) / ((1 + i)**(int(account.contract_id.period_in_months) - 1))
                    monthly_payment = float(account.initial_price) * credit_coefficient

                    percent = CreditAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').get()
                    percent.payments.append(monthly_payment)
                    percent_current_price = float(percent.current_price) + monthly_payment
                    percent.income = monthly_payment
                    percent.current_price = str(percent_current_price)
                    percent.save()
                    if account.contract_id.date_of_ending.month == 12:
                        ending_date = 1
                        ending_year = account.contract_id.date_of_ending.year + 1
                    else:
                        ending_date = account.contract_id.date_of_ending.month + 1
                        ending_year = account.contract_id.date_of_ending.year
                    account_ending_date = datetime.date(int(ending_year), int(ending_date),
                                                        int(account.contract_id.date_of_ending.day))
                    account.contract_id.date_of_ending = account_ending_date
                    account.contract_id.save()
                    bank_price = float(bank.current_price) + monthly_payment
                    bank.current_price = bank_price
                    bank.save()
            else:
                if account.closed == True:
                    percent = CreditAccount.objects.filter(contract_id=account.contract_id, account_type='PRC').get()
                    percent.income = "0"
                    if account.contract_id.type == "DIF":
                        current = float(percent.initial_price) + float(percent.current_price)
                        percent.current_price = str(current)

                    account.closed = False
                    account.save()
                    percent.save()

        accounts_list = CreditAccount.objects.all().order_by('contract_id')
        print(accounts_list)
        return render(
            request,
            'credits.html',
            context={'list': accounts_list}
        )
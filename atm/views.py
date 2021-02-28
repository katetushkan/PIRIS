from datetime import datetime

import firebase_admin
from django import views
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from firebase_admin import credentials, db

from atm.models import CreditCard
from atm.utils import create_check
from piris.models import CreditAccount


class MainATMView(views.View):
    def get(self, request):

        context = {'header': 'Hello! To Continue Your operation enter a credit card!',
                   'field': "Number",
                   'message': "Card's number should has 16 digits"}
        return render(
            request,
            'atm.html',
            context
        )

    def post(self, request, **kwargs):

        param = request.POST['value']
        param = param.replace(' ', '')
        if len(param) > 4:
            try:
                CreditCard.objects.filter(card_number=param).get()
                context = {'header': 'Enter a pin: ',
                           'field': "PIN",
                           'message': "PIN should has 4 digits",
                           'card': param}
            except Exception:
                context = {'header': 'There is no such card, try again!',
                           'field': "Number",
                           'message': "Card's number should has 16 digits"}
        elif len(param) == 4:
            try:
                account = CreditCard.objects.filter(card_number=request.POST['card'], pin=param).get()
                if account.pin == param:
                    return render(
                        request,
                        'actions.html',
                        context={'card': request.POST['card']}
                    )
                else:
                    context = {'header': 'PIN is wrong! Try again',
                               'field': "pin",
                               'message': "PIN should has 4 digits",
                               'card': request.POST['card']}
            except Exception:
                context = {'header': 'PIN is wrong! Try again',
                           'field': "pin",
                           'message': "PIN should has 4 digits",
                           'card': request.POST['card']}


        return render(
            request,
            'atm.html',
            context
        )


class ActionsView(views.View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):

        return render(
            request,
            'actions.html'
        )

    def post(self, request):
        action = request.POST['action'].split('_')[0]

        try:
            if_check = request.POST['action'].split('_')[1]
        except Exception:
            if_check = False

        if action == 'card':
            return redirect('atm')

        if action == 'balance':

            account_card = CreditCard.objects.filter(card_number=request.POST['card']).get()
            account = CreditAccount.objects.filter(id=account_card.account_id.id).get()
            header = 'The current balance is: ' + account.income
            context = {'card': request.POST['card'], 'header': header}
            if if_check:
                create_check(datetime.now(), 0, account.income, request.POST['card'], "balance")

            return render(
                request,
                'balance.html',
                context
            )
        elif action == 'cash':
            context = {'card': request.POST['card']}

            return render(
                request,
                'cash.html',
                context
            )

        elif action == 'confirm':
            price = request.POST['value']
            account_card = CreditCard.objects.filter(card_number=request.POST['card']).get()
            account = CreditAccount.objects.filter(id=account_card.account_id.id).get()
            if float(account.income) >= int(price):
                new_price = float(account.income) - int(price)
                account.income = new_price
                account.save()
                if if_check:
                   create_check(datetime.now(), price, new_price, request.POST['card'], "cash")
                context = {'card': request.POST['card']}
                return render(
                    request,
                    'actions.html',
                    context
                )
            else:
                message = "There is not enough money"
                context = {'card': request.POST['card'], 'message': message}
                return render(
                    request,
                    'cash.html',
                    context
                )

            context = {'card': request.POST['card']}

            return render(
                request,
                'cash.html',
                context
            )

        elif action == "phone":
            try:
                price = request.POST['value']
                card_number = request.POST['card']
                account_card = CreditCard.objects.filter(card_number=card_number).get()
                account = CreditAccount.objects.filter(id=account_card.account_id.id).get()
                if float(account.income) >= int(price):
                    new_price = float(account.income) - int(price)
                    account.income = new_price
                    account.save()
                    grandma_gift = f'U get {price}byn from ur grandma.'
                    message_ref = db.reference('/message')
                    message_ref.set({
                        'header': 'Incoming payment',
                        'body': grandma_gift
                    })


                    context = {'card': request.POST['card']}
                    return render(
                        request,
                        'actions.html',
                        context
                    )
                else:
                    message = "There is not enough money"
                    context = {'card': request.POST['card'], 'message': message, 'number':request.POST['number']}
                    return render(
                        request,
                        'phone_payment.html',
                        context
                    )
            except Exception:
                context = {'card': request.POST['card']}

                return render(
                    request,
                    'phone_payment.html',
                    context
                )

        return render(
            request,
            'actions.html',
            context={'card': request.POST['card']}
        )
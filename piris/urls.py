from django.urls import path

from piris import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('task/create', views.PersonCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/edit', views.PersonUpdateView.as_view(), name='update_task'),
    path('task/<int:pk>/delete', views.PersonDeleteView.as_view(), name='delete_task'),
    path('task/contract/<int:id>', views.CreateAContract.as_view(), name='contract'),
    path('task/contract_r/<int:id>', views.CreateAContractRevoc.as_view(), name='contract_r'),
    path('task/credit/<int:id>', views.CreditContract.as_view(), name='credit'),
    path('task/finish_bank_day', views.FinishingBankDay.as_view(), name='bank_day'),
    path('task/finish_credit_bank_day', views.FinishingCreditBankDay.as_view(), name='credit_bank_day'),
    path('task/accounts', views.AccountsListView.as_view(), name='accounts'),
    path('task/credits', views.CreditListView.as_view(), name='credits'),

]
from django.urls import path

from atm import views

urlpatterns = [
    path('', views.MainATMView.as_view(), name='atm'),
    path('actions', views.ActionsView.as_view(), name='actions')
]


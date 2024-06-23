from django.urls import path

from licenceapp.views import AddLicenceKeyView

urlpatterns = [
path('add_licence_key/', AddLicenceKeyView.as_view(), name='add_licence_key'),
]

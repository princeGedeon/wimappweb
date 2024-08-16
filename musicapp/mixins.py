from rest_framework import serializers
from licenceapp.models import Licence, Classe, Niveau

class LicenceFilterMixin:
    def filter_by_licence(self, queryset, licence_value):
        try:
            licence = Licence.objects.get(valeur=licence_value, is_active=True)
        except Licence.DoesNotExist:
            raise serializers.ValidationError("Licence not found or inactive")

        # Filter queryset based on licence's classe and niveau
        if hasattr(queryset.model, 'classe') and licence.classe:
            queryset = queryset.filter(classe__nom=licence.classe.nom)
        if hasattr(queryset.model, 'niveau') and licence.niveau:
            queryset = queryset.filter(niveau__nom=licence.niveau.nom)

        return queryset

class LicenceValidationMixin:
    def validate_licence(self, user, licence_value):
        try:
            licence = Licence.objects.get(valeur=licence_value, is_active=True)
        except Licence.DoesNotExist:
            raise serializers.ValidationError("Licence not found or inactive")

        if licence.user != user:
            raise serializers.ValidationError("This licence does not belong to you. Please add it to your profile first.")

        return licence

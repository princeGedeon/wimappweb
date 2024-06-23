
from rest_framework import serializers
from licenceapp.models import Licence
from django.utils import timezone

class AddLicenceSerializer(serializers.Serializer):
    licence_valeur = serializers.CharField()

    def validate(self, data):
        licence_valeur = data.get('licence_valeur')
        try:
            licence = Licence.objects.get(valeur=licence_valeur)
        except Licence.DoesNotExist:
            raise serializers.ValidationError("Licence non trouvée.")

        if licence.user is not None:
            raise serializers.ValidationError("Licence déjà utilisée.")

        if not licence.is_active or licence.date_exp < timezone.now().date():
            raise serializers.ValidationError("Licence inactive ou expirée.")

        data['licence'] = licence
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        licence = self.validated_data['licence']

        if hasattr(user, 'licence') and user.licence is not None:
            raise serializers.ValidationError("L'utilisateur possède déjà une licence.")

        licence.user = user
        licence.save()
        return licence
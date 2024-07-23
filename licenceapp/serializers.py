
from rest_framework import serializers
from licenceapp.models import Licence
from django.utils import timezone

from rest_framework import serializers

class UploadLicencesSerializer(serializers.Serializer):
    source_id = serializers.IntegerField()
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError('Invalid file format. Please upload an Excel file.')
        return value


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = '__all__'

class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = ['id', 'date_exp', 'valeur', 'is_active', 'classe', 'niveau', 'type', 'source']
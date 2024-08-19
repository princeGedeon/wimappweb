from licenceapp.models import Licence, Classe, Niveau, Matiere
from rest_framework import serializers

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'image', 'color']




class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = '__all__'

class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = '__all__'

class UploadLicencesSerializer(serializers.Serializer):
    source_id = serializers.IntegerField()
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError('Invalid file format. Please upload an Excel file.')
        return value


class LicenceSerializer(serializers.ModelSerializer):
    classe_name = serializers.CharField(write_only=True, required=False)
    niveau_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Licence
        fields = ['id', 'date_exp', 'valeur', 'is_active', 'classe_name', 'niveau_name', 'type', 'source', 'createdAt', 'updatedAt']

    def create(self, validated_data):
        classe_name = validated_data.pop('classe_name', None)
        niveau_name = validated_data.pop('niveau_name', None)

        if classe_name:
            classe, _ = Classe.objects.get_or_create(nom=classe_name)
        else:
            classe = None

        if niveau_name:
            niveau, _ = Niveau.objects.get_or_create(nom=niveau_name)
        else:
            niveau = None

        licence = Licence.objects.create(classe=classe, niveau=niveau, **validated_data)
        return licence


    def update(self, instance, validated_data):
        classe_name = validated_data.pop('classe_name', None)
        niveau_name = validated_data.pop('niveau_name', None)
        if classe_name:
            classe, _ = Classe.objects.get_or_create(nom=classe_name)
            instance.classe = classe
        else:
            instance.classe = None
        if niveau_name:
            niveau, _ = Niveau.objects.get_or_create(nom=niveau_name)
            instance.niveau = niveau
        else:
            instance.niveau = None
        # Mise à jour des autres champs de l'instance
        instance.date_exp = validated_data.get('date_exp', instance.date_exp)
        instance.valeur = validated_data.get('valeur', instance.valeur)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.type = validated_data.get('type', instance.type)
        instance.source = validated_data.get('source', instance.source)
        instance.save()
        return instance

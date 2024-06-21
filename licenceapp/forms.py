# forms.py

from django import forms
from .models import Licence, Classe, Niveau, Source
import uuid

class BulkLicenceForm(forms.Form):
    source = forms.ModelChoiceField(queryset=Source.objects.all(), label="Source")
    date_exp = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Expiration Date")
    classes = forms.ModelMultipleChoiceField(queryset=Classe.objects.all(), widget=forms.CheckboxSelectMultiple, label="Classes")
    niveaux = forms.ModelMultipleChoiceField(queryset=Niveau.objects.all(), widget=forms.CheckboxSelectMultiple, label="Niveaux")
    number_of_licences = forms.IntegerField(min_value=1, max_value=100, label="Number of Licences")

    def save(self):
        licences = []
        source = self.cleaned_data['source']
        date_exp = self.cleaned_data['date_exp']
        classes = self.cleaned_data['classes']
        niveaux = self.cleaned_data['niveaux']
        number_of_licences = self.cleaned_data['number_of_licences']

        for _ in range(number_of_licences):
            licence = Licence.objects.create(
                source=source,
                date_exp=date_exp,
                valeur=uuid.uuid4().hex,
                is_active=True
            )
            licence.classes.set(classes)
            licence.niveaux.set(niveaux)
            licences.append(licence)

        return licences

#-*- coding:utf-8 -*-

from django import forms

from macro.models import Laminas
#from mechg.choices import choices_none             SERA USADO NOS GRAFICOS, NAO NECESSARIO POR ENQUANTO
from macro.choices import default_choices_disp
from macro.prop import PROP_DISP

class FormLaminas(forms.ModelForm):
    select = forms.IntegerField(widget=forms.Select(choices=default_choices_disp()), required=False)
    
    class Meta:
        model = Laminas
        fields = ['select'] + PROP_DISP
        localized_fields = '__all__'

#########################################################################################
#########################  Migração mais focada 	#########################
########################################################################################
####          Fev 13, 2016 , para simplicar o desenvolvimento

from macro.models import Varredura

class FormVarredura(forms.ModelForm):
    select = forms.IntegerField(widget=forms.Select(choices=default_choices_disp()), required=False)
    
    class Meta:
        model = Laminas
####          Fev 14, 2016 , não é preciso ver os valores dos campos.
#        fields = ['E1','E2','G12','NU12']
        fields = []
        localized_fields = '__all__'

#########################################################################################
#########################  Testes 	#########################
########################################################################################
####          Agosto 13, 2016 , passamos um arquivo para gerar um teste


class DocumentForm(forms.Form):
######Para select lamina
    select = forms.IntegerField(widget=forms.Select(choices=default_choices_disp()), required=False)

    class Meta:
        model = Laminas
        fields = []
        localized_fields = '__all__'
##Para upload:
    docfile = forms.FileField(
        label='Indique um arquivo de Teste'
    )

## Outubro 2016, para controle das versões
#########################  Testes 	#########################
class versoe_sArquivos(forms.Form):
######Para select lamina
    select = forms.IntegerField(widget=forms.Select(choices=default_choices_disp()), required=False)

    class Meta:
        model = Laminas
        fields = []
        localized_fields = '__all__'
##Para upload: 
    docfile1 = forms.FileField(
        label='Indique um arquivo de Teste'
    )



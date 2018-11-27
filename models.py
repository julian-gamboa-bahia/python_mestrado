#-*- coding:utf-8 -*-

#Base do banco de dados do módulo macro
from django.db import models
from django.contrib.auth.models import User

from macro.prop import PROPRIEDADES
from micro.models import validate_not_neg_zero, validate_not_negative

class Laminas4(models.Model):
    #Propriedades Basicas
    NOME = models.CharField(verbose_name=PROPRIEDADES['NOME']['NOME_HTML'], max_length=100)
    DENSIDADE = models.FloatField(verbose_name=PROPRIEDADES['DENSIDADE']['NOME_HTML'], validators=[validate_not_neg_zero])
    #Constantes
    E1 = models.FloatField(verbose_name = PROPRIEDADES['E1']['NOME_HTML'], help_text = PROPRIEDADES['E1']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    E2 = models.FloatField(verbose_name = PROPRIEDADES['E2']['NOME_HTML'], help_text = PROPRIEDADES['E2']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    E3 = models.FloatField(verbose_name = PROPRIEDADES['E3']['NOME_HTML'], help_text = PROPRIEDADES['E3']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    G12 = models.FloatField(verbose_name = PROPRIEDADES['G12']['NOME_HTML'], help_text = PROPRIEDADES['G12']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    G13 = models.FloatField(verbose_name = PROPRIEDADES['G13']['NOME_HTML'], help_text = PROPRIEDADES['G13']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    G23 = models.FloatField(verbose_name = PROPRIEDADES['G23']['NOME_HTML'], help_text = PROPRIEDADES['G23']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    NU12 = models.FloatField(verbose_name = PROPRIEDADES['NU12']['NOME_HTML'], help_text = PROPRIEDADES['NU12']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    NU13 = models.FloatField(verbose_name = PROPRIEDADES['NU13']['NOME_HTML'], help_text = PROPRIEDADES['NU13']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    NU23 = models.FloatField(verbose_name = PROPRIEDADES['NU23']['NOME_HTML'], help_text = PROPRIEDADES['NU23']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    #Resistencias
    SIGMA_T_1 = models.FloatField(verbose_name=PROPRIEDADES['SIGMA_T_1']['NOME_HTML'], help_text=PROPRIEDADES['SIGMA_T_1']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    SIGMA_T_2 = models.FloatField(verbose_name=PROPRIEDADES['SIGMA_T_2']['NOME_HTML'], help_text=PROPRIEDADES['SIGMA_T_2']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    SIGMA_C_1 = models.FloatField(verbose_name=PROPRIEDADES['SIGMA_C_1']['NOME_HTML'], help_text=PROPRIEDADES['SIGMA_C_1']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative]) 
    SIGMA_C_2 = models.FloatField(verbose_name=PROPRIEDADES['SIGMA_C_2']['NOME_HTML'], help_text=PROPRIEDADES['SIGMA_C_2']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])  
    TAU12 = models.FloatField(verbose_name= PROPRIEDADES['TAU12']['NOME_HTML'], help_text=PROPRIEDADES['TAU12']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative]) 
    TAU13 = models.FloatField(verbose_name= PROPRIEDADES['TAU13']['NOME_HTML'], help_text=PROPRIEDADES['TAU13']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    TAU23 = models.FloatField(verbose_name= PROPRIEDADES['TAU23']['NOME_HTML'], help_text=PROPRIEDADES['TAU23']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    #Deformacoes
    EPSILON_T_1 = models.FloatField(verbose_name=PROPRIEDADES['EPSILON_T_1']['NOME_HTML'], help_text=PROPRIEDADES['EPSILON_T_1']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])  
    EPSILON_T_2 = models.FloatField(verbose_name=PROPRIEDADES['EPSILON_T_2']['NOME_HTML'], help_text=PROPRIEDADES['EPSILON_T_2']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])  
    EPSILON_C_1 = models.FloatField(verbose_name=PROPRIEDADES['EPSILON_C_1']['NOME_HTML'], help_text=PROPRIEDADES['EPSILON_C_1']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])  
    EPSILON_C_2 = models.FloatField(verbose_name=PROPRIEDADES['EPSILON_C_2']['NOME_HTML'], help_text=PROPRIEDADES['EPSILON_C_2']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])  
    GAMMA12 = models.FloatField(verbose_name=PROPRIEDADES['GAMMA12']['NOME_HTML'], help_text=PROPRIEDADES['GAMMA12']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    #Fisicas
    ALPHA1  = models.FloatField(verbose_name=PROPRIEDADES['ALPHA1']['NOME_HTML'], help_text=PROPRIEDADES['ALPHA1']['TOOLTIP'], null=True, blank=True)
    ALPHA2  = models.FloatField(verbose_name=PROPRIEDADES['ALPHA2']['NOME_HTML'], help_text=PROPRIEDADES['ALPHA2']['TOOLTIP'], null=True, blank=True)
    ALPHA3 = models.FloatField(verbose_name=PROPRIEDADES['ALPHA3']['NOME_HTML'], help_text=PROPRIEDADES['ALPHA3']['TOOLTIP'], null=True, blank=True)
    BETA1  = models.FloatField(verbose_name=PROPRIEDADES['BETA1']['NOME_HTML'], help_text=PROPRIEDADES['BETA1']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    BETA2  = models.FloatField(verbose_name=PROPRIEDADES['BETA2']['NOME_HTML'], help_text=PROPRIEDADES['BETA2']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    BETA3 = models.FloatField(verbose_name=PROPRIEDADES['BETA3']['NOME_HTML'], help_text=PROPRIEDADES['BETA3']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    C   = models.FloatField(verbose_name=PROPRIEDADES['C']['NOME_HTML'], help_text=PROPRIEDADES['C']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    K1  = models.FloatField(verbose_name=PROPRIEDADES['K1']['NOME_HTML'], help_text=PROPRIEDADES['K1']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    K2  = models.FloatField(verbose_name=PROPRIEDADES['K2']['NOME_HTML'], help_text=PROPRIEDADES['K2']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    K3  = models.FloatField(verbose_name=PROPRIEDADES['K3']['NOME_HTML'], help_text=PROPRIEDADES['K3']['TOOLTIP'], null=True, blank=True, validators=[validate_not_negative])
    
    user = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % (self.NOME)


#########################################################################################

######################### Área do programador	#########################
########################################################################################

class Document(models.Model):
    docfile = models.FileField(upload_to='areaProgramador/testeEsforcos/') #Pasamos ara um endereço melhor



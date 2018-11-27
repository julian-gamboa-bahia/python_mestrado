# coding: utf-8

### Agosto 21, 2018
import math
import numpy as np
from math import pi, sqrt, cos, sin, pow
import sys, traceback
import math as math

from django.shortcuts import render

#########################################################################################
# Agosto 21, 2018 
#
# Códificação em Python, considerar:
# 1) Quando for invocado o JS do critérios (neste caso: "criterios_maxima_tensao.js" ) ele deve processar informações que FORAM coletadas pelo gestor URL
# 2) Mas o gestor URL passa as informações ao VIEW 
# 3) e desde lá passa as informações para este AMBIENTE, com ajuda da FUNCAO coletando_informacaos_view 
#########################################################################################	

# Agosto 21, 2018 , função de uso comum para todos os critérios e ENVELOPES, 
# dado que permite coletar as informações que foram colocadas pela linha de comando

def coletando_informacaos_view(nome_criterioVIEW,anguloVIEW,materialVIEW,livreVIEW,sigma_xVIEW,sigma_yVIEW,tau_xyVIEW,livre_2VIEW):


	global nome_criterio
	global angulo
	global material
	global livre
	global sigma_x
	global sigma_y
	global tau_xy
	global livre_2
	# agora colocando os valores
	nome_criterio=nome_criterioVIEW
	angulo=anguloVIEW
	material=materialVIEW
	livre=livreVIEW
	sigma_x=sigma_xVIEW
	sigma_y=sigma_yVIEW
	tau_xy=tau_xyVIEW
	livre_2=livre_2VIEW

def passando_materiais(materiaisVIEW):
	global materiais
	materiais=materiaisVIEW

def passando_historico(historicoVIEW,materiais_historicosVIEW,esforcos_historicosVIEW,angulo_historicoVIEW):
	global historico
	historico=historicoVIEW
	global materiais_historicos
	materiais_historicos=materiais_historicosVIEW
	global esforcos_historicos
	esforcos_historicos=esforcos_historicosVIEW
	global angulo_historico
	angulo_historico=angulo_historicoVIEW

def historicos_e_lista_materiais(request):
	c = {
	 'angulo': angulo,
	'material':material,
	'livre':livre,
	'sigma_x':sigma_x,
	'sigma_y':sigma_y,
	'tau_xy':tau_xy,	
	'livre_2':livre_2,  
	'materiais':materiais,
	'historico':historico,
	'materiais_historicos':materiais_historicos,	
	'esforcos_historicos':esforcos_historicos,
	'angulo_historico':angulo_historico,
	}	


	arquivo_js='historicos_e_lista_materiais.js'
	return render(request, arquivo_js,c)			
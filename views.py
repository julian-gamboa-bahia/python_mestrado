
#coding: utf-8
# detalhes:
#
#	simplificando ao Máximo, para tentar organizar tudo.
# usamos a mesma arquitetura para poder criar cada novo modulo (numa pasta).
#
#
#

from django.shortcuts import render
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from HTMLParser import HTMLParser as hp
from bs4 import BeautifulSoup as bs
import json
import math
import string

# Julho 30, este modelo de Laminas e FormLaminas será importando de "macro"

from macro.models import Laminas
from macro.forms import FormLaminas

from micro.forms import FormMicro
from micro.models import FaseDispersa

from calculos import comp_math as cm
from auxiliares import funcoes_auxiliares as aux

from macro.prop import *
import macro.nomes_html
from macro.nomes_html import *

from micro.nomes_html import NOME_DISP as NOME_DISP_MICRO

from macro.calc import CalcPropriedades2D, Calc_Criterios_De_Falha,\
    CalcPropriedades3D


#from calculos import  TemporalFev11julian as fj
#from calculos import  TemporalFev17julian as envelopes

################

import os as os
import subprocess # para ler os arquivos programados


import csv
import sys
import math
import numpy as np
from numpy import matrix
from numpy import linalg
import matplotlib.pyplot as plt
from numpy import random


def js(request):
    return render_pagina(request, 'envelopesDidaticos/js/js.js')
def js_dialog(request):
    return render_pagina(request, 'envelopesDidaticos/js/js_dialog.js')


#########################################################################################
######################   Ajuda 				########################
#########################################################################################

#volta
def SaidasAjudaEnvelope(request,criterioHTML):
	criterioHTML=int(criterioHTML)

	# Agosto 05, lemos cada código MATLAB e colocamos ele como saída.

	module_dir = os.path.dirname(__file__)  # get current directory


# na pasta matlabFontes, metemos todos os arquivos de MATLAB 

	module_dir=module_dir+'/ajudasCriterios/'

	if criterioHTML == 0: #max_tensao
		file_path = os.path.join(module_dir, 'maxima_tensao.html')# = macro_max_tensao(request)
	elif criterioHTML == 1: #max_deformacao
		file_path = os.path.join(module_dir, 'maxima_deformacao.html')# = macro_max_deformacao(request)
	elif criterioHTML == 2: #tsai-hill
		file_path = os.path.join(module_dir, 'tsai_hill.html')# = macro_tsai_hill(request)
	elif criterioHTML == 3: #azzi-tsai
		file_path = os.path.join(module_dir, 'azzi_tsai.html')# = macro_azzi_tsai(request)
	elif criterioHTML == 4: #tsai-wu
		file_path = os.path.join(module_dir, 'tsai_wu.html')# = macro_tsai_wu(request)
	elif criterioHTML == 5: #hoffman
		file_path = os.path.join(module_dir, 'Hoffman.html')# = macro_hoffman(request)
	elif criterioHTML == 6: #hashin
		file_path = os.path.join(module_dir, 'hashin.html')# = macro_hashin(request)
	elif criterioHTML == 7: #christensen
		file_path = os.path.join(module_dir, 'cristensen.html')# = macro_christensen(request)
	elif criterioHTML == 8: #puck
		file_path = os.path.join(module_dir, 'puck.html')# = macro_puck(request)
	elif criterioHTML == 9: #
		file_path = os.path.join(module_dir, 'larc03.html')

#<meta http-equiv="content-type" content="text/html"></head><body></body></html>
#	response = HttpResponse(content_type='text/text')
#	response = HttpResponse(content_type='text/html ; charset=UTF-8')
	response = HttpResponse()
	fonteAjuda=open(file_path,"r")
	for line in fonteAjuda:
		response.write(str(line))
	fonteAjuda.close()

	return response


# pegamos o FORMULARIO,
# do qual precisamos o SELECT

	form = DocumentForm()  

#	return HttpResponseRedirect( '/areaProgramadorAgosto/carregando_arquivo_teste_passo_2/%d/%f/%d/' % (lamina,angulo,criterio))
#	'areaProgramadorAgosto/list.html',



	c = {
		'form': form,
	}

	return render(request,'areaProgramadorAgosto/gerarArquivoTeste.htm',c)



#########################################################################################
# Agosto 20, 2018 
#
# melhora: é preciso colocar um "/"
# http://127.0.0.1:8000/criterios_envelopes_julian/entradas/iframe_entradas_html
# Com o intuito de facilitar o comportamento do gestor de URL
# E ao parecer será preciso tirar o estilo AJAX "?" (https://stackoverflow.com/questions/5500472/how-do-i-match-the-question-mark-character-in-a-django-url)
# E trocar o carater ? pelo !
#
#
#########################################################################################	@login_required

def criterios_tsai_wu(request,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2,parametro_wu):

	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(material)):
		SIGMA_T_1=p.SIGMA_T_1
		SIGMA_T_2=p.SIGMA_T_2
		SIGMA_C_1=-p.SIGMA_C_1  # Convenio de sinais
		SIGMA_C_2=-p.SIGMA_C_2  # Convenio de sinais
		NOME=p.NOME

		EPSILON_T_1=p.EPSILON_T_1
		EPSILON_T_2=p.EPSILON_T_2
		EPSILON_C_1=-p.EPSILON_C_1  # Convenio de sinais
		EPSILON_C_2=-p.EPSILON_C_2  # Convenio de sinais

		# cisalhantes:

		GAMMA12=p.GAMMA12
		TAU12=p.TAU12

	c = {
	'nome_criterioGLOBAL':"tsai_wu.htm",
	 'angulo': angulo,
	'material':material,
	'livre':livre,
	'sigma_x':sigma_x,
	'sigma_y':sigma_y,
	'tau_xy':tau_xy,	
	'livre_2':livre_2,  
# até aqui os argumentos de entrada da função. 
# Agora as propriedades do material para TESTE inicial
	'nome':NOME,
	'SIGMA_T_1':SIGMA_T_1,#var ="{{SIGMA_T_1}}";//        SIGMA_T_1=dados[laminaURL_numerico].SIGMA_T_1;
	'SIGMA_T_2':SIGMA_T_2,#var ="{{SIGMA_T_2}}";//        SIGMA_T_2=dados[laminaURL_numerico].SIGMA_T_2;
	'SIGMA_C_1':SIGMA_C_1,#var ="{{SIGMA_C_1}}";//        SIGMA_C_1=dados[laminaURL_numerico].SIGMA_C_1;
	'SIGMA_C_2':SIGMA_C_2,#var ="{{SIGMA_C_2}}";//        SIGMA_C_2=dados[laminaURL_numerico].SIGMA_C_2;
	'TAU12':TAU12,#var ="{{TAU12}}";//        TAU12=dados[laminaURL_numerico].TAU12;
	'EPSILON_T_1':EPSILON_T_1,#var ="{{EPSILON_T_1}}";//        EPSILON_T_1=dados[laminaURL_numerico].EPSILON_T_1;
	'EPSILON_T_2':EPSILON_T_2,#var ="{{EPSILON_T_2}}";//        EPSILON_T_2=dados[laminaURL_numerico].EPSILON_T_2;
	'EPSILON_C_1':EPSILON_C_1,#var ="{{EPSILON_C_1}}";//        EPSILON_C_1=dados[laminaURL_numerico].EPSILON_C_1;
	'EPSILON_C_2':EPSILON_C_2,#var ="{{EPSILON_C_2}}";//        EPSILON_C_2=dados[laminaURL_numerico].EPSILON_C_2;
	'GAMMA12':GAMMA12,
	'parametro_wu':parametro_wu,
	 }

	#indicamos uma lista de materiais Cadastrados

	materiais=[]
	for p in Laminas.objects.raw('SELECT * FROM macro_laminas'):
		materiais.append(p.NOME)	

	#colocamos um histórico de cálculos prévios

	historico("tsai_wu.htm",angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)		

	criterio_tsai_wu.coletando_informacaos_view("tsai_wu.htm",angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
	criterio_tsai_wu.passando_materiais(materiais)
	criterio_tsai_wu.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)	


	return render(request,'iframe/criterios/tsai_wu.htm',c)		


#Setembro27

evolucao_migracao=" Operações de Engenahria Reversa registradas para o dia Quinta-feira 27 de Setembro 2018"

#Outubro 07

evolucao_migracao="Sábado 07 de Outubro 2018,  Operações de Engenahria Reversa registradas para o dia"

#Domingo 15

evolucao_migracao="Domingo 15 de Outubro 2018,  Operações de Engenahria Reversa registradas para o dia"


def envelopes(request,nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2):

	global nome_criterioGLOBAL
	global anguloGLOBAL
	global materialGLOBAL
	global livreGLOBAL
	global sigma_xGLOBAL
	global sigma_yGLOBAL
	global tau_xyGLOBAL
	global livre_2GLOBAL
	global parametro_wuGLOBAL

	nome_criterioGLOBAL=nome_criterio
	anguloGLOBAL=angulo
	materialGLOBAL=material
	livreGLOBAL=livre
	sigma_xGLOBAL=sigma_x
	sigma_yGLOBAL=sigma_y
	tau_xyGLOBAL=tau_xy
	livre_2GLOBAL=livre_2
	

	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(material)):
		SIGMA_T_1=p.SIGMA_T_1
		SIGMA_T_2=p.SIGMA_T_2
		SIGMA_C_1=-p.SIGMA_C_1  # Convenio de sinais
		SIGMA_C_2=-p.SIGMA_C_2  # Convenio de sinais
		NOME=p.NOME
		EPSILON_T_1=p.EPSILON_T_1
		EPSILON_T_2=p.EPSILON_T_2
		EPSILON_C_1=-p.EPSILON_C_1  # Convenio de sinais
		EPSILON_C_2=-p.EPSILON_C_2  # Convenio de sinais

		# cisalhantes:

		GAMMA12=p.GAMMA12
		TAU12=p.TAU12
		NU12=p.NU12
	#Setembro27

	#evolucao_migracao=" Engenahria Reversa"

	c = {
	 'angulo': angulo, #"anguloCRIANDO",
	'material':material,
	'livre':livre,
	'sigma_x':sigma_x,
	'sigma_y':sigma_y,
	'tau_xy':tau_xy,	
	'livre_2':livre_2,  
# até aqui os argumentos de entrada da função. 
# Agora as propriedades do material para TESTE inicial
	'nome':NOME,
	'SIGMA_T_1':SIGMA_T_1,#var ="{{SIGMA_T_1}}";//        SIGMA_T_1=dados[laminaURL_numerico].SIGMA_T_1;
	'SIGMA_T_2':SIGMA_T_2,#var ="{{SIGMA_T_2}}";//        SIGMA_T_2=dados[laminaURL_numerico].SIGMA_T_2;
	'SIGMA_C_1':SIGMA_C_1,#var ="{{SIGMA_C_1}}";//        SIGMA_C_1=dados[laminaURL_numerico].SIGMA_C_1;
	'SIGMA_C_2':SIGMA_C_2,#var ="{{SIGMA_C_2}}";//        SIGMA_C_2=dados[laminaURL_numerico].SIGMA_C_2;
	'TAU12':TAU12,#var ="{{TAU12}}";//        TAU12=dados[laminaURL_numerico].TAU12;
	'EPSILON_T_1':EPSILON_T_1,#var ="{{EPSILON_T_1}}";//        EPSILON_T_1=dados[laminaURL_numerico].EPSILON_T_1;
	'EPSILON_T_2':EPSILON_T_2,#var ="{{EPSILON_T_2}}";//        EPSILON_T_2=dados[laminaURL_numerico].EPSILON_T_2;
	'EPSILON_C_1':EPSILON_C_1,#var ="{{EPSILON_C_1}}";//        EPSILON_C_1=dados[laminaURL_numerico].EPSILON_C_1;
	'EPSILON_C_2':EPSILON_C_2,#var ="{{EPSILON_C_2}}";//        EPSILON_C_2=dados[laminaURL_numerico].EPSILON_C_2;
	'GAMMA12':GAMMA12,
	'evoluacao':evolucao_migracao,
	'NU12':NU12,
	 }

	return render(request,'iframe/envelopes/'+nome_criterio,c)	

#javaScript para desativar

def ordenar_quatro_pontos(request):
	return render(request, 'ordenar_quatro_pontos.js')

def equacoes_41_412(request):
	return render(request, 'equacoes_41_412.js')	

def usar_GraphView(request):
	return render(request, 'usar_GraphView.js')	
		
def construir_COM_POLIGONO_TRUE_pontos(request):
	return render(request, 'construir_COM_POLIGONO_TRUE_pontos.js')			

#########################################################################################
# Agosto 21, 2018 
#
# Passando as informações para cada arquivo de CRITERIO ou ENVELOPE
#
#########################################################################################	


########### Histórico Generalizado de Cálculos

# Historico URL
global lista_historicos
lista_historicos=[]

#Historico de materiais
global materiais_historicos
materiais_historicos=[]

#Historico de esforços
global esforcos_historicos
esforcos_historicos=[]
#Historico de angulos
global angulo_historico
angulo_historico=[]

def historico(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2):
	lista_historicos.append(nome_criterio+"!/"+angulo+"/"+material+"/"+livre+"/"+sigma_x+"/"+sigma_y+"/"+tau_xy+"/"+livre_2);	
	materiais_historicos.append(material);
	esforcos_historicos.append("("+sigma_x+","+sigma_y+","+tau_xy+")");
	angulo_historico.append(angulo);
	
########### Critérios

from criteriosDidaticos import criterio_maxima_tensao
from criteriosDidaticos import criterio_maxima_deformacao
from criteriosDidaticos import criterio_tsai_hill
from criteriosDidaticos import criterio_azzi_tsai
from criteriosDidaticos import criterio_tsai_wu
from criteriosDidaticos import criterio_hoffman
from criteriosDidaticos import criterio_hashin
from criteriosDidaticos import criterio_christensen
from criteriosDidaticos import criterio_puck
from criteriosDidaticos import criterio_larc03

################################################################################################################

def criterios(request,nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2):

	nome_criterioGLOBAL=nome_criterio


	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(material)):
		SIGMA_T_1=p.SIGMA_T_1
		SIGMA_T_2=p.SIGMA_T_2
		SIGMA_C_1=-p.SIGMA_C_1  # Convenio de sinais
		SIGMA_C_2=-p.SIGMA_C_2  # Convenio de sinais
		NOME=p.NOME

		EPSILON_T_1=p.EPSILON_T_1
		EPSILON_T_2=p.EPSILON_T_2
		EPSILON_C_1=-p.EPSILON_C_1  # Convenio de sinais
		EPSILON_C_2=-p.EPSILON_C_2  # Convenio de sinais
		LARC03_EPSILON_T_1=p.EPSILON_T_1

		# cisalhantes:

		GAMMA12=p.GAMMA12
		TAU12=p.TAU12

		# para construir a matriz S

		E1=p.E1
		E2=p.E2
		G12=p.G12
		NU12=p.NU12

	#indicamos uma lista de materiais Cadastrados

	materiais=[]
	for p in Laminas.objects.raw('SELECT * FROM macro_laminas'):
		materiais.append(p.NOME)	

	#colocamos um histórico de cálculos prévios

	historico(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)		

	c = {
	'nome_criterioGLOBAL':nome_criterioGLOBAL,
	 'angulo': angulo,
	'material':material,
	'livre':livre,
	'sigma_x':sigma_x,
	'sigma_y':sigma_y,
	'tau_xy':tau_xy,	
	'livre_2':livre_2,  
	'lista_historicos':lista_historicos,
# até aqui os argumentos de entrada da função. 
# Agora as propriedades do material para TESTE inicial
	'nome':NOME,
	'SIGMA_T_1':SIGMA_T_1,#var ="{{SIGMA_T_1}}";//        SIGMA_T_1=dados[laminaURL_numerico].SIGMA_T_1;
	'SIGMA_T_2':SIGMA_T_2,#var ="{{SIGMA_T_2}}";//        SIGMA_T_2=dados[laminaURL_numerico].SIGMA_T_2;
	'SIGMA_C_1':SIGMA_C_1,#var ="{{SIGMA_C_1}}";//        SIGMA_C_1=dados[laminaURL_numerico].SIGMA_C_1;
	'SIGMA_C_2':SIGMA_C_2,#var ="{{SIGMA_C_2}}";//        SIGMA_C_2=dados[laminaURL_numerico].SIGMA_C_2;
	'TAU12':TAU12,#var ="{{TAU12}}";//        TAU12=dados[laminaURL_numerico].TAU12;
	'EPSILON_T_1':EPSILON_T_1,#var ="{{EPSILON_T_1}}";//        EPSILON_T_1=dados[laminaURL_numerico].EPSILON_T_1;
	'EPSILON_T_2':EPSILON_T_2,#var ="{{EPSILON_T_2}}";//        EPSILON_T_2=dados[laminaURL_numerico].EPSILON_T_2;
	'EPSILON_C_1':EPSILON_C_1,#var ="{{EPSILON_C_1}}";//        EPSILON_C_1=dados[laminaURL_numerico].EPSILON_C_1;
	'EPSILON_C_2':EPSILON_C_2,#var ="{{EPSILON_C_2}}";//        EPSILON_C_2=dados[laminaURL_numerico].EPSILON_C_2;
	'GAMMA12':GAMMA12,
	'E1':E1,
	'E2':E2,
	'G12':G12,
	'NU12':NU12,
	'LARC03_EPSILON_T_1':LARC03_EPSILON_T_1,	
	 }


	#As informações conforme um SELECT para cada critério, sendo este SELET apenas de arquivos
	#Setembro 24, 
	#MT
	if(nome_criterioGLOBAL == "maxima_tensao.htm"):
		criterio_maxima_tensao.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_maxima_tensao.passando_materiais(materiais)
		criterio_maxima_tensao.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)
	#MD
	if(nome_criterioGLOBAL == "maxima_deformacao.htm"):
		criterio_maxima_deformacao.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_maxima_deformacao.passando_materiais(materiais)
		criterio_maxima_deformacao.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)	

#	Tsai Hill
	if(nome_criterioGLOBAL == "tsai_hill.htm"):		
		criterio_tsai_hill.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_tsai_hill.passando_materiais(materiais)
		criterio_tsai_hill.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)	

# Azzi Tsai 
	if(nome_criterioGLOBAL == "azzi_tsai.htm"):		
		criterio_azzi_tsai.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_azzi_tsai.passando_materiais(materiais)
		criterio_azzi_tsai.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)	

#	Hoffman
	if(nome_criterioGLOBAL == "hoffman.htm"):		
		criterio_hoffman.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_hoffman.passando_materiais(materiais)
		criterio_hoffman.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)			
#	hashin
	if(nome_criterioGLOBAL == "hashin.htm"):		
		criterio_hashin.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_hashin.passando_materiais(materiais)
		criterio_hashin.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)					
#	christensen
	if(nome_criterioGLOBAL == "christensen.htm"):		
		criterio_christensen.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_christensen.passando_materiais(materiais)
		criterio_christensen.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)							

#	puck
	if(nome_criterioGLOBAL == "puck.htm"):		
		criterio_puck.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_puck.passando_materiais(materiais)
		criterio_puck.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)									
#	larc03
	if(nome_criterioGLOBAL == "larc03.htm"):		
		criterio_larc03.coletando_informacaos_view(nome_criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2)
		criterio_larc03.passando_materiais(materiais)
		criterio_larc03.passando_historico(lista_historicos,materiais_historicos,esforcos_historicos,angulo_historico)								

	if(nome_criterioGLOBAL != "tsai_wu.htm"):		
		return render(request,'iframe/criterios/'+nome_criterio,c)	
	else:
		
		return criterios_tsai_wu(request,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2,TAU12)

#########################################################################################
#########################################################################################
#########################################################################################

#########################################################################################

#########################################################################################


from envelopes_Didaticos import envelope_maxima_tensao
from envelopes_Didaticos import envelope_maxima_deformacao
from envelopes_Didaticos import envelope_tsai_hill
from envelopes_Didaticos import envelope_azzi_tsai
from envelopes_Didaticos import envelope_tsai_wu
from envelopes_Didaticos import envelope_hoffman
from envelopes_Didaticos import envelope_hashin
from envelopes_Didaticos import envelope_christensen
from envelopes_Didaticos import envelope_larc03
from envelopes_Didaticos import envelope_puck
#########################################################################################
# Agosto 25, 2018 
# Sábado
# Agosto 27, 2018
# Segunda: Colocando as LEGENDAS , com ANGULO
# 			Estranho que não funciona com as primeiras 
#	5 legendas
#ABANDONADO ----> Sol: Passando apenas um texto único (usando o indice E NÂO o I )
# esta função entrega as informações quando for invocada por:
# 	url(r'^entradas/iframe_entradas_html/iframe_flot/', views.iframe_flot, name='iframe_flot'),   

#http://127.0.0.1:8000/criterios_envelopes_julian/entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/	
#######################################################################################	

def iframe_flot(request):

	VETORdjango_limite=[]

	VETOR_extremos=[]

	EnvelopeFalhaFlotJson="/criterios_envelopes_julian/entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/"

	GNU_botao="/criterios_envelopes_julian/entradas/iframe_entradas_html/gerarGNU/"	

	MATLAB_botao="/criterios_envelopes_julian/entradas/iframe_entradas_html/matlab/"	

	nome_criterio_vertices="sem_vertices_especificos"

	#Outubro 01 selector

	if(nome_criterioGLOBAL == "maxima_tensao.htm"):	
		VETORdjango_limite=envelope_maxima_tensao.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_maxima_tensao.VETOR_extremos()
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "maxima_tensao/"])	
		GNU_botao=''.join([GNU_botao, "maxima_tensao/"])	
		MATLAB_botao=''.join([MATLAB_botao, "maxima_tensao/"])	
		nome_criterio_vertices="maxima_tensao"		

		
	#Setembro 27 , as duas (02) funções devem ser invocadas de forma simultanea
	
	if(nome_criterioGLOBAL == "maxima_deformacao.htm"):	
		VETORdjango_limite=envelope_maxima_deformacao.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_maxima_deformacao.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "maxima_deformacao/"])
		GNU_botao=''.join([GNU_botao, "maxima_deformacao/"])
		MATLAB_botao=''.join([MATLAB_botao, "maxima_deformacao/"])
		nome_criterio_vertices="maxima_deformacao"		

# Outubro 06, Sábado

#	Tsai Hill
	if(nome_criterioGLOBAL == "tsai_hill.htm"):				
		VETORdjango_limite=envelope_tsai_hill.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_tsai_hill.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "tsai_hill/"])
		GNU_botao=''.join([GNU_botao, "tsai_hill/"])
		MATLAB_botao=''.join([MATLAB_botao, "tsai_hill/"])
		nome_criterio_vertices="tsai_hill"		


# Outubro 08,
#	Azzi Tsai 
	if(nome_criterioGLOBAL == "azzi_tsai.htm"):				
		VETORdjango_limite=envelope_azzi_tsai.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_azzi_tsai.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "azzi_tsai/"])
		GNU_botao=''.join([GNU_botao, "azzi_tsai/"])
		MATLAB_botao=''.join([MATLAB_botao, "azzi_tsai/"])
		nome_criterio_vertices="azzi_tsai"				


# Outubro 08, 
	if(nome_criterioGLOBAL == "tsai_wu.htm"):				
		VETORdjango_limite=envelope_tsai_wu.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_tsai_wu.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "tsai_wu/"])
		GNU_botao=''.join([GNU_botao, "tsai_wu/"])
		MATLAB_botao=''.join([MATLAB_botao, "tsai_wu/"])
		nome_criterio_vertices="tsai_wu"			

# Outubro 08, 
	if(nome_criterioGLOBAL == "hoffman.htm"):				
		VETORdjango_limite=envelope_hoffman.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_hoffman.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "hoffman/"])
		GNU_botao=''.join([GNU_botao, "hoffman/"])
		MATLAB_botao=''.join([MATLAB_botao, "hoffman/"])
		nome_criterio_vertices="hoffman"		

# Outubro 23, 
	if(nome_criterioGLOBAL == "hashin.htm"):				
		VETORdjango_limite=envelope_hashin.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_hashin.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "hashin/"])
		GNU_botao=''.join([GNU_botao, "hashin/"])
		MATLAB_botao=''.join([MATLAB_botao, "hashin/"])
		nome_criterio_vertices="hashin"			

# Outubro 23, 
	if(nome_criterioGLOBAL == "christensen.htm"):				
		VETORdjango_limite=envelope_christensen.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_christensen.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "christensen/"])
		GNU_botao=''.join([GNU_botao, "christensen/"])
		MATLAB_botao=''.join([MATLAB_botao, "christensen/"])
		nome_criterio_vertices="christensen"				

# Outubro 18, 2018
	if(nome_criterioGLOBAL == "puck.htm"):				
		VETORdjango_limite=envelope_puck.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_puck.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "puck/"])
		GNU_botao=''.join([GNU_botao, "puck/"])
		MATLAB_botao=''.join([MATLAB_botao, "puck/"])
		nome_criterio_vertices="puck"		


# Outubro 16, 2018
	if(nome_criterioGLOBAL == "larc03.htm"):				
		VETORdjango_limite=envelope_larc03.coletando_informacaos_view(nome_criterioGLOBAL,anguloGLOBAL,	materialGLOBAL,livreGLOBAL,sigma_xGLOBAL,sigma_yGLOBAL,tau_xyGLOBAL,livre_2GLOBAL)
		VETOR_extremos    =envelope_larc03.VETOR_extremos()	
		EnvelopeFalhaFlotJson=''.join([EnvelopeFalhaFlotJson, "larc03/"])
		GNU_botao=''.join([GNU_botao, "larc03/"])
		MATLAB_botao=''.join([MATLAB_botao, "larc03/"])
		nome_criterio_vertices="larc03"			

# INSERIR envelope		
		
	#Setembro 27 

	minimoY=VETOR_extremos[0];
	maximoY=VETOR_extremos[1];
	minimoX=VETOR_extremos[2];
	maximoX=VETOR_extremos[3];

	#È preciso definir o valor INEXISTENTE
	#Preciso apagar as informações 
	#Anti 
	#JSON http://127.0.0.1:8000/criterios_envelopes_julian/entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/

	django_limite1=0
	django_limite2=0
	django_limite3=0
	django_limite4=0
	django_limite5=0
	django_limite6=0


	if(len(VETORdjango_limite)>=1):
		django_limite1=VETORdjango_limite[0]
	if(len(VETORdjango_limite)>=2):
		django_limite2=VETORdjango_limite[1]
	if(len(VETORdjango_limite)>=3):		
		django_limite3=VETORdjango_limite[2]
	if(len(VETORdjango_limite)>=4):
		django_limite4=VETORdjango_limite[3]
	if(len(VETORdjango_limite)>=5):
		django_limite5=VETORdjango_limite[4]
	if(len(VETORdjango_limite)>=6):
		django_limite6=VETORdjango_limite[5]

	#estas informacoes pode-se coletar usando um vetor RETURN desde envelope_maxima_tensao.coletando_informacaos_view


	c = {
	 'django_limite1': django_limite1,
	 'django_limite2': django_limite2,
	 'django_limite3': django_limite3,
	 'django_limite4': django_limite4,
	 'django_limite5': django_limite5,
	 'django_limite6': django_limite6,
	 ########### Extremos para o FLOT
		'minimoY':minimoY,
		'maximoY':maximoY,
		'minimoX':minimoX,
		'maximoX':maximoX,
	########### Conforme o endereço ele vai procurar o JSON
		'EnvelopeFalhaFlotJson':EnvelopeFalhaFlotJson,
		'nome_criterio_vertices':nome_criterio_vertices,
		'redesenho_criterio':nome_criterio_vertices,
#GNU 
		'GNU_botao':GNU_botao,		
		'MATLAB_botao':MATLAB_botao,	
	 }

	return render(request,'iframe_flot/iframe_flot.html',c)	


#########################################################################################
# Agosto 20, 2018 
#
# melhora: é preciso colocar um "/"
# http://127.0.0.1:8000/criterios_envelopes_julian/entradas/iframe_entradas_html
# Com o intuito de facilitar o comportamento do gestor de URL
# E ao parecer será preciso tirar o estilo AJAX "?" (https://stackoverflow.com/questions/5500472/how-do-i-match-the-question-mark-character-in-a-django-url)
# E trocar o carater ? pelo !
#
#
#########################################################################################	@login_required

@login_required
def iframe_entradas_html(request):		
		return render(request,'iframe/index.htm')	

#########################################################################################
######################   Área programador 				
# Terça 20, 2018. Novembro
#
#################
#########################################################################################

@login_required
def area_programador(request):
	return render(request, 'area_programador/apenas_testes.htm')

# Quarta 21, 2018. Novembro
#gerar_arquivo_esforcos



#########################################################################################
# Agosto 19, 2018 
#
# Inicio simples com IFRAME
#
#
#########################################################################################

def entradas(request):
	return render(request, 'entradas.htm')	


#########################################################################################
# Nov 19, 2018 
#
# Aulas didaticas
#
#
#########################################################################################

def aulas(request,numeroURL):
	return render(request, 'aulas_didaticas/%d.htm' % (int(numeroURL)))

#########################################################################################
# Nov 19, 2018 
#
# Aulas didaticas
#
#
#########################################################################################


response_data = {}

response_data['criterio']=[]
response_data['data']=[]
response_data['dimensao_data']=[]
response_data['extremos']=[]


def coletarENVELOPE(request,nome_criterio,numero_envelope):	

	if(len(response_data['criterio'])==6):
		response_data.clear()
		response_data['criterio']=[]
		response_data['data']=[]
		response_data['dimensao_data']=[]
		response_data['extremos']=[]
		
	
	if(nome_criterio=="maxima_tensao"):
		legenda=envelope_maxima_tensao.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_maxima_tensao.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_maxima_tensao.coletar_LIMITES(numero_envelope)
		extremos=envelope_maxima_tensao.coletar_EXTREMOS(numero_envelope)

	if(nome_criterio=="maxima_deformacao"):
		legenda=envelope_maxima_deformacao.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_maxima_deformacao.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_maxima_deformacao.coletar_LIMITES(numero_envelope)
		extremos=envelope_maxima_deformacao.coletar_EXTREMOS(numero_envelope)		

	if(nome_criterio=="tsai_hill"):
		legenda=envelope_tsai_hill.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_tsai_hill.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_tsai_hill.coletar_LIMITES(numero_envelope)
		extremos=envelope_tsai_hill.coletar_EXTREMOS(numero_envelope)		

	if(nome_criterio=="azzi_tsai"):
		legenda=envelope_azzi_tsai.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_azzi_tsai.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_azzi_tsai.coletar_LIMITES(numero_envelope)
		extremos=envelope_azzi_tsai.coletar_EXTREMOS(numero_envelope)
	if(nome_criterio=="tsai_wu"):
		legenda=envelope_tsai_wu.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_tsai_wu.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_tsai_wu.coletar_LIMITES(numero_envelope)
		extremos=envelope_tsai_wu.coletar_EXTREMOS(numero_envelope)			
	if(nome_criterio=="hoffman"):
		legenda=envelope_hoffman.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_hoffman.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_hoffman.coletar_LIMITES(numero_envelope)
		extremos=envelope_hoffman.coletar_EXTREMOS(numero_envelope)	
	if(nome_criterio=="hashin"):
		legenda=envelope_hashin.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_hashin.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_hashin.coletar_LIMITES(numero_envelope)
		extremos=envelope_hashin.coletar_EXTREMOS(numero_envelope)		
	if(nome_criterio=="christensen"):
		legenda=envelope_christensen.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_christensen.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_christensen.coletar_LIMITES(numero_envelope)
		extremos=envelope_christensen.coletar_EXTREMOS(numero_envelope)	
	if(nome_criterio=="puck"):
		legenda=envelope_puck.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_puck.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_puck.coletar_LIMITES(numero_envelope)
		extremos=envelope_puck.coletar_EXTREMOS(numero_envelope)	
	if(nome_criterio=="larc03"):
		legenda=envelope_larc03.coletarENVELOPE_legenda(numero_envelope)
		dados=envelope_larc03.coletarENVELOPE_data(numero_envelope)
		dimensao_data=envelope_larc03.coletar_LIMITES(numero_envelope)
		extremos=envelope_larc03.coletar_EXTREMOS(numero_envelope)										


	temporal_criterio=response_data['criterio']		
	temporal_criterio.append(legenda)
	response_data['criterio'] = temporal_criterio
	

	temporal_criterio=response_data['data']		
	temporal_criterio.append(dados)
	response_data['data'] = temporal_criterio	

	temporal_criterio=response_data['dimensao_data']		
	temporal_criterio.append(dimensao_data)
	response_data['dimensao_data'] = temporal_criterio	


	temporal_criterio=response_data['extremos']		
	temporal_criterio.append(extremos)
	response_data['extremos'] = temporal_criterio	

# Máximo 6 elementos		
	return HttpResponse(len(response_data['criterio']))

#########################################################################################

def entregarENVELOPE(request):		
	return HttpResponse(json.dumps(response_data))

#########################################################################################
# Nov 22, 2018 

def redesenho_flot(request):
	return render(request,'iframe_flot/iframe_flot_multiplos.html')

#########################################################################################
# Nov 23, 2018 
def ZERAR_coletarENVELOPE(request):
	
	response_data.clear()
	response_data['criterio']=[]
	response_data['data']=[]
	response_data['dimensao_data']=[]
	response_data['extremos']=[]
	return HttpResponse("zerado")


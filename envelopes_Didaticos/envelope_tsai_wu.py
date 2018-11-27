# coding: utf-8

### Agosto 21, 2018
import math
import numpy as np
from math import pi, sqrt, cos, sin, pow
import sys, traceback
import math as Math
import json
from django.http import HttpResponse


from django.shortcuts import render

from numpy.linalg import inv

##################################Entrada#########################################
# Agosto 23, 2018 
#
# 1) Todas as informações do URL são essenciais
# 2) 
#########################################################################################	

from macro.models import Laminas

numeroENVELOPES_EnvelopeFalhaSaidaJSON=0
response_data = {}
response_data['criterio']=[]

TRUE_pontos_x=[]
TRUE_pontos_y=[]

global EXTREMOASvaloresX
EXTREMOASvaloresX=[]

global EXTREMOASvaloresY
EXTREMOASvaloresY=[]

global VETORdjango_limite
VETORdjango_limite=[] 		# saida indicando o numero de PONTOS

EnvelopeFalhaSaidaJSON=[]

GNU_EnvelopeFalhaSaidaJSON=""

dados_coletarENVELOPE_data=[]
LIMITES_coletarENVELOPE=[]

##################################Entrada#########################################
# Outubro 06, Sábado
#
# 1) Todas as informações do URL são essenciais, portanto são coletadas
# 2) 
#########################################################################################	

def coletando_informacaos_view(criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2):

	global global_material
	global_material=material
	global global_criterio
	global_criterio=criterio
	global global_angulo
	global_angulo=angulo


	livre_2=float(livre_2)+0.0

	if (livre_2==0.0):
		global EnvelopeFalhaSaidaJSON
		EnvelopeFalhaSaidaJSON=[]
		global GNU_EnvelopeFalhaSaidaJSON
		GNU_EnvelopeFalhaSaidaJSON=""

		global dados_coletarENVELOPE_data
		dados_coletarENVELOPE_data=[]
		global LIMITES_coletarENVELOPE
		LIMITES_coletarENVELOPE=[]	

	global possiveis_pontos_x
	possiveis_pontos_x=[]
		
	global possiveis_pontos_y
	possiveis_pontos_y=[]

	global possiveis_pontos_xy
	possiveis_pontos_xy=[]

# A varíavel POLIGONO_TRUE_pontos_x, permite colocar as informações cálculadas no momento de passar os valores

	global POLIGONO_TRUE_pontos_x
	POLIGONO_TRUE_pontos_x=[]

	global POLIGONO_TRUE_pontos_y
	POLIGONO_TRUE_pontos_y=[]

	global POLIGONO_TRUE_pontos_xy
	POLIGONO_TRUE_pontos_xy=[]

	global valoresX
	valoresX = []

	global valoresY
	valoresY = []			

	if (livre_2==0.0):
		response_data.clear()
		response_data['criterio']=[]
		EnvelopeFalhaSaidaJSON=[]

	temporal_criterio=response_data['criterio']	

	if(len(temporal_criterio)==6):
		response_data.clear()
		response_data['criterio']=[]
		EnvelopeFalhaSaidaJSON=[]
		global GNU_EnvelopeFalhaSaidaJSON
		GNU_EnvelopeFalhaSaidaJSON=""	

		dados_coletarENVELOPE_data=[]
		LIMITES_coletarENVELOPE=[]

	global hrefs_enderecos

	global tauXY
	tauXY=float(tau_xy)

	hrefs_enderecos="%s!/%s/%s/%s/" % (criterio,angulo,material,livre)

	angulo=float(angulo)
	sigma_x=float(sigma_x)
	sigma_y=float(sigma_y)
	tau_xy=float(tau_xy)
	# são coletadas as propriedades do material conforme o indice "material"

	global SIGMA_T_1
	global SIGMA_T_2
	global SIGMA_C_1
	global SIGMA_C_2		
	global TAU12

	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(material)):
		SIGMA_T_1=p.SIGMA_T_1
		SIGMA_T_2=p.SIGMA_T_2
		SIGMA_C_1=p.SIGMA_C_1  # Convenio de sinais
		SIGMA_C_2=p.SIGMA_C_2  # Convenio de sinais
		NOME=p.NOME
		TAU12=p.TAU12
	
	# estás informações são usadas para obter os potenciais PONTOS do envelope usando as equações"	

	temporal_criterio=response_data['criterio']	
	LEGENDA_TIPO_ANGULO_MATERIAL="".join([u'Tsai Wu  , com ângulo (Degree)  ', str(angulo),'   com el material  ',NOME,u' com parâmetro biaxial ',str(biaxial_experimental_global)])	
#GNU
	GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON," #  ",LEGENDA_TIPO_ANGULO_MATERIAL,"\n"]) 	

	#LEGENDA_TIPO_ANGULO_MATERIAL="".join([u'Tsai Wu  , com ângulo (Degree)  ', str(angulo),'   com el material  ',NOME])	
	temporal_criterio.append(LEGENDA_TIPO_ANGULO_MATERIAL)
	response_data['criterio'] = temporal_criterio

	# Até aqui foi preciso coletar informações gerais, DA aqui em diante começam as operações de cálculo
# Outubro 06, Sábado
	calculo_envelope(angulo)

	VETORdjango_limite.append(len(POLIGONO_TRUE_pontos_x))

	return VETORdjango_limite


#########################################################################################
# Outubro 06, 2018
#
#########################################################################################	

def EnvelopeFalhaFlotJson(request):	
	response_data['data'] = EnvelopeFalhaSaidaJSON 	
	return HttpResponse(json.dumps(response_data))	

#########################################################################################
# Outubro 06, 2018
#
#########################################################################################	

def vertices(request):

	#return HttpResponse("vertices")

	saida_PONTOS_extremos_X=[]
	saida_PONTOS_extremos_Y=[]
	
	for i in range(0,len(PONTOS_extremos_X)):
		saida_PONTOS_extremos_X.append(PONTOS_extremos_X[i])
	
	for i in range(0,len(PONTOS_extremos_Y)):
		saida_PONTOS_extremos_Y.append(PONTOS_extremos_Y[i])

	c = {
	 'vertices_POLIGONO_TRUE_pontos_x': saida_PONTOS_extremos_X,
	 'vertices_POLIGONO_TRUE_pontos_y': saida_PONTOS_extremos_Y,
	 'biaxial_experimental_global'	:biaxial_experimental_global,
	 'hrefs_enderecos':hrefs_enderecos,
	 'tauXY':tauXY,
	 'biaxial_experimental_global':biaxial_experimental_global,
	}

	arquivo_js='vertices.js'
	return render(request, arquivo_js,c)	

#########################################################################################
# Outubro 06, 2018
# Faz duas (02) coisas:
# 1) Definir os PONTOS extremos 
# 2) Obter apenas os extremos
#########################################################################################	
	

def VETOR_extremos():

	global PONTOS_extremos_X
	PONTOS_extremos_X=[]
	global PONTOS_extremos_Y
	PONTOS_extremos_Y=[]	

	VETOR_extremos=[]
	
	EXTREMOASvaloresX.sort()
	EXTREMOASvaloresY.sort()

	amplificao=1.5	

#Outubro 08. A sequencia de invocação de extremos:

#minimoY=VETOR_extremos[0];
	temp=0.0
	temp_i=0
	for i in range (0,len(POLIGONO_TRUE_pontos_y)):	#(i=0;i<pares_pontos_y.length;i++)
		if(POLIGONO_TRUE_pontos_y[i]<=temp):	
			temp=POLIGONO_TRUE_pontos_y[i]
			temp_i=i;
	VETOR_extremos.append(POLIGONO_TRUE_pontos_y[temp_i]*amplificao)	
	# Par de oordenadas
	PONTOS_extremos_X.append(POLIGONO_TRUE_pontos_x[temp_i])	
	PONTOS_extremos_Y.append(POLIGONO_TRUE_pontos_y[temp_i])	

#maximoY=VETOR_extremos[1];	
	temp=0.0
	temp_i=0
	for i in range (0,len(POLIGONO_TRUE_pontos_y)):	#(i=0;i<pares_pontos_y.length;i++)
		if(POLIGONO_TRUE_pontos_y[i]>=temp):	
			temp=POLIGONO_TRUE_pontos_y[i]
			temp_i=i;
	VETOR_extremos.append(POLIGONO_TRUE_pontos_y[temp_i]*amplificao)	
	# Par de oordenadas
	PONTOS_extremos_X.append(POLIGONO_TRUE_pontos_x[temp_i])	
	PONTOS_extremos_Y.append(POLIGONO_TRUE_pontos_y[temp_i])		

#minimoX=VETOR_extremos[2];

	temp=0.0
	temp_i=0
	for i in range (0,len(POLIGONO_TRUE_pontos_x)):	#(i=0;i<pares_pontos_y.length;i++)
		if(POLIGONO_TRUE_pontos_x[i]<=temp):	
			temp=POLIGONO_TRUE_pontos_x[i]
			temp_i=i;
	VETOR_extremos.append(POLIGONO_TRUE_pontos_x[temp_i]*amplificao)	
	# Par de oordenadas
	PONTOS_extremos_X.append(POLIGONO_TRUE_pontos_x[temp_i])	
	PONTOS_extremos_Y.append(POLIGONO_TRUE_pontos_y[temp_i])		

#maximoX=VETOR_extremos[3];

	temp=0.0
	temp_i=0
	for i in range (0,len(POLIGONO_TRUE_pontos_x)):	#(i=0;i<pares_pontos_y.length;i++)
		if(POLIGONO_TRUE_pontos_x[i]>=temp):	
			temp=POLIGONO_TRUE_pontos_x[i]
			temp_i=i;

	VETOR_extremos.append(POLIGONO_TRUE_pontos_x[temp_i]*amplificao)	

	# Par de oordenadas
	PONTOS_extremos_X.append(POLIGONO_TRUE_pontos_x[temp_i])	
	PONTOS_extremos_Y.append(POLIGONO_TRUE_pontos_y[temp_i])		
	return VETOR_extremos

#########################################################################################
# Outubro 08, 2018
# Função para calcular apenas o Envelope
#########################################################################################	

def calculo_envelope(angulo):	
	#global numeroPontos
	#numeroPontos=55 #coletar_numero_pontos(55);
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
    
	#global	biaxial_experimental
	#					 1859520000
	#biaxial_experimental=1859520000
	#calcular_coeficientes(cos,sin,biaxial_experimental)
	calcular_coeficientes(cos,sin)

	calcula_raios_origem_rotacao_elipse()

	controle_conica_tipo_elipse()

	forma_polar_conica_elipse()	

	adicionar_JSON()


#########################################################################################
# Outubro 08, 2018
# SUPORTE para calculo_envelope
#########################################################################################		


#########################################################################################
# Outubro 08, 2018
# SUPORTE para calculo_envelope
#########################################################################################		

def controle_conica_tipo_elipse():
	B=2*b_f;
	A=a_f;
	C=c_f;

	if((B*B-4*A*C)>=0):	
		return "nao_elipse"

#########################################################################################
# Outubro 08, 2018
# SUPORTE para calculo_envelope
#########################################################################################		

def calcula_raios_origem_rotacao_elipse():

	global a_f
	global 	b_f
	global 	c_f
	global 	d_f
	global 	f_f
	global 	g_f	

	a_f=a
	b_f=b
	c_f=c
	d_f=d
	f_f=f
	g_f=g

#Sendo preciso agora usar a formulaÃ§Ã£o mais explicita
	global rotacionado
	
	if(b!=0):
		B=2*b_f
		D=2*d_f
		E=2*f_f
		A=a_f
		C=c_f
		numerador=(C-A-Math.sqrt(Math.pow(A-C,2)+B*B))
		rotacionado=Math.atan(numerador/B)
        
	#cumprimento dos eixos, usando todos os coeficientes:	
	global raioMaior
	global raioMenor
	raioMaior=Math.sqrt((2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g))/((b*b-a*c)*( Math.sqrt(Math.pow((a-c),2)+4*b*b)-(a+c))))
	raioMenor=Math.sqrt((2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g))/((b*b-a*c)*(-Math.sqrt(Math.pow((a-c),2)+4*b*b)-(a+c))))

	#Origem

	global origem_x
	global origem_y

	origem_x=(c*d-b*f)/(b*b-a*c)
	origem_y=(a*f-b*d)/(b*b-a*c)

#########################################################################################
# Outubro 08, 2018
# SUPORTE para calculo_envelope
# É preciso explicitar os extremos para que posssa funcionar no FLOAT
# Assim como cumrpimento do vetor de saída POLIGONO_TRUE_pontos_x
#########################################################################################		

def forma_polar_conica_elipse():
	ang=0
	passo=(2*Math.pi/numeroPontos)
#Fazemos a varredura de Izquerda para DIREITA , desde 0 para 2*Pi
	for i in range(0,numeroPontos):	#i=0;i<numeroPontos;i++)    
		c=Math.cos(ang)
		s=Math.sin(ang)
		r=(raioMaior*raioMenor)/(Math.sqrt(raioMaior*raioMaior*s*s+raioMenor*raioMenor*c*c))
		x=r*c
		y=r*s
		#aplicamos uma rotaÃ§Ã£o de euler
		temporal_x=x*Math.cos(rotacionado)-y*Math.sin(rotacionado)
		temporal_y=x*Math.sin(rotacionado)+y*Math.cos(rotacionado)
        
		if (origem_x!=0):
			temporal_x=temporal_x+origem_x        
		if (origem_y!=0):
			temporal_y=temporal_y+origem_y

		ang=ang+passo
		POLIGONO_TRUE_pontos_x.append(temporal_x)
		POLIGONO_TRUE_pontos_y.append(temporal_y)
    #for

#########################################################################################
# Outubro 08, 2018
# SUPORTE para calculo_envelope
# É preciso explicitar os extremos para que posssa funcionar no FLOAT
# Assim como cumrpimento do vetor de saída POLIGONO_TRUE_pontos_x
#########################################################################################	

def calcular_coeficientes(cos,sin):

	biaxial_experimental=biaxial_experimental_global

	is1=((1/SIGMA_T_1)-(1/SIGMA_C_1))
	is2=((1/SIGMA_T_2)-(1/SIGMA_C_2))
	is1q=(1/SIGMA_T_1)*(1/SIGMA_C_1)
	is2q=(1/SIGMA_T_2)*(1/SIGMA_C_2)
	t12=(1/TAU12)*(1/TAU12)

	F12_potencia_1=((1/SIGMA_T_1)-(1/SIGMA_C_1)+(1/SIGMA_T_2)-(1/SIGMA_C_2))*biaxial_experimental

	F12_potencia_2=((1/(SIGMA_T_1*SIGMA_C_1))+(1/(SIGMA_T_2*SIGMA_C_2)))*biaxial_experimental*biaxial_experimental

	F12_sem_normalizar=1-F12_potencia_1-F12_potencia_2	

	F12=(1.0/(2*biaxial_experimental*biaxial_experimental))*F12_sem_normalizar 


	fatorRotar_a=2*F12*Math.pow(cos,2)*Math.pow(sin,2) + Math.pow(cos,4)*is1q + Math.pow(cos,2)*Math.pow(sin,2)*t12+ is2q*Math.pow(sin,4)

	fatorRotar_c=+ 2*F12*Math.pow(cos,2)*Math.pow(sin,2) + Math.pow(cos,4)*is2q  + Math.pow(cos,2)*Math.pow(sin,2)*t12 + is1q*Math.pow(sin,4)

	fatorRotar_d=-4*F12*Math.pow(cos,3)*sin*tauXY+ 4*F12*cos*Math.pow(sin,3)*tauXY + 4*Math.pow(cos,3)*is1q*sin*tauXY - 2*Math.pow(cos,3)*sin*t12*tauXY + Math.pow(cos,2)*is1 - 4*cos*is2q*Math.pow(sin,3)*tauXY + 2*cos*Math.pow(sin,3)*t12*tauXY  + is2*Math.pow(sin,2)

	fatorRotar_f=-4*F12*cos*Math.pow(sin,3)*tauXY+4*F12*Math.pow(cos,3)*sin*tauXY-4*Math.pow(cos,3)*is2q*sin*tauXY+2*Math.pow(cos,3)*sin*t12*tauXY+Math.pow(cos,2)*is2+4*cos*is1q*Math.pow(sin,3)*tauXY-2*cos*Math.pow(sin,3)*t12*tauXY+is1*Math.pow(sin,2)

	fatorRotar_b=2*F12* Math.pow(cos,4)+ 2*F12*Math.pow(sin,4) + 2*Math.pow(cos,2)*is1q*Math.pow(sin,2) + 2*Math.pow(cos,2)*is2q*Math.pow(sin,2) - 2*Math.pow(cos,2)*Math.pow(sin,2)*t12

	fatorRotar_g=-1-2*cos*is2*sin*tauXY+4*Math.pow(cos,2)*is1q*Math.pow(sin,2)*Math.pow(tauXY,2) +4*Math.pow(cos,2)*is2q*Math.pow(sin,2)*Math.pow(tauXY,2)-2*Math.pow(cos,2)*Math.pow(sin,2)*t12*Math.pow(tauXY,2) +2*cos*is1*sin*tauXY+Math.pow(sin,4)*t12*Math.pow(tauXY,2)-8*F12*Math.pow(cos,2)*Math.pow(sin,2)*Math.pow(tauXY,2)+Math.pow(cos,4)*t12*Math.pow(tauXY,2)

	global a,c,b,d,f,g

	a=fatorRotar_a
	c=fatorRotar_c
	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=fatorRotar_g

#########################################################################################
# Outubro 15, 2018
# SUPORTE para calculo_envelope
# CAIXAS
# de entrada 
#########################################################################################		

def coletar_numeroPontos(request,numeroPontos_entrada):
	global numeroPontos
	numeroPontos=int(numeroPontos_entrada)

	return HttpResponse("numeroPontos  "+numeroPontos_entrada)


def coletar_biaxial_experimental(request,biaxial_experimental_entrada):	
	global biaxial_experimental_global
	biaxial_experimental_global=float(biaxial_experimental_entrada)


	return HttpResponse("numeroPontos  "+biaxial_experimental_entrada)	

################################## ######################################################################################### 
########    Arquivos MATLAB e GNU
# Segunda 19, 2018. Novembro
################################## ########################################################################################

import datetime

def gerarGNU(request):	
	response = HttpResponse(content_type='text/text')

	nomeTEMPO= datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

	response['Content-Disposition'] = 'attachment; filename="EnvelopesTsaiWu_%s.dat"' % (nomeTEMPO)

#	response['Content-Disposition'] = 'attachment; filename="data.dat"'

# Informações do envelope

	response.write(u'# Arquivo GNU gerado com ajuda do Software MECHG-LAPOL (https://gcomp-srv01.nuvem.ufrgs.br/)\n')
	response.write(u'# Fonte do projeto: https://github.com/julian-gamboa-bahia/android_mestrado\n')
	response.write('\n')
	response.write('\n')
	response.write(GNU_EnvelopeFalhaSaidaJSON)

	return response

#########################################################################################


def adicionar_JSON():
	# Aproveita-se para adicionar os valores de GNU

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):   # TRUE_pontos_x
		valoresX.append([POLIGONO_TRUE_pontos_x[i],POLIGONO_TRUE_pontos_y[i]])
		# para os extremos
		EXTREMOASvaloresX.append(POLIGONO_TRUE_pontos_x[i])
		EXTREMOASvaloresY.append(POLIGONO_TRUE_pontos_y[i])
	#colocamos o valor inicial para fechar		
	print "#colocamos o valor inicial para fechar		"
	if(len(POLIGONO_TRUE_pontos_x)>0):
		valoresX.append([POLIGONO_TRUE_pontos_x[0],POLIGONO_TRUE_pontos_y[0]])

	valoresX.append("null")
	indice=0
# lembrar aqui que pe global mesma
	global GNU_EnvelopeFalhaSaidaJSON
	GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON," # Inicio do Envelope   ","\n"]) 

	for x in valoresX:
		EnvelopeFalhaSaidaJSON.append(valoresX[indice])
		if(valoresX[indice]!="null"):
			GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON,str(valoresX[indice][0]),"    ",str(valoresX[indice][1]),"\n"]) 
		else:
			GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON,"# Fim deste Envelope  ","\n\n\n\n"]) 
		indice=indice+1
	#Nov22		
	dados_coletarENVELOPE_data_JSON()	

#########################################################################################
########    Arquivos MATLAB
# Terça 20, 2018. Novembro

#########################################################################################
#########################################################################################
######################   MATLAB 				########################
#########################################################################################

def matlab(request):
	response = HttpResponse(content_type='text/text')
	nomeTEMPO= datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	
	response['Content-Disposition'] = 'attachment; filename="EnvelopesTsaiWu_%s.txt"' % (nomeTEMPO)

# Informações do envelope

	response.write(u'% Arquivo MATLAB gerado com ajuda do Software MECHG-LAPOL (https://gcomp-srv01.nuvem.ufrgs.br/)\n')
	response.write(u'% Fonte do projeto: https://github.com/julian-gamboa-bahia/codigos_matlab\n')
	response.write('\n')
	response.write('\n')	


	p=Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(global_material))[0]

	SIGMA_T_1=p.SIGMA_T_1
	SIGMA_T_2=p.SIGMA_T_2
	SIGMA_C_1=p.SIGMA_C_1  # Convenio de sinais
	SIGMA_C_2=p.SIGMA_C_2  # Convenio de sinais
	NOME=p.NOME
	TAU12=p.TAU12

	# para construir  a matriz S:
	E1=p.E1
	E2=p.E2
	G12=p.G12
	NU12=p.NU12

	# escrevemos cada propriedade

	response.write('\n')
	response.write('\n%limpamos a memoria\n')
	response.write('clear;\n')
	response.write('clc; \n%Indicando as RESISTENCIAS\n')
	response.write('\nSIGMA_T_1='+str(SIGMA_T_1)+';')
	response.write('\nSIGMA_T_2='+str(SIGMA_T_1)+';')
	response.write('\n')
	response.write('SIGMA_C_1='+str(SIGMA_T_1)+';')
	response.write('\n')
	response.write('SIGMA_C_2='+str(SIGMA_T_1)+';')
	response.write('\n')
	response.write('TAU12='+str(SIGMA_T_1)+';')
	response.write('\n')

	response.write('NOME='+'\''+str(NOME)+'\''+';')
	response.write('\n')
	response.write('anguloDEGREE='+str(global_angulo)+';')
	response.write('\n')
	response.write('tau_xy='+str(tauXY)+';')
	response.write('\n')


	return response

#########################################################################################
# Nov 22, 2018 
#
# Integrando num único 
#
#
#########################################################################################
def coletarENVELOPE_legenda(numero_envelope):
	return response_data['criterio'][int(numero_envelope)]

def coletarENVELOPE_data(numero_envelope):

	return dados_coletarENVELOPE_data[int(numero_envelope)]

def coletar_LIMITES(numero_envelope):
	return LIMITES_coletarENVELOPE[int(numero_envelope)]

#####################################################################################
#  Cuidado
#este 
# dados_coletarENVELOPE_data
#não pode crescer de forma indefinida, quando for zerado por atingir 6 ENVELOPES
#
# Devera ser zerada também
#

def dados_coletarENVELOPE_data_JSON():
	STRING_dados_coletarENVELOPE_data=""

	global minimo_X_coletar_EXTREMOS
	global maximo_X_coletar_EXTREMOS

	global minimo_Y_coletar_EXTREMOS
	global maximo_Y_coletar_EXTREMOS

	if(len(valoresX)>0):
		minimo_X_coletar_EXTREMOS=valoresX[0][0]
		maximo_X_coletar_EXTREMOS=valoresX[0][0]
		minimo_Y_coletar_EXTREMOS=valoresX[0][1]
		maximo_Y_coletar_EXTREMOS=valoresX[0][1]

	indice=0

	for x in valoresX:		
		if(valoresX[indice]!="null"):
			STRING_dados_coletarENVELOPE_data="".join([STRING_dados_coletarENVELOPE_data,"[",str(valoresX[indice][0]),",",str(valoresX[indice][1]),"],"]) 

			if(minimo_X_coletar_EXTREMOS>=valoresX[indice][0]):
				minimo_X_coletar_EXTREMOS=valoresX[indice][0]

			if(maximo_X_coletar_EXTREMOS<=valoresX[indice][0]):
				maximo_X_coletar_EXTREMOS=valoresX[indice][0]

			if(minimo_Y_coletar_EXTREMOS>=valoresX[indice][1]):
				minimo_Y_coletar_EXTREMOS=valoresX[indice][1]

			if(maximo_Y_coletar_EXTREMOS<=valoresX[indice][1]):
				maximo_Y_coletar_EXTREMOS=valoresX[indice][1]
		else:
			STRING_dados_coletarENVELOPE_data="".join([STRING_dados_coletarENVELOPE_data,"null"]) 
		indice=indice+1
	dados_coletarENVELOPE_data.append(STRING_dados_coletarENVELOPE_data)
	LIMITES_coletarENVELOPE.append(indice)

#########################################################################################	
def dimensao_data():	
	return size(valoresX)
#########################################################################################	
def coletar_EXTREMOS(numero_envelope):
	return [minimo_X_coletar_EXTREMOS,maximo_X_coletar_EXTREMOS,minimo_Y_coletar_EXTREMOS,maximo_Y_coletar_EXTREMOS]
#########################################################################################	
#########################################################################################		










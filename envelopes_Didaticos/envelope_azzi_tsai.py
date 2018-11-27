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
# 2) Este critério se diferença do Tsai-Hill por ter uma etapa de filtros.
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
		SIGMA_C_1=-p.SIGMA_C_1  # Convenio de sinais
		SIGMA_C_2=-p.SIGMA_C_2  # Convenio de sinais
		NOME=p.NOME
		TAU12=p.TAU12
	
	# estás informações são usadas para obter os potenciais PONTOS do envelope usando as equações"	

	temporal_criterio=response_data['criterio']	
	LEGENDA_TIPO_ANGULO_MATERIAL="".join([u'Azzi Tsai  , com ângulo (Degree)  ', str(angulo),'   com el material  ',NOME])	

#GNU
	GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON," #  ",LEGENDA_TIPO_ANGULO_MATERIAL,"\n"])

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
	 'hrefs_enderecos':hrefs_enderecos,
	 'tauXY':tauXY,
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
	global numeroPontos
	numeroPontos=55 #coletar_numero_pontos(55);
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)

	global PONTOS_x_forma_polar_conica_elipse
	global PONTOS_y_forma_polar_conica_elipse	
	PONTOS_x_forma_polar_conica_elipse=[]
	PONTOS_y_forma_polar_conica_elipse=[]	
    
#POS POS
	calcular_coeficientesPOSPOS(cos,sin)
	calcula_raios_origem_rotacao_elipse()	
	controle_conica_tipo_elipse()
	forma_polar_conica_elipse()	
	filtro_calculo_conica_POSPOS(angulo,tauXY)

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):
		POLIGONO_TRUE_pontos_x.append(PONTOS_x_forma_polar_conica_elipse[i])
		POLIGONO_TRUE_pontos_y.append(PONTOS_y_forma_polar_conica_elipse[i])
	POLIGONO_TRUE_pontos_x.append(0.0)
	POLIGONO_TRUE_pontos_y.append(0.0)		
#NEG POS	
	calcular_coeficientesNEGPOS(cos,sin)
	calcula_raios_origem_rotacao_elipse()
	controle_conica_tipo_elipse()
	forma_polar_conica_elipse()		

	filtro_calculo_conica_NEGPOS(angulo,tauXY)

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):
		POLIGONO_TRUE_pontos_x.append(PONTOS_x_forma_polar_conica_elipse[i])
		POLIGONO_TRUE_pontos_y.append(PONTOS_y_forma_polar_conica_elipse[i])
	POLIGONO_TRUE_pontos_x.append(0.0)
	POLIGONO_TRUE_pontos_y.append(0.0)		

#MEG NEG	
	calcular_coeficientesNEGNEG(cos,sin)
	calcula_raios_origem_rotacao_elipse()
	controle_conica_tipo_elipse()
	forma_polar_conica_elipse()	

	filtro_calculo_conica_NEGNEG(angulo,tauXY)

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):
		POLIGONO_TRUE_pontos_x.append(PONTOS_x_forma_polar_conica_elipse[i])
		POLIGONO_TRUE_pontos_y.append(PONTOS_y_forma_polar_conica_elipse[i])	
	POLIGONO_TRUE_pontos_x.append(0.0)
	POLIGONO_TRUE_pontos_y.append(0.0)		

#POS NEG		
	calcular_coeficientesPOSNEG(cos,sin)
	calcula_raios_origem_rotacao_elipse()
	controle_conica_tipo_elipse()
	forma_polar_conica_elipse()	

	filtro_calculo_conica_POSNEG(angulo,tauXY)

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):
		POLIGONO_TRUE_pontos_x.append(PONTOS_x_forma_polar_conica_elipse[i])
		POLIGONO_TRUE_pontos_y.append(PONTOS_y_forma_polar_conica_elipse[i])		
	POLIGONO_TRUE_pontos_x.append(0.0)
	POLIGONO_TRUE_pontos_y.append(0.0)		

	adicionar_JSON()


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
		#POLIGONO_TRUE_pontos_x.append(temporal_x)
		#POLIGONO_TRUE_pontos_y.append(temporal_y)
		PONTOS_x_forma_polar_conica_elipse.append(temporal_x)
		PONTOS_y_forma_polar_conica_elipse.append(temporal_y)
    #for

#########################################################################################
# Outubro 15, 2018
# Será preciso calcular 4 vezes os coeficientes das curvas CÔNICAS
#########################################################################################		

def calcular_coeficientesPOSPOS(cos,sin):
	Quadrado_t1=(1/SIGMA_T_1)*(1/SIGMA_T_1);
	Quadrado_t2=(1/SIGMA_T_2)*(1/SIGMA_T_2);
	Quadrado_t12=(1/TAU12)*(1/TAU12);

	fatorRotar_a=Math.pow(cos,4)*Quadrado_t1+ Math.pow(sin,4)*Quadrado_t2- Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 + Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_c=Math.pow(sin,4)*Quadrado_t1 + Math.pow(cos,4)*Quadrado_t2 - Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 + Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_b=- Math.pow(cos,4)*Quadrado_t1 + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 - 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12- Math.pow(sin,4)*Quadrado_t1  + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2

	fatorRotar_d=6*Math.pow(cos,3)*sin*Quadrado_t1*tauXY - 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY - 2*cos*Math.pow(sin,3)*Quadrado_t1*tauXY+ 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY - 4*cos*Math.pow(sin,3)*Quadrado_t2*tauXY

	fatorRotar_f=2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY - 4*Math.pow(cos,3)*sin*Quadrado_t2*tauXY - 2*Math.pow(cos,3)*sin*Quadrado_t1*tauXY+ 6*cos*Math.pow(sin,3)*Quadrado_t1*tauXY - 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY

	factorRotar_g=8*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2+ Math.pow(cos,4)*Quadrado_t12+ Math.pow(sin,4)*Quadrado_t12

#
# Defina-se como glovais com o intuito de ser usadas do mesmo modo que foram usadas nos ESPELHOS javaScript
	global a,c,b,d,f,g

	a=fatorRotar_a
	c=fatorRotar_c
	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)

##################################
##################################
#####################
# Outubro 15, 2018
# Será preciso calcular 4 vezes os coeficientes das curvas CÔNICAS
######################################
###################################################		


def calcular_coeficientesNEGPOS(cos,sin):
	Quadrado_t1=(1/SIGMA_C_1)*(1/SIGMA_C_1)
	Quadrado_t2=(1/SIGMA_T_2)*(1/SIGMA_T_2)
	Quadrado_t12=(1/TAU12)*(1/TAU12)

	fatorRotar_a=Math.pow(cos,4)*Quadrado_t1+ Math.pow(sin,4)*Quadrado_t2- Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 + Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_c=Math.pow(sin,4)*Quadrado_t1 + Math.pow(cos,4)*Quadrado_t2 - Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 + Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_b=- Math.pow(cos,4)*Quadrado_t1 + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 - 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12- Math.pow(sin,4)*Quadrado_t1  + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2

	fatorRotar_d=6*Math.pow(cos,3)*sin*Quadrado_t1*tauXY - 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY - 2*cos*Math.pow(sin,3)*Quadrado_t1*tauXY+ 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY - 4*cos*Math.pow(sin,3)*Quadrado_t2*tauXY

	fatorRotar_f=2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY - 4*Math.pow(cos,3)*sin*Quadrado_t2*tauXY - 2*Math.pow(cos,3)*sin*Quadrado_t1*tauXY+ 6*cos*Math.pow(sin,3)*Quadrado_t1*tauXY - 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY

	factorRotar_g=8*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2+ Math.pow(cos,4)*Quadrado_t12+ Math.pow(sin,4)*Quadrado_t12

	a=fatorRotar_a
	c=fatorRotar_c

	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)

##################################
##################################
#####################
# Outubro 15, 2018
# Será preciso calcular 4 vezes os coeficientes das curvas CÔNICAS
######################################
###################################################	
def calcular_coeficientesNEGNEG(cos,sin):
	Quadrado_t1=(1/SIGMA_C_1)*(1/SIGMA_C_1)
	Quadrado_t2=(1/SIGMA_C_2)*(1/SIGMA_C_2)
	Quadrado_t12=(1/TAU12)*(1/TAU12)


	fatorRotar_a=Math.pow(cos,4)*Quadrado_t1+ Math.pow(sin,4)*Quadrado_t2- Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 + Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_c=Math.pow(sin,4)*Quadrado_t1 + Math.pow(cos,4)*Quadrado_t2 - Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 + Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_b=- Math.pow(cos,4)*Quadrado_t1 + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 - 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12- Math.pow(sin,4)*Quadrado_t1  + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2

	fatorRotar_d=6*Math.pow(cos,3)*sin*Quadrado_t1*tauXY - 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY - 2*cos*Math.pow(sin,3)*Quadrado_t1*tauXY+ 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY - 4*cos*Math.pow(sin,3)*Quadrado_t2*tauXY

	fatorRotar_f=2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY - 4*Math.pow(cos,3)*sin*Quadrado_t2*tauXY - 2*Math.pow(cos,3)*sin*Quadrado_t1*tauXY+ 6*cos*Math.pow(sin,3)*Quadrado_t1*tauXY - 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY

	factorRotar_g=8*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2+ Math.pow(cos,4)*Quadrado_t12+ Math.pow(sin,4)*Quadrado_t12

	a=fatorRotar_a
	c=fatorRotar_c

	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)

##################################
##################################
#####################
# Outubro 15, 2018
# Será preciso calcular 4 vezes os coeficientes das curvas CÔNICAS
######################################
###################################################	
def calcular_coeficientesPOSNEG(cos,sin):
	Quadrado_t1=(1/SIGMA_T_1)*(1/SIGMA_T_1)
	Quadrado_tc=(1/SIGMA_C_1)*(1/SIGMA_C_1)
	Quadrado_t2=(1/SIGMA_C_2)*(1/SIGMA_C_2)
	Quadrado_t12=(1/TAU12)*(1/TAU12)


	fatorRotar_a=Math.pow(cos,4)*Quadrado_t1 + Math.pow(sin,4)*Quadrado_t2 - Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_tc  + Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_c=Math.pow(sin,4)*Quadrado_t1+ Math.pow(cos,4)*Quadrado_t2           - Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_tc+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12

	fatorRotar_b=- Math.pow(cos,4)*Quadrado_tc + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 - 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12 - Math.pow(sin,4)*Quadrado_tc + 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2

	fatorRotar_d=+4*Math.pow(cos,3)*sin*Quadrado_t1*tauXY   + 2*sin*Math.pow(cos,3)*Quadrado_tc*tauXY  - 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY - 2*cos*Math.pow(sin,3)*Quadrado_tc*tauXY  + 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY - 4*cos*Math.pow(sin,3)*Quadrado_t2*tauXY

	fatorRotar_f=2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY      - 4*Math.pow(cos,3)*sin*Quadrado_t2*tauXY     - 2*Math.pow(cos,3)*sin*Quadrado_tc*tauXY     + 4*cos*Math.pow(sin,3)*Quadrado_t1*tauXY     + 2*cos*Math.pow(sin,3)*Quadrado_tc*tauXY     - 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY

	factorRotar_g=4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1+4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_tc- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2+ Math.pow(cos,4)*Quadrado_t12+ Math.pow(sin,4)*Quadrado_t12

	a=fatorRotar_a
	c=fatorRotar_c

	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)


#########################################################################################
# Outubro 15, 2018
# Filtros para poder integrar o envelope
#########################################################################################	

def filtro_calculo_conica_POSPOS(angulo,tau_xy):
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]

	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):		#$(i=0;i<pares_pontos_x.length;i++)
		pares_pontos_locais_1.append(c2*PONTOS_x_forma_polar_conica_elipse[i]+s2*PONTOS_y_forma_polar_conica_elipse[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*PONTOS_x_forma_polar_conica_elipse[i]+c2*PONTOS_y_forma_polar_conica_elipse[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*PONTOS_x_forma_polar_conica_elipse[i]+sin*cos*PONTOS_y_forma_polar_conica_elipse[i]+(c2-s2)*tau_xy)
#Filtragem em coordenadas locais

#//   Para valores de X

	for i in range(0,len(pares_pontos_locais_1)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]<0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//   Para valores de Y
	for i in range(0,len(pares_pontos_locais_2)):	#for(i=0;i<pares_pontos_locais_2.length;i++)
		if(pares_pontos_locais_2[i]<0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del PONTOS_x_forma_polar_conica_elipse[:]
	del PONTOS_y_forma_polar_conica_elipse[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			PONTOS_x_forma_polar_conica_elipse.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			PONTOS_y_forma_polar_conica_elipse.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])


##################################
##################################
#####################
# Outubro 15, 2018
# Será preciso calcular 4 vezes os coeficientes das curvas CÔNICAS
######################################
###################################################	
def filtro_calculo_conica_NEGPOS(angulo,tau_xy):
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]

	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):		#$(i=0;i<pares_pontos_x.length;i++)
		pares_pontos_locais_1.append(c2*PONTOS_x_forma_polar_conica_elipse[i]+s2*PONTOS_y_forma_polar_conica_elipse[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*PONTOS_x_forma_polar_conica_elipse[i]+c2*PONTOS_y_forma_polar_conica_elipse[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*PONTOS_x_forma_polar_conica_elipse[i]+sin*cos*PONTOS_y_forma_polar_conica_elipse[i]+(c2-s2)*tau_xy)
#Filtragem em coordenadas locais

#//   Para valores de X

	for i in range(0,len(pares_pontos_locais_1)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]>0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//   Para valores de Y
	for i in range(0,len(pares_pontos_locais_2)):	#for(i=0;i<pares_pontos_locais_2.length;i++)
		if(pares_pontos_locais_2[i]<0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del PONTOS_x_forma_polar_conica_elipse[:]
	del PONTOS_y_forma_polar_conica_elipse[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			PONTOS_x_forma_polar_conica_elipse.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			PONTOS_y_forma_polar_conica_elipse.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])			

##################################
##################################
#####################
# Outubro 15, 2018
# Será preciso calcular 4 vezes os coeficientes das curvas CÔNICAS
######################################
###################################################	
def filtro_calculo_conica_NEGNEG(angulo,tau_xy):
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]

	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):		#$(i=0;i<pares_pontos_x.length;i++)
		pares_pontos_locais_1.append(c2*PONTOS_x_forma_polar_conica_elipse[i]+s2*PONTOS_y_forma_polar_conica_elipse[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*PONTOS_x_forma_polar_conica_elipse[i]+c2*PONTOS_y_forma_polar_conica_elipse[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*PONTOS_x_forma_polar_conica_elipse[i]+sin*cos*PONTOS_y_forma_polar_conica_elipse[i]+(c2-s2)*tau_xy)
#Filtragem em coordenadas locais

#//   Para valores de X

	for i in range(0,len(pares_pontos_locais_1)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]>0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//   Para valores de Y
	for i in range(0,len(pares_pontos_locais_2)):	#for(i=0;i<pares_pontos_locais_2.length;i++)
		if(pares_pontos_locais_2[i]>0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del PONTOS_x_forma_polar_conica_elipse[:]
	del PONTOS_y_forma_polar_conica_elipse[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			PONTOS_x_forma_polar_conica_elipse.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			PONTOS_y_forma_polar_conica_elipse.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])			


##################################
##################################
#####################
# Outubro 15, 2018
# Será preciso calcular 4 vezes os coeficientes das curvas CÔNICAS
######################################
###################################################	
def filtro_calculo_conica_POSNEG(angulo,tau_xy):
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]

	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(PONTOS_x_forma_polar_conica_elipse)):		#$(i=0;i<pares_pontos_x.length;i++)
		pares_pontos_locais_1.append(c2*PONTOS_x_forma_polar_conica_elipse[i]+s2*PONTOS_y_forma_polar_conica_elipse[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*PONTOS_x_forma_polar_conica_elipse[i]+c2*PONTOS_y_forma_polar_conica_elipse[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*PONTOS_x_forma_polar_conica_elipse[i]+sin*cos*PONTOS_y_forma_polar_conica_elipse[i]+(c2-s2)*tau_xy)
#Filtragem em coordenadas locais

#//   Para valores de X

	for i in range(0,len(pares_pontos_locais_1)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]<0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//   Para valores de Y
	for i in range(0,len(pares_pontos_locais_2)):	#for(i=0;i<pares_pontos_locais_2.length;i++)
		if(pares_pontos_locais_2[i]>0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"
#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del PONTOS_x_forma_polar_conica_elipse[:]
	del PONTOS_y_forma_polar_conica_elipse[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			PONTOS_x_forma_polar_conica_elipse.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			PONTOS_y_forma_polar_conica_elipse.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])			



#########################################################################################
# Outubro 15, 2018
#filtro de Distâncias
#########################################################################################	

def filtro_distancia():
	distancias=[]
	anterior_x=POLIGONO_TRUE_pontos_x[0]
	anterior_y=POLIGONO_TRUE_pontos_y[0]

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):#(i=0;i<pares_pontos_x.length-1;i++)	
		delta_x=Math.pow((anterior_x-POLIGONO_TRUE_pontos_x[i]),2)
		delta_y=Math.pow((anterior_y-POLIGONO_TRUE_pontos_y[i]),2)
		tempDISTANCIA=Math.sqrt(delta_x+delta_y)
		distancias.append(tempDISTANCIA)
		anterior_x=POLIGONO_TRUE_pontos_x[i]
		anterior_y=POLIGONO_TRUE_pontos_y[i]
#//calculamos a media
		soma=0

	for i in range(0,len(distancias)):#(i=0;i<distancias.length;i++)	
		soma=soma+distancias[i]
#//colocamos apenas aqueles que sejam proximos)
	media=(soma/len(distancias))
	for i in range(0,len(distancias)):
		if(Math.fabs(distancias[i]-media)>(media/1)):
			POLIGONO_TRUE_pontos_x[i]=0.0
			POLIGONO_TRUE_pontos_y[i]=0.0

################################## ######################################################################################### 
########    Arquivos MATLAB e GNU
# Segunda 19, 2018. Novembro
################################## ########################################################################################

import datetime

def gerarGNU(request):	
	response = HttpResponse(content_type='text/text')

	nomeTEMPO= datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

	response['Content-Disposition'] = 'attachment; filename="EnvelopesAzziTsai_%s.dat"' % (nomeTEMPO)

#	response['Content-Disposition'] = 'attachment; filename="data.dat"'

# Informações do envelope

	response.write(u'# Arquivo GNU gerado com ajuda do Software MECHG-LAPOL (https://gcomp-srv01.nuvem.ufrgs.br/)\n')
	response.write(u'# Fonte do projeto: https://github.com/julian-gamboa-bahia/android_mestrado\n')
	response.write('\n')
	response.write('\n')
	response.write(GNU_EnvelopeFalhaSaidaJSON)

	return response

#########################################################################################
# Outubro 06, 2018
#
#########################################################################################	


def adicionar_JSON():

	# lembrar aqui que pe global mesma
	global GNU_EnvelopeFalhaSaidaJSON
	GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON," # Inicio do Envelope   ","\n"]) 

	filtro_distancia()

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):   # TRUE_pontos_x
		if((POLIGONO_TRUE_pontos_x[i]!=0.0) and (POLIGONO_TRUE_pontos_y[i]!=0.0)):
			valoresX.append([POLIGONO_TRUE_pontos_x[i],POLIGONO_TRUE_pontos_y[i]])
			# para os extremos
			EXTREMOASvaloresX.append(POLIGONO_TRUE_pontos_x[i])
			EXTREMOASvaloresY.append(POLIGONO_TRUE_pontos_y[i])
		else:
			valoresX.append("null")
	#colocamos o valor inicial para fechar		
	
	if(len(POLIGONO_TRUE_pontos_x)>0):		
		valoresX.append([POLIGONO_TRUE_pontos_x[0],POLIGONO_TRUE_pontos_y[0]])

	valoresX.append("null")
	indice=0
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
	
	response['Content-Disposition'] = 'attachment; filename="EnvelopesAzziTsai_%s.txt"' % (nomeTEMPO)

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
			STRING_dados_coletarENVELOPE_data="".join([STRING_dados_coletarENVELOPE_data,"null,"]) 
		indice=indice+1

	temp=STRING_dados_coletarENVELOPE_data[:-1]

	dados_coletarENVELOPE_data.append(temp)
	LIMITES_coletarENVELOPE.append(indice)

#########################################################################################	
def dimensao_data():	
	return size(valoresX)
#########################################################################################	
def coletar_EXTREMOS(numero_envelope):
	return [minimo_X_coletar_EXTREMOS,maximo_X_coletar_EXTREMOS,minimo_Y_coletar_EXTREMOS,maximo_Y_coletar_EXTREMOS]
#########################################################################################	
#########################################################################################		




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
	global angulo_global
	angulo_global=float(angulo)

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
	LEGENDA_TIPO_ANGULO_MATERIAL="".join([u'Hashin  , com ângulo (Degree)  ', str(angulo),'   com el material  ',NOME])	
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
	temp=POLIGONO_TRUE_pontos_y[0]
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
	temp=POLIGONO_TRUE_pontos_y[0]
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

	temp=POLIGONO_TRUE_pontos_x[0]
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

	temp=POLIGONO_TRUE_pontos_x[0]
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

def calculo_envelopeANTIGO(angulo):	
	#global numeroPontos
	#numeroPontos=55 #coletar_numero_pontos(55);
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
    

	calcular_coeficientes(cos,sin)
	if(controle_conica_tipo_elipse()=="elipse"):
		calcula_raios_origem_rotacao_elipse()
		forma_polar_conica_elipse()	
		adicionar_JSON()
	else:
		POLIGONO_TRUE_pontos_x.append(0.0)
		POLIGONO_TRUE_pontos_y.append(0.0)


def calculo_envelope(angulo):	
	#global numeroPontos
	#numeroPontos=55 #coletar_numero_pontos(55);
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
    
	if((angulo%90)==0):
		if(calcular_apenas_4_vertices(angulo,tauXY)=="raiz_imaginaria"):
			POLIGONO_TRUE_pontos_x.append(0.0)
			POLIGONO_TRUE_pontos_y.append(0.0)
	else:
		calcular_conicas(angulo,tauXY)
	adicionar_JSON()



#########################################################################################
# Outubro 08, 2018
# SUPORTE para calculo_envelope
#########################################################################################		


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

def coletar_TAU23(request,TAU23_entrada):	
	global TAU23_global
	TAU23_global=float(TAU23_entrada)
	return HttpResponse("TAU23_global  "+TAU23_entrada)		

#########################################################################################
# Outubro 08, 2018
# SUPORTE para calculo_envelope
#########################################################################################		

def controle_conica_tipo_elipse():
	a_f=a
	b_f=b
	c_f=c
	d_f=d
	f_f=f
	g_f=g
#Usamos um conjunto de funcoes para facilitar estas determinantes
	delta=calcular_delta(a_f,b_f,c_f,d_f,f_f,g_f)
	I=a_f+c_f
	J=calcular_J(a_f,b_f,c_f,d_f,f_f,g_f)
	K=calcular_K(a_f,b_f,c_f,d_f,f_f,g_f)

	tipo_conica="nao_determinado"

	if((delta!=0)and (J>0) and ((delta/I)<0)):
		tipo_conica="elipse"
	if((delta!=0) and(J==0)):
		tipo_conica="parabola"
	if((delta!=0) and (J<0)):
		tipo_conica="hyperbola"
	if((delta==0) and (J==0)):
		tipo_conica="paralelas_real"	
	if((delta==0) and (J>0) and (K>0)):
		tipo_conica="linhas_intersection_imaginarias"
	if((delta==0) and (J<0) and (K<0)):
		tipo_conica="linhas_intersection_real"
	if((delta==0) and (J<0) and (K==0)):
		tipo_conica="linhas_concidentes"
	return tipo_conica

#//matriz de 3x3

def calcular_delta(a,b,c,d,f,g):
	return 	(a*c*g-a*Math.pow(f,2) - Math.pow(b,2)*g + 2*b*d*f - c*Math.pow(d,2))

#Matriz de 2x2

def calcular_J(a,b,c,d,f,g):
	return 	(a*c - Math.pow(b,2))

#	(Matriz de 2x2)+(Matriz de 2x2)

def calcular_K(a,b,c,d,f,g):
	return 	(a*g + c*g - Math.pow(d,2) - Math.pow(f,2))


#########################################################################################
# Outubro 26, 2018
#########################################################################################		
def calcular_apenas_4_vertices(angulo,tauXY):
	theta_radianos=(Math.pi/180)*angulo
	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	TAU23=TAU23_global#coletar_TAU23(TAU12);
	resolvente_quadratica_termo_a=Math.pow((1.0/(2.0*TAU23)),2)
	termoTAU23=Math.pow((SIGMA_C_2/(2.0*TAU23)),2)
	resolvente_quadratica_termo_b=(1.0/(SIGMA_C_2))*(termoTAU23-1)
	a=resolvente_quadratica_termo_a
	b=resolvente_quadratica_termo_b
	radicando=(Math.pow(b,2))-4*a*(-1.0)
	if(radicando>=0):	
		preROOT_1=+Math.sqrt(radicando)
		preROOT_2=-Math.sqrt(radicando)
		ROOT_1=(-b+preROOT_1)/(2.0*a)
		ROOT_2=(-b+preROOT_2)/(2.0*a)	
		if(ROOT_1<=0):
			raiz_de_interesse=ROOT_1
		if(ROOT_2<=0):
			raiz_de_interesse=ROOT_2
	else:
		return "raiz_imaginaria"

	SIGMA_C_2_raiz=raiz_de_interesse


#Com apenas  tau_xy NULO

	if(tauXY==0):
		SIGMA_T_1_rotacionado=c2*SIGMA_T_1+s2*SIGMA_T_2
		SIGMA_T_2_rotacionado=s2*SIGMA_T_1+c2*SIGMA_T_2

		SIGMA_C_1_rotacionado=c2*(-SIGMA_C_1)+s2*(SIGMA_C_2_raiz)
		SIGMA_C_2_rotacionado=s2*(-SIGMA_C_1)+c2*(SIGMA_C_2_raiz)
	else:
#Com tau_xy VIVO Devem ser feitos mais calculos
		resolvente_quadratica_termo_a=Math.pow((1.0/(SIGMA_T_1)),2)
		normalizado_tau12=(tauXY/TAU12)
		resolvente_quadratica_termo_c=-1.0+Math.pow(normalizado_tau12,2)
		a=resolvente_quadratica_termo_a
		b=0.0
		c=resolvente_quadratica_termo_c
		radicando=-4*a*c

		if(radicando>=0):
			preROOT_1=+Math.sqrt(radicando)
			preROOT_2=-Math.sqrt(radicando)
			ROOT_1=(preROOT_1)/(2.0*a)
			ROOT_2=(preROOT_2)/(2.0*a)
		#A raíz negativa será considerada como a raíz de interesse
			if(ROOT_1>=0):
				raiz_de_interesse=ROOT_1
			if(ROOT_2>=0):
				raiz_de_interesse=ROOT_2			
		else:
			return "raiz_imaginaria"

		SIGMA_T_1_raiz=raiz_de_interesse
#Parte SIGMA_2 positivo
		resolvente_quadratica_termo_a=Math.pow((1.0/(SIGMA_T_2)),2)
		normalizado_tau12=(tauXY/TAU12)
		resolvente_quadratica_termo_c=-1.0+Math.pow(normalizado_tau12,2)
		a=resolvente_quadratica_termo_a
		b=0.0
		c=resolvente_quadratica_termo_c
		radicando=-4*a*c

		if(radicando>=0):
			preROOT_1=+Math.sqrt(radicando)
			preROOT_2=-Math.sqrt(radicando)
			ROOT_1=(preROOT_1)/(2.0*a)
			ROOT_2=(preROOT_2)/(2.0*a)		
		#A raíz negativa será considerada como a raíz de interesse
			if(ROOT_1>=0):
				raiz_de_interesse=ROOT_1
			if(ROOT_2>=0):
				raiz_de_interesse=ROOT_2
		else:
			return "raiz_imaginaria"
		
		SIGMA_T_2_raiz=raiz_de_interesse;

		TAU23=TAU23_global#coletar_TAU23(TAU12);
		resolvente_quadratica_termo_a=Math.pow((1.0/(2.0*TAU23)),2)
		termoTAU23=Math.pow((SIGMA_C_2/(2.0*TAU23)),2)
		resolvente_quadratica_termo_b=(1.0/(SIGMA_C_2))*(termoTAU23-1)
		a=resolvente_quadratica_termo_a
		b=resolvente_quadratica_termo_b
		radicando=(Math.pow(b,2))-4*a*(-1.0)
		if(radicando>=0):
			preROOT_1=+Math.sqrt(radicando)
			preROOT_2=-Math.sqrt(radicando)
			ROOT_1=(-b+preROOT_1)/(2.0*a)
			ROOT_2=(-b+preROOT_2)/(2.0*a)

		#A raíz negativa será considerada como a raíz de interesse
			if(ROOT_1<=0):
				raiz_de_interesse=ROOT_1
			if(ROOT_2<=0):
				raiz_de_interesse=ROOT_2
		else:
			return "raiz_imaginaria"		
		SIGMA_C_2_raiz=raiz_de_interesse

		SIGMA_T_1_rotacionado=c2*SIGMA_T_1_raiz+s2*SIGMA_T_2_raiz
		SIGMA_T_2_rotacionado=s2*SIGMA_T_1_raiz+c2*SIGMA_T_2_raiz

		SIGMA_C_1_rotacionado=c2*(-SIGMA_C_1)+s2*(SIGMA_C_2_raiz)		
		SIGMA_C_2_rotacionado=s2*(-SIGMA_C_1)+c2*(SIGMA_C_2_raiz)


#vertice + +
	POLIGONO_TRUE_pontos_x.append(SIGMA_T_1_rotacionado)
	POLIGONO_TRUE_pontos_y.append(SIGMA_T_2_rotacionado)

#vertice - +
	POLIGONO_TRUE_pontos_x.append(SIGMA_C_1_rotacionado)
	POLIGONO_TRUE_pontos_y.append(SIGMA_T_2_rotacionado)

#vertice --
	POLIGONO_TRUE_pontos_x.append(SIGMA_C_1_rotacionado)
	POLIGONO_TRUE_pontos_y.append(SIGMA_C_2_rotacionado)

#vertice + -
	POLIGONO_TRUE_pontos_x.append(SIGMA_T_1_rotacionado)
	POLIGONO_TRUE_pontos_y.append(SIGMA_C_2_rotacionado)

#########################################################################################
# Outubro Sábado 27, 2018
#
# São gerados por partes: TRACAO_FIBRA
#
#
#########################################################################################		
def calcular_conicas(angulo,tau_xy):
	tolerancia=0.01
#TRACAO_FIBRA
	theta_radianos=(Math.pi/180)*angulo
	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	pares_pontos_temp_x=[]
	pares_pontos_temp_y=[]
# 1) 
	gerador_TRACAO_FIBRA(cos,sin,tau_xy)
	numero_pontos_if_unitario=0

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		indice_temp=criterio_puro(POLIGONO_TRUE_pontos_x[i],POLIGONO_TRUE_pontos_y[i],tau_xy,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
		if((indice_temp<(1+tolerancia)) and (indice_temp>(1-tolerancia))):
			pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
			pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			
			numero_pontos_if_unitario=numero_pontos_if_unitario+1
#2) TRACAO_MATRIZ
	gerador_TRACAO_MATRIZ(cos,sin,tau_xy)
	numero_pontos_if_unitario=0			

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		indice_temp=criterio_puro(POLIGONO_TRUE_pontos_x[i],POLIGONO_TRUE_pontos_y[i],tau_xy,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)

		if((indice_temp<(1+tolerancia)) and (indice_temp>(1-tolerancia))):
			pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
			pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			
			numero_pontos_if_unitario=numero_pontos_if_unitario+1				


# 3) COMPRESSAO_MATRIZ

	gerador_COMPRESSAO_MATRIZ(cos,sin,tau_xy)
	numero_pontos_if_unitario=0

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		indice_temp=criterio_puro(POLIGONO_TRUE_pontos_x[i],POLIGONO_TRUE_pontos_y[i],tau_xy,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)

		if((indice_temp<(1+tolerancia)) and (indice_temp>(1-tolerancia))):
			pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
			pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			
			numero_pontos_if_unitario=numero_pontos_if_unitario+1	

#COMPRESSAO_FIBRA

	gerador_COMPRESSAO_FIBRA(cos,sin,tau_xy)
	numero_pontos_if_unitario=0

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		indice_temp=criterio_puro(POLIGONO_TRUE_pontos_x[i],POLIGONO_TRUE_pontos_y[i],tau_xy,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)		
		if((indice_temp<(1+tolerancia)) and (indice_temp>(1-tolerancia))):
			pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
			pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			
			numero_pontos_if_unitario=numero_pontos_if_unitario+1	


	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]	

	for i in range(0,len(pares_pontos_temp_x)):
		POLIGONO_TRUE_pontos_x.append(pares_pontos_temp_x[i])
		POLIGONO_TRUE_pontos_y.append(pares_pontos_temp_y[i])


#########################################################################################
# Outubro Sábado 27, 2018
#
# São gerados por partes: TRACAO_FIBRA
#
#
#########################################################################################		
def calcular_conicas_SEM_FILTRADO(angulo,tau_xy):
	tolerancia=0.01
#TRACAO_FIBRA
	theta_radianos=(Math.pi/180)*angulo
	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	pares_pontos_temp_x=[]
	pares_pontos_temp_y=[]
# 1) 
	gerador_TRACAO_FIBRA(cos,sin,tau_xy)
	numero_pontos_if_unitario=0

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):				
		pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
		pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			

#2) TRACAO_MATRIZ
	gerador_TRACAO_MATRIZ(cos,sin,tau_xy)
	numero_pontos_if_unitario=0			

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):				
		pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
		pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			


# 3) COMPRESSAO_MATRIZ

	gerador_COMPRESSAO_MATRIZ(cos,sin,tau_xy)
	numero_pontos_if_unitario=0

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):				
		pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
		pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			

#COMPRESSAO_FIBRA

	gerador_COMPRESSAO_FIBRA(cos,sin,tau_xy)
	numero_pontos_if_unitario=0

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):				
		pares_pontos_temp_x.append(POLIGONO_TRUE_pontos_x[i])
		pares_pontos_temp_y.append(POLIGONO_TRUE_pontos_y[i])			


	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]	

	for i in range(0,len(pares_pontos_temp_x)):
		POLIGONO_TRUE_pontos_x.append(pares_pontos_temp_x[i])
		POLIGONO_TRUE_pontos_y.append(pares_pontos_temp_y[i])



######################################
# Outubro Sábado 27, 2018
#
#Suporte de calcular_conicas
#
#
######################################
def gerador_COMPRESSAO_FIBRA(cos,sin,tau_xy):
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]	
	calcular_coeficientesCOMPRESSAO_FIBRA(cos,sin)
	conica=controle_conica_tipo_elipse()
	if(conica=="elipse"):
		gerar_pontos()		
	if(conica=="hyperbola"):
		gerar_pontos_hyberpola()

	filtro_calculo_conica_COMPRESSAO_FIBRA(angulo_global,tau_xy)


######################################
# Outubro Sábado 27, 2018
#
#Suporte de calcular_conicas
#
#
######################################
def gerador_COMPRESSAO_MATRIZ(cos,sin,tau_xy):
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]	
	calcular_coeficientesCOMPRESSAO_MATRIZ(cos,sin)
	conica=controle_conica_tipo_elipse()
	if(conica=="elipse"):
		gerar_pontos()		
	if(conica=="hyperbola"):
		gerar_pontos_hyberpola()

	filtro_calculo_conica_COMPRESSAO_MATRIZ(angulo_global,tau_xy)

######################################
# Outubro Sábado 27, 2018
#
#Suporte de calcular_conicas
#
#
######################################
def gerador_TRACAO_MATRIZ(cos,sin,tau_xy):
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]
	calcular_coeficientes_MATRIZ_TRACAO(cos,sin)
	conica=controle_conica_tipo_elipse()
	if(conica=="elipse"):
		gerar_pontos()		
	if(conica=="hyperbola"):
		gerar_pontos_hyberpola()

	filtro_calculo_conica_TRACAO_MATRIZ(angulo_global,tau_xy)	

######################################
# Outubro Sábado 27, 2018
#
#Suporte de calcular_conicas
#
#
######################################
def gerador_TRACAO_FIBRA(cos,sin,tau_xy):
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]
	calcular_coeficientesTRACA_OFIBRA(cos,sin)
	conica=controle_conica_tipo_elipse()
	if(conica=="elipse"):
		gerar_pontos()
	if(conica=="hyperbola"):
		gerar_pontos_hyberpola()
	filtro_calculo_conica_TRACA_OFIBRA(angulo_global,tau_xy)	


###################################### 	
# Outubro Sábado 27, 2018
#
#Suporte de calcular_conicas
#
#
######################################
def calcular_coeficientesTRACA_OFIBRA(cos,sin):
	Quadrado_t1=(1/SIGMA_T_1)*(1/SIGMA_T_1)
	Quadrado_t2=(1/SIGMA_T_2)*(1/SIGMA_T_2)
	Quadrado_t12=(1/TAU12)*(1/TAU12)

	fatorRotar_a=- Math.pow(cos,4)*Quadrado_t1+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_c=Math.pow(sin,4)*Quadrado_t1+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_b=+ 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 - 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_d=4*Math.pow(cos,3)*sin*Quadrado_t1*tauXY- 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY+ 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY

	fatorRotar_f=4*Math.pow(sin,3)*cos*Quadrado_t1*tauXY- 2*Math.pow(sin,3)*cos*Quadrado_t12*tauXY+ 2*sin*Math.pow(cos,3)*Quadrado_t12*tauXY

	factorRotar_g=4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12	+ Math.pow(cos,4)*Quadrado_t12+ Math.pow(sin,4)*Quadrado_t12

	global a,c,b,d,f,g
	a=fatorRotar_a
	c=fatorRotar_c
	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)


######################################
# Outubro Sábado 27, 2018
#
#Suporte de calcular_conicas
######################################

def calcular_coeficientesCOMPRESSAO_FIBRA(cos,sin):
	Quadrado_t1=(1/SIGMA_C_1)*(1/SIGMA_C_1)
	Quadrado_t2=(1/SIGMA_T_2)*(1/SIGMA_T_2)
	Quadrado_t12=(1/TAU12)*(1/TAU12)

	fatorRotar_a=- Math.pow(cos,4)*Quadrado_t1+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_c=Math.pow(sin,4)*Quadrado_t1+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_b=+ 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1 - 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_d=4*Math.pow(cos,3)*sin*Quadrado_t1*tauXY- 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY+ 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY
	fatorRotar_f=4*Math.pow(sin,3)*cos*Quadrado_t1*tauXY- 2*Math.pow(sin,3)*cos*Quadrado_t12*tauXY+ 2*sin*Math.pow(cos,3)*Quadrado_t12*tauXY
	factorRotar_g=4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t1- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ Math.pow(cos,4)*Quadrado_t12+ Math.pow(sin,4)*Quadrado_t12

	global a,c,b,d,f,g
	a=fatorRotar_a
	c=fatorRotar_c
	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)

######################################
# Outubro Sábado 27, 2018
##Suporte de calcular_conicas
######################################
def calcular_coeficientes_MATRIZ_TRACAO(cos,sin):
	Quadrado_t1=(1/SIGMA_T_1)*(1/SIGMA_T_1)
	Quadrado_tc=(1/SIGMA_C_1)*(1/SIGMA_C_1)
	Quadrado_t2=(1/SIGMA_C_2)*(1/SIGMA_C_2)
	Quadrado_t12=(1/TAU12)*(1/TAU12)

	fatorRotar_a=+ Math.pow(sin,4)*Quadrado_t2+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_c=+ Math.pow(cos,4)*Quadrado_t2+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_b=- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2
	fatorRotar_d=- 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY+ 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY- 4*cos*Math.pow(sin,3)*Quadrado_t2*tauXY
	fatorRotar_f=- 2*Math.pow(sin,3)*cos*Quadrado_t12*tauXY+ 2*sin*Math.pow(cos,3)*Quadrado_t12*tauXY- 4*sin*Math.pow(cos,3)*Quadrado_t2*tauXY
	factorRotar_g=- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2+ Math.pow(cos,4)*Quadrado_t12+ Math.pow(sin,4)*Quadrado_t12

	global a,c,b,d,f,g
	a=fatorRotar_a
	c=fatorRotar_c
	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)

######################################
# Outubro Sábado 27, 2018
#Suporte de calcular_conicas
#
######################################
def calcular_coeficientesCOMPRESSAO_MATRIZ(cos,sin):
	TAU23=TAU23_global
	Quadrado_t2=Math.pow((1/(2*TAU23)),2)
	coeficiente=(SIGMA_C_2/(2*TAU23))
	Simples_t2=(-1+Math.pow(coeficiente,2))*(1/SIGMA_C_2);
	Quadrado_t12=(1/TAU12)*(1/TAU12)

	fatorRotar_a=+ Math.pow(sin,4)*Quadrado_t2+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_c=+ Math.pow(cos,4)*Quadrado_t2+ Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12
	fatorRotar_b=- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2
	fatorRotar_d=- 2*Math.pow(cos,3)*sin*Quadrado_t12*tauXY+Math.pow(sin,2)*Simples_t2*tauXY+ 2*cos*Math.pow(sin,3)*Quadrado_t12*tauXY- 4*cos*Math.pow(sin,3)*Quadrado_t2*tauXY
	fatorRotar_f=- 2*Math.pow(sin,3)*cos*Quadrado_t12*tauXY+Math.pow(cos,2)*Simples_t2+ 2*sin*Math.pow(cos,3)*Quadrado_t12*tauXY- 4*sin*Math.pow(cos,3)*Quadrado_t2*tauXY
	factorRotar_g=-2*cos*sin*Simples_t2*tauXY- 2*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t12+ 4*Math.pow(cos,2)*Math.pow(sin,2)*Quadrado_t2+ Math.pow(sin,4)*Quadrado_t12+ Math.pow(cos,4)*Quadrado_t12;                

	global a,c,b,d,f,g
	a=fatorRotar_a
	c=fatorRotar_c
	b=(fatorRotar_b/2)
	d=(fatorRotar_d/2)
	f=(fatorRotar_f/2)
	g=-1+factorRotar_g*(tauXY*tauXY)

######################################
# Outubro Sábado 27, 2018
#Suporte de calcular_conicas
#
######################################

def gerar_pontos_hyberpola():
	origem_x=0.0
	origem_y=0.0

	gerar_pontos_hyberpola_D=calcular_J(a,b,c,d,f,g)
	centro_hyper_x=-(1.0/gerar_pontos_hyberpola_D)*(d*c-f*b)
	centro_hyper_y=-(1.0/gerar_pontos_hyberpola_D)*(a*f-d*b)

	termo_b=a+c
	lambda_1=termo_b+Math.sqrt(Math.pow(termo_b,2)-4*gerar_pontos_hyberpola_D)
	lambda_1=lambda_1/2
	lambda_2=termo_b-Math.sqrt(Math.pow(termo_b,2)-4*gerar_pontos_hyberpola_D)
	lambda_2=lambda_2/2
	
	gerar_pontos_hyberpola_Delta=calcular_delta(a,b,c,d,f,g)

	Quadrado_eixo_a=-(gerar_pontos_hyberpola_Delta/gerar_pontos_hyberpola_D)*(1/lambda_1)
	Quadrado_eixo_b=-(gerar_pontos_hyberpola_Delta/gerar_pontos_hyberpola_D)*(1/lambda_2)

	eixo_horizontal=0.0
	eixo_vertical=0.0

	if(Quadrado_eixo_a>0):
		eixo_horizontal=Math.sqrt(Quadrado_eixo_a)
	else:
		if(Quadrado_eixo_b>0):
			eixo_horizontal=Math.sqrt(Quadrado_eixo_b)
#menor
	if(Quadrado_eixo_b<0):
		eixo_vertical=Math.sqrt(-Quadrado_eixo_b)
	else:
		if(Quadrado_eixo_a<0):
			eixo_vertical=Math.sqrt(-Quadrado_eixo_a)

#ngulo de rotacao desta hyperbola
	anguloHYPERBOLA=0.5*Math.atan((2*b)/(a-c))

#geramos os pontos
	ang=-Math.pi
	passo=(2*Math.pi/numeroPontos)

#Fazemos a varredura de Izquerda para DIREITA , desde 0 para 2*Pi
	for i in range(0,numeroPontos):
		if(ang!=(Math.pi/2)):
			cos=Math.cos(ang)
			sin=Math.sin(ang)

			x=eixo_horizontal*(Math.cosh(ang))
			y=eixo_vertical*Math.sinh(ang)

			# aplicamos uma rotação de euler:

			temporal_x=x*Math.cos(anguloHYPERBOLA)-y*Math.sin(anguloHYPERBOLA);
			temporal_y=x*Math.sin(anguloHYPERBOLA)+y*Math.cos(anguloHYPERBOLA);

			# Origem
			if (origem_x!=0):
				temporal_x=temporal_x+centro_hyper_x		
			if (origem_y!=0):
				temporal_y=temporal_y+centro_hyper_y

			POLIGONO_TRUE_pontos_x.append(temporal_x);
			POLIGONO_TRUE_pontos_y.append(temporal_y);
		ang=ang+passo

#Outra rama
#geramos os pontos
	ang=-Math.pi
	passo=(2*Math.pi/numeroPontos)

#Fazemos a varredura de Izquerda para DIREITA , desde 0 para 2*Pi

	for i in range(0,numeroPontos):#(i=0;i<numeroPontos;i++)    
		if(ang!=(Math.pi/2)):
			cos=Math.cos(ang)
			sin=Math.sin(ang)
			x=-eixo_horizontal*(Math.cosh(ang))
			y=eixo_vertical*Math.sinh(ang)

			# aplicamos uma rotação de euler:

			temporal_x=x*Math.cos(anguloHYPERBOLA)-y*Math.sin(anguloHYPERBOLA)
			temporal_y=x*Math.sin(anguloHYPERBOLA)+y*Math.cos(anguloHYPERBOLA)

			# Origem
			if (origem_x!=0):
				temporal_x=temporal_x+centro_hyper_x
			if (origem_y!=0):
				temporal_y=temporal_y+centro_hyper_y

			POLIGONO_TRUE_pontos_x.append(temporal_x);
			POLIGONO_TRUE_pontos_y.append(temporal_y);
		ang=ang+passo


######################################
# Outubro Sábado 27, 2018
#Suporte de calcular_conicas
#
# Filtro Simples
#
####################################

def filtro_calculo_conica_COMPRESSAO_FIBRA(angulo,tau_xy):
#Transformando para coordenadas LOCAIS
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		pares_pontos_locais_1.append(c2*POLIGONO_TRUE_pontos_x[i]+s2*POLIGONO_TRUE_pontos_y[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*POLIGONO_TRUE_pontos_x[i]+c2*POLIGONO_TRUE_pontos_y[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*POLIGONO_TRUE_pontos_x[i]+sin*cos*POLIGONO_TRUE_pontos_y[i]+(c2-s2)*tau_xy)

#Filtragem em coordenadas locais

	for i in range(0,len(pares_pontos_locais_2)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]>0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"

#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			POLIGONO_TRUE_pontos_x.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			POLIGONO_TRUE_pontos_y.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])	


######################################
# Outubro Sábado 27, 2018
#Suporte de calcular_conicas
#
# Filtro Simples
#
####################################

def filtro_calculo_conica_COMPRESSAO_MATRIZ(angulo,tau_xy):
#Transformando para coordenadas LOCAIS
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		pares_pontos_locais_1.append(c2*POLIGONO_TRUE_pontos_x[i]+s2*POLIGONO_TRUE_pontos_y[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*POLIGONO_TRUE_pontos_x[i]+c2*POLIGONO_TRUE_pontos_y[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*POLIGONO_TRUE_pontos_x[i]+sin*cos*POLIGONO_TRUE_pontos_y[i]+(c2-s2)*tau_xy)

#Filtragem em coordenadas locais

	for i in range(0,len(pares_pontos_locais_2)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_2[i]>0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"

#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			POLIGONO_TRUE_pontos_x.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			POLIGONO_TRUE_pontos_y.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])	


######################################
# Outubro Sábado 27, 2018
#Suporte de calcular_conicas
#
# Filtro Simples
#
####################################

def filtro_calculo_conica_TRACAO_MATRIZ(angulo,tau_xy):
#Transformando para coordenadas LOCAIS
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		pares_pontos_locais_1.append(c2*POLIGONO_TRUE_pontos_x[i]+s2*POLIGONO_TRUE_pontos_y[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*POLIGONO_TRUE_pontos_x[i]+c2*POLIGONO_TRUE_pontos_y[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*POLIGONO_TRUE_pontos_x[i]+sin*cos*POLIGONO_TRUE_pontos_y[i]+(c2-s2)*tau_xy)

#Filtragem em coordenadas locais
#//   Para valores de X

	for i in range(0,len(pares_pontos_locais_2)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_2[i]<0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"

#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			POLIGONO_TRUE_pontos_x.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			POLIGONO_TRUE_pontos_y.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])	


######################################
# Outubro Sábado 27, 2018
#Suporte de calcular_conicas
#
# Filtro Simples
#
####################################


def filtro_calculo_conica_TRACA_OFIBRA(angulo,tau_xy):
#Transformando para coordenadas LOCAIS
	pares_pontos_locais_1=[]
	pares_pontos_locais_2=[]
	pares_pontos_locais_12=[]
	theta_radianos=(Math.pi/180)*angulo

	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		pares_pontos_locais_1.append(c2*POLIGONO_TRUE_pontos_x[i]+s2*POLIGONO_TRUE_pontos_y[i]+2*cos*sin*tau_xy)
		pares_pontos_locais_2.append(s2*POLIGONO_TRUE_pontos_x[i]+c2*POLIGONO_TRUE_pontos_y[i]-2*cos*sin*tau_xy)
		pares_pontos_locais_12.append(-sin*cos*POLIGONO_TRUE_pontos_x[i]+sin*cos*POLIGONO_TRUE_pontos_y[i]+(c2-s2)*tau_xy)

#Filtragem em coordenadas locais
#//   Para valores de X

	for i in range(0,len(pares_pontos_locais_1)):	#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]<0.0):
			pares_pontos_locais_1[i]="null"
			pares_pontos_locais_2[i]="null"
			pares_pontos_locais_12[i]="null"

#//Eliminas os null antes

#/Zeramos para poder encher de novo
	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]

	for i in range(0,len(pares_pontos_locais_1)):		#(i=0;i<pares_pontos_locais_1.length;i++)
		if(pares_pontos_locais_1[i]!="null"):
			POLIGONO_TRUE_pontos_x.append(c2*pares_pontos_locais_1[i]+s2*pares_pontos_locais_2[i]-2*cos*sin*pares_pontos_locais_12[i])
			POLIGONO_TRUE_pontos_y.append(s2*pares_pontos_locais_1[i]+c2*pares_pontos_locais_2[i]+2*cos*sin*pares_pontos_locais_12[i])		

#########################################################################################
# Outubro Sábado 27, 2018
#
#
#
#########################################################################################		

def criterio_puro(sigma_x,sigma_y,tau_xy,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
	theta_radianos=(Math.pi/180)*theta
	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)
	c2=cos*cos
	s2=sin*sin
	sigma_1=c2*sigma_x+s2*sigma_y+2*cos*sin*tau_xy
	sigma_2=s2*sigma_x+c2*sigma_y-2*cos*sin*tau_xy
	tau_12=-sin*cos*sigma_x+sin*cos*sigma_y+(c2-s2)*tau_xy

	if_sigma_1_MAIOR=0.0
	if_sigma_1_MENOR=0.0
	if_sigma_2_MAIOR=0.0
	if_sigma_2_MENOR=0.0
 # tração na fibra
	if(sigma_1>0):
		normalizado_sigma_1=sigma_1/SIGMA_T_1
		normalizado_tau_12 =tau_12/TAU12
		if_sigma_1_MAIOR=Math.pow(normalizado_sigma_1,2)+Math.pow(normalizado_tau_12,2)
	else:
		normalizado_sigma_1=Math.fabs(sigma_1/SIGMA_C_1)
		if_sigma_1_MENOR=normalizado_sigma_1
#//tração na matriz
	if(sigma_2>0):
		normalizado_sigma_2=sigma_2/SIGMA_T_2
		normalizado_tau_12 =tau_12/TAU12
		if_sigma_2_MAIOR=Math.pow(normalizado_sigma_2,2)+Math.pow(normalizado_tau_12,2)
	else:# //compressão na fibra
		TAU23=TAU23_global;
		normalizado_sigma_2=sigma_2/(2*TAU23)
		normalizado_sigma_2_c=sigma_2/SIGMA_C_2
		normalizado_tau_12 =tau_12/TAU12
		potencia=(Math.pow((SIGMA_C_2/(2*TAU23)),2)-1)
		complemento_especial=normalizado_sigma_2_c*potencia
		if_sigma_2_MENOR=Math.pow(normalizado_sigma_2,2)+complemento_especial+Math.pow(normalizado_tau_12,2)

	indices=[if_sigma_1_MAIOR,if_sigma_1_MENOR,if_sigma_2_MAIOR,if_sigma_2_MENOR]		
	indices.sort()
	return indices[3]

#########################################################################################
# Outubro Sábado 27, 2018
#
#
#
#########################################################################################	

def gerar_pontos():	
	a_f=a
	b_f=b
	c_f=c
	d_f=d
	f_f=f
	g_f=g

	if(b!=0):
		B=2*b_f
		D=2*d_f
		E=2*f_f
		A=a_f
		C=c_f
		numerador=(C-A-Math.sqrt(Math.pow(A-C,2)+B*B))
		rotacionado=Math.atan(numerador/B)

	raioMaior=Math.sqrt((2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g))/((b*b-a*c)*(Math.sqrt(Math.pow((a-c),2)+4*b*b)-(a+c))))
	raioMenor=Math.sqrt((2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g))/((b*b-a*c)*(-Math.sqrt(Math.pow((a-c),2)+4*b*b)-(a+c))))

	eixo_menor_elipse=raioMenor
	eixo_maior_elipse=raioMaior

	origem_x=(c*d-b*f)/(b*b-a*c)
	origem_y=(a*f-b*d)/(b*b-a*c)

	ang=0
	passo=(2.0*Math.pi/numeroPontos)

#Fazemos a varredura de Izquerda para DIREITA , desde 0 para 2*Pi


	for i in range(0,numeroPontos):
		cos=Math.cos(ang)
		sin=Math.sin(ang)
		r=(raioMaior*raioMenor)/(Math.sqrt(raioMaior*raioMaior*sin*sin+raioMenor*raioMenor*cos*cos))
		x=r*cos
		y=r*sin
		temporal_x=x*Math.cos(rotacionado)-y*Math.sin(rotacionado)
		temporal_y=x*Math.sin(rotacionado)+y*Math.cos(rotacionado)
		if (origem_x!=0):
			temporal_x=temporal_x+origem_x
		if (origem_y!=0):
			temporal_y=temporal_y+origem_y
		
		ang=ang+passo
		POLIGONO_TRUE_pontos_x.append(temporal_x)
		POLIGONO_TRUE_pontos_y.append(temporal_y)

################################## ######################################################################################### 
########    Arquivos MATLAB e GNU
# Segunda 19, 2018. Novembro
################################## ########################################################################################

import datetime

def gerarGNU(request):	
	response = HttpResponse(content_type='text/text')

	nomeTEMPO= datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

	response['Content-Disposition'] = 'attachment; filename="EnvelopesHashin_%s.dat"' % (nomeTEMPO)

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
	
	response['Content-Disposition'] = 'attachment; filename="EnvelopesHashin_%s.txt"' % (nomeTEMPO)

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




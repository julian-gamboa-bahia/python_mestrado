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

#Para larc03
	global EPSILON_T_1
	global EPSILON_C_1
	global NU12
	global E1
	global E2
	global G12
	global GAMMA12

	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(material)):
		SIGMA_T_1=p.SIGMA_T_1
		SIGMA_T_2=p.SIGMA_T_2
		SIGMA_C_1=p.SIGMA_C_1  # Convenio de sinais
		SIGMA_C_2=p.SIGMA_C_2  # Convenio de sinais
		NOME=p.NOME
		TAU12=p.TAU12
		GAMMA12=p.GAMMA12
#Para larc03
		G12=p.G12
		NU12=p.NU12
		E1=p.E1
		E2=p.E2
		EPSILON_T_1=p.EPSILON_T_1
		EPSILON_C_1=p.EPSILON_C_1

	global LARC03_E1
	global LARC03_E2
	global LARC03_EPSILON_T_1
	LARC03_E1=E1
	LARC03_E2=E2
	LARC03_EPSILON_T_1=EPSILON_T_1
		
	
	# estás informações são usadas para obter os potenciais PONTOS do envelope usando as equações"	

	temporal_criterio=response_data['criterio']	
	LEGENDA_TIPO_ANGULO_MATERIAL="".join([u'Puck  , com ângulo (Degree)  ', str(angulo),'   com el material  ',NOME])	
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

def calculo_envelope(angulo):	


	estudando_segmento_02(angulo)
	estudando_segmento_01(angulo)

	calculo_centro_grid()
	calcula_if_grid(angulo)

	graham_scan()

	adicionar_JSON()

def calcula_if_grid(theta):
	grid_x_if_unitario=[]
	grid_y_if_unitario=[]
	tolerancia=0.1
	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		IF=puck(POLIGONO_TRUE_pontos_x[i],POLIGONO_TRUE_pontos_y[i],tauXY,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
		if(IF[0]<=(1+tolerancia)):
			if(IF[1]<=(1+tolerancia)):
				if(IF[2]<=(1+tolerancia)):
					if(IF[3]<=(1+tolerancia)):						
						if(IF[4]<=(1+tolerancia)):							
							unitario=0
							if(IF[0]>=(1-tolerancia)):
								unitario=1
							if(IF[1]>=(1-tolerancia)):
								unitario=1
							if(IF[2]>=(1-tolerancia)):
								unitario=1
							if(IF[3]>=(1-tolerancia)):
								unitario=1
							if(IF[4]>=(1-tolerancia)):
								unitario=1	
							if(unitario==1):
								grid_x_if_unitario.append(POLIGONO_TRUE_pontos_x[i])
								grid_y_if_unitario.append(POLIGONO_TRUE_pontos_y[i])

	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]

	for i in range(0,len(grid_x_if_unitario)):
		POLIGONO_TRUE_pontos_x.append(grid_x_if_unitario[i])
		POLIGONO_TRUE_pontos_y.append(grid_y_if_unitario[i])


def calculo_centro_grid():
	total_x=0.0
	total_y=0.0
	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		total_x=total_x+POLIGONO_TRUE_pontos_x[i]
		total_y=total_y+POLIGONO_TRUE_pontos_y[i]

	centro_x=total_x/len(POLIGONO_TRUE_pontos_x)
	centro_y=total_y/len(POLIGONO_TRUE_pontos_y)

	for i in range(0,10):
		print "##################"
	print centro_x
	print centro_y


	comparando_cada_vertice(centro_x,centro_y)

#########################################################################################
# Outubro 18, 2018
# Construimos uma grid com muitos elementos para poder calcular o IF
#########################################################################################	

def comparando_cada_vertice(centro_x,centro_y):
	distancia=[]
	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		distancia.append(Math.sqrt(Math.pow(POLIGONO_TRUE_pontos_x[i]-centro_x,2)+Math.pow(POLIGONO_TRUE_pontos_y[i]-centro_y,2)))

	distancia.sort()
	raio_maior=distancia[len(distancia)-1]
	raio_menor=distancia[0]

	# Nove02
	#numero_circulos=100

	passos_inter_circulos=(raio_maior)/numero_circulos

	raio=0.0 #raio_menor
	for i in range(0,numero_circulos):
		circulo(raio,centro_x,centro_y)
		raio=raio+passos_inter_circulos
		


def circulo(raio,centro_x,centro_y):
	# Nov02
	#numero_passos_grid=100

	passo_angular=(2*Math.pi)/numero_passos_grid
	theta=0
	
	for i in range(0,numero_passos_grid):
		POLIGONO_TRUE_pontos_x.append(raio*Math.cos(theta)+centro_x)
		POLIGONO_TRUE_pontos_y.append(raio*Math.sin(theta)+centro_y)
		theta=theta+passo_angular


#########################################################################################
# Outubro 17, 2018
# O larc03 é uma linha reta que pode-se aplicar na condição de quadrante de:
# sigma_11>0
# 
# Se faz preciso estudar o Larc02, considerado como segmento superior no plano LOCAL (sigma_1,sigma_2)
# Larc02 considera elementos tanto positivos como negativos de sigma_1
#
#########################################################################################	

def estudando_segmento_02(angulo):
#Calculando o Ponto (Larc03.03 & Larc03.02) podemos obter uma linha reta 	
	ponto_corte_02_03=corte_02_03(angulo,tauXY)
	ponto_corte_02_05=testando_larc02_05(angulo,tauXY,ponto_corte_02_03)


# Respeitamos a ordem

	POLIGONO_TRUE_pontos_x.append(ponto_corte_02_05[0])
	POLIGONO_TRUE_pontos_y.append(ponto_corte_02_05[1])

	POLIGONO_TRUE_pontos_x.append(ponto_corte_02_03[0])
	POLIGONO_TRUE_pontos_y.append(ponto_corte_02_03[1])

# Com este dois pontos 	ponto_corte_02_05 (direita) ponto_corte_02_05 (esquerda) estamos perante um inicio e fim da provavel da curva
# Sendo preciso fazer o estudo de curvatura

def estudando_segmento_01(angulo):	
	ponto_corte_03_01=corte_03_01(angulo,tauXY)
	ponto_corte_01_06=testando_larc03_01(angulo,tauXY,ponto_corte_03_01)

# Respeitamos a ordem

	POLIGONO_TRUE_pontos_x.append(ponto_corte_03_01[0])
	POLIGONO_TRUE_pontos_y.append(ponto_corte_03_01[1])

	POLIGONO_TRUE_pontos_x.append(ponto_corte_01_06[0])
	POLIGONO_TRUE_pontos_y.append(ponto_corte_01_06[1])	

def corte_03_01(angulo,tau_xy):
#Em função do coeficiente angular do larc03.02 fazemos a varredura:
	cos=Math.cos((angulo*Math.pi)/180)
	sin=Math.sin((angulo*Math.pi)/180)

	denominador=((sin*sin)/LARC03_E1-((cos*cos)/LARC03_E2)*NU12)
	numerador_b=LARC03_EPSILON_T_1-2*cos*sin*tau_xy*((1.0)/LARC03_E1+((1.0)/LARC03_E2)*NU12)
	numerador_m=-(((cos*cos)/LARC03_E1)-((sin*sin)/LARC03_E2)*NU12)

	coeficiente_angular=numerador_m/denominador

	b=numerador_b/denominador
	
	corte_eixo_x=-(b/coeficiente_angular)

	return metodo_bisection_linha_criterio_02(corte_eixo_x,coeficiente_angular,b,angulo,2)


#########################################################################################
# Outubro 16, 2018
# Ponto fixo: definico como o ponto de corte com o eixo
# O ponto aqui obtido representa a união dos critérios 02 com critério 03
#########################################################################################	

def corte_02_03(angulo,tauXY):
	theta_radianos=(Math.pi/180)*angulo
	cos=Math.cos(theta_radianos)
	sin=Math.sin(theta_radianos)    
	denominador=((sin*sin)/LARC03_E1-((cos*cos)/LARC03_E2)*NU12)
	numerador_b=LARC03_EPSILON_T_1-2*cos*sin*tauXY*((1.0)/LARC03_E1+((1.0)/LARC03_E2)*NU12)
	numerador_m=-(((cos*cos)/LARC03_E1)-((sin*sin)/LARC03_E2)*NU12)
	coeficiente_angular=numerador_m/denominador
	b=numerador_b/denominador
	corte_eixo_x=-(b/coeficiente_angular)

	return metodo_bisection_linha_criterio_02(corte_eixo_x,coeficiente_angular,b,angulo,1)
	

#########################################################################################
# Outubro 16, 2018
# bisection para colocar outros pontos no envelope
#########################################################################################	

def metodo_bisection_linha_criterio_02(corte_eixo_x,coeficiente_angular,b,angulo,indice_interesse):	
#Vemos se o INICIO e FIM representam um intervalo CONVENIENTE
	amplificacao=1.0
#INICIO
	y=corte_eixo_x*coeficiente_angular+b
	if_inicial=puck(corte_eixo_x,y,tauXY,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
#FIM
	if(indice_interesse==1):
		x=corte_eixo_x*(1+amplificacao)
	if(indice_interesse==2):
		x=0.0
	y=x*coeficiente_angular+b
	if_final=puck(x,y,tauXY,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)

	anterior=x
	novo=0.0
	multiplicador=10.0
	passo_reducao=(x-corte_eixo_x)/multiplicador

	#Usando o método numérico BISECTION

	gaurdian=1
	proximidade=Math.fabs(if_inicial[indice_interesse]-if_final[indice_interesse])

	while (0.0001<proximidade):
		gaurdian_interno=1
		while((if_inicial[indice_interesse]<1) and (if_final[indice_interesse]>1)):
			x=anterior-passo_reducao
			y=x*coeficiente_angular+b
			if_final=puck(x,y,tauXY,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
#//APENAS quando for maior, pode-se atualizar o anterior
			if(if_final[indice_interesse]>1):
				anterior=x
			if(if_final[indice_interesse]<1):
				novo=x
			if(gaurdian_interno>1000):
				break				        
			gaurdian_interno=gaurdian_interno+1
# fim do while
		x=anterior
		y=x*coeficiente_angular+b
		if_final=puck(x,y,tauXY,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
		x=novo
		y=x*coeficiente_angular+b
		if_inicial=puck(x,y,tauXY,angulo,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
		passo_reducao=(anterior-novo)/(multiplicador*10.0)
		proximidade=Math.fabs(if_inicial[indice_interesse]-if_final[indice_interesse])
		if(gaurdian>1000):		    	
			break        			    
		gaurdian=gaurdian_interno+1

	return [x,y]


#########################################################################################
# Outubro 16, 2018
# Critério puro
#########################################################################################	
def puck(sigma_x,sigma_y,tau_xy,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
	theta_radianos=(Math.pi/180)*theta
	c=Math.cos(theta_radianos)
	s=Math.sin(theta_radianos)
	c2=c*c
	s2=s*s
	sigma_1=c2*sigma_x+s2*sigma_y+2*c*s*tau_xy
	sigma_2=s2*sigma_x+c2*sigma_y-2*c*s*tau_xy
	tau_12=-s*c*sigma_x+s*c*sigma_y+(c2-s2)*tau_xy

########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################

# Modos do IF
#	Modo 1
	if_puck_modo_1=0.0
	if (sigma_1 >= 0.0):		
		EPSILON_1=((sigma_1/E1)-NU12*(sigma_2/E2))
#		E1_f=E1+0.0
#		NU12_f=NU12+0.0
#		m_sigF=0.0
		aux4_1 = (NU12_f/E1_f)*m_sigF*sigma_2
		aux4 = EPSILON_1 + aux4_1		
		if_puck_modo_1 = (1.0/EPSILON_T_1)*aux4

########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################

#  Modo 2 
	if_puck_modo_2=0.0
	if (sigma_1 < 0.0):
		EPSILON_1=((sigma_1/E1)-NU12*(sigma_2/E2))
#		E1_f=E1+0.0
#		m_sigF=0.0
#		NU12_f=NU12+0.0
		aux5_1 = (NU12_f/E1_f)*m_sigF*sigma_2
		aux5_2 = EPSILON_1 + aux5_1
		aux5 = (1.0/EPSILON_C_1)*Math.fabs(aux5_2)
		aux6 = Math.pow( 10*GAMMA12,2)
		if_puck_modo_2 = aux5 + aux6
	
#######################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
	#Modo 3 ,
	if_puck_modo_3=0.0
	if (sigma_2 >= 0.0):
#		p_plus_TL=1.0
#		sigma_1_D=1.0
		aux7_1 = tau_12/TAU12
		aux7 = Math.pow(aux7_1, 2)
		aux8_1 = p_plus_TL*(SIGMA_T_2/TAU12)
		aux8_2 = Math.pow(1 - aux8_1, 2)
		aux8_3_1 = sigma_2/SIGMA_T_2
		aux8_3 = Math.pow(aux8_3_1, 2)
		aux8 = aux8_2*aux8_3
		raiz= Math.sqrt( aux7 + aux8 )
		aux0_1 = tau_12/TAU12
		aux0=p_plus_TL*aux0_1
		termo_fibra=Math.fabs(sigma_1/sigma_1_D)
		if_puck_modo_3=aux0+raiz


########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################

#	Modo 4 if_puck_modo_4
	if_puck_modo_4=0.0
	if_puck_modo_5=0.0

	if (sigma_2 < 0.0):
#		p_plus_TL=1.0
#		sigma_1_D=1.0		
#		tau12_C=1.0
#		R_TT_A=1.0
		t = Math.fabs(sigma_2/TAU12)
		t_maior = R_TT_A/Math.fabs(tau12_C)
		if((t >= 0) and (t <= t_maior)):
#			p_minus_TL=1.0
#			sigma_1_D=1.0
			aux7_1 = tau_12
			aux7 = Math.pow(aux7_1, 2)
			aux8_1 = p_minus_TL*SIGMA_T_2
			aux8_2 = Math.pow(aux8_1, 2)
			raiz=Math.sqrt(aux7+aux8_2)
			aux0_1=raiz+p_minus_TL
			aux0=aux0_1/TAU12					
			termo_fibra=Math.fabs(sigma_1/sigma_1_D)
			if_puck_modo_4=termo_fibra+aux0
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################	
#	Modo 5, Compressão na Fibra, Depende do valor de fi
		t_INV = Math.fabs(TAU12/sigma_2)
		t_maior_INV = Math.fabs(tau12_C)/R_TT_A
		if((t_INV >= 0) and (t <= t_maior_INV)):
#			p_minus_TT=1.0
#			sigma_1_D=1.0
			aux12_1 = 2*(1 + p_minus_TT)*tau12_C
			aux12_2 = tau_12/aux12_1
			aux12 = Math.pow(aux12_2,2)
			aux13_1 = sigma_2/SIGMA_C_2
			aux13 = Math.pow(aux13_1,2)
			aux14_1 = SIGMA_C_2/(-sigma_2)
			aux14 = aux14_1*( aux12 + aux13 )
			termo_fibra=Math.fabs(sigma_1/sigma_1_D)
			if_puck_modo_5=termo_fibra+aux14

########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################	


	#entrega de resultados
	IFs=[]
	IFs.append(if_puck_modo_1)
	IFs.append(if_puck_modo_2)
	IFs.append(if_puck_modo_3)
	IFs.append(if_puck_modo_4)
	IFs.append(if_puck_modo_5)
	
	return IFs


#########################################################################################		
# Nov 03, 2018
# Auxilio
#########################################################################################		
def APAGARcalcular_Fi(sigma_1,sigma_2,tau_12,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
	alpha_0=53.2*(Math.pi/180)
	S_L_is=Math.sqrt(2)*TAU12
	eta_L=(TAU12*Math.cos(alpha_0*2))/(SIGMA_C_2*Math.pow(Math.cos(alpha_0),2))
	radicando=1-4*((S_L_is/SIGMA_C_1)+eta_L)*(S_L_is/SIGMA_C_1)
	if(radicando<0.0):
		return 0.0
	numerador=Math.sqrt(radicando)
	divisor=2*((S_L_is/SIGMA_C_1)+eta_L)
	critico=Math.atan(numerador/divisor)


	numerador=Math.fabs(TAU12)+critico*(G12-SIGMA_C_1)
	divisor=G12+sigma_1-sigma_2
	fi=(numerador/divisor)
	return fi

########################## valores EXPERIMENTAIS ##########################################
# Outubro 08, 2018
# SUPORTE para COLETEAR valores EXPERIMENTAIS
#########################################################################################		

def coletar_numeroPontos(request,numeroPontos_entrada):
	global numeroPontos
	numeroPontos=int(numeroPontos_entrada)

	return HttpResponse("numeroPontos  "+numeroPontos_entrada)


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
# Outubro 17, 2018
# Usandoo a função do IF puro, pode-se projetar esta linha reta (paralela ao eixo X)
#########################################################################################	

def testando_larc02_05(theta,tau_xy,ponto):
#
	theta_radianos=(Math.pi/180)*theta
	c=Math.cos(theta_radianos)
	s=Math.sin(theta_radianos)
	c2=c*c
	s2=s*s

	coeficiente_angular=-(s2/c2);
#Usando a formula COEFICIENTE_ANGULAR com Ponto 
	x_0=ponto[0]
	y_0=ponto[1]

	b=-coeficiente_angular*x_0+y_0;	

#agosto18 usando um método mais simples que o BISECTION, temos
	
	if_inicial=puck(x_0,y_0,tau_xy,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12);
	if_larc_03_compressao_matriz_larc0302=if_inicial[1];

	x=x_0
	y=y_0

	passo=Math.fabs(x_0/10)
	
	guardian=1
	while(Math.fabs(1-if_larc_03_compressao_matriz_larc0302)<0.01):
		x=x-passo
		y=coeficiente_angular*x+b

		if_inicial=puck(x,y,tau_xy,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
		if_larc_03_compressao_matriz_larc0302=if_inicial[1]

		if(guardian>1000):
			break
		guardian=guardian+1

	return[x,y]

#########################################################################################
# Outubro 17, 2018
# Usandoo a função do IF puro, pode-se projetar esta linha reta (paralela ao eixo X)
#########################################################################################	

def testando_larc03_01(theta,tau_xy,ponto):
	theta_radianos=(Math.pi/180)*theta
	c=Math.cos(theta_radianos)
	s=Math.sin(theta_radianos)
	c2=c*c
	s2=s*s

	coeficiente_angular=-(s2/c2)
#Usando a formula COEFICIENTE_ANGULAR com Ponto 
	x_0=ponto[0]
	y_0=ponto[1]
	b=-coeficiente_angular*x_0+y_0
#agosto18 usando um método mais simples que o BISECTION, temos	
	if_inicial=puck(x_0,y_0,tau_xy,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)
	if_larc_03_compressao_matriz_larc0301=if_inicial[2]
	x=x_0
	y=y_0
	passo=Math.fabs(x_0/10)

	guardian=1
	while(Math.fabs(1-if_larc_03_compressao_matriz_larc0301)<0.01):
		x=x-passo
		y=coeficiente_angular*x+b
		if_inicial=puck(x,y,tau_xy,theta,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12);
		if_larc_03_compressao_matriz_larc0301=if_inicial[2]

		if(guardian>1000):
			break
		guardian=guardian+1	

	return[x,y]


#########################################################################################
# Outubro 18, 2018
# Passo 1 : obter o que está na parte mais infeior do eixo Y
#########################################################################################		
def graham_scan_parcial():
	copiados_x=POLIGONO_TRUE_pontos_x[:]
	copiados_y=POLIGONO_TRUE_pontos_y[:]


#########################################################################################
# Outubro 18, 2018
# Passo 1 : obter o que está na parte mais infeior do eixo Y
#########################################################################################		
	pontos_ordenados_x=[]
	pontos_ordenados_y=[]

	menor_x=copiados_x[0]
	menor_y=copiados_y[0]
	indice=0
	for i in range(0,len(copiados_y)):
		if(menor_y>=copiados_y[i]):
			menor_y=copiados_y[i]
			menor_x=copiados_x[i]
			indice=i
			# desempate no caso de ter a mesma Y

	pontos_ordenados_x.append(menor_x)			
	pontos_ordenados_y.append(menor_y)			

	del copiados_x[indice]
	del copiados_y[indice]    

#########################################################################################
# Outubro 18, 2018
# Passo 2 : ordenamos os pontos conforme o ângulo usando ARC TAN(x)
#########################################################################################	

	angulos=[]	
	for i in range(0,len(copiados_x)):
		delta_x=(copiados_x[i]-menor_x)+0.0
		delta_y=(copiados_y[i]-menor_y)+0.0
		if(delta_y!=0):
			angulos.append(Math.atan(delta_x/delta_y))
		else:
			angulos.append(Math.pi/2.0)			


# com os ângulos pode-se ordenar
	for j in range(0,len(angulos)):
		menor_angulo=angulos[0]	
		x_menor_angulo=copiados_x[0]
		y_menor_angulo=copiados_y[0]	
		indice=0
		for i in range(0,len(angulos)):
			if(menor_angulo>=angulos[i]):
				menor_angulo=angulos[i]	
				x_menor_angulo=copiados_x[i]
				y_menor_angulo=copiados_y[i]
				indice=i

		del copiados_x[indice]
		del copiados_y[indice]
		del angulos[indice]
		pontos_ordenados_x.append(x_menor_angulo)			
		pontos_ordenados_y.append(y_menor_angulo)

	angulos.sort()

	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]

	for i in range(0,len(pontos_ordenados_x)):
		POLIGONO_TRUE_pontos_x.append(pontos_ordenados_x[i])
		POLIGONO_TRUE_pontos_y.append(pontos_ordenados_y[i])	


def graham_scan():

	copiados_x=POLIGONO_TRUE_pontos_x[:]
	copiados_y=POLIGONO_TRUE_pontos_y[:]


	#########################################################################################
	# Outubro 18, 2018
	# Passo 1 : obter o que está na parte mais infeior do eixo Y
	# Com o critério de DESEMPATE
	#########################################################################################		
	pontos_ordenados_x=[]
	pontos_ordenados_y=[]

	menor_x_list=[]
	menor_y_list=[]
# Na verdade é um duplo ordenamento DISSIMULADO
	for j in range(0,len(copiados_y)):
		menor_x=copiados_x[0]
		menor_y=copiados_y[0]		
		indice=0
		for i in range(1,len(copiados_y)):
			if(menor_y>=copiados_y[i]):			
				menor_y=copiados_y[i]
				menor_x=copiados_x[i]							
				indice=i
				# desempate no caso de ter a mesma Y, será usado o ponto com menor X  			
		menor_x_list.append(menor_x)
		menor_y_list.append(menor_y)
		del copiados_x[indice]
		del copiados_y[indice]		


	#Agora escolhemos o menor valor de Y e se este tiver multiplicidade acima de um será preciso ordenar
	menor_x=menor_x_list[0]
	menor_y=menor_y_list[0]


	#####Tinha esquecido um valor
	####################################################################################
	

	multiplicidade=0.0
	for i in range(1,len(menor_y_list)):
		#print ("comparando menor_y %f contra menor_y_list[i]  %f" % (menor_y,menor_y_list[i]))
		if(menor_y==menor_y_list[i]):
			multiplicidade=multiplicidade+1.0


	if(multiplicidade>0):
		# Será preciso ordenar em X
		menor_x=menor_x_list[0]
		menor_y=menor_y_list[0]
		indice=0
		for i in range(0,len(menor_x_list)):
			if(menor_x>=menor_x_list[i]):
				menor_x=menor_x_list[i]
				menor_y=menor_y_list[i]
				indice=i
	

	pontos_ordenados_x.append(menor_x)			
	pontos_ordenados_y.append(menor_y)		  

#########################################################################################
# Outubro 18, 2018
# Passo 2 : ordenamos os pontos conforme o ângulo usando ARC TAN(x)
#########################################################################################	

	#copiamos de NOVO dado que foi destruido 
	copiados_x=POLIGONO_TRUE_pontos_x[:]
	copiados_y=POLIGONO_TRUE_pontos_y[:]

	indice_apagar=0

	angulos=[]	
	for i in range(0,len(copiados_x)):		
		delta_x=(copiados_x[i]-menor_x)+0.0
		delta_y=(copiados_y[i]-menor_y)+0.0
		if(delta_x!=0.0):
			angulos.append(Math.atan(delta_y/delta_x))
		else:
			if(delta_y==0.0):
				indice_apagar=i				
			else:
				angulos.append(Math.pi/2.0)
				

	del copiados_x[indice_apagar]
	del copiados_y[indice_apagar]

# com os ângulos pode-se ordenar
# resrevamos os ângulos para verificar a qualidade do Algoritmo

	angulo_ordenado=[]
	for j in range(0,len(angulos)):
		menor_angulo=angulos[0]	
		x_menor_angulo=copiados_x[0]
		y_menor_angulo=copiados_y[0]	
		indice=0
		for i in range(0,len(angulos)):
			if(menor_angulo>=angulos[i]):
				menor_angulo=angulos[i]	
				x_menor_angulo=copiados_x[i]
				y_menor_angulo=copiados_y[i]
				indice=i
		del copiados_x[indice]
		del copiados_y[indice]
		del angulos[indice]

		angulo_ordenado.append(menor_angulo)

		pontos_ordenados_x.append(x_menor_angulo)			
		pontos_ordenados_y.append(y_menor_angulo)

	# Agora ver se de verdade é uma ENVOLVENTE
	stack_x=[]
	stack_y=[]
# Para 0 
	stack_x.append(pontos_ordenados_x[0])
	stack_y.append(pontos_ordenados_y[0])
# Para 1
	stack_x.append(pontos_ordenados_x[1])
	stack_y.append(pontos_ordenados_y[1])



# Em tese deveria meter todos os pontos, mas é preciso ter cuidado com aqueles que estejam MUITO ADENTRO
 
	for i in range(2,len(pontos_ordenados_x)):
		proximoTOP=len(stack_x)-2
		TOP=len(stack_x)-1
		#print ("Testando com: %d " % (i))
		o=ccw(stack_x[proximoTOP],stack_x[TOP],pontos_ordenados_x[i],stack_y[proximoTOP],stack_y[TOP],pontos_ordenados_y[i])


		if(o==0.0): 
			# Caso extremo que TODOS estejam numa única linha reta
			stack_x.pop()
			stack_y.pop() 

			stack_x.append(pontos_ordenados_x[i])
			stack_y.append(pontos_ordenados_y[i])

		else: 
			if(o>0.0):  
				# aceita positivos
				stack_x.append(pontos_ordenados_x[i]) 
				stack_y.append(pontos_ordenados_y[i])				
				#print("POSITIVO %f Será inserido o %f" % (o,pontos_ordenados_x[i]))
				#print"stack_x"
				#print stack_x				
			else: 
				# Nos negatiovos, ele deve REMOVER o ponto
				#print("NEGATIVO %f será eliminado %f" % (o,stack_x[TOP]))				
#Cuidado				
				while((o<=0.0) and (proximoTOP>=0.0)):
					stack_x.pop() # elimina o topo da filha ou elemento C do teste
					stack_y.pop()
					proximoTOP=len(stack_x)-2
					TOP=len(stack_x)-1	
					o=ccw(stack_x[proximoTOP],stack_x[TOP],pontos_ordenados_x[i],stack_y[proximoTOP],stack_y[TOP],pontos_ordenados_y[i])					 
					
				stack_x.append(pontos_ordenados_x[i])
				stack_y.append(pontos_ordenados_y[i])
		#print "##Estudo de O"    			
		#print stack_x    			
# end FOR

	del POLIGONO_TRUE_pontos_x[:]
	del POLIGONO_TRUE_pontos_y[:]

	for i in range(0,len(stack_x)):
		POLIGONO_TRUE_pontos_x.append(stack_x[i])
		POLIGONO_TRUE_pontos_y.append(stack_y[i])


#Return a  positive number for a left turn (ACEITA)
# and negative for a right turn (elimina)
#########################################################################################
# Outubro 18, 2018
# Passo 2 : ordenamos os pontos conforme o ângulo usando ARC TAN(x)
#########################################################################################	
def ccw(p1_x, p2_x, p3_x,p1_y, p2_y, p3_y):
	return (p2_x - p1_x)*(p3_y - p1_y) - (p2_y - p1_y)*(p3_x - p1_x)
		


#########################################################################################
# Nov02
# SUPORTE para calculo_envelope
# CAIXAS
# de entrada 
#########################################################################################		

def coletar_numero_circulos(request,numero_circulos_entrada):
	global numero_circulos
	numero_circulos=int(numero_circulos_entrada)

	return HttpResponse("numero_circulos_entrada  "+numero_circulos_entrada)

def coletar_numero_passos_grid(request,numero_passos_grid_entrada):
	global numero_passos_grid
	numero_passos_grid=int(numero_passos_grid_entrada)

	return HttpResponse("numero_passos_grid_entrada  "+numero_passos_grid_entrada)

#########################################################################################
# Nov05
# SUPORTE para calculo_envelope
# CAIXAS
# de entrada 
#########################################################################################		

def coletar_E1_f(request,E1_f_entrada):
	global E1_f
	E1_f=float(E1_f_entrada)
	return HttpResponse("E1_f_entrada  "+E1_f_entrada)


def coletar_NU12_f(request,NU12_f_entrada):
	global NU12_f
	NU12_f=float(NU12_f_entrada)
	return HttpResponse("NU12_f_entrada  "+NU12_f_entrada)	
	
def coletar_m_sigF(request,m_sigF_entrada):
	global m_sigF
	m_sigF=float(m_sigF_entrada)
	return HttpResponse("m_sigF_entrada  "+m_sigF_entrada)		


#		p_plus_TL=1.0
def coletar_p_plus_TL(request,p_plus_TL_entrada):
	global p_plus_TL
	p_plus_TL=float(p_plus_TL_entrada)
	return HttpResponse("p_plus_TL_entrada  "+p_plus_TL_entrada)		


#		p_minus_TL=1.0
def coletar_p_minus_TL(request,p_minus_TL_entrada):
	global p_minus_TL
	p_minus_TL=float(p_minus_TL_entrada)
	return HttpResponse("p_minus_TL_entrada  "+p_minus_TL_entrada)	


#		sigma_1_D=1.0
def coletar_sigma_1_D(request,sigma_1_D_entrada):
	global sigma_1_D
	sigma_1_D=float(sigma_1_D_entrada)
	return HttpResponse("sigma_1_D_entrada  "+sigma_1_D_entrada)		

#		tau12_C=1.0
def coletar_tau12_C(request,tau12_C_entrada):
	global tau12_C
	tau12_C=float(tau12_C_entrada)
	return HttpResponse("tau12_C_entrada  "+tau12_C_entrada)		


#		R_TT_A=1.0
def coletar_R_TT_A(request,R_TT_A_entrada):
	global R_TT_A
	R_TT_A=float(R_TT_A_entrada)
	print "################# Nov 06 ################# "
	print "R_TT_A"
	print R_TT_A	
	return HttpResponse("R_TT_A_entrada  "+R_TT_A_entrada)		

#		p_minus_TL=1.0
def coletar_p_minus_TT(request,p_minus_TT_entrada):
	global p_minus_TT
	p_minus_TT=float(p_minus_TT_entrada)

	return HttpResponse("p_minus_TT_entrada  "+p_minus_TT_entrada)		

################################## ######################################################################################### 
########    Arquivos MATLAB e GNU
# Segunda 19, 2018. Novembro
################################## ########################################################################################

import datetime

def gerarGNU(request):	
	response = HttpResponse(content_type='text/text')

	nomeTEMPO= datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

	response['Content-Disposition'] = 'attachment; filename="EnvelopesPuck_%s.dat"' % (nomeTEMPO)

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
	
	response['Content-Disposition'] = 'attachment; filename="EnvelopesPuck_%s.txt"' % (nomeTEMPO)

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






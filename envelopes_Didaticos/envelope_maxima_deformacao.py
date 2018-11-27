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
# 1) Todas as informações do URL são essenciais, por tanto os campos nãi usados se colocam iniclamente como LIVRES
# 2) 
#########################################################################################	

from macro.models import Laminas

numeroENVELOPES_EnvelopeFalhaSaidaJSON=0
response_data = {}
response_data['criterio']=[]

TRUE_pontos_x=[]
TRUE_pontos_y=[]
TRUE_pontos_xy=[]

global EXTREMOASvaloresX
EXTREMOASvaloresX=[]

global EXTREMOASvaloresY
EXTREMOASvaloresY=[]

global VETORdjango_limite
VETORdjango_limite=[] # saida indicando o numero de PONTOS

#Outubro 05, Antigamente definida

EnvelopeFalhaSaidaJSON_data=[]

GNU_EnvelopeFalhaSaidaJSON=""

dados_coletarENVELOPE_data=[]
LIMITES_coletarENVELOPE=[]


def coletando_informacaos_view(criterio,angulo,material,livre,sigma_x,sigma_y,tau_xy,livre_2):

	global global_material
	global_material=material
	global global_criterio
	global_criterio=criterio
	global global_angulo
	global_angulo=angulo

	livre_2=float(livre_2)+0.0

	if (livre_2==0.0):
		global EnvelopeFalhaSaidaJSON_data
		EnvelopeFalhaSaidaJSON_data=[]
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


	#Outubro 05. Parece mais conveniente que cada critério tenha a capacidade de DEFINIR
	# como processa este livre_2
	# para assim poder adaptações futuras

	if (livre_2==0.0):
		response_data.clear()
		#truque para que possa ESCREVER o valor de critério
		response_data['criterio']=[]
		response_data['data']=[]

		EnvelopeFalhaSaidaJSON_data=[]
		#zeramenteo total de todo
		#Pelo simples fato de tentar zerar aqui, considera esta como LOCAL, o que é perigoso: TRUE_pontos_x=[]
		'''
		TRUE_pontos_y=[]
		TRUE_pontos_xy=[]
		possiveis_pontos_x=[]	
		possiveis_pontos_y=[]
		possiveis_pontos_xy=[]
		POLIGONO_TRUE_pontos_x=[]		
		POLIGONO_TRUE_pontos_y=[]
		POLIGONO_TRUE_pontos_xy=[]
		valoresX = []
		valoresY = []
		'''

	#Outubro 01, estranho		

	temporal_criterio=response_data['criterio']	

	if(len(temporal_criterio)==6):
		response_data.clear()
		response_data['criterio']=[]
		EnvelopeFalhaSaidaJSON_data=[]
		global GNU_EnvelopeFalhaSaidaJSON
		GNU_EnvelopeFalhaSaidaJSON=""	

		dados_coletarENVELOPE_data=[]
		LIMITES_coletarENVELOPE=[]		

	global hrefs_enderecos

	global tauXY
	tauXY=tau_xy

	global angulo_GLOBAL
	angulo_GLOBAL=float(angulo)

	#Outubro 01, por ser uma códificação rápida

	global gammaXY_global
	gammaXY_global=float(tau_xy)

	hrefs_enderecos="%s!/%s/%s/%s/" % (criterio,angulo,material,livre)

	#Outubro 05, problema com ás variavéis

	angulo=float(angulo)
	sigma_x=float(sigma_x)
	sigma_y=float(sigma_y)
	tau_xy=float(tau_xy)
	# são coletadas as propriedades do material conforme o indice "material"

	global EPSILON_T_1
	global EPSILON_T_2
	global EPSILON_C_1
	global EPSILON_C_2
	global GAMMA12

	global E1
	global E2
	global NU12
	global G12

	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(material)):

		NOME=p.NOME		

		EPSILON_T_1=p.EPSILON_T_1
		EPSILON_T_2=p.EPSILON_T_2
		EPSILON_C_1=-p.EPSILON_C_1  # Convenio de sinais
		EPSILON_C_2=-p.EPSILON_C_2  # Convenio de sinais
		GAMMA12=p.GAMMA12

		E1=p.E1
		E2=p.E2
		NU12=p.NU12
		G12=p.G12
	
	# estás informações são usadas para obter os potenciais PONTOS do envelope usando as equações"	

	temporal_criterio=response_data['criterio']	
	LEGENDA_TIPO_ANGULO_MATERIAL="".join([u'Maxima Deformação  , com ângulo (Degree)  ', str(angulo),'   com el material  ',NOME])	
#GNU
	GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON," #  ",LEGENDA_TIPO_ANGULO_MATERIAL,"\n"]) 		
	temporal_criterio.append(LEGENDA_TIPO_ANGULO_MATERIAL)

	response_data['criterio'] = temporal_criterio

	alfa=1.0
	beta=2.0
	c = Math.cos((Math.pi / 180) * angulo)
	s = Math.sin((Math.pi / 180) * angulo)

	c2 = c * c
	s2 = s * s

	a = c2
	b = s2
	C = b
	d = a


	# Para usar apenas um VETOR
	if(len(POLIGONO_TRUE_pontos_x)>0):
		del	POLIGONO_TRUE_pontos_x[:]

	if(len(POLIGONO_TRUE_pontos_y)>0):
		del	POLIGONO_TRUE_pontos_y[:]	

	if(len(POLIGONO_TRUE_pontos_xy)>0):
		del	POLIGONO_TRUE_pontos_xy[:]		

	if(angulo % 90.0 == 0):
		calcula_apenas_4_vertices(alfa, s, c, tau_xy,a,b,C,d)
		# Outubro 02
		transformando_deformacoes_esforcos()
		ordenar_quatro_pontos()	
	else:
		calcula_apenas_4_vertices(alfa, s, c, tau_xy,a,b,C,d)
		if(angulo % 45.0 == 0):			
			ordenar_quatro_pontos()
		# //Para eq. 4.5 até 4.8:
		a = c2;
		b = s2;
		C = -beta * s * c;
		d = beta * s * c;
			# 
		calcula_eq4_ate_eq8_vertices(alfa, s, c, tau_xy,a,b,C,d)
			# 
			# //Para eq. 4.9 até 4.12:
			# 
		a = s2;
		b = c2;
		C = -beta * s * c;
		d = beta * s * c;

		if(angulo % 45.0 != 0):
			calcula_eq9_ate_eq12_vertices(alfa, s, c, tau_xy,a,b,C,d)

		criterio_puro_maxima_tensao(angulo, tau_xy)

		if (len(TRUE_pontos_x)==4):		# if (TRUE_pontos_x.length==4) {
			fecharPONTOS()				# alert("Envelope de 4 vértices"); # fecharPONTOS();
			
			# //Varios ELSES , de 5 esquinas
		if (len(TRUE_pontos_x)==5):		# if (TRUE_pontos_x.length==4) {
			fechar5PONTOS()				# alert("Envelope de 4 vértices"); # fecharPONTOS();

			
		if (len(TRUE_pontos_x)==6):		# if (TRUE_pontos_x.length==4) {
			fechar6PONTOS()				# alert("Envelope de 4 vértices"); # fecharPONTOS();
# Agosto 23, 2018 . 15:51
# Agosto 24, 2018 . 13:51 # por algum estranho motivo está entrando zerado aqui.

	if(len(POLIGONO_TRUE_pontos_x)>0):
	#if(len(TRUE_pontos_x)>0): <---mas o TRUE_pontos_x está funcionando muito bem
		adicionar_JSON()

	# Agosto 25, 2018 . 3:51
	VETORdjango_limite.append(len(POLIGONO_TRUE_pontos_x))

#Setembro 27, Ele passa apenas o numero de elementos vetorias que devem ser transferidos, 
# a função que verdadeiramente passa as informações é adicionar_JSON

	return VETORdjango_limite

# Agosto 23, 2018 . 17:21
def	criterio_puro_maxima_tensao(angulo, gamma_xy):
	Saida = []
	c = Math.cos((Math.pi / 180) * angulo)
	s = Math.sin((Math.pi / 180) * angulo)
	c2 = c * c
	s2 = s * s
#outubro 04, este valores de alpha e beta permitem refator rápidamente o sistema
	alpha=1.0 
	beta=2.0



	for i in range(0,len(possiveis_pontos_x)):# for (i = 0; i < possiveis_pontos_x.length; i++) {
		epsilon_x = possiveis_pontos_x[i]
		epsilon_y = possiveis_pontos_y[i]
	
		epsilon_1 = c2 * epsilon_x -0.0+ s2 * epsilon_y + alpha * c * s * gamma_xy
		epsilon_2 = s2 * epsilon_x -0.0+ c2 * epsilon_y - alpha * c * s * gamma_xy
		gamma_12 = -beta*s * c * epsilon_x -0.0+ beta*s * c * epsilon_y + (c2 - s2) * gamma_xy

		if(epsilon_1>0):
			normalizado_if_1 = Math.fabs(epsilon_1 / EPSILON_T_1)
		else:
			normalizado_if_1 = Math.fabs(epsilon_1 / EPSILON_C_1)
	
		if(epsilon_2>0):
			normalizado_if_2 = Math.fabs(epsilon_2 / EPSILON_T_2) 
		else:
			normalizado_if_2 = Math.fabs(epsilon_2 / EPSILON_C_2)

		normalizado_if_12 = Math.fabs(gamma_12 / GAMMA12)

		tolerancia = 0.01		
	
		if (
		(normalizado_if_1 < 1+tolerancia) &
		(normalizado_if_2 < 1+tolerancia) &
		(normalizado_if_12 < 1+tolerancia)
		):
			Saida.append("true")
		else:
			Saida.append("false")
	
	if(len(TRUE_pontos_x)>0):
		del	TRUE_pontos_x[:]

	if(len(TRUE_pontos_y)>0):
		del	TRUE_pontos_y[:]

	if(len(TRUE_pontos_xy)>0):
		del	TRUE_pontos_xy[:]		

	transformando_deformacoes_esforcos();

	for i in range(0,len(possiveis_pontos_y)):
		if (Saida[i]=="true"):
			TRUE_pontos_x.append(possiveis_pontos_x[i])
			TRUE_pontos_y.append(possiveis_pontos_y[i])
			TRUE_pontos_xy.append(possiveis_pontos_xy[i])


def fechar6PONTOS():

	numeros=[]

	numeros.append(1)
	numeros.append(2)
	numeros.append(3)
	numeros.append(4)
	numeros.append(5)

	ponto_inicial_x = TRUE_pontos_x[0]
	ponto_inicial_y = TRUE_pontos_y[0]

	#Fazemos a varredura dos pares para obter o ângulo.
	#Solução rápida: Invocar a função várias vezes

	angulo_temporal=0.0
	i_temp=0
	j_temp=0

	for i in range(1,len(TRUE_pontos_x)): #( i = 1; i < TRUE_pontos_x.length; i++)
		for j in range(i+1,len(TRUE_pontos_x)):#( j=i+1; j<TRUE_pontos_x.length;j++)
            #{
			angulo=calcular_angulo(ponto_inicial_x,ponto_inicial_y,i,j)
			if(angulo>=angulo_temporal):
                #{
				angulo_temporal=angulo
				i_temp=i
				j_temp=j
                #}

            #}
        #}

	ANGULADOS_TRUE_pontos_x=[]
	ANGULADOS_TRUE_pontos_y=[]

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[0])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[0])

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[i_temp])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[i_temp])

        #numeros.splice(numeros.indexOf(i_temp),1);
        #numeros.splice(numeros.indexOf(j_temp),1);

	ANTIGO_i_temp=i_temp
	ANTIGO_j_temp=j_temp

    #    //Estudo inicial partendo do primeiro ponto
	ponto_inicial_x = TRUE_pontos_x[ANTIGO_i_temp]
	ponto_inicial_y = TRUE_pontos_y[ANTIGO_i_temp]

	ponto_inicial_x_CONTRA = TRUE_pontos_x[ANTIGO_j_temp]
	ponto_inicial_y_CONTRA = TRUE_pontos_y[ANTIGO_j_temp]

	#//Fazemos a varredura dos pares para obter o ângulo.
	#//Solução rápida: Invocar a função várias vezes

	#//Tendo 3 ptos. Será preciso apenas detetar os outros
	angulo_temporal=0.0

	for j in range(1,len(TRUE_pontos_x)):#(j=1; j<TRUE_pontos_x.length;j++)#for(j=1; j<TRUE_pontos_x.length;j++) //acima de 0 (Antigo Ponto Inicial)
        #{
		if(j!=ANTIGO_i_temp):
         #   {
			angulo=calcular_angulo(
                        ponto_inicial_x,
                        ponto_inicial_y,
                        0,
                        j)

			if(angulo>=angulo_temporal):
            #    {
				angulo_temporal=angulo
				j_temp=j
           #     }
          #  }
        #}

    #    numeros.splice(numeros.indexOf(j_temp),1);

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])

	#// Agora do outro lado

	angulo_temporal=0.0

	for j in range(1,len(TRUE_pontos_x)): #for(j=1; j<TRUE_pontos_x.length; j++) //acima de 0 (Antigo Ponto Inicial)
        #{
		if(j!=ANTIGO_j_temp):
            #{

			angulo=calcular_angulo(
                        ponto_inicial_x_CONTRA,
                        ponto_inicial_y_CONTRA,
                        0,
                        j)

			if(angulo>=angulo_temporal):
                #{
				angulo_temporal=angulo
				i_temp=0;
				j_temp=j;
                #}
            #}
        #}
        #colocamos o não usado como inicial, é como um restante

	POLIGONO_TRUE_pontos_x.append(TRUE_pontos_x[numeros[0]])
	POLIGONO_TRUE_pontos_y.append(TRUE_pontos_y[numeros[0]])

	POLIGONO_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])
	POLIGONO_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])

	for i in range(0,len(ANGULADOS_TRUE_pontos_x)):#(i=0;i<ANGULADOS_TRUE_pontos_x.length;i++)
    #    {
		POLIGONO_TRUE_pontos_x.append(ANGULADOS_TRUE_pontos_x[i])
		POLIGONO_TRUE_pontos_y.append(ANGULADOS_TRUE_pontos_y[i])
     #   }
	

	#construir_COM_POLIGONO_TRUE_pontos(angulo,tau_xy)
    

#////////////////////



def fechar5pontos():
	numeros=[]
#Por segurança limpamos a lista
	numeros.append(1)
	numeros.append(2)
	numeros.append(3)
	numeros.append(4)
	numeros.append(5)

	ponto_inicial_x = TRUE_pontos_x[0]
	ponto_inicial_y = TRUE_pontos_y[0]

	#Fazemos a varredura dos pares para obter o ângulo.
	#Aqui será um duplo for para justamente poder obter o primeiro segmento

	angulo_temporal=0.0
	i_temp=0
	j_temp=0

	for i in range(1,len(TRUE_pontos_x)): # for ( i = 1; i < TRUE_pontos_x.length; i++)
    #{
		for j in range(i+1,len(TRUE_pontos_x)):#for( j=i+1; j<TRUE_pontos_x.length;j++): 
        #{
			angulo=calcular_angulo(ponto_inicial_x,ponto_inicial_y,i,j)
			if(angulo>=angulo_temporal):
            #{
				angulo_temporal=angulo
				i_temp=i
				j_temp=j
            #}
        #}
     #}
	ANGULADOS_TRUE_pontos_x=[]
	ANGULADOS_TRUE_pontos_Y=[]

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[0])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[0])

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[i_temp])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[i_temp])

	#numeros.splice(numeros.indexOf(i_temp),1);<---------------------------------------
	#numeros.splice(numeros.indexOf(j_temp),1);<---------------------------------------

	#Ele pega o maior ângulo, dado que envolve uma figura....

	#Eliminamos o primeiro elemento.

	#Extremo para ser estudado:

	ANTIGO_i_temp=i_temp
	ANTIGO_j_temp=j_temp

    #Estudo inicial partendo do primeiro ponto
	ponto_inicial_x = TRUE_pontos_x[ANTIGO_i_temp]
	ponto_inicial_y = TRUE_pontos_y[ANTIGO_i_temp]

	ponto_inicial_x_CONTRA = TRUE_pontos_x[ANTIGO_j_temp]
	ponto_inicial_y_CONTRA = TRUE_pontos_y[ANTIGO_j_temp]

    #Fazemos a varredura dos pares para obter o ângulo.

	angulo_temporal=0.0

	for j in range(1,len(TRUE_pontos_x)): #(j=1; j<TRUE_pontos_x.length;j++):# for(j=1; j<TRUE_pontos_x.length;j++) //acima de 0 (Antigo Ponto Inicial)
    #{
		if(j!=ANTIGO_i_temp):
        #{
			angulo=calcular_angulo(
                     ponto_inicial_x,
                     ponto_inicial_y,
                     0,
                     j)

			if(angulo>=angulo_temporal):
             #{
				angulo_temporal=angulo
				j_temp=j
             #}
        #}
    #}


	#numeros.splice(numeros.indexOf(j_temp),1);

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])

	#Domingo
	#Agora do outro lado

	angulo_temporal=0.0

	for j in range(1,len(TRUE_pontos_x)):#for( j=1; j<TRUE_pontos_x.length;j++) //acima de 0 (Antigo Ponto Inicial)
    # {
		if(j!=ANTIGO_j_temp):
        #{
			angulo=calcular_angulo(
                     ponto_inicial_x_CONTRA,
                     ponto_inicial_y_CONTRA,
                     0,
                     j)

			if(angulo>=angulo_temporal):
            # {
				angulo_temporal=angulo
				i_temp=0
				j_temp=j
            #}
        #}
    #}

	POLIGONO_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])
	POLIGONO_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])
	#POLIGONO_TRUE_pontos_xy.append(TRUE_pontos_xy[j_temp])

	for i in range(0,len(ANGULADOS_TRUE_pontos_x)): # for(i=0;i<ANGULADOS_TRUE_pontos_x.length;i++)
    #{
		POLIGONO_TRUE_pontos_x.append(ANGULADOS_TRUE_pontos_x[i])
		POLIGONO_TRUE_pontos_y.append(ANGULADOS_TRUE_pontos_y[i])
    #}

	construir_COM_POLIGONO_TRUE_pontos(angulo_GLOBAL,tauXY)

def calcular_angulo(ponto_inicial_x,ponto_inicial_y,i,j):
		vetor_1_x=TRUE_pontos_x[i]-ponto_inicial_x
		vetor_1_y=TRUE_pontos_y[i]-ponto_inicial_y
        #ponto final
		vetor_2_x=TRUE_pontos_x[j]-ponto_inicial_x
		vetor_2_y=TRUE_pontos_y[j]-ponto_inicial_y
		norma_1=Math.sqrt(vetor_1_x*vetor_1_x-0.0+vetor_1_y*vetor_1_y)
		norma_2=Math.sqrt(vetor_2_x*vetor_2_x-0.0+vetor_2_y*vetor_2_y)
        #Produto interno
		interno=vetor_1_x*vetor_2_x-0.0+vetor_1_y*vetor_2_y
		argumento=interno/(norma_1*norma_2)
		angulo=Math.acos(argumento)
		return (angulo*180)/Math.pi

# Agosto 23, 2018 . 18:31
def fecharPONTOS():
# //Fazemos um estudo MASSIVO dos pontos
# //Estudo inicial partendo do primeiro ponto, que será um estudo especial dado que
# // não sabemos qual é o primeiro ângulo interno da área
# 
	numeros=[]
# //Preparaos o array de numeração conforme a dimensão do TRUE_pontos_x
	for i in range(0,len(TRUE_pontos_x)):# for(i=0;i<TRUE_pontos_x.length;i++)
		numeros.append(i)
# //Fazemos a varredura dos pares para obter o ângulo.
# //Solução rápida: Invocar a função várias vezes
# 
	ponto_inicial_x = TRUE_pontos_x[0]
	ponto_inicial_y = TRUE_pontos_y[0]

	angulo_temporal=0.0
	i_temp=0.0
	j_temp=0.0
# 
	for i in range(1,len(TRUE_pontos_x)):# for (i = 1; i < TRUE_pontos_x.length; i++)
		for j in range(i+1,len(TRUE_pontos_x)):# for(j=i+1; j<TRUE_pontos_x.length;j++)			
			angulo=calcular_angulo(ponto_inicial_x,ponto_inicial_y,i,j)
			if(angulo>=angulo_temporal):
				angulo_temporal=angulo
				i_temp=i
				j_temp=j
# { for i 
	# { for j 
		# {
		# var angulo=calcular_angulo(ponto_inicial_x,ponto_inicial_y,i,j);
		# 
		# if(angulo>=angulo_temporal)
		# {
			# angulo_temporal=angulo;
			# i_temp=i;
			# j_temp=j;
		# }
	# }
# }
# 
	ANGULADOS_TRUE_pontos_x=[]
	ANGULADOS_TRUE_pontos_y=[]

	

	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])# ANGULADOS_TRUE_pontos_x.push(TRUE_pontos_x[j_temp]);
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])# ANGULADOS_TRUE_pontos_y.push(TRUE_pontos_y[j_temp]);
	# 
	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[0])# ANGULADOS_TRUE_pontos_x.push(TRUE_pontos_x[0]);
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[0])# ANGULADOS_TRUE_pontos_y.push(TRUE_pontos_y[0]);
	# 
	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[i_temp])# ANGULADOS_TRUE_pontos_x.push(TRUE_pontos_x[i_temp]);
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[i_temp])# ANGULADOS_TRUE_pontos_y.push(TRUE_pontos_y[i_temp]);
# 
# //Extremo para ser estudado:
# 
	ANTIGO_i_temp=i_temp;
	ANTIGO_j_temp=j_temp;
# 
# //Estudo inicial partendo do primeiro ponto
	ponto_inicial_x = TRUE_pontos_x[ANTIGO_i_temp];
	ponto_inicial_y = TRUE_pontos_y[ANTIGO_i_temp];
# 
	ponto_inicial_x_CONTRA = TRUE_pontos_x[ANTIGO_j_temp];
	ponto_inicial_y_CONTRA = TRUE_pontos_y[ANTIGO_j_temp];
# 
# //Tendo 3 ptos. Será preciso apenas detetar os outros
# // No caso de apenas 4 pontos, aqui deve concluir o algoritmos
	angulo_temporal=0.0;
# 
	for j in range(1,len(TRUE_pontos_x)): # for(j=1; j<TRUE_pontos_x.length;j++) //acima de 0 (Antigo Ponto Inicial)
	# {
		if(j!=ANTIGO_i_temp):
		# {
			angulo=calcular_angulo(ponto_inicial_x, ponto_inicial_y, 0,j);
			# 
			if(angulo>=angulo_temporal):
			# {
				angulo_temporal=angulo
				j_temp=j
			# }
			# }
	# }
	# 
	ANGULADOS_TRUE_pontos_x.append(TRUE_pontos_x[j_temp])
	ANGULADOS_TRUE_pontos_y.append(TRUE_pontos_y[j_temp])
# 
	for i in range(0,len(ANGULADOS_TRUE_pontos_x)):# for(i=0;i<ANGULADOS_TRUE_pontos_x.length;i++)
# {
		POLIGONO_TRUE_pontos_x.append(ANGULADOS_TRUE_pontos_x[i])
		POLIGONO_TRUE_pontos_y.append(ANGULADOS_TRUE_pontos_y[i])
# }
# 
# 
	print "POLIGONO_TRUE_pontos_x"
	print POLIGONO_TRUE_pontos_x

	print "POLIGONO_TRUE_pontos_y"
	print POLIGONO_TRUE_pontos_y

	#construir_COM_POLIGONO_TRUE_pontos(angulo_GLOBAL,tauXY)
# }

# usando as bibliotecas matemáticas do python
def calcula_apenas_4_vertices(alfa, s, c, tau_xy,a,b,C,d):		
	matriz_invertida = inv(np.array([[a,b],[C,d]])) 	#matriz_invertida=funcao_inversa_RETURN(a, b, C, d)
	matriz = np.array([[a,b],[C,d]]) 	#matriz_invertida=funcao_inversa_RETURN(a, b, C, d)
	eq4_1(alfa, s, c, tau_xy, matriz)	
	eq4_2(alfa, s, c, tau_xy, matriz)	
	eq4_3(alfa, s, c, tau_xy, matriz)	
	eq4_4(alfa, s, c, tau_xy, matriz)

# Agosto 23, 2018 . 16:51
def calcula_eq4_ate_eq8_vertices(alfa, s, c, tau_xy,a,b,C,d):	
	matriz_invertida = inv(np.array([[a,b],[C,d]])) 	#matriz_invertida=funcao_inversa_RETURN(a, b, C, d)
	matriz = np.array([[a,b],[C,d]]) 	#matriz_invertida=funcao_inversa_RETURN(a, b, C, d)
	eq4_5(alfa, s, c, tau_xy, matriz)	
	eq4_6(alfa, s, c, tau_xy, matriz)	
	eq4_7(alfa, s, c, tau_xy, matriz)	
	eq4_8(alfa, s, c, tau_xy, matriz)

# Agosto 23, 2018 . 17:11
def calcula_eq9_ate_eq12_vertices(alfa, s, c, tau_xy,a,b,C,d):		
	matriz_invertida = inv(np.array([[a,b],[C,d]])) 	#matriz_invertida=funcao_inversa_RETURN(a, b, C, d)
	matriz=np.array([[a,b],[C,d]]) 	#matriz_invertida=funcao_inversa_RETURN(a, b, C, d)
	eq4_9(alfa, s, c, tau_xy, matriz)
	eq4_10(alfa, s, c, tau_xy, matriz)
	eq4_11(alfa, s, c, tau_xy, matriz)
	eq4_12(alfa, s, c, tau_xy, matriz)	

# Agosto 23, 2018 . 14:13:51	
def eq4_1(alfa, s, c, tau_xy, matriz_invertida):	
	#Para eq. 4.1:
	vetor_1 = EPSILON_C_1 - alfa * s * c * tau_xy
	vetor_2 = EPSILON_C_2 -0.0+ alfa * s * c * tau_xy	
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])
# Agosto 23, 2018 . 14:39
def eq4_2(alfa, s, c, tau_xy, matriz_invertida):	
# eq4_2(alfa, s, c, tau_xy, matriz_invertida)
	vetor_1 = EPSILON_T_1 - alfa * s * c * tau_xy;
	vetor_2 = EPSILON_T_2  -0.0+ alfa * s * c * tau_xy;
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])
# Agosto 23, 2018 . 14:40
def eq4_3(alfa, s, c, tau_xy, matriz_invertida):	
#eq4_3(alfa, s, c, tau_xy, matriz_invertida)
	vetor_1 = EPSILON_T_1 - alfa * s * c * tau_xy;
	vetor_2 = EPSILON_C_2 -0.0+ alfa * s * c * tau_xy;
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])
# Agosto 23, 2018 . 14:41
def eq4_4(alfa, s, c, tau_xy, matriz_invertida):	
	vetor_1 = EPSILON_C_1 - alfa * s * c * tau_xy;
	vetor_2 = EPSILON_T_2 -0.0+ alfa * s * c * tau_xy;
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	


# Agosto 23, 2018 . 17:0
def eq4_5(alfa, s, c, tau_xy, matriz_invertida):	
	#Para eq. 4.5:
	c2 =c*c
	s2= s*s
	vetor_1 = EPSILON_C_1 - alfa * s * c * tau_xy
	vetor_2 = -GAMMA12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	
# Agosto 23, 2018 . 17:06
def eq4_6(alfa, s, c, tau_xy, matriz_invertida):	
	#Para eq. 4.6:
	c2 =c*c
	s2= s*s
	vetor_1 = EPSILON_T_1 - alfa * s * c * tau_xy
	vetor_2 = GAMMA12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	
# Agosto 23, 2018 . 17:06
def eq4_7(alfa, s, c, tau_xy, matriz_invertida):	
    #Para eq. 4.7:
	c2 =c*c
	s2= s*s
	vetor_1 = EPSILON_T_1 - alfa * s * c * tau_xy
	vetor_2 = -GAMMA12 + (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	
# Agosto 23, 2018 . 17:06
def eq4_8(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.8
	vetor_1 = EPSILON_C_1 - alfa * s * c * tau_xy
	vetor_2 = GAMMA12 -0.0+ (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	


# Agosto 23, 2018 . 17:12
def eq4_9(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.9
	vetor_1 = EPSILON_C_2 - alfa * s * c * tau_xy
	vetor_2 = -GAMMA12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	

# Agosto 23, 2018 . 17:12
def eq4_10(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.10
	vetor_1 = EPSILON_T_2 - alfa * s * c * tau_xy
	vetor_2 = GAMMA12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])

# Agosto 23, 2018 . 17:13
def eq4_11(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.11
	vetor_1 = EPSILON_T_2 - alfa * s * c * tau_xy
	vetor_2 = -GAMMA12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])				

# Agosto 23, 2018 . 17:13
def eq4_12(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.12
	vetor_1 = EPSILON_C_2 - alfa * s * c * tau_xy;
	vetor_2 = GAMMA12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])		

##################
	



#########################################################################################
# Agosto 21, 2018 
#
# Códificação em Python, considerar:
# 1) A sintaxes entre JavaScript e Python tem como elementos em comum
#########################################################################################	

def construir_COM_POLIGONO_TRUE_pontos(request):
	arquivo_js='construir_COM_POLIGONO_TRUE_pontos.js'
	return render(request, arquivo_js)	


##################################Saída########################################
########################################################################################
######Agosto 22, 2018
#Este formato de saída deve ser programado em cada envelope, o que se evidencia nas chamadas:

#	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/maxima_tensao/$', envelope_maxima_tensao.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson'),               
#	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/maxima_deformacao/$', envelope_maxima_deformacao.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson'),               

#######################################################################################
########################################################################################


def EnvelopeFalhaFlotJson(request):	

	response_data['data'] = EnvelopeFalhaSaidaJSON_data 	

	'''
	print ("Outubro 05, 2018                                  ")
	print ("Outubro 05, 2018                                  ")
	print "response_data"
	print response_data
	print valoresX
	print ("Outubro 05, 2018                                  ")
	print ("Outubro 05, 2018                                  ")
	print ("Outubro 05, 2018                                  ")
	'''

	return HttpResponse(json.dumps(response_data))	

########################################################################################
# Num novo esquema ele recebe o endereço pronto!!!
#####Agosto 25, 2018 Grande problema que o iframe é chamado em oportunidade posterior ao iframe
#######################################################################################


def verticesANTIGO(request):
	
	vertices_POLIGONO_TRUE_pontos_x=[]	
	vertices_POLIGONO_TRUE_pontos_y=[]

	#Outubro 04, este caso especial precisa não APENAS de um TauXY e se de um conjunto de TauS

	vertices_POLIGONO_TRUE_pontos_xy=[]	

	for i in range(0,len(possiveis_pontos_xy)):
		vertices_POLIGONO_TRUE_pontos_xy.append(POLIGONO_TRUE_pontos_xy[i])	

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		vertices_POLIGONO_TRUE_pontos_x.append(POLIGONO_TRUE_pontos_x[i])

	for i in range(0,len(POLIGONO_TRUE_pontos_y)):
		vertices_POLIGONO_TRUE_pontos_y.append(POLIGONO_TRUE_pontos_y[i])		

	c = {
	 'vertices_POLIGONO_TRUE_pontos_x': vertices_POLIGONO_TRUE_pontos_x,
	 'vertices_POLIGONO_TRUE_pontos_y': vertices_POLIGONO_TRUE_pontos_y,	
	 'hrefs_enderecos':hrefs_enderecos,
	 'tauXY':tauXY,
	 'vertices_POLIGONO_TRUE_pontos_xy':vertices_POLIGONO_TRUE_pontos_xy,
	}

	arquivo_js='vertices.js'
	return render(request, arquivo_js,c)	

def VETOR_extremos():
	VETOR_extremos=[]
	
	EXTREMOASvaloresX.sort()
	EXTREMOASvaloresY.sort()

	print "valEXTREMOASvaloresXoresX" 
	print EXTREMOASvaloresX

	print "EXTREMOASvaloresY" 
	print EXTREMOASvaloresY

	amplificao=1.5

	#minimoY=
	VETOR_extremos.append(amplificao*EXTREMOASvaloresY[0])
	#maximoY=
	VETOR_extremos.append(amplificao*EXTREMOASvaloresY[len(EXTREMOASvaloresY)-1])
	#minimoX=
	VETOR_extremos.append(amplificao*EXTREMOASvaloresX[0])
	#maximoX=
	VETOR_extremos.append(amplificao*EXTREMOASvaloresX[len(EXTREMOASvaloresX)-1])

	return VETOR_extremos
	
########################################################################################
#
#
#
#
#Ouutbro 01, 
#######################################################################################

def transformando_deformacoes_esforcos():
	cos = Math.cos((Math.pi / 180) * angulo_GLOBAL)
	sin = Math.sin((Math.pi / 180) * angulo_GLOBAL)

	valores_SIMGA_x=[]
	valores_SIMGA_y=[]

	valores_Q=[]
	valores_Q=obter_elementos_Q_barra(angulo_GLOBAL)

	Q11=float(valores_Q[0])
	Q12=float(valores_Q[1])
	Q22=float(valores_Q[2])
	Q66=float(valores_Q[3])

	Q16=float(valores_Q[4])
	Q26=float(valores_Q[5])



	for i in range(0,len(possiveis_pontos_x)): 					#(i=0;i<possiveis_pontos_x.length;i++):	
		sigma_x=Q11*possiveis_pontos_x[i]+Q12*possiveis_pontos_y[i]+Q16*gammaXY_global
		sigma_y=Q12*possiveis_pontos_x[i]+Q22*possiveis_pontos_y[i]+Q26*gammaXY_global
		possivel_tau_xy =Q16*possiveis_pontos_x[i]+Q26*possiveis_pontos_y[i]+Q66*gammaXY_global
		valores_SIMGA_x.append(sigma_x)
		valores_SIMGA_y.append(sigma_y); 

		# Para poder colocar o valor de TAUXY no momento de chamar o verificador

		possiveis_pontos_xy.append(possivel_tau_xy)
	
	# Outubro 11, 2018, LIMPAMOS a lista para poder colocar as informações
	del possiveis_pontos_x[:]
	del possiveis_pontos_y[:]


					



#Entrega-se a transformação
	for i in range(0,len(valores_SIMGA_x)):					#(i=0;i<valores_SIMGA_x.length;i++)
		possiveis_pontos_x.append(valores_SIMGA_x[i])
		possiveis_pontos_y.append(valores_SIMGA_y[i])


#function obter_elementos_Q_barra()
def obter_elementos_Q_barra(angulo):
	theta_radianos = (Math.pi / 180) * angulo
	cos= Math.cos(theta_radianos)
	sin= Math.sin(theta_radianos)
#var NU21=NU12*(E2/E1);
	NU21=NU12*(E2/E1)
#
#var Q11=E1/(1-NU21*NU12);
	Q11=E1/(1-NU21*NU12)
#var Q12=(NU12*E2)/(1-NU21*NU12);
	Q12=(NU12*E2)/(1-NU21*NU12)
#var Q22=E2/(1-NU21*NU12);
	Q22=E2/(1-NU21*NU12)
#var Q66=0.0+G12;
	Q66=G12
#
#
#var Q11_barra=0.0+(Math.pow(c,4))*Q11+ (Math.pow(s,4))*Q22 + 2*(Math.pow(c,2))*(Math.pow(s,2))*(Q12 + 2*Q66);
	Q11_barra=(Math.pow(cos,4))*Q11+ (Math.pow(sin,4))*Q22 + 2*(Math.pow(cos,2))*(Math.pow(sin,2))*(Q12 + 2*Q66);
#var Q12_barra=0.0+(Math.pow(c,4) + Math.pow(s,4))*Q12 + (Math.pow(c,2))*(Math.pow(s,2))*(Q11 + Q22 - 4*Q66);
	Q12_barra=0.0+(Math.pow(cos,4) + Math.pow(sin,4))*Q12 + (Math.pow(cos,2))*(Math.pow(sin,2))*(Q11 + Q22 - 4*Q66);
#var Q22_barra=0.0+(Math.pow(s,4))*Q11 + 2*(Math.pow(c,2))*(Math.pow(s,2))*(Q12 + 2*Q66) + (Math.pow(c,4))*Q22;
	Q22_barra=0.0+(Math.pow(sin,4))*Q11 + 2*(Math.pow(cos,2))*(Math.pow(sin,2))*(Q12 + 2*Q66) + (Math.pow(cos,4))*Q22;
#var Q66_barra=0.0+(Math.pow(c,2))*(Math.pow(s,2))*(Q11 + Q22 - 2*Q12 - 2*Q66) + (Math.pow(c,4) + Math.pow(s,4))*Q66;]
	Q66_barra=0.0+(Math.pow(cos,2))*(Math.pow(sin,2))*(Q11 + Q22 - 2*Q12 - 2*Q66) + (Math.pow(cos,4) + Math.pow(sin,4))*Q66;
	#var Q16_barra=0.0+(Math.pow(c,3))*s*(Q11 - Q12 - 2*Q66) - c*(Math.pow(s,3))*(Q22 - Q12 - 2*Q66);
	Q16_barra=0.0+(Math.pow(cos,3))*sin*(Q11 - Q12 - 2*Q66) - cos*(Math.pow(sin,3))*(Q22 - Q12 - 2*Q66);
#var Q26_barra=0.0+c*(Math.pow(s,3))*(Q11 - Q12 - 2*Q66) - s*(Math.pow(c,3))*(Q22 - Q12 - 2*Q66);
	Q26_barra=0.0+cos*(Math.pow(sin,3))*(Q11 - Q12 - 2*Q66) - sin*(Math.pow(cos,3))*(Q22 - Q12 - 2*Q66);
#
#var saidaQbar=[];
	saidaQbar=[]
#
#saidaQbar.push(Q11_barra);
	saidaQbar.append(Q11_barra)
#saidaQbar.push(Q12_barra);
	saidaQbar.append(Q12_barra)
#saidaQbar.push(Q22_barra);
	saidaQbar.append(Q22_barra)
#saidaQbar.push(Q66_barra);
	saidaQbar.append(Q66_barra)
#
#saidaQbar.push(Q16_barra);
	saidaQbar.append(Q16_barra)
#saidaQbar.push(Q26_barra);
	saidaQbar.append(Q26_barra);
#
	return saidaQbar

########################################################################################
#
# Cuidado, o método de ordenar 4 pontos de MD é mais sofisticado que o MT
#
#
#Ouutbro 02, 
#######################################################################################


def ordenar_quatro_pontos():
#{
 #       var separacao_tecnica=Math.abs(possiveis_pontos_x[0])*1.0e-3; //pegamos o primeiro elemento
	separacao_tecnica=Math.fabs(possiveis_pontos_x[0])*1.0e-3; #pegamos o primeiro elemento
#        //primeiramente evitamos que tenha um valor de X com multiplicidade
        #for ( i = 0; i < possiveis_pontos_x.length; i++) {
         #   for ( j = i -0+1; j < possiveis_pontos_x.length; j++) {
          #      var diff = possiveis_pontos_x[i] - possiveis_pontos_x[j];
           #     if (diff == 0.0) {
            #        possiveis_pontos_x[j]=possiveis_pontos_x[i] -0.0+ separacao_tecnica;
             #   }
            #}
        #}

	for i in range (0,len(possiveis_pontos_x)):
		for j in range (i+1,len(possiveis_pontos_x)):# ( j = i -0+1; j < possiveis_pontos_x.length; j++):
			diff = possiveis_pontos_x[i] - possiveis_pontos_x[j]
			if (diff == 0.0):
				possiveis_pontos_x[j]=possiveis_pontos_x[i] -0.0+ separacao_tecnica;

#//Fazemos ordenamento por burbulha
        #var ORDEM_ASCII="true";
        #var minimo=possiveis_pontos_x[0];

	ORDEM_ASCII="true";
	minimo=possiveis_pontos_x[0];

        #for(i = 0; i < possiveis_pontos_x.length; i++)
        #{
        #    if(possiveis_pontos_x[i]<minimo)
        #    {
        #        ORDEM_ASCII="false";
        #    }
        #    minimo=possiveis_pontos_x[i];
        #}

	for i in range(0,len(possiveis_pontos_x)):
		if(possiveis_pontos_x[i]<minimo):
			ORDEM_ASCII="false"
		minimo=possiveis_pontos_x[i]        

        #if(ORDEM_ASCII=="false")
        #{
        #    var menor_arco_1_x;
        #    var menor_arco_1_y;
        #    var TEMP_arco_1_x;
        #    var TEMP_arco_1_y;
        #    for (i = 0; i < possiveis_pontos_x.length; i++)
        #    {
        #        menor_arco_1_x=possiveis_pontos_x[i]-0.0;
        #        menor_arco_1_y=possiveis_pontos_y[i]-0.0;
		#       for(j=i-0+1;j<possiveis_pontos_x.length;j++)
#                {
 #                   if((possiveis_pontos_x[j]-0.0)<(menor_arco_1_x-0.0))
  #                  {		

                        #TEMP_arco_1_x=possiveis_pontos_x[j];
                        #possiveis_pontos_x[j]=menor_arco_1_x;
                        #possiveis_pontos_x[i]=TEMP_arco_1_x;
                        #TEMP_arco_1_y=possiveis_pontos_y[j];
                        #possiveis_pontos_y[j]=menor_arco_1_y;
                        #possiveis_pontos_y[i]=TEMP_arco_1_y;
                        #break;
                    #}
#///for
 #               }
  #          }
        #}


	if(ORDEM_ASCII=="false"):
		for i in range(0,len(possiveis_pontos_x)):#(i = 0; i < possiveis_pontos_x.length; i++):
		# {
			menor_arco_1_x=possiveis_pontos_x[i]-0.0;
			menor_arco_1_y=possiveis_pontos_y[i]-0.0;
		#
			for j in range(i+1,len(possiveis_pontos_x)):# for(j=i-0+1;j<possiveis_pontos_x.length;j++)
			# {
				if((possiveis_pontos_x[j]-0.0)<(menor_arco_1_x-0.0)):				# if((possiveis_pontos_x[j]-0.0)<(menor_arco_1_x-0.0))
					TEMP_arco_1_x=possiveis_pontos_x[j]# TEMP_arco_1_x=possiveis_pontos_x[j];
					possiveis_pontos_x[j]=menor_arco_1_x# possiveis_pontos_x[j]=menor_arco_1_x;
					possiveis_pontos_x[i]=TEMP_arco_1_x# possiveis_pontos_x[i]=TEMP_arco_1_x;
					# //O mesmo para Y para assim manter o sistema ordenado
					TEMP_arco_1_y=possiveis_pontos_y[j]# TEMP_arco_1_y=possiveis_pontos_y[j];
					possiveis_pontos_y[j]=menor_arco_1_y# possiveis_pontos_y[j]=menor_arco_1_y;
					possiveis_pontos_y[i]=TEMP_arco_1_y# possiveis_pontos_y[i]=TEMP_arco_1_y;
					break# break;
				# }
			# ///for
			# }
		# }
	# }	

        #//É preciso apenas ordenar por altura dado que
#//Numeração em forma horaria começa pelo extremo esquerdo
 #       // 1) O extremo esquerdo será o ponto 1
  #      // 2) O extremo direito será o ponto 3
  #      // 3) A dúvida existe sobre os pontos 2 3  , mas entre estes escolhemos pelo coeficiente ângular
  #      // como regra.
  #      // Aquela que permita construir uma reta com o maior coeficiente ângular é o ponto.
        #//TOMAR DE possiveis_pontos_y os pontos possiveis pontos 2 e 3
        #var confuso_2_x=possiveis_pontos_x[1]; //Lembrar que os dois pontos estão à direito do ponto 1
	confuso_2_x=possiveis_pontos_x[1]# //Lembrar que os dois pontos estão à direito do ponto 1
        #var confuso_2_y=possiveis_pontos_y[1];
	confuso_2_y=possiveis_pontos_y[1] #
        #var confuso_3_x=possiveis_pontos_x[2];
	confuso_3_x=possiveis_pontos_x[2]
        #var confuso_3_y=possiveis_pontos_y[2];
	confuso_3_y=possiveis_pontos_y[2] #
#//Calculamos os coeficientes angulares:
        #var m_do_confuso_2=(confuso_2_y-possiveis_pontos_y[0])/(confuso_2_x-possiveis_pontos_x[0]);
	m_do_confuso_2=(confuso_2_y-possiveis_pontos_y[0])/(confuso_2_x-possiveis_pontos_x[0])
        #var m_do_confuso_3=(confuso_3_y-possiveis_pontos_y[0])/(confuso_3_x-possiveis_pontos_x[0]);
	m_do_confuso_3=(confuso_3_y-possiveis_pontos_y[0])/(confuso_3_x-possiveis_pontos_x[0])
#//Aquele ponto confuso de mairo coeficiente angular será o ponto 2
        #var temp_x;
        #var temp_y;

        #if(m_do_confuso_2>m_do_confuso_3)
        #{
            #temp_x=possiveis_pontos_x[3];
            #temp_y=possiveis_pontos_y[3];
#//O de maior coeficiente angular será o ponto 2
            #possiveis_pontos_x[1]=confuso_2_x;
            #possiveis_pontos_y[1]=confuso_2_y;
#//E o de menor será o ponto 4
            #possiveis_pontos_x[3]=confuso_3_x;
            #possiveis_pontos_y[3]=confuso_3_y;
#//O antigo ponto 4 será o ponto 3
            #possiveis_pontos_x[2]=temp_x;
            #possiveis_pontos_y[2]=temp_y;
        #}
        #else
        #{
         #   temp_x=possiveis_pontos_x[3];          
            #temp_y=possiveis_pontos_y[3];
#//O de maior coeficiente angular será o ponto 2
            #possiveis_pontos_x[1]=confuso_3_x;
            #possiveis_pontos_y[1]=confuso_3_y;
#//E o de menor será o ponto 4
            #possiveis_pontos_x[3]=confuso_2_x;
            #possiveis_pontos_y[3]=confuso_2_y;
#//O antigo ponto 4 será o ponto 3
            #possiveis_pontos_x[2]=temp_x;
            #possiveis_pontos_y[2]=temp_y;
        #}

	if(m_do_confuso_2>m_do_confuso_3):
		temp_x=possiveis_pontos_x[3]
		temp_y=possiveis_pontos_y[3]
		possiveis_pontos_x[1]=confuso_2_x
		possiveis_pontos_y[1]=confuso_2_y
#//E o de menor será o ponto 4
		possiveis_pontos_x[3]=confuso_3_x
		possiveis_pontos_y[3]=confuso_3_y
#//O antigo ponto 4 será o ponto 3
		possiveis_pontos_x[2]=temp_x
		possiveis_pontos_y[2]=temp_y
	else:
		temp_x=possiveis_pontos_x[3]
		temp_y=possiveis_pontos_y[3]
#//O de maior coeficiente angular será o ponto 2
		possiveis_pontos_x[1]=confuso_3_x
		possiveis_pontos_y[1]=confuso_3_y
#//E o de menor será o ponto 4
		possiveis_pontos_x[3]=confuso_2_x
		possiveis_pontos_y[3]=confuso_2_y
#//O antigo ponto 4 será o ponto 3
		possiveis_pontos_x[2]=temp_x
		possiveis_pontos_y[2]=temp_y
#	}
# Outubro 02
	for i in range(0,len(possiveis_pontos_x)):
		POLIGONO_TRUE_pontos_x.append(possiveis_pontos_x[i])
		POLIGONO_TRUE_pontos_y.append(possiveis_pontos_y[i])
		POLIGONO_TRUE_pontos_xy.append(possiveis_pontos_xy[i])

#//////////////////
#}


def ordenar_quatro_pontosANTIGO():
	separacao_tecnica=Math.fabs(possiveis_pontos_x[0])*1.0e-3; #pegamos o primeiro elemento
	#
	# //primeiramente evitamos que tenha um valor de X com multiplicidade
	#
	# for ( i = 0; i < possiveis_pontos_x.length; i++) {
	# for ( j = i -0+1; j < possiveis_pontos_x.length; j++) {
	# var diff = possiveis_pontos_x[i] - possiveis_pontos_x[j];
	# if (diff == 0.0) {
	# possiveis_pontos_x[j]=possiveis_pontos_x[i] -0.0+ separacao_tecnica;
	# }
	# }
	# }

	for i in range (0,len(possiveis_pontos_x)):
		for j in range (i+1,len(possiveis_pontos_x)):# ( j = i -0+1; j < possiveis_pontos_x.length; j++):
			diff = possiveis_pontos_x[i] - possiveis_pontos_x[j]
			if (diff == 0.0):
				possiveis_pontos_x[j]=possiveis_pontos_x[i] -0.0+ separacao_tecnica;
	#
	# //Fazemos ordenamento por burbulha
	#
	ORDEM_ASCII="true";

	minimo=possiveis_pontos_x[0];
	#
	# for(i = 0; i < possiveis_pontos_x.length; i++)
	# {
	# if(possiveis_pontos_x[i]<minimo)
	# {
	# ORDEM_ASCII="false";
	# }
	# minimo=possiveis_pontos_x[i];
	# }

	for i in range(0,len(possiveis_pontos_x)):
		if(possiveis_pontos_x[i]<minimo):
			ORDEM_ASCII="false"
		minimo=possiveis_pontos_x[i]

	# if(ORDEM_ASCII=="false")
	# {
	# var menor_arco_1_x;
	# var menor_arco_1_y;
	# var TEMP_arco_1_x;
	# var TEMP_arco_1_y;
	#
	#
	# for (i = 0; i < possiveis_pontos_x.length; i++)
	# {
	# menor_arco_1_x=possiveis_pontos_x[i]-0.0;
	# menor_arco_1_y=possiveis_pontos_y[i]-0.0;
	#
	# for(j=i-0+1;j<possiveis_pontos_x.length;j++)
	# {
	# if((possiveis_pontos_x[j]-0.0)<(menor_arco_1_x-0.0))
	# {
	# //lert(possiveis_pontos_x[j]+" menor "+menor_arco_1_x);
	#
	# TEMP_arco_1_x=possiveis_pontos_x[j];
	# possiveis_pontos_x[j]=menor_arco_1_x;
	# possiveis_pontos_x[i]=TEMP_arco_1_x;
	# //O mesmo para Y para assim manter o sistema ordenado
	# TEMP_arco_1_y=possiveis_pontos_y[j];
	# possiveis_pontos_y[j]=menor_arco_1_y;
	# possiveis_pontos_y[i]=TEMP_arco_1_y;
	# break;
	# }
	# ///for
	# }
	# }
	# }
	#

	if(ORDEM_ASCII=="false"):
		for i in range(0,len(possiveis_pontos_x)):#(i = 0; i < possiveis_pontos_x.length; i++):
		# {
			menor_arco_1_x=possiveis_pontos_x[i]-0.0;
			menor_arco_1_y=possiveis_pontos_y[i]-0.0;
		#
			for j in range(i+1,len(possiveis_pontos_x)):# for(j=i-0+1;j<possiveis_pontos_x.length;j++)
			# {
				if((possiveis_pontos_x[j]-0.0)<(menor_arco_1_x-0.0)):				# if((possiveis_pontos_x[j]-0.0)<(menor_arco_1_x-0.0))
				# {
				# //lert(possiveis_pontos_x[j]+" menor "+menor_arco_1_x);
				#
					TEMP_arco_1_x=possiveis_pontos_x[j]# TEMP_arco_1_x=possiveis_pontos_x[j];
					possiveis_pontos_x[j]=menor_arco_1_x# possiveis_pontos_x[j]=menor_arco_1_x;
					possiveis_pontos_x[i]=TEMP_arco_1_x# possiveis_pontos_x[i]=TEMP_arco_1_x;
					# //O mesmo para Y para assim manter o sistema ordenado
					TEMP_arco_1_y=possiveis_pontos_y[j]# TEMP_arco_1_y=possiveis_pontos_y[j];
					possiveis_pontos_y[j]=menor_arco_1_y# possiveis_pontos_y[j]=menor_arco_1_y;
					possiveis_pontos_y[i]=TEMP_arco_1_y# possiveis_pontos_y[i]=TEMP_arco_1_y;
					break# break;
				# }
			# ///for
			# }
		# }
	# }	

	# transformando_deformacoes_esforcos();

	for i in range(0,len(possiveis_pontos_x)):
		POLIGONO_TRUE_pontos_x.append(possiveis_pontos_x[i])
		POLIGONO_TRUE_pontos_y.append(possiveis_pontos_y[i])


#Outubro 04, este caso especial precisa não APENAS de um TauXY e se de um conjunto de TauS
# Não sendo preciso que passe a linha poligonal em ordem, senão apenas os valores verdadeiros

def vertices(request):
	
	vertices_POLIGONO_TRUE_pontos_x=[]	
	vertices_POLIGONO_TRUE_pontos_y=[]


	vertices_POLIGONO_TRUE_pontos_xy=[]	

	for i in range(0,len(TRUE_pontos_xy)):
		vertices_POLIGONO_TRUE_pontos_xy.append(TRUE_pontos_xy[i])	

	for i in range(0,len(TRUE_pontos_x)):
		vertices_POLIGONO_TRUE_pontos_x.append(TRUE_pontos_x[i])

	for i in range(0,len(TRUE_pontos_y)):
		vertices_POLIGONO_TRUE_pontos_y.append(TRUE_pontos_y[i])		

	c = {
	 'vertices_POLIGONO_TRUE_pontos_x': vertices_POLIGONO_TRUE_pontos_x,
	 'vertices_POLIGONO_TRUE_pontos_y': vertices_POLIGONO_TRUE_pontos_y,	
	 'hrefs_enderecos':hrefs_enderecos,
	 'tauXY':tauXY,
	 'vertices_POLIGONO_TRUE_pontos_xy':vertices_POLIGONO_TRUE_pontos_xy,
	}

	arquivo_js='vertices.js'
	return render(request, arquivo_js,c)	

################################## ######################################################################################### 
########    Arquivos MATLAB e GNU
# Segunda 19, 2018. Novembro
################################## ########################################################################################

import datetime

def gerarGNU(request):	
	response = HttpResponse(content_type='text/text')

	nomeTEMPO= datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

	response['Content-Disposition'] = 'attachment; filename="EnvelopesMaximaDeformacao_%s.dat"' % (nomeTEMPO)

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

	if(len(POLIGONO_TRUE_pontos_x)>0):
		valoresX.append([POLIGONO_TRUE_pontos_x[0],POLIGONO_TRUE_pontos_y[0]])

	valoresX.append("null")
	indice=0
# lembrar aqui que pe global mesma
	global GNU_EnvelopeFalhaSaidaJSON
	GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON," # Inicio do Envelope   ","\n"]) 

	for x in valoresX:
		EnvelopeFalhaSaidaJSON_data.append(valoresX[indice])
		if(valoresX[indice]!="null"):
			GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON,str(valoresX[indice][0]),"    ",str(valoresX[indice][1]),"\n"]) 
		else:
			GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON,"# Fim deste Envelope  ","\n\n\n\n"]) 
		indice=indice+1
#Nov22		
	dados_coletarENVELOPE_data_JSON()		


# Melhorada com o intuito de colocar o 
	

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
	
	response['Content-Disposition'] = 'attachment; filename="EnvelopesMaximaDeformacao_%s.txt"' % (nomeTEMPO)

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




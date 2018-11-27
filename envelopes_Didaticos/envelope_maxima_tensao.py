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
VETORdjango_limite=[] # saida indicando o numero de PONTOS

EnvelopeFalhaSaidaJSON=[]

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
		GNU_EnvelopeFalhaSaidaJSON=""

		dados_coletarENVELOPE_data=[]
		LIMITES_coletarENVELOPE=[]

	global hrefs_enderecos

	global tauXY
	tauXY=tau_xy


	hrefs_enderecos="%s!/%s/%s/%s/" % (criterio,angulo,material,livre)

	#global possiveis_pontos_x
	#possiveis_pontos_x=[]		
	#global possiveis_pontos_y
	#possiveis_pontos_y=[]
	#global POLIGONO_TRUE_pontos_x
	#POLIGONO_TRUE_pontos_x=[]
	#global POLIGONO_TRUE_pontos_y
	#POLIGONO_TRUE_pontos_y=[]
	#global valoresX
	#valoresX = []


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
	
	LEGENDA_TIPO_ANGULO_MATERIAL="".join([u'Maxima Tensao  , com ângulo (Degree)  ', str(angulo),'   com el material  ',NOME])	
#GNU
	GNU_EnvelopeFalhaSaidaJSON="".join([GNU_EnvelopeFalhaSaidaJSON," #  ",LEGENDA_TIPO_ANGULO_MATERIAL,"\n"]) 

	temporal_criterio.append(LEGENDA_TIPO_ANGULO_MATERIAL)
	response_data['criterio'] = temporal_criterio
	
	alfa=2.0
	beta=1.0
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

	if(angulo % 90.0 == 0):
		calcula_apenas_4_vertices(alfa, s, c, tau_xy,a,b,C,d)
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
			# 
			# 
			# 
			# if(angulo % 45.0 != 0)
		if(angulo % 45.0 != 0):
			calcula_eq9_ate_eq12_vertices(alfa, s, c, tau_xy,a,b,C,d)
			# {
			# calcula_eq9_ate_eq12_vertices(alfa, s, c, tau_xy,a,b,C,d);
			# }
			# else
			# {
			# alert("não cálcula os pontos degenerados");
			# }
			# 
			# //Agora é preciso avaliar e saber quais destes pontos devem ser ordenados, aqueles que vamos chamar de "TRUE_pontos_x" os quais são transformados
			# 

		criterio_puro_maxima_tensao(angulo, tau_xy)


			# 
			# //Varios ELSES , de 4 esquinas sem ângulo multiplo de Pi/2
			# 

		if (len(TRUE_pontos_x)==4):		# if (TRUE_pontos_x.length==4) {
			fecharPONTOS()				# alert("Envelope de 4 vértices"); # fecharPONTOS();
			
			# //Varios ELSES , de 5 esquinas
		if (len(TRUE_pontos_x)==5):		# if (TRUE_pontos_x.length==4) {
			fechar5PONTOS()				# alert("Envelope de 4 vértices"); # fecharPONTOS();
			# fechar5pontos();
			# }
			# //Varios ELSES , de 6 esquinas
		if (len(TRUE_pontos_x)==6):		# if (TRUE_pontos_x.length==4) {
			fechar6PONTOS()				# alert("Envelope de 4 vértices"); # fecharPONTOS();
			# fechar6pontos();
			# }
			# 
			# /////////fim do else
			# }
			# 

# Agosto 23, 2018 . 15:51
# Agosto 24, 2018 . 13:51 # por algum estranho motivo está entrando zerado aqui.

	if(len(POLIGONO_TRUE_pontos_x)>0):
		adicionar_JSON()

	# Agosto 25, 2018 . 3:51
	VETORdjango_limite.append(len(POLIGONO_TRUE_pontos_x))

#Setembro 27, Ele passa apenas o numero de elementos vetorias que devem ser transferidos, 
# a função que verdadeiramente passa as informações é adicionar_JSON

	return VETORdjango_limite

# Agosto 23, 2018 . 17:21
def	criterio_puro_maxima_tensao(angulo, tau_xy):	

	Saida = []
#
#
# var c = Math.cos(theta_radianos);
# var s = Math.sin(theta_radianos);
# var c2 = c ++ c;
# var s2 = s ++ s;

	c = Math.cos((Math.pi / 180) * angulo)
	s = Math.sin((Math.pi / 180) * angulo)
	c2 = c * c
	s2 = s * s

#
# //vemos o IF diretamente
#
# var sigma_x;
# var sigma_y;
#
# var sigma_1;
# var sigma_2;
# var tau_12;
# var normalizado_SIGMA_T_1;
# var normalizado_SIGMA_C_1;
# var normalizado_SIGMA_T_2;
# var normalizado_SIGMA_C_2;
# var normalizado_TAU12;
#
# //Máxima Tensão, por tanto o alpha é 2
	alpha=2.0
	beta=1.0
	for i in range(0,len(possiveis_pontos_x)):# for (i = 0; i < possiveis_pontos_x.length; i++) {
		sigma_x = possiveis_pontos_x[i]
		sigma_y = possiveis_pontos_y[i]# sigma_y = possiveis_pontos_y[i];
	#
	# //calculando em locais
	#
		sigma_1 = c2 * sigma_x -0.0+ s2 * sigma_y + alpha * c * s * tau_xy
		sigma_2 = s2 * sigma_x -0.0+ c2 * sigma_y - alpha * c * s * tau_xy
		tau_12 = -beta*s * c * sigma_x -0.0+ beta*s * c * sigma_y + (c2 - s2) * tau_xy
	#
	#
	# //normalizando
	# //Para a direção local 1
		if(sigma_1>0):# if(sigma_1>0)
	# {
			normalizado_if_1 = Math.fabs(sigma_1 / SIGMA_T_1)# // Tração# normalizado_if_1 = Math.abs(sigma_1 / SIGMA_T_1); // Tração
	# }
		else:# else
	# {
			normalizado_if_1 = Math.fabs(sigma_1 / SIGMA_C_1)# normalizado_if_1 = Math.abs(sigma_1 / SIGMA_C_1); // Compressão
	# }
	# //Para a direção local 2
		if(sigma_2>0):# if(sigma_2>0)
	# {
			normalizado_if_2 = Math.fabs(sigma_2 / SIGMA_T_2); # normalizado_if_2 = Math.abs(sigma_2 / SIGMA_T_2); // Tração
	# }
		else:# else
	# {
			normalizado_if_2 = Math.fabs(sigma_2 / SIGMA_C_2)# normalizado_if_2 = Math.abs(sigma_2 / SIGMA_C_2); // Compressão
	# }
	# //Para o esforço cisalhante
		normalizado_if_12 = Math.fabs(tau_12 / TAU12)# normalizado_if_12 = Math.abs(tau_12 / TAU12);
	# //Se qualquer um dos anteriores supera o valor de 1, significa que o IF foi superado.
	# //janeiro24 mas estando ciente do erro numérico pode ser mími é preciso definir uma tolerância
	# // de 0.01

		tolerancia = 0.01
		
	#
	# //alert(possiveis_pontos_x.length+" "+i);
	#
	# if (
	# (normalizado_if_1 < 1+tolerancia) &&
	# (normalizado_if_2 < 1+tolerancia) &&
	# (normalizado_if_12 < 1+tolerancia)
	# ) {
		if (
		(normalizado_if_1 < 1+tolerancia) &
		(normalizado_if_2 < 1+tolerancia) &
		(normalizado_if_12 < 1+tolerancia)
		):
			Saida.append("true")
		else:
			Saida.append("false")
	# //alert("normalizado_if_1 "+normalizado_if_1+" "+normalizado_if_2+" "+normalizado_if_12);
	# } else {
	# Saida.push("false");
	# //alert("NAO PRESTA normalizado_if_1 "+normalizado_if_1+" "+normalizado_if_2+" "+normalizado_if_12);
	# }
	#
	# //////end for
	# }
# /++
# Transformamos para poder criar pontos verdadeiros
# ++/
# transformando_deformacoes_esforcos();
	if(len(TRUE_pontos_x)>0):
		del	TRUE_pontos_x[:]

	if(len(TRUE_pontos_y)>0):
		del	TRUE_pontos_y[:]

	for i in range(0,len(possiveis_pontos_y)):# for (i = 0; i < possiveis_pontos_y.length; i++)		
# {
		if (Saida[i]=="true"):# if (Saida[i]=="true") {
# //usando apenas os pontos que sejam definidos como convenientes ou seja aqueles
# // de IF unitário
			TRUE_pontos_x.append(possiveis_pontos_x[i])# TRUE_pontos_x.push(possiveis_pontos_x[i]);
			TRUE_pontos_y.append(possiveis_pontos_y[i])# TRUE_pontos_y.push(possiveis_pontos_y[i]);

# }
# }
#
#
# ///////////
# }	
# Agosto 24, 2018 . 06:1	

def fechar6PONTOS():

	#Fazemos um estudo MASSIVO dos 6 pontos
	#Estudo inicial partendo do primeiro ponto

	#Para ter um controle de quais são os pontos que foram estudados e escolhidos
	#como parte do caminho

#	global POLIGONO_TRUE_pontos_x
#	POLIGONO_TRUE_pontos_x=[]

#	global POLIGONO_TRUE_pontos_y
#	POLIGONO_TRUE_pontos_y=[]


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

        #numeros.splice(numeros.indexOf(i_temp),1);

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

	#global POLIGONO_TRUE_pontos_x
	#POLIGONO_TRUE_pontos_x=[]
	#global POLIGONO_TRUE_pontos_y
	#POLIGONO_TRUE_pontos_y=[]

	

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
	vetor_1 = SIGMA_C_1 - alfa * s * c * tau_xy
	vetor_2 = SIGMA_C_2 -0.0+ alfa * s * c * tau_xy	
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])
# Agosto 23, 2018 . 14:39
def eq4_2(alfa, s, c, tau_xy, matriz_invertida):	
# eq4_2(alfa, s, c, tau_xy, matriz_invertida)
	vetor_1 = SIGMA_T_1 - alfa * s * c * tau_xy;
	vetor_2 = SIGMA_T_2  -0.0+ alfa * s * c * tau_xy;
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])
# Agosto 23, 2018 . 14:40
def eq4_3(alfa, s, c, tau_xy, matriz_invertida):	
#eq4_3(alfa, s, c, tau_xy, matriz_invertida)
	vetor_1 = SIGMA_T_1 - alfa * s * c * tau_xy;
	vetor_2 = SIGMA_C_2 -0.0+ alfa * s * c * tau_xy;
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])
# Agosto 23, 2018 . 14:41
def eq4_4(alfa, s, c, tau_xy, matriz_invertida):	
	vetor_1 = SIGMA_C_1 - alfa * s * c * tau_xy;
	vetor_2 = SIGMA_T_2 -0.0+ alfa * s * c * tau_xy;
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	


# Agosto 23, 2018 . 17:0
def eq4_5(alfa, s, c, tau_xy, matriz_invertida):	
	#Para eq. 4.5:
	c2 =c*c
	s2= s*s
	vetor_1 = SIGMA_C_1 - alfa * s * c * tau_xy
	vetor_2 = -TAU12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	
# Agosto 23, 2018 . 17:06
def eq4_6(alfa, s, c, tau_xy, matriz_invertida):	
	#Para eq. 4.6:
	c2 =c*c
	s2= s*s
	vetor_1 = SIGMA_T_1 - alfa * s * c * tau_xy
	vetor_2 = TAU12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	
# Agosto 23, 2018 . 17:06
def eq4_7(alfa, s, c, tau_xy, matriz_invertida):	
    #Para eq. 4.7:
	c2 =c*c
	s2= s*s
	vetor_1 = SIGMA_T_1 - alfa * s * c * tau_xy
	vetor_2 = -TAU12 + (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	
# Agosto 23, 2018 . 17:06
def eq4_8(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.8
	vetor_1 = SIGMA_C_1 - alfa * s * c * tau_xy
	vetor_2 = TAU12 -0.0+ (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	


# Agosto 23, 2018 . 17:12
def eq4_9(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.9
	vetor_1 = SIGMA_C_2 - alfa * s * c * tau_xy
	vetor_2 = -TAU12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])	

# Agosto 23, 2018 . 17:12
def eq4_10(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.10
	vetor_1 = SIGMA_T_2 - alfa * s * c * tau_xy
	vetor_2 = TAU12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])

# Agosto 23, 2018 . 17:13
def eq4_11(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.11
	vetor_1 = SIGMA_T_2 - alfa * s * c * tau_xy
	vetor_2 = -TAU12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])				

# Agosto 23, 2018 . 17:13
def eq4_12(alfa, s, c, tau_xy, matriz_invertida):	
	c2 =c*c
	s2= s*s
	#Para eq. 4.12
	vetor_1 = SIGMA_C_2 - alfa * s * c * tau_xy;
	vetor_2 = TAU12 - (c2 - s2) * tau_xy
	vetorX = np.linalg.solve(matriz_invertida, np.array([vetor_1,vetor_2]))
	possiveis_pontos_x.append(vetorX[0])
	possiveis_pontos_y.append(vetorX[1])		





def ordenar_quatro_pontos():
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
#Este formato de saída deve ser programado em cada envelope
#######################################################################################
########################################################################################


def EnvelopeFalhaFlotJson(request):	
	#print len(temporal_criterio)		
	#print "tarefa de integração estranha 	print len(temporal_criterio)		"

	response_data['data'] = EnvelopeFalhaSaidaJSON 	
	return HttpResponse(json.dumps(response_data))	

########################################################################################
# Num novo esquema ele recebe o endereço pronto!!!
#####Agosto 25, 2018 Grande problema que o iframe é chamado em oportunidade posterior ao iframe
#######################################################################################

def vertices(request):

	#return HttpResponse("vertices")
	
	vertices_POLIGONO_TRUE_pontos_x=[]
	vertices_POLIGONO_TRUE_pontos_y=[]	

	for i in range(0,len(POLIGONO_TRUE_pontos_x)):
		vertices_POLIGONO_TRUE_pontos_x.append(POLIGONO_TRUE_pontos_x[i])

	for i in range(0,len(POLIGONO_TRUE_pontos_y)):
		vertices_POLIGONO_TRUE_pontos_y.append(POLIGONO_TRUE_pontos_y[i])		

	c = {
	 'vertices_POLIGONO_TRUE_pontos_x': vertices_POLIGONO_TRUE_pontos_x,
	 'vertices_POLIGONO_TRUE_pontos_y': vertices_POLIGONO_TRUE_pontos_y,	
	 'hrefs_enderecos':hrefs_enderecos,
	 'tauXY':tauXY,
	}

	arquivo_js='vertices.js'
	return render(request, arquivo_js,c)	

def VETOR_extremos():
	VETOR_extremos=[]
	
	EXTREMOASvaloresX.sort()
	EXTREMOASvaloresY.sort()

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
	




################################## ######################################################################################### 
########    Arquivos MATLAB e GNU
# Segunda 19, 2018. Novembro
################################## ########################################################################################

import datetime

def gerarGNU(request):	
	response = HttpResponse(content_type='text/text')

	nomeTEMPO= datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

	response['Content-Disposition'] = 'attachment; filename="EnvelopesMaximaTensao_%s.dat"' % (nomeTEMPO)

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
	
	response['Content-Disposition'] = 'attachment; filename="EnvelopesMaximaTensao_%s.txt"' % (nomeTEMPO)

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
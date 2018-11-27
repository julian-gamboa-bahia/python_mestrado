# coding: utf-8

import math as Math
from math import pi, sqrt, cos, sin, pow
import numpy as np

### Novembro 27, 2018

###########################
# quando for superado o IF será representada
# 
# ponto branco, quando for menor será
# ponto preto
###########################
#Fim da definição de funções AUXILIARES

# como propriedades do material enrtra a lamina e o ângulo de rotação desta


### Novembro 27, 2018

def mapa_maxima_tensao(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):	
# Vemos o IF na direção local 1 
	if_1_t=Math.fabs(sigma_1/SIGMA_T_1) # Tração 
	if_1_c=Math.fabs(sigma_1/SIGMA_C_1) # Compressão

	if(sigma_1>0):
		if_1=if_1_t
	else:	
		if_1=if_1_c

	# Vemos o IF na direção local 2

	if_2_t=Math.fabs(sigma_2/SIGMA_T_2) # Tração 
	if_2_c=Math.fabs(sigma_2/SIGMA_C_2) # Compressão

	if(sigma_2>0):
		if_2=if_2_t
	else:
		if_2=if_2_c

	if_12=Math.fabs(tau_12/TAU12) #cisalhamento

	# sistema e saída especial

	saida=0
	if((if_1>=1) or (if_2>=1) or (if_12>=1)):
		saida=1
        
	return saida

#########################################################################################
### Novembro 27, 2018
#########################################################################################		


def mapa_maxima_deformacao(sigma_1,sigma_2,tau_12,EPSILON_T_1,EPSILON_T_2,EPSILON_C_1,EPSILON_C_2,GAMMA12,E1,E2,G12,NU12):	
# Usamos a matriz S para obter as deformações
	epsilon_1=(sigma_1/E1)-sigma_2*(NU12/E1)
	epsilon_2=(sigma_2/E2)-sigma_1*(NU12/E1)
	gamma_12=tau_12/G12
# Vemos o IF na direção local 1 
	if_1_t=Math.fabs(epsilon_1/EPSILON_T_1)
	if_1_c=Math.fabs(epsilon_1/EPSILON_C_1)

	if(sigma_1>0):
		if_1=if_1_t
	else:
		if_1=if_1_c

# Vemos o IF na direção local 2
	if_2_t=Math.fabs(epsilon_2/EPSILON_T_2)
	if_2_c=Math.fabs(epsilon_2/EPSILON_C_2)

	if(sigma_2>0):
		if_2=if_2_t
	else:
		if_2=if_2_c

	if_12=Math.fabs(gamma_12/GAMMA12)

	saida=0
	if((if_1>=1) or (if_2>=1) or (if_12>=1)):
		saida=1
        
	return saida

#########################################################################################
### Novembro 27, 2018
#########################################################################################		

def mapa_tsai_hill(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
	componente_1=(sigma_1/SIGMA_T_1)
	termo_1=componente_1*componente_1
	componente_2=(sigma_2/SIGMA_T_2) 
	termo_2=componente_2*componente_2
	componente_3=(tau_12/TAU12)
	termo_3=componente_3*componente_3
#Componente cruzado
	componente_12=((sigma_1*sigma_2)/(SIGMA_T_1*SIGMA_T_1))
	somando=termo_1+termo_2+termo_3-componente_12
	if_unico=somando

	if(if_unico>=1):
		return 1
	else:
		return 0

#########################################################################################
### Novembro 27, 2018
#########################################################################################		
def mapa_azzi_tsai(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
#sigma_1
	if(sigma_1>0):
		componente_1=(sigma_1/SIGMA_T_1)
	else:
		componente_1=(sigma_1/SIGMA_C_1)

	termo_1=componente_1*componente_1

#sigma_2

	if(sigma_2>0):
		componente_2=(sigma_2/SIGMA_T_2)
#Componente cruzado
		componente_12=((sigma_1*sigma_2)/(SIGMA_T_1*SIGMA_T_1))
	else:
		componente_2=(sigma_2/SIGMA_C_2)
#Componente cruzado
		componente_12=((sigma_1*sigma_2)/(SIGMA_C_1*SIGMA_C_1))

	termo_2=componente_2*componente_2

	componente_3=(tau_12/TAU12)
	termo_3=componente_3*componente_3

	if_unico=termo_1+termo_2+termo_3-componente_12

	if(if_unico>=1):
		return 1
	else:
		return 0
#########################################################################################
### Novembro 27, 2018
#########################################################################################						 
def mapa_tsai_wu(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12,biaxial_experimental):
	componente_potencia_1_sigma_1=sigma_1*((1.0/SIGMA_T_1)-(1/SIGMA_C_1))
	componente_potencia_1_sigma_2=sigma_2*((1.0/SIGMA_T_2)-(1/SIGMA_C_2))

	componente_potencia_2_sigma_1=(sigma_1*sigma_1)*(1.0/(SIGMA_T_1*SIGMA_C_1))
	componente_potencia_2_sigma_2=(sigma_2*sigma_2)*(1.0/(SIGMA_T_2*SIGMA_C_2))

	componente_potencia_2_tau_12=(tau_12*tau_12)*(1.0/(TAU12*TAU12))

#Previo ao compoente experimental 

	F12_potencia_1=((1.0/SIGMA_T_1)-(1.0/SIGMA_C_1)+(1.0/SIGMA_T_2)-(1/SIGMA_C_2))*biaxial_experimental
	F12_potencia_2=((1.0/(SIGMA_T_1*SIGMA_C_1))+(1.0/(SIGMA_T_2*SIGMA_C_2)))*biaxial_experimental*biaxial_experimental
	F12_sem_normalizar=1.0-F12_potencia_1-F12_potencia_2
	F12=F12_sem_normalizar/(2*biaxial_experimental*biaxial_experimental)

	componente_experimental=2*sigma_1*sigma_2*F12

	somando=componente_potencia_1_sigma_1+componente_potencia_1_sigma_2+componente_potencia_2_sigma_1+componente_potencia_2_sigma_2+componente_potencia_2_tau_12+componente_experimental

	if_unico=somando

	if(if_unico>=1):
		return 1
	else:
		return 0

#########################################################################################
### Novembro 27, 2018
#########################################################################################		
def mapa_hoffman(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
#Muito parecido com o Tsai-Wu, apenas muda o tratamento dado ao H
	componente_potencia_1_sigma_1=sigma_1*((1/SIGMA_T_1)-(1/SIGMA_C_1))
	componente_potencia_1_sigma_2=sigma_2*((1/SIGMA_T_2)-(1/SIGMA_C_2))
	componente_potencia_2_sigma_1=(sigma_1*sigma_1)*(1/(SIGMA_T_1*SIGMA_C_1))
	componente_potencia_2_sigma_2=(sigma_2*sigma_2)*(1/(SIGMA_T_2*SIGMA_C_2))
	componente_potencia_2_tau_12=(tau_12*tau_12)*(1/(TAU12*TAU12))

#Previo ao compoente experimental 

	H=-1/(2*(SIGMA_T_1*SIGMA_C_1))
	componente_experimental=2*sigma_1*sigma_2*H
	somando=componente_potencia_1_sigma_1+componente_potencia_1_sigma_2+componente_potencia_2_sigma_1+componente_potencia_2_sigma_2+componente_potencia_2_tau_12+componente_experimental

	if_unico=somando;

	if(if_unico>=1):
		return 1
	else:
		return 0
#########################################################################################
### Novembro 27, 2018
#########################################################################################		
def mapa_hashin(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
#tração na fibra
	if(sigma_1>0):
		normalizado_sigma_1=sigma_1/SIGMA_T_1
		normalizado_tau_12 =tau_12/TAU12
		if_fibra=Math.pow(normalizado_sigma_1,2)+Math.pow(normalizado_tau_12,2)
	else:
		normalizado_sigma_1=Math.fabs(sigma_1)/SIGMA_C_1
		if_fibra=normalizado_sigma_1

#tração na matriz
	if(sigma_2>0):
		normalizado_sigma_2=sigma_2/SIGMA_T_2
		normalizado_tau_12 =tau_12/TAU12	
		if_matriz=Math.pow(normalizado_sigma_2,2)+Math.pow(normalizado_tau_12,2)
#compressão na fibra
 	else:
 		TAU23=TAU12
		normalizado_sigma_2=sigma_2/(2*TAU23)
		normalizado_sigma_2_c=sigma_2/SIGMA_C_2
		normalizado_tau_12 =tau_12/TAU12
		potencia=(Math.pow((SIGMA_C_2/(2*TAU23)),2)-1)
		complemento_especial=normalizado_sigma_2_c*potencia
		if_matriz=Math.pow(normalizado_sigma_2,2)+complemento_especial+Math.pow(normalizado_tau_12,2)
	
	saida=0
	if((if_fibra>=1) or (if_matriz>=1)):
		saida=1
        
	return saida

#########################################################################################
### Novembro 27, 2018
#########################################################################################		
def mapa_christensen(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
# Modo 1 , falha na fibra:
	termo_inversos=(1/SIGMA_T_1)-(1/SIGMA_C_1)	
	termo_inversos_produtos=(1/(SIGMA_T_1*SIGMA_C_1))
	if_falha_fibra=termo_inversos*sigma_1+termo_inversos_produtos*Math.pow(sigma_1,2)
#  Modo 2 , falha na Matriz:
	termo_inversos=(1/SIGMA_T_2)-(1/SIGMA_C_2)	
	termo_inversos_produtos=(1/(SIGMA_T_2*SIGMA_C_2))
	normalizado_tau_12=tau_12/TAU12

	if_falha_matriz=termo_inversos*sigma_2+termo_inversos_produtos*Math.pow(sigma_2,2)+normalizado_tau_12*normalizado_tau_12

	saida=0
	if((if_falha_fibra>=1) or (if_falha_matriz>=1)):
		saida=1
        
	return saida
#########################################################################################
### Novembro 27, 2018
#########################################################################################		


def mapa_larc03(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12,NU12,E2,E1,G12,EPSILON_T_1,sigma_x,sigma_y,tau_xy):

	alpha=52.3
	TAU23=TAU12

	Y_T_is=1.12*Math.sqrt(2)*SIGMA_T_2
	S_L_is=Math.sqrt(2)*TAU12

# Modos do IF
#	Modo 1, Compressão na Matriz	Muito parecido com um circulo de Mohr
	#Caso do Termo T	
	if_larc_03_compressao_matriz_larc0301=0.0
	if(sigma_2<0):
		if(sigma_2<=sigma_1):
			alpha_0=53.2*(Math.pi/180)
			eta_L=(TAU12*Math.cos(alpha_0*2))/(SIGMA_C_2*Math.pow(Math.cos(alpha_0),2))
			tau_eff_L=Math.cos(alpha)*(Math.fabs(tau_12)+eta_L*sigma_2*Math.cos(alpha))
			termo_L=Math.pow(tau_eff_L/TAU12,2)
			#	Caso do Termo L			
			eta_T=-1/(Math.tan(2*alpha_0))
			tau_eff_T=-sigma_2*Math.cos(alpha)*(Math.sin(alpha)-eta_T*Math.cos(alpha))
			termo_T=Math.pow(tau_eff_T/TAU23,2)
			if_larc_03_compressao_matriz_larc0301=termo_T+termo_L

########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################

#  Modo 2 , TRAÇÂO na matriz:
#where Y T and S L are the material tensile and shear strengths as measured from unidirectional laminate tests	
# Matrix Cracking
	if_larc_03_tracao_matriz=0.0
	if(sigma_2>=0):
		NU21=NU12*(E2/E1)
		lambda_22=2*((1/E2)-(Math.pow(NU21,2)/E1))
		lambda_44=1/G12
		g=(lambda_22/lambda_44)*Math.pow((Y_T_is/S_L_is),2)

	#####Melhor usar g como quociente de G  quando não for nulo	
		
		#calculo dos termos o IF2
		termo_sigma_2=(1-g)*(sigma_2/Y_T_is)
		termo_sigma_2_QUADRADO=g*Math.pow(sigma_2/Y_T_is,2)
		termo_tau_12_QUADRADO=Math.pow(tau_12/S_L_is,2)

		if_larc_03_tracao_matriz=termo_sigma_2+termo_sigma_2_QUADRADO+termo_tau_12_QUADRADO;


########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################

	#Modo 3 , TRAÇÂO na fibra:
	if_larc_03_tracao_fibra=0.0
	if(sigma_1>=0):
		numerador_if_larc_03_tracao_fibra=((sigma_1/E1)-(sigma_2/E2)*NU12)
		if_larc_03_tracao_fibra=numerador_if_larc_03_tracao_fibra/EPSILON_T_1


########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################

#	Modo 4, Compressão na Fibra, Depende do valor de sigma_2_m
	if_larc_03_compressao_fibra_larc03_04=0.0
	if_larc_03_compressao_fibra_larc03_05=0.0

	fi=calcular_Fi(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12)

	theta_radianos=(Math.pi/180)*fi
	c=Math.cos(theta_radianos)
	s=Math.sin(theta_radianos)
	c2=c*c
	s2=s*s
	sigma_1_m=c2*sigma_x+s2*sigma_y+2*c*s*tau_xy
	sigma_2_m=s2*sigma_x+c2*sigma_y-2*c*s*tau_xy
	tau_12_m=-s*c*sigma_x+s*c*sigma_y+(c2-s2)*tau_xy

	if(sigma_1<0):
		if(sigma_2_m<0):
			alpha_0=53.2*(Math.pi/180)
			eta_L=(TAU12*Math.cos(alpha_0*2))/(SIGMA_C_2*Math.pow(Math.cos(alpha_0),2))
			if_larc_03_compressao_fibra_larc03_04=(Math.fabs(tau_12_m)+eta_L*sigma_2_m)/(S_L_is)


###########################################################
#############################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################	

#	Modo 5, Compressão na Fibra, Depende do valor de fi

	if_larc_03_compressao_fibra_larc03_05=0.0;

	if(sigma_1<0):
		if(sigma_2_m>=0):
			NU21=NU12*(E2/E1)
			lambda_22=2*((1/E2)-(Math.pow(NU21,2)/E1))
			lambda_44=1/G12
			#pode-se obter apenas usando os Lambda, e os valores de (Y_T_is,S_L_is)
			#caso lâmina grossa
			# estes valores de SIGMA_T_2 podem se usar como uma boa aproximação
			g=(lambda_22/lambda_44)*Math.pow((Y_T_is/S_L_is),2)
		#####Melhor usar g como quociente de G  quando não for nulo				
			#calculo dos termos o IF2
			termo_sigma_2=(1-g)*(sigma_2_m/Y_T_is)
			termo_sigma_2_QUADRADO=g*Math.pow(sigma_2_m/Y_T_is,2)
			termo_tau_12_QUADRADO=Math.pow(tau_12_m/S_L_is,2)

			if_larc_03_compressao_fibra_larc03_05=termo_sigma_2+termo_sigma_2_QUADRADO+termo_tau_12_QUADRADO

########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################
########################################################################################################################################################################	

#	Modo 6, Compressão na Matriz	Muito similar ao MODO 1 , mas nesta vez é preciso considerar valores "m"
	if_larc_03_compressao_matriz_larc03_06=0.0
	
	if(sigma_2<0):
		if(sigma_2>sigma_1):
#Caso do Termo T_m
			alpha_0=53.2*(Math.pi/180)
#			alpha=alpha_0
			eta_L=0.0
			tau_eff_L=Math.cos(alpha)*(Math.fabs(tau_12)+eta_L*sigma_2*Math.cos(alpha))
			termo_L=Math.pow(tau_eff_L/TAU12,2)

		#	Caso do Termo L_m
			#TAU23=TAU12
			eta_T=-1/(Math.tan(2*alpha_0))
			tau_eff_T=-sigma_2*Math.cos(alpha)*(Math.sin(alpha)-eta_T*Math.cos(alpha))
			termo_T=Math.pow(tau_eff_T/TAU23,2)
			
			if_larc_03_compressao_matriz_larc03_06=termo_T+termo_L	


	saida=0
	if(
		(if_larc_03_compressao_matriz_larc0301>=1) 
		or (if_larc_03_tracao_matriz>=1) 
		or (if_larc_03_tracao_fibra>1) 
		or (if_larc_03_compressao_fibra_larc03_04>1) 
		or (if_larc_03_compressao_fibra_larc03_05>1) 
		or (if_larc_03_compressao_matriz_larc03_06>1)):
		saida=1        
	return saida


#########################################################################################
### Novembro 27, 2018
# Auxilio
#########################################################################################		
def calcular_Fi(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12):
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
#########################################################################################
### Novembro 27, 2018
#########################################################################################		
def mapa_puck(sigma_1,sigma_2,tau_12,SIGMA_T_1,SIGMA_T_2,SIGMA_C_1,SIGMA_C_2,TAU12,EPSILON_T_1,E1,NU12,E2,EPSILON_C_1,GAMMA12):
# Modos do IF
#	Modo 1
	if_puck_modo_1=0.0
	if (sigma_1 >= 0.0):		
		EPSILON_1=((sigma_1/E1)-NU12*(sigma_2/E2))
########################################################################################################################################################################		
		E1_f=E1+0.0
########################################################################################################################################################################		
		NU12_f=NU12
########################################################################################################################################################################		
		m_sigF=0.0
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
########################################################################################################################################################################
		E1_f=E1+0.0
########################################################################################################################################################################
		m_sigF=0.0
########################################################################################################################################################################
		NU12_f=NU12+0.0
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
########################################################################################################################################################################	
		p_plus_TL=1.0
########################################################################################################################################################################
		sigma_1_D=1.0
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
########################################################################################################################################################################
		p_plus_TL=1.0
		p_minus_TL=1.0
		p_minus_TT=1.0
########################################################################################################################################################################
		sigma_1_D=1.0		
########################################################################################################################################################################
		tau12_C=1.0
########################################################################################################################################################################
		R_TT_A=1.0		
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
	saida=0
	if(
		(if_puck_modo_1>=1) 
		or (if_puck_modo_2>=1) 
		or (if_puck_modo_3>=1) 
		or (if_puck_modo_4>=1) 
		or (if_puck_modo_5>=1) ):
		saida=1        
	return saida
# coding: utf-8

# Inicio: Quarta 21, 2018. Novembro

from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect


from forms import DocumentForm
from macro.models import Laminas

import math 


#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################		

def gerar_arquivo_esforcos(request):
	if request.method == 'POST':	

		lamina=request.POST['select']
		lamina=int(lamina)

		for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(lamina)):
			SIGMA_T_1=p.SIGMA_T_1
			SIGMA_T_2=p.SIGMA_T_2
			SIGMA_C_1=-p.SIGMA_C_1  # Convenio de sinais
			SIGMA_C_2=-p.SIGMA_C_2  # Convenio de sinais
			NOME=p.NOME
			TAU12=p.TAU12

		form = DocumentForm()  

		legendaResultado="<a class=\"btn btn-primary\" href=\"/criterios_envelopes_julian/area_programador/Lendo_Arquivo_Teste/%d/\"  role=\"button\">Arquivo Gerado %s</a><br><br><b>Foi gerado um arquivo de teste  considerando os valores:</b>" % (lamina,NOME)
		
		legendaResultado="".join([legendaResultado,"<br> SIGMA_T_1 (Pa): ",str(SIGMA_T_1)]);
		legendaResultado="".join([legendaResultado,"<br> SIGMA_T_2 (Pa): ",str(SIGMA_T_2)]);
		legendaResultado="".join([legendaResultado,"<br> SIGMA_C_1 (Pa): ",str(SIGMA_C_1)]);
		legendaResultado="".join([legendaResultado,"<br> SIGMA_C_2 (Pa): ",str(SIGMA_C_2)]);

		color_fundo="background-color:gold;"

		c = {
			'form': form,			
			'legendaResultado':legendaResultado,
			'color_fundo':color_fundo,			
		}

		return render(request,'area_programador/gerarArquivoTeste.htm',c)
####END fo if			
	form = DocumentForm()
	color_fundo="background-color:powderblue;"
	c = {
		'form': form,
		'color_fundo':color_fundo,
	}
	return render(request,'area_programador/gerarArquivoTeste.htm',c)


#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################		
########################################################################################
#########################################################################################
#########################################################################################
######################   MONTE CARLO 				########################
#########################################################################################

import os as os
import csv
from numpy import random


def Lendo_Arquivo_Teste(request,lamina):

	critero="paraTodosCriterios"
# saida: um arquivo cvs indicando os valores que foram usados no teste

	response = HttpResponse(content_type='text/text')

	lamina=int(lamina)
	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(lamina)):
			SIGMA_T_1=p.SIGMA_T_1
			SIGMA_T_2=p.SIGMA_T_2
			SIGMA_C_1=p.SIGMA_C_1
			SIGMA_C_2=p.SIGMA_C_2
			NOME=p.NOME
			TAU12=p.TAU12

	compararExtremos=[]
	compararExtremos.append(SIGMA_T_1)
	compararExtremos.append(SIGMA_T_2)
	compararExtremos.append(SIGMA_C_1)
	compararExtremos.append(SIGMA_C_2)
	compararExtremos.sort()
	maximo=compararExtremos[-1]*1.5


	response['Content-Disposition'] = 'attachment; filename="Teste_%s_%s.txt"' % (NOME,critero)

	module_dir = os.path.dirname(__file__)  # diretorio atual
	print "module_dir"
	print module_dir
	csv_pre = os.path.join(module_dir, "arquivosTesteGerados")
	csv_novo = os.path.join(csv_pre, "Teste_%s_%s.txt" % (NOME,critero))
	print csv_novo

# escrevemos um arquivo csv

#temp

	with open(csv_novo, 'w') as csvfile:

	# escrevemos inicialmente o cabelhaço 
		fieldnames = ['sigma_x', 'sigma_y', 'tau_xy',]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
	# passamos os dados:
	# o esforço estatico absoluto deve ser o primero de ser testado:
		dic = {'sigma_x': 0.0, 'sigma_y': 0.0, 'tau_xy': 0.0}		
		writer.writerow(dic)
		filas=100


		for x in random.rand(filas, 2):
	# ++
			dic['sigma_x']= maximo*x[0]
			dic['sigma_y']= maximo*x[1]
			dic['tau_xy']= 0.1
			writer.writerow(dic)

	# +-
			dic['sigma_x']= maximo*x[0]
			dic['sigma_y']= -maximo*x[1]
			dic['tau_xy']= 0.1
			writer.writerow(dic)
	# --
			dic['sigma_x']= -maximo*x[0]
			dic['sigma_y']= -maximo*x[1]
			dic['tau_xy']= 0.1
			writer.writerow(dic)

	# -+
			dic['sigma_x']= -maximo*x[0]
			dic['sigma_y']= maximo*x[1]
			dic['tau_xy']= 0.1
			writer.writerow(dic)



# abre o arquivo anterior e entrega como attac
# copiamos para entrega 

	fonteCSV=open(csv_novo,"r")

	for line in fonteCSV:
		response.write(str(line))

	fonteCSV.close()
	return response


#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################		

from models import Document

def carregando_arquivo_teste_passo_1(request):

	if request.method == 'POST':	
		lamina=request.POST['select']
		lamina=int(lamina)
		criterio=request.POST['criterio']
		criterio=int(criterio)
		angulo=float(request.POST['angulo_inicial'])
		form = DocumentForm(request.POST, request.FILES)		
		if form.is_valid():
			docfile=request.FILES['docfile']
			newdoc = Document(docfile=request.FILES['docfile'])
			entrada_Esforcos=[]
			module_dir = os.path.dirname(__file__)	
			file_path = os.path.join(module_dir, 'temporal.csv')
			temporal=open(file_path,"w")
			for chunk in docfile.chunks():
				temporal.write(chunk)

			temporal.close()

			color_fundo="background-color:LightPink;"	
			# /criterios_envelopes_julian/area_programador/funcao/carregando_arquivo_teste_passo_1
			return HttpResponseRedirect( '/criterios_envelopes_julian/area_programador/carregando_arquivo_teste_passo_2/%d/%f/%d/' % (lamina,angulo,criterio))
		else:
			documents = Document.objects.all()
			color_fundo="background-color:LightPink;"			
			c={'documents': documents, 
			'form': form,
			'color_fundo':color_fundo,
			}			
			return render(request,'area_programador/list.html',c)
	else:
		form = DocumentForm()  # A empty, unbound form
			
# END IF (REQUEST METHOD)
	documents = Document.objects.all()
	color_fundo="background-color:Tan;"			
	c={'documents': documents, 
	'form': form,
	'color_fundo':color_fundo,
	}
	
	return render(request,'area_programador/list.html',c)
#########################################################################################
# Segunda 26, 2018. Novembro
#########################################################################################				
from mapas_cores import *


def carregando_arquivo_teste_passo_2(request,lamina,angulo,criterio):
	ang=float(angulo)
	criterio=int(criterio)

	for p in Laminas.objects.raw('SELECT * FROM macro_laminas where id= %s'%(lamina)):
		sig1_T=p.SIGMA_T_1
		sig2_T=p.SIGMA_T_2
		sig1_C=p.SIGMA_C_1  # Convenio de sinais
		sig2_C=p.SIGMA_C_2  # Convenio de sinais
		NOME=p.NOME
		tau12_lam=p.TAU12	

		E1=p.E1;
		E2=p.E2;
		G12=p.G12;
		NU12=p.NU12;

		EPSILON_T_1=p.EPSILON_T_1
		EPSILON_T_2=p.EPSILON_T_2
		EPSILON_C_1=p.EPSILON_C_1
		EPSILON_C_2=p.EPSILON_C_2
		GAMMA12=p.GAMMA12

	G12_lam=1
#lendo o arquivo temporal podemos ver quais são os esforços que devem ser representados
	module_dir = os.path.dirname(__file__)	
	file_path = os.path.join(module_dir, 'temporal.csv')

#Carregando o conteúdo do ARQUIVO em memoria

	entrada_Esforcos=[]
	with open(file_path) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			entrada_Esforcos.append([row['sigma_x'],row['sigma_y'],row['tau_xy']])

	resultadosBrancoPreto=[]

##########################################
	# Segunda 26, 2018. Novembro
	#Todos os critperios receberam as coordenadas locais:

	theta=math.radians(ang)
	# cuidado, com um angulo zero temos um tratamento diferente
	c=cos(theta)
	s=sin(theta)
	

	#########################################	

	for x in entrada_Esforcos:
		####### definimos a matriz de rotacao ####
		T=np.array([[c*c, s*s, 2*s*c],[s*s, c*c, -2*s*c],[-s*c, s*c,c*c-s*s]])
		esforcosGlobais=np.array([[float(x[0])], [float(x[1])], [float(x[2])]])
		#locais
		locais=np.dot(T,esforcosGlobais)
		sigma_1=locais[0]
		sigma_2=locais[1]
		tau_12=locais[2]


		if criterio == 0: #max_tensao
			nome_criterio="máxima tensão"
			#E1,E2,G12
			resultadosBrancoPreto.append(mapa_maxima_tensao(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam))
		if criterio == 1: 
			nome_criterio="máxima deformação"			
			resultadosBrancoPreto.append(mapa_maxima_deformacao(sigma_1,sigma_2,tau_12,EPSILON_T_1,EPSILON_T_2,EPSILON_C_1,EPSILON_C_2,GAMMA12,E1,E2,G12,NU12))
		if criterio == 2: 
			nome_criterio="Tsai-Hill"			
			resultadosBrancoPreto.append(mapa_tsai_hill(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam))											 			
		if criterio == 3: 
			nome_criterio="Azzi Tsai"			
			resultadosBrancoPreto.append(mapa_azzi_tsai(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam))
		if criterio == 4: 
			nome_criterio="Tsai Wu"			
			parametro_wu=tau12_lam*1.0
			resultadosBrancoPreto.append(mapa_tsai_wu(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam,parametro_wu))
		if criterio == 5: 
			nome_criterio="Hoffman"			
			parametro_wu=tau12_lam*1.0
			resultadosBrancoPreto.append(mapa_hoffman(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam))			
		if criterio == 6: 
			nome_criterio="Hashin"						
			resultadosBrancoPreto.append(mapa_hashin(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam))
		if criterio == 7: 
			nome_criterio="Christensen"
			resultadosBrancoPreto.append(mapa_christensen(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam))
		if criterio == 8: 
			nome_criterio="Puck"
			resultadosBrancoPreto.append(mapa_puck(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam,EPSILON_T_1,E1,NU12,E2,EPSILON_C_1,GAMMA12))
		if criterio == 9: 
			nome_criterio="Larc03"
			sigma_x=float(x[0])
			sigma_y=float(x[1])
			tau_xy=float(x[2])
			resultadosBrancoPreto.append(mapa_larc03(sigma_1,sigma_2,tau_12,sig1_T,sig2_T,sig1_C,sig2_C,tau12_lam,NU12,E2,E1,G12,EPSILON_T_1,sigma_x,sigma_y,tau_xy))


			
# escolhemos apenas os pontos BRANCOS (IF = 1)	
	brancos=[]
	indice=0
	for x in resultadosBrancoPreto:
		if (x==1):
			brancos.append([entrada_Esforcos[indice][0],entrada_Esforcos[indice][1]])
		indice=indice+1		
# escolhemos apenas os pontos pretos (IF = 0 )
	indice=0
	pretos=[]
	for x in resultadosBrancoPreto:
		if (x==0):
			pretos.append([entrada_Esforcos[indice][0],entrada_Esforcos[indice][1]])		
		indice=indice+1
	# saidaRender

	saidaRender = {
	 'brancos': brancos,
	 'pretos': pretos,
	'NOME':NOME,
	'nome_criterio':nome_criterio,
	}
	
	return render(request,'area_programador/passo_2_carregando.htm',saidaRender)

#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################		

#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################	

#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################		

#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################	

#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################		

#########################################################################################
# Quarta 21, 2018. Novembro
#########################################################################################	
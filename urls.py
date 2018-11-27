#coding: utf-8

from django.conf.urls import  url

from criterios_envelopes_julian import views
#criterios
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
#envelopes
from envelopes_Didaticos import envelope_maxima_tensao
from envelopes_Didaticos import envelope_maxima_deformacao
from envelopes_Didaticos import envelope_tsai_hill
from envelopes_Didaticos import envelope_azzi_tsai
from envelopes_Didaticos import envelope_tsai_wu
from envelopes_Didaticos import envelope_hoffman
from envelopes_Didaticos import envelope_hashin
from envelopes_Didaticos import envelope_christensen
from envelopes_Didaticos import envelope_puck
from envelopes_Didaticos import envelope_larc03


#Area programador
from area_Programador import arquivos_esforcos

urlpatterns = [
################################## ########################################################################################

# Agosto, 19 , 2018:
# ENTRADAS
	url(r'^entradas/$', views.entradas, name='entradas'),       # Agosto, 19 , 2018:
# iframe
	url(r'^entradas/iframe_entradas_html/$', views.iframe_entradas_html, name='iframe_entradas_html'),               
# Agosto, 22 , 2018:
# funções auxuliares
# Setembro 27, 2018. É preciso fazer chamadas personalizadas para que cada classe possa entregar as informações conforme cada tipo de envelope
# Antigamente usava-se este sistema de única URL:
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/maxima_tensao/$', envelope_maxima_tensao.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_maxima_tensao'),               
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/maxima_deformacao/$', envelope_maxima_deformacao.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_maxima_deformacao'),               	
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/tsai_hill/$', envelope_tsai_hill.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_tsai_hill'),               
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/azzi_tsai/$', envelope_azzi_tsai.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_azzo_tsai'),               
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/tsai_wu/$', envelope_tsai_wu.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_tsai_wu'),               


	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/$', envelope_puck.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_puck'),               
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/larc03/$', envelope_larc03.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_larc03'),               	
	#Auxiliares Para Tsai Wu coletar_numeroPontos
	
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/tsai_wu/coletar_biaxial_experimental/(?P<biaxial_experimental_entrada>[\w\-\.\d]+)/$', envelope_tsai_wu.coletar_biaxial_experimental, name='EnvelopeFalhaFlotJson_tsai_wu_coletar_biaxial_experimental'),               	
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/tsai_wu/coletar_numeroPontos/(?P<numeroPontos_entrada>[\w\-\.\d]+)/$', envelope_tsai_wu.coletar_numeroPontos, name='EnvelopeFalhaFlotJson_tsai_wu_coletar_numeroPontos'),               		

	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/hoffman/$', envelope_hoffman.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_hoffman'),         
	#Auxiliares Para Hoffman coletar_numeroPontos
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/hoffman/coletar_numeroPontos/(?P<numeroPontos_entrada>[\w\-\.\d]+)/$', envelope_hoffman.coletar_numeroPontos, name='EnvelopeFalhaFlotJson_hoffman_coletar_numeroPontos'),               		

	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/hashin/$', envelope_hashin.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_hashin'),         
	#Auxiliares Para Hashin coletar_numeroPontos
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/hashin/coletar_numeroPontos/(?P<numeroPontos_entrada>[\w\-\.\d]+)/$', envelope_hashin.coletar_numeroPontos, name='EnvelopeFalhaFlotJson_hashin_coletar_numeroPontos'),               		
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/hashin/coletar_TAU23/(?P<TAU23_entrada>[\w\-\.\d]+)/$', envelope_hashin.coletar_TAU23, name='EnvelopeFalhaFlotJson_hashin_coletar_TAU23'),               				

	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/christensen/$', envelope_christensen.EnvelopeFalhaFlotJson, name='EnvelopeFalhaFlotJson_christensen'),         
	#Auxiliares Para Christensen coletar_numeroPontos
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/christensen/coletar_numeroPontos/(?P<numeroPontos_entrada>[\w\-\.\d]+)/$', envelope_christensen.coletar_numeroPontos, name='EnvelopeFalhaFlotJson_christensen_coletar_numeroPontos'),               			


	#Auxiliares Para Puck coletar_numero_circulos
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_numero_circulos/(?P<numero_circulos_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_numero_circulos, name='EnvelopeFalhaFlotJson_puck_coletar_numero_circulos'),               			
	#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_numero_passos_grid/(?P<numero_passos_grid_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_numero_passos_grid, name='EnvelopeFalhaFlotJson_puck_coletar_numero_passos_grid'),               			
	#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_E1_f/(?P<E1_f_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_E1_f, name='EnvelopeFalhaFlotJson_puck_coletar_E1_f'),               			
	#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_NU12_f/(?P<NU12_f_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_NU12_f, name='EnvelopeFalhaFlotJson_puck_coletar_NU12_f'),  

	#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_m_sigF/(?P<m_sigF_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_m_sigF, name='EnvelopeFalhaFlotJson_puck_coletar_m_sigF'),  
	#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_p_plus_TL/(?P<p_plus_TL_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_p_plus_TL, name='EnvelopeFalhaFlotJson_puck_coletar_p_plus_TL'),  	

	#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_p_minus_TL/(?P<p_minus_TL_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_p_minus_TL, name='EnvelopeFalhaFlotJson_puck_coletar_p_minus_TL'),  	
	#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_p_minus_TT/(?P<p_minus_TT_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_p_minus_TT, name='EnvelopeFalhaFlotJson_puck_coletar_p_minus_TT'),  	
		#Auxiliares Para Puck numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_sigma_1_D/(?P<sigma_1_D_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_sigma_1_D, name='EnvelopeFalhaFlotJson_puck_coletar_sigma_1_D'),  	

	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_tau12_C/(?P<tau12_C_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_tau12_C, name='EnvelopeFalhaFlotJson_puck_coletar_tau12_C'),  	

	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/puck/coletar_R_TT_A/(?P<R_TT_A_entrada>[\w\-\.\d]+)/$', envelope_puck.coletar_R_TT_A, name='EnvelopeFalhaFlotJson_puck_coletar_R_TT_A'),  		


	#Auxiliares Para Larc03 coletar_numero_circulos
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/larc03/coletar_numero_circulos/(?P<numero_circulos_entrada>[\w\-\.\d]+)/$', envelope_larc03.coletar_numero_circulos, name='EnvelopeFalhaFlotJson_larc03_coletar_numero_circulos'),               			
	#Auxiliares Para Larc03 numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/larc03/coletar_numero_passos_grid/(?P<numero_passos_grid_entrada>[\w\-\.\d]+)/$', envelope_larc03.coletar_numero_passos_grid, name='EnvelopeFalhaFlotJson_larc03_coletar_numero_passos_grid'),               			


	#ESPECIAIS Auxiliares Para Larc03 numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/larc03/coletar_alpha/(?P<alpha_entrada>[\w\-\.\d]+)/$', envelope_larc03.coletar_alpha, name='EnvelopeFalhaFlotJson_larc03_coletar_alpha'),               			

	#ESPECIAIS Auxiliares Para Larc03 numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/larc03/coletar_TAU23/(?P<TAU23_entrada>[\w\-\.\d]+)/$', envelope_larc03.coletar_TAU23, name='EnvelopeFalhaFlotJson_larc03_coletar_TAU23'),               			

	#ESPECIAIS Auxiliares Para Larc03 numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/larc03/coletar_Y_T_is/(?P<Y_T_is_entrada>[\w\-\.\d]+)/$', envelope_larc03.coletar_Y_T_is, name='EnvelopeFalhaFlotJson_larc03_coletar_Y_T_is'),               			

	#ESPECIAIS Auxiliares Para Larc03 numero_passos_grid_entrada
	url(r'^entradas/iframe_entradas_html/EnvelopeFalhaFlotJson/larc03/coletar_S_L_is/(?P<S_L_is_entrada>[\w\-\.\d]+)/$', envelope_larc03.coletar_S_L_is, name='EnvelopeFalhaFlotJson_larc03_coletar_S_L_is'),               				


# Agosto, 20 , 2018:
# pasta dos CRITERIOS
	url(r'^entradas/iframe_entradas_html/criterios/(?P<nome_criterio>[\w\-\.\d]+)!/(?P<angulo>[\w\-\.\d]+)/(?P<material>[\w\-\.\d]+)/(?P<livre>[\w\-\.\d]+)/(?P<sigma_x>[\w\-\.\d]+)/(?P<sigma_y>[\w\-\.\d]+)/(?P<tau_xy>[\w\-\.\d]+)/(?P<livre_2>[\w\-\.\d]+)/$', views.criterios, name='criterios'),   
#caso especifico do TSAI WU	
	url(r'^entradas/iframe_entradas_html/criterios/tsai_wu.htm!/(?P<angulo>[\w\-\.\d]+)/(?P<material>[\w\-\.\d]+)/(?P<livre>[\w\-\.\d]+)/(?P<sigma_x>[\w\-\.\d]+)/(?P<sigma_y>[\w\-\.\d]+)/(?P<tau_xy>[\w\-\.\d]+)/(?P<livre_2>[\w\-\.\d]+)/(?P<parametro_wu>[\w\-\.\d]+)/$', views.criterios_tsai_wu, name='criterios_tsai_wu'),   	
# Agosto, 21 , 2018: Lembrar que dentro de cada Template é invocada uma função relacionada com cada critério de falha
################################## ######################################################################################### 
########     Critérios
# Função Auxiliar
# Históricos
################################ ########################################################################################
url(r'^maxima_tensao.htm/historicos_e_lista_materiais.js$', criterio_maxima_tensao.historicos_e_lista_materiais),	
url(r'^maxima_deformacao.htm/historicos_e_lista_materiais.js$', criterio_maxima_deformacao.historicos_e_lista_materiais),	
url(r'^tsai_hill.htm/historicos_e_lista_materiais.js$', criterio_tsai_hill.historicos_e_lista_materiais),	
url(r'^azzi_tsai.htm/historicos_e_lista_materiais.js$', criterio_azzi_tsai.historicos_e_lista_materiais),	

url(r'^tsai_wu.htm/historicos_e_lista_materiais.js$', criterio_tsai_wu.historicos_e_lista_materiais),	
url(r'^hoffman.htm/historicos_e_lista_materiais.js$', criterio_hoffman.historicos_e_lista_materiais),	
url(r'^hashin.htm/historicos_e_lista_materiais.js$', criterio_hashin.historicos_e_lista_materiais),	
url(r'^christensen.htm/historicos_e_lista_materiais.js$', criterio_christensen.historicos_e_lista_materiais),	

url(r'^larc03.htm/historicos_e_lista_materiais.js$', criterio_larc03.historicos_e_lista_materiais),	


################################## ######################################################################################### 
########    Arquivos MATLAB 
# Segunda 19, 2018. Novembro
################################## ########################################################################################
	url(r'^entradas/iframe_entradas_html/gerarGNU/maxima_tensao/$', envelope_maxima_tensao.gerarGNU),        
	url(r'^entradas/iframe_entradas_html/gerarGNU/maxima_deformacao/$', envelope_maxima_deformacao.gerarGNU),
	url(r'^entradas/iframe_entradas_html/gerarGNU/tsai_hill/$', envelope_tsai_hill.gerarGNU), 
	url(r'^entradas/iframe_entradas_html/gerarGNU/azzi_tsai/$', envelope_azzi_tsai.gerarGNU), 
	url(r'^entradas/iframe_entradas_html/gerarGNU/tsai_wu/$', envelope_tsai_wu.gerarGNU), 

	url(r'^entradas/iframe_entradas_html/gerarGNU/hoffman/$', envelope_hoffman.gerarGNU), 
	url(r'^entradas/iframe_entradas_html/gerarGNU/hashin/$', envelope_hashin.gerarGNU), 
	#christensen
	url(r'^entradas/iframe_entradas_html/gerarGNU/christensen/$', envelope_christensen.gerarGNU), 
	url(r'^entradas/iframe_entradas_html/gerarGNU/puck/$', envelope_puck.gerarGNU), 
	url(r'^entradas/iframe_entradas_html/gerarGNU/larc03/$', envelope_larc03.gerarGNU), 
# 20, 2018. Novembro	
	url(r'^entradas/iframe_entradas_html/matlab/maxima_tensao/$', envelope_maxima_tensao.matlab),        
	url(r'^entradas/iframe_entradas_html/matlab/maxima_deformacao/$', envelope_maxima_deformacao.matlab),
	url(r'^entradas/iframe_entradas_html/matlab/tsai_hill/$', envelope_tsai_hill.matlab), 
	url(r'^entradas/iframe_entradas_html/matlab/azzi_tsai/$', envelope_azzi_tsai.matlab), 
	url(r'^entradas/iframe_entradas_html/matlab/tsai_wu/$', envelope_tsai_wu.matlab), 

	url(r'^entradas/iframe_entradas_html/matlab/hoffman/$', envelope_hoffman.matlab), 
	url(r'^entradas/iframe_entradas_html/matlab/hashin/$', envelope_hashin.matlab), 	
	url(r'^entradas/iframe_entradas_html/matlab/christensen/$', envelope_christensen.matlab), 
	url(r'^entradas/iframe_entradas_html/matlab/puck/$', envelope_puck.matlab), 
	url(r'^entradas/iframe_entradas_html/matlab/larc03/$', envelope_larc03.matlab), 

################################## ######################################################################################### 
########     Envelopes
################################## ########################################################################################
	url(r'^entradas/iframe_entradas_html/envelopes/(?P<nome_criterio>[\w\-\.\d]+)!/(?P<angulo>[\w\-\.\d]+)/(?P<material>[\w\-\.\d]+)/(?P<livre>[\w\-\.\d]+)/(?P<sigma_x>[\w\-\.\d]+)/(?P<sigma_y>[\w\-\.\d]+)/(?P<tau_xy>[\w\-\.\d]+)/(?P<livre_2>[\w\-\.\d]+)/$', views.envelopes, name='envelopes'),   
#apagar
	#url(r'^ordenar_quatro_pontos.js$', views.ordenar_quatro_pontos),
	#url(r'^equacoes_41_412.js$', views.equacoes_41_412),
	#url(r'^usar_GraphView.js$', views.usar_GraphView),
	#url(r'^construir_COM_POLIGONO_TRUE_pontos.js$', views.construir_COM_POLIGONO_TRUE_pontos),
#flot
#VERTICES no esquema de envelopes, ou seja chamada única e redestribuida 
	url(r'^vertices/maxima_tensao', envelope_maxima_tensao.vertices, name='vertices_maxima_tensao'),   
	url(r'^vertices/maxima_deformacao', envelope_maxima_deformacao.vertices, name='vertices_maxima_deformacao'),   
	url(r'^vertices/tsai_hill', envelope_tsai_hill.vertices, name='vertices_tsai_hill'),   
	url(r'^vertices/azzi_tsai', envelope_azzi_tsai.vertices, name='vertices_azzi_tsai'),   	
	url(r'^vertices/tsai_wu', envelope_tsai_wu.vertices, name='vertices_tsai_wu'),   	
	url(r'^vertices/hoffman', envelope_hoffman.vertices, name='vertices_hoffman'),   
	url(r'^vertices/hashin', envelope_hashin.vertices, name='vertices_hashin'),   
	url(r'^vertices/christensen', envelope_christensen.vertices, name='vertices_christensen'),   
	url(r'^vertices/puck', envelope_puck.vertices, name='vertices_puck'),   
	url(r'^vertices/larc03', envelope_larc03.vertices, name='vertices_larc03'),   

# Dúvida, este aqui vai sem a chamada de critério
	url(r'^entradas/iframe_entradas_html/iframe_flot/', views.iframe_flot, name='iframe_flot'),   	


################################## ######################################################################################### 
########     Área programador   ############# 
################################## ########################################################################################
# TELA PRINCIPAL para pegar um arquivo de texto e ver com quais valores gera um IF de um ou zero.
	url(r'^area_programador/$', views.area_programador),

	url(r'^area_programador/funcao/gerar_arquivo_esforcos$', arquivos_esforcos.gerar_arquivo_esforcos),  
	url(r'^area_programador/Lendo_Arquivo_Teste/(?P<lamina>\d+)/$', arquivos_esforcos.Lendo_Arquivo_Teste),               
#carregar arquivo	
	url(r'^area_programador/funcao/carregando_arquivo_teste_passo_1$', arquivos_esforcos.carregando_arquivo_teste_passo_1),               
	url(r'^area_programador/carregando_arquivo_teste_passo_2/(?P<lamina>\d+)/(?P<angulo>-?[0-9]\d*(\.\d+)?)/(?P<criterio>\d+)/$', arquivos_esforcos.carregando_arquivo_teste_passo_2),

################################## aulas:
	url(r'^aulas/(?P<numeroURL>-?[0-9]\d*(\.\d+)?)/$', views.aulas, name='aulas'),	
# js para os botonzinhos que permite trocar entre funções:
               url(r'^js/$', views.js, name='js'),
               url(r'^js/dialog/$', views.js_dialog, name='js_dialog'),
# ajudas:
	      url(r'^SaidasAjudaEnvelope/(?P<criterioHTML>\d{1})/$', views.SaidasAjudaEnvelope),
	#  2016 Agosto 23
	      #url(r'^FlotJson/$', views.FlotJson, name='FlotJson'),
################################## ######################################################################################### 
########    Tela unificada e filtro
# Segunda 26, 2018. Novembro
################################## ########################################################################################
	url(r'^redesenho/(?P<nome_criterio>[\w\-\.\d]+)/(?P<numero_envelope>\d+)/$', views.coletarENVELOPE),        	
	url(r'^redesenho/entregarENVELOPE/$', views.entregarENVELOPE),        	
	url(r'^redesenho/flot/$', views.redesenho_flot),        	
	url(r'^redesenho/zerar/$', views.ZERAR_coletarENVELOPE),        	
]

/*
Agosto 21:
Arranjos de Argumentos que serão apresentados na tela
*/	

	/*
	A lista de materiais é passada usando um FOR
	*/
	lista_materiais=[];
	{% for material in materiais %}
	lista_materiais.push("{{material}}");
	{% endfor %}

	/*
	No formato URL : O histórico de cálculos será passado usando um FOR
	*/
	lista_historico=[];
	{% for elemento_historico in historico %}
	lista_historico.push("{{elemento_historico}}");
	{% endfor %}

	/*
	O histórico de ESFORCOS será passado usando um FOR
	*/
	esforcos_historicos=[];
	{% for elemento_esforcos_historicos in esforcos_historicos %}
	esforcos_historicos.push("{{elemento_esforcos_historicos}}");
	{% endfor %}

	/*
	O histórico de Materiais será passado usando um FOR
	*/
	materiais_historicos=[];
	{% for elemento_materiais_historicos in materiais_historicos %}
	materiais_historicos.push("{{elemento_materiais_historicos}}");
	{% endfor %}

	/*
	O histórico de ANGULOS será passado usando um FOR
	*/
	angulo_historico=[];
	{% for elemento_angulo_historico in angulo_historico %}
	angulo_historico.push("{{elemento_angulo_historico}}");
	{% endfor %}

	//alert("lista_historico");

/*
Agosto 22:
Vértices para serem representados no sistema
*/	





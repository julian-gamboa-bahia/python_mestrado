/*
Agosto 25 00:32 

*/

	

$(document).ready(function(){	

	POLIGONO_TRUE_pontos_x=[];
	POLIGONO_TRUE_pontos_y=[];

	//"Outubro 04 "

	POLIGONO_TRUE_pontos_xy=[];

	//alert("vertices_POLIGONO_TRUE_pontos_x"); 	alert({{vertices_POLIGONO_TRUE_pontos_x}});

	{% for x in vertices_POLIGONO_TRUE_pontos_x %}
	POLIGONO_TRUE_pontos_x.push({{x}});
	{% endfor %}

	{% for y in vertices_POLIGONO_TRUE_pontos_y %}
	POLIGONO_TRUE_pontos_y.push({{y}});
	{% endfor %}

	//vertices_POLIGONO_TRUE_pontos_xy


	{% for y in vertices_POLIGONO_TRUE_pontos_xy %}
	POLIGONO_TRUE_pontos_xy.push({{y}});
	{% endfor %}

	//alert("POLIGONO_TRUE_pontos_xy  "+POLIGONO_TRUE_pontos_xy);
	//alert("POLIGONO_TRUE_pontos_y");	alert(POLIGONO_TRUE_pontos_y);	alert("POLIGONO_TRUE_pontos_x");	alert(POLIGONO_TRUE_pontos_x);

/*
    url_original=window.location.href;
    base_url= url_original.split("!");
//trocando para critérios
    url_criterios=base_url[0].replace("/envelopes/","/criterios/");    //+"---"+base_url[1].replace("envelopes","criterios");    
*/
    //alert(url_criterios);

    //alert(POLIGONO_TRUE_pontos_x.length);

    for(i=0;i<POLIGONO_TRUE_pontos_x.length;i++)
    {
        teste_sigma_x=POLIGONO_TRUE_pontos_x[i];
        teste_sigma_y=POLIGONO_TRUE_pontos_y[i];        

        /*

			#http://127.0.0.1:8000/criterios_envelopes_julian/entradas/iframe_entradas_html/criterios/maxima_tensao.htm!/0/1/00/0/0/0/0/
			# 																							maxima_tensao.htm!/11/1/00/0/

			hrefs_enderecos="%s!/%s/%s/%s/" % (criterio,angulo,material,livre)
        */

        
        //url_criterios+"!/"+angulo+"/"+laminaURL+"/00/"+teste_sigma_x+"/"+teste_sigma_y+"/"+tauXY+"/0/";
        if(POLIGONO_TRUE_pontos_xy.length==0)
        {
			endereco="/criterios_envelopes_julian/entradas/iframe_entradas_html/criterios/"+"{{hrefs_enderecos}}"+teste_sigma_x+"/"+teste_sigma_y+"/"+"{{tauXY}}"+"/0/";
        }
        else
        {
        	endereco="/criterios_envelopes_julian/entradas/iframe_entradas_html/criterios/"+"{{hrefs_enderecos}}"+teste_sigma_x+"/"+teste_sigma_y+"/"+POLIGONO_TRUE_pontos_xy[i]+"/0/";	
        }  

        biaxial_experimental_global="{{biaxial_experimental_global}}";

        if(biaxial_experimental_global.length>0)
        {
//			endereco="http://127.0.0.1/outubro/criterios/tsai_wu.htm?/{{angulo}}/1/00/"+teste_sigma_x+"/"+teste_sigma_y+"/"+"{{tauXY}}"+"/0/{{biaxial_experimental_global}}";	
			endereco="/criterios_envelopes_julian/entradas/iframe_entradas_html/criterios/"+"{{hrefs_enderecos}}"+teste_sigma_x+"/"+teste_sigma_y+"/"+"{{tauXY}}"+"/0/{{biaxial_experimental_global}}";
        }   	
		
		//alert("{{hrefs_enderecos}}");
		//alert(endereco);

        $("#vertice_"+i).text("("+teste_sigma_x+","+teste_sigma_y+")");
        $("#vertice_"+i).attr("href",endereco);
    }

///////////
});

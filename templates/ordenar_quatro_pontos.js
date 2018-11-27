function ordenar_quatro_pontos()
{
        var separacao_tecnica=Math.abs(possiveis_pontos_x[0])*1.0e-3; //pegamos o primeiro elemento

        //primeiramente evitamos que tenha um valor de X com multiplicidade

        for ( i = 0; i < possiveis_pontos_x.length; i++) {
            for ( j = i -0+1; j < possiveis_pontos_x.length; j++) {
                var diff = possiveis_pontos_x[i] - possiveis_pontos_x[j];
                if (diff == 0.0) {
                    possiveis_pontos_x[j]=possiveis_pontos_x[i] -0.0+ separacao_tecnica;
                }
            }
        }

//Fazemos ordenamento por burbulha

        var ORDEM_ASCII="true";

        var minimo=possiveis_pontos_x[0];

        for(i = 0; i < possiveis_pontos_x.length; i++)
        {
            if(possiveis_pontos_x[i]<minimo)
            {
                ORDEM_ASCII="false";
            }
            minimo=possiveis_pontos_x[i];
        }

        if(ORDEM_ASCII=="false")
        {
            var menor_arco_1_x;
            var menor_arco_1_y;
            var TEMP_arco_1_x;
            var TEMP_arco_1_y;


            for (i = 0; i < possiveis_pontos_x.length; i++)
            {
                menor_arco_1_x=possiveis_pontos_x[i]-0.0;
                menor_arco_1_y=possiveis_pontos_y[i]-0.0;

                for(j=i-0+1;j<possiveis_pontos_x.length;j++)
                {
                    if((possiveis_pontos_x[j]-0.0)<(menor_arco_1_x-0.0))
                    {
			//lert(possiveis_pontos_x[j]+" menor "+menor_arco_1_x);

                        TEMP_arco_1_x=possiveis_pontos_x[j];
                        possiveis_pontos_x[j]=menor_arco_1_x;
                        possiveis_pontos_x[i]=TEMP_arco_1_x;
//O mesmo para Y para assim manter o sistema ordenado
                        TEMP_arco_1_y=possiveis_pontos_y[j];
                        possiveis_pontos_y[j]=menor_arco_1_y;
                        possiveis_pontos_y[i]=TEMP_arco_1_y;
                        break;
                    }
///for
                }
            }
        }


//Agora temos ordenada a informação
        for ( i = 0; i < possiveis_pontos_x.length; i++) {
		dados_GNU=dados_GNU+possiveis_pontos_x[i]+"  "+possiveis_pontos_y[i]+"%5Cn"; //%5Cn
	}

//////////////////
}

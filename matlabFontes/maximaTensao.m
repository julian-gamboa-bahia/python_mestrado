

%-- 21/04/2016 15:10 --%

% simulação do critério de falha de máxima tensão.

%disp('teste do criterio de falha');
%disp('Máxima Tensão');


% matriz de rotação para qualquer ângulo:

c=cos(pi*(x/180));
s=sin(pi*(x/180));

% definimos a matriz T , com entrada em degree x

T=[ c*c s*s 2*s*c; s*s c*c  -2*s*c; -c*s s*c c*c-s*s]; 

%  Indicamos valores numericos
%  dos valores extremos de esforços de tração e compressão

%disp('valores extremos em unidades de Pascal');

% tendo apenas um esforço inicial, neste caso o tau_xy, podemos propor 
% 6 sistemas de equações com o intuito de obter 

syms sigma_x  sigma_y;

esforcos_globais=[ sigma_x ; sigma_y ; tau_xy ];

sistema_geral=T*esforcos_globais;

%disp('ponto 1');
%disp('Tensão Tensão');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_T_1   ;
        sistema_geral(2,1)-SIGMA_T_2   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto1_x=eval(sigma_x);
ponto1_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto1_x,ponto1_y);

%%%%%%%%%%break 

%disp('ponto 2');
%disp('Compressão Compressão');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_C_1   ;
        sistema_geral(2,1)-SIGMA_C_2   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto2_x=eval(sigma_x);
ponto2_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto2_x,ponto2_y);

%%%%%%%%%%break 

%disp('ponto 3');
%disp('Tensão Compressão');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_T_1   ;
        sistema_geral(2,1)-SIGMA_C_2   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto3_x=eval(sigma_x);
ponto3_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto3_x,ponto3_y);

%%%%%%%%%%break 

%disp('ponto 4');
%disp('Compressão Tensão');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_C_1   ;
        sistema_geral(2,1)-SIGMA_T_2   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto4_x=eval(sigma_x);
ponto4_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto4_x,ponto4_y);

%%%%%break

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Agora com
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% cisalhamento 

%disp('ponto 5');
%disp('Tensão Cisalhamento Positivo');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_T_1   ;
        sistema_geral(3,1)-TAU12   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto5_x=eval(sigma_x);
ponto5_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto5_x,ponto5_y);

%%%%%break

%disp('ponto 6');
%disp('Compressão Cisalhamento Positivo');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_C_1   ;
        sistema_geral(3,1)-TAU12   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto6_x=eval(sigma_x);
ponto6_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto6_x,ponto6_y);

%%%%%break

%disp('ponto 7');
%disp('Tensão Cisalhamento Negativo');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_T_1   ;
        sistema_geral(3,1)+TAU12   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto7_x=eval(sigma_x);
ponto7_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto7_x,ponto7_y);

%%%%%break

%disp('ponto 8');
%disp('Compressão Cisalhamento Negativo');

sistema1=[ 
        sistema_geral(1,1)-SIGMA_C_1   ;
        sistema_geral(3,1)+TAU12   
          ];
[sigma_x,sigma_y]=solve(sistema1(1,1),sistema1(2,1));      
ponto8_x=eval(sigma_x);
ponto8_y=eval(sigma_y);

sprintf('X: %f Y: %f',ponto8_x,ponto8_y);

% Agora cálculamos os pontos de interseção das retas definidas pelos 8
% ptos. do sistema.

% graficamos o primeiro quadrado:

quadrado1_x=[
ponto1_x; 
ponto3_x;
ponto2_x;
ponto4_x;
ponto1_x; 
];

quadrado1_y=[
ponto1_y; 
ponto3_y;
ponto2_y;
ponto4_y;
ponto1_y; 
];

% graficamos o segundo quadrado:

quadrado2_x=[
ponto5_x;
ponto7_x;
ponto8_x;
ponto6_x;
ponto5_x;
];

quadrado2_y=[
ponto5_y;
ponto7_y;
ponto8_y;
ponto6_y;
ponto5_y;
];


% Agora calculamos:
% 1) coefificente angular
% 2) Ponto de interseção enre as diversas retas definidas

envelopePonto1=novoPonto(ponto4_x,ponto4_y,ponto1_x,ponto1_y,ponto6_x,ponto6_y,ponto5_x,ponto5_y);
envelopePonto2=novoPonto(ponto4_x,ponto4_y,ponto1_x,ponto1_y,ponto7_x,ponto7_y,ponto8_x,ponto8_y);
envelopePonto3=novoPonto(ponto2_x,ponto2_y,ponto3_x,ponto3_y,ponto7_x,ponto7_y,ponto8_x,ponto8_y);
envelopePonto4=novoPonto(ponto2_x,ponto2_y,ponto3_x,ponto3_y,ponto6_x,ponto6_y,ponto5_x,ponto5_y);

% Graficamos o envelope final:

envelope_x=[
envelopePonto1(1,1);
envelopePonto2(1,1);
envelopePonto3(1,1);
envelopePonto4(1,1);
envelopePonto1(1,1);
];
envelope_y=[
envelopePonto1(2,1);
envelopePonto2(2,1);
envelopePonto3(2,1);
envelopePonto4(2,1);
envelopePonto1(2,1);
];

plot(quadrado1_x(1:5),quadrado1_y(1:5))  % este é o cuadrado que representa o envelope de falha

titulo=sprintf('Grafico do envelope de falha do critéro \n de Máxima Tensão do %s com ângulo de %3.2f' ,NOME,x);
title(titulo);
text(0,0,sprintf('\\tau_{xy}=%3.2f',tau_xy),'FontSize',18);
ylabel('\sigma_y (Pa)');
xlabel('\sigma_x (Pa)');
grid;




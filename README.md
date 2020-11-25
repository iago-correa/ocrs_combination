# Uma Análise da Combinação de Motores de Reconhecimento Óptico de Caracteres

Código resultante do projeto de graduação no curso de Engenharia de Automação. 

**Resumo**

Muitas empresas que realizam compras de peças ou ferramentas retêm documentos como notas, recibos, formulários ou manuais de instrução ao decorrer dos anos e atualmente se encontram com a necessidade de digitalizar esses documentos acumulados, não só como forma de reter informações para consultas de forma mais rápido, mas também como forma de implementar novos sistemas automáticos de busca. Assim, ao utilizar sistemas de OCR para o reconhecimento de caracteres nesses documentos é possível notar que esses sistemas podem apresentar duas dificuldades principais. A primeira é localizar o texto que é disposto de uma forma não contínua, diferente de um texto corrido. E a segunda, é acertar palavras que se aproximam mais de códigos e menos de palavras da linguagem humana.  

Apesar de existirem muitos trabalhos na literatura acerca de texto não corrido, como formulários e tabelas, não existe uma preocupação a respeito do problema com códigos. Sendo assim, como forma de possibilitar que tais empresas possam facilmente corrigir esse problema sem necessidade de buscar por extensivos bancos de dados ou realizar treinamento ou desenvolvimento de novos modelos, este trabalho analisou como aproveitar modelos pré-treinados de motores de OCR através da estratégia de combinação de classificadores para documentos assemelham aos descritos.

Neste trabalho primeiro foram apresentados resultados individuais dos motores de OCR, utilizando modelos padrões e sem nenhum refinamento de parâmetros ou treinamento. Então, são realizados experimentos explorando como forma de combinação o voto majoritário, ranqueamento e mediana de strings com e sem ponderamento das confianças dos OCRs. Os resultados obtidos através dos experimentos realizados neste trabalho indicam que a combinação entre a saída de diferentes motores de OCR podem apresentar melhoria nos resultados para algumas combinações e conjuntos de OCR.

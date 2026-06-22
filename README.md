Projeto de Predição de Abandono do Tratamento da Tuberculose!

Este projeto foi desenvolvido no contexto do Nanodegree de Machine Learning, com o objetivo de construir modelos capazes de prever a probabilidade de abandono do tratamento da tuberculose (Loss to Follow-up – LTFU) a partir de dados do Sistema de Informação de Agravos de Notificação (SINAN). Além do treinamento e avaliação dos modelos, o projeto contempla técnicas de explicabilidade e uma aplicação web para apoio à decisão clínica.

Objetivo

Desenvolver e avaliar modelos de aprendizado de máquina capazes de identificar pacientes com maior risco de abandono do tratamento da tuberculose, permitindo a adoção de estratégias preventivas e contribuindo para o acompanhamento de pacientes mais vulneráveis.

Estrutura do Projeto

projeto-tuberculose
│
├── dados/
│
├── fonte/
│   ├── tratamento_dados.py
│   ├── treinar_modelo.py
│   └── avaliar_modelo.py
│
├── interface/
│   └── app_tb.py
│
├── modelo/
│   ├── modelo_rf.pkl
│   ├── modelo_rf_reduzido.pkl
│   └── ...
│
├── notebooks/
│   └── projeto.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore

Base de Dados

Os dados utilizados neste projeto foram disponibilizados no contexto do Nanodegree de Machine Learning e são provenientes do Sistema de Informação de Agravos de Notificação (SINAN).

Os arquivos processados não são armazenados neste repositório devido ao seu tamanho. Os conjuntos de dados, juntamente com as instruções para instalação dos mesmos podem ser obtidos em:

https://github.com/klein-natan/tuberculosis-ltfu-prediction

Arquivos utilizados:

* treino.csv
* teste1.csv
* teste2.csv

Modelos Desenvolvidos

Foram desenvolvidos os seguintes modelos:

* Regressão Logística (baseline);
* Random Forest completo;
* Random Forest reduzido utilizando apenas as variáveis mais importantes.

Desempenho dos modelos

Modelo	Accuracy	Precision	Recall	F1-score	ROC-AUC
Regressão Logística	0,71	0,63	0,81	0,71	0,808
Random Forest Completo	0,73	0,65	0,83	0,73	0,813
Random Forest Reduzido	0,73	0,66	0,81	0,73	0,812

Técnicas Utilizadas

* Python
* Pandas
* NumPy
* Scikit-Learn
* Random Forest
* Regressão Logística
* SHAP
* Permutation Importance
* Joblib
* Streamlit

Executando o Projeto

1. Clone o repositório

git clone https://github.com/leoross20/trabalho_tb.git

2. Instale as dependências

pip install -r requirements.txt

3. Coloque os arquivos de dados na pasta dados

dados/
├── treino.csv
├── teste1.csv
└── teste2.csv

4. Execute a interface

streamlit run interface/app_tb.py

Explicabilidade

Para interpretação do modelo foram utilizadas técnicas de Inteligência Artificial Explicável (xAI):

* Permutation Importance;
* SHAP Summary Plot;
* SHAP Waterfall Plot.

Essas técnicas permitiram identificar as variáveis mais relevantes associadas ao abandono do tratamento e compreender o impacto de cada característica nas predições realizadas.

Aplicação

Foi desenvolvida uma aplicação em Streamlit para permitir que profissionais da saúde insiram um conjunto reduzido de informações do paciente e obtenham uma estimativa da probabilidade de abandono do tratamento, servindo como ferramenta de apoio à decisão.

Autores

* Leonardo Ross Dapper — RA: 1136153
* João Vitor Bastos — RA: 1136345
* Eduardo Cardoso — RA: 1221865

Instituição

ATITUS Educação
Curso de Ciência da Computação
Nanodegree de Machine Learning
2026

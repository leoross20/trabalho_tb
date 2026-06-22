import streamlit as st
import pandas as pd
import os
import joblib

st.set_page_config(page_title="Abandono TB — Predição", layout="centered")

st.markdown("""
<style>
    .topo {
        border-left: 3px solid #2563EB;
        padding: 0.5rem 1rem;
        margin-bottom: 1.4rem;
        background: #F8FAFF;
        border-radius: 0 5px 5px 0;
    }
    .topo h2 { margin: 0; font-size: 1.2rem; color: #1E3A5F; font-weight: 600; }
    .topo p  { margin: 0.2rem 0 0 0; font-size: 0.82rem; color: #6B7280; }

    .secao {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #9CA3AF;
        margin: 1.4rem 0 0.5rem 0;
    }

    .res-alto  { background:#FFF5F5; border:1.5px solid #FC8181; border-radius:7px; padding:1.1rem 1.4rem; margin-top:1.2rem; }
    .res-medio { background:#FFFBF0; border:1.5px solid #F6AD55; border-radius:7px; padding:1.1rem 1.4rem; margin-top:1.2rem; }
    .res-baixo { background:#F0FFF4; border:1.5px solid #68D391; border-radius:7px; padding:1.1rem 1.4rem; margin-top:1.2rem; }

    .res-alto h3  { color:#C53030; margin:0 0 0.15rem 0; font-size:1.55rem; }
    .res-medio h3 { color:#C05621; margin:0 0 0.15rem 0; font-size:1.55rem; }
    .res-baixo h3 { color:#276749; margin:0 0 0.15rem 0; font-size:1.55rem; }

    .res-alto p, .res-medio p, .res-baixo p {
        margin: 0.35rem 0 0 0;
        font-size: 0.88rem;
        line-height: 1.55;
        color: #374151;
    }

    .rodape {
        font-size: 0.72rem;
        color: #C0C7D0;
        text-align: center;
        margin-top: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topo">
    <h2>Predição de abandono de tratamento — Tuberculose</h2>
    <p>Preencha os dados do paciente. O resultado é uma estimativa de risco para apoiar a decisão clínica, não substitui avaliação profissional.</p>
</div>
""", unsafe_allow_html=True)


@st.cache_resource
def carregar_modelo():
    caminho = "modelo/modelo_final.pkl"

    if os.path.exists(caminho):
        return joblib.load(caminho)

    return None


modelo = carregar_modelo()
demo = modelo is None

if demo:
    st.warning(
        "Modelo não encontrado em `modelo/modelo_final.pkl`. "
        "A interface funcionará apenas com uma estimativa demonstrativa."
    )


st.markdown('<div class="secao">Identificação</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    idade = st.number_input(
        "Idade",
        min_value=00,
        max_value=110,
        value= None,
        step=1
    )

with c2:
    sexo = st.selectbox(
    "Sexo",
    ["", "Masculino", "Feminino"],
    index=0
)

c3, c4 = st.columns(2)

with c3:
    raca = st.selectbox(
    "Raça/Cor",
    ["", "Branca", "Preta", "Parda", "Amarela", "Indígena", "Ignorado"],
    index=0
)

with c4:
    escolaridade = st.selectbox(
        "Escolaridade",
        [
            "",
            "Sem escolaridade",
            "Fund. incompleto (1ª–4ª série)",
            "Fund. incompleto (5ª–8ª série)",
            "Fund. completo",
            "Médio incompleto",
            "Médio completo",
            "Superior incompleto",
            "Superior completo",
            "Ignorado",
        ],
        index=0
    )


st.markdown('<div class="secao">Dados clínicos</div>', unsafe_allow_html=True)

c5, c6 = st.columns(2)

with c5:
    entrada = st.selectbox(
    "Tipo de entrada",
    ["", "Caso novo", "Recidiva", "Reingresso após abandono", "Não sabe"],
    index=0
)

with c6:
    hiv = st.selectbox(
    "Sorologia HIV",
    ["", "Positivo", "Negativo", "Em andamento", "Não realizado"],
    index=0
)

c7, c8 = st.columns(2)

with c7:
    raiox = st.selectbox(
    "Raio-X de tórax",
    ["", "Suspeito", "Normal", "Outra patologia", "Não realizado"],
    index=0
)

with c8:
    contatos = st.number_input(
    "Número de contatos identificados",
    min_value=0,
    max_value=99,
    value=None,
    placeholder="Informe o número"
)

tipo_unidade = st.selectbox(
    "Tipo de unidade notificadora",
    ["", "Unidade básica / ambulatório", "Hospital",
     "Pronto atendimento / urgência", "Outra unidade"],
    index=0
)


st.markdown('<div class="secao">Comorbidades</div>', unsafe_allow_html=True)

cc1, cc2, cc3 = st.columns(3)

with cc1:
    aids = st.checkbox("AIDS")
    alcool = st.checkbox("Alcoolismo")

with cc2:
    drogas = st.checkbox("Uso de drogas ilícitas")
    tabaco = st.checkbox("Tabagismo")

with cc3:
    st.write("")


st.markdown('<div class="secao">Situação social</div>', unsafe_allow_html=True)

cs1, cs2 = st.columns(2)

with cs1:
    ppl = st.checkbox("Privado de liberdade")

with cs2:
    rua = st.checkbox("Situação de rua")


def sn_int(valor):
    return "1" if valor else "2"


def sn_float(valor):
    return "1.0" if valor else "2.0"


mapa_sexo = {
    "Masculino": "M",
    "Feminino": "F"
}

mapa_raca = {
    "Branca": "1",
    "Preta": "2",
    "Amarela": "3",
    "Parda": "4",
    "Indígena": "5",
    "Ignorado": "9"
}

mapa_escol = {
    "Sem escolaridade": "0",
    "Fund. incompleto (1ª–4ª série)": "1",
    "Fund. incompleto (5ª–8ª série)": "3",
    "Fund. completo": "4",
    "Médio incompleto": "5",
    "Médio completo": "6",
    "Superior incompleto": "7",
    "Superior completo": "8",
    "Ignorado": "9",
}

mapa_entrada = {
    "Caso novo": "1",
    "Recidiva": "2",
    "Reingresso após abandono": "3",
    "Não sabe": "4"
}

mapa_hiv = {
    "Positivo": "1.0",
    "Negativo": "2.0",
    "Em andamento": "3.0",
    "Não realizado": "4.0"
}

mapa_raiox = {
    "Suspeito": "1.0",
    "Normal": "2.0",
    "Outra patologia": "3.0",
    "Não realizado": "4.0"
}

mapa_unidade = {
    "Unidade básica / ambulatório": 2,
    "Hospital": 5,
    "Pronto atendimento / urgência": 7,
    "Outra unidade": 9,
}


if st.button("Calcular risco", type="primary"):

    if st.button("Calcular risco", type="primary"):

        if (
            idade is None
            or contatos is None
            or sexo == ""
            or raca == ""
            or escolaridade == ""
            or entrada == ""
            or hiv == ""
            or raiox == ""
            or tipo_unidade == ""
        ):
            st.error("Preencha todos os campos antes de calcular o risco.")
            st.stop()

    registro = {
        ...
    }

    registro = {
        "TRATAMENTO": mapa_entrada[entrada],
        "POP_LIBER": sn_int(ppl),
        "AGRAVDROGA": sn_float(drogas),
        "POP_RUA": sn_int(rua),
        "AGRAVALCOO": sn_float(alcool),
        "HIV": mapa_hiv[hiv],
        "NU_CONTATO": contatos,
        "RAIOX_TORA": mapa_raiox[raiox],
        "idade_val": idade,
        "CS_ESCOL_N": mapa_escol[escolaridade],
        "TPUNINOT": mapa_unidade[tipo_unidade],
        "AGRAVAIDS": sn_float(aids),
        "CS_SEXO": mapa_sexo[sexo],
        "AGRAVTABAC": sn_float(tabaco),
        "CS_RACA": mapa_raca[raca],
    }

    df = pd.DataFrame([registro])

    for coluna in df.select_dtypes(include="object").columns:
        df[coluna] = df[coluna].astype(str)

    if demo:
        pontos = 0

        if mapa_entrada[entrada] == "3":
            pontos += 30
        elif mapa_entrada[entrada] == "2":
            pontos += 15

        if drogas:
            pontos += 15
        if alcool:
            pontos += 12
        if hiv == "Positivo":
            pontos += 12
        if rua:
            pontos += 20
        if ppl:
            pontos += 10
        if aids:
            pontos += 8
        if tabaco:
            pontos += 5

        prob = min(pontos / 100, 0.95)

    else:
        try:
            prob = modelo.predict_proba(df)[0][1]
        except Exception as erro:
            st.error(f"Erro ao executar o modelo: {erro}")
            st.stop()

    pct = prob * 100

    if prob >= 0.70:
        classe = "res-alto"
        nivel = "Risco alto"
        texto = (
            "Recomenda-se acompanhamento intensificado. "
            "O paciente apresenta características associadas a maior risco de abandono do tratamento."
        )

    elif prob >= 0.50:
        classe = "res-medio"
        nivel = "Risco moderado"
        texto = (
            "Recomenda-se monitoramento próximo e reforço das orientações sobre a importância da continuidade do tratamento."
        )

    else:
        classe = "res-baixo"
        nivel = "Risco baixo"
        texto = (
            "Seguir acompanhamento padrão, mantendo a reavaliação ao longo do tratamento."
        )

    st.markdown(f"""
    <div class="{classe}">
        <h3>{pct:.1f}%</h3>
        <strong>{nivel}</strong>
        <p>{texto}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Dados enviados ao modelo"):
        st.dataframe(df.T.rename(columns={0: "Valor"}))

    if demo:
        st.caption(
            "Resultado demonstrativo. Para usar o modelo real, salve o arquivo em `modelo/modelo_final.pkl`."
        )


st.markdown(
    '<div class="rodape">SINAN · DataSUS · Projeto de Machine Learning — apoio à decisão clínica</div>',
    unsafe_allow_html=True
)
import streamlit as st
import pandas as pd
import pickle
import os

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


# carrega o modelo se existir
@st.cache_resource
def carregar_modelo():
    for nome in ["rf_model.pkl", "model.pkl", "modelo.pkl"]:
        if os.path.exists(nome):
            with open(nome, "rb") as f:
                return pickle.load(f)
    return None

modelo = carregar_modelo()
demo = modelo is None

if demo:
    st.info(
        "Modelo não encontrado na pasta. Para conectar, salve com:\n\n"
        "```python\nimport pickle\nwith open('rf_model.pkl', 'wb') as f:\n"
        "    pickle.dump(rf_model, f)\n```\n\n"
        "Por enquanto os resultados são uma estimativa baseada em heurística."
    )


# ── campos do formulário ────────────────────────────────────────

st.markdown('<div class="secao">Identificação</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    idade = st.number_input("Idade", min_value=18, max_value=110, value=35, step=1)
with c2:
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
with c3:
    ano = st.number_input("Ano de notificação", min_value=2000, max_value=2025, value=2023, step=1)

c4, c5 = st.columns(2)
with c4:
    raca = st.selectbox("Raça/Cor", ["Branca", "Preta", "Parda", "Amarela", "Indígena", "Ignorado"])
with c5:
    escolaridade = st.selectbox("Escolaridade", [
        "Sem escolaridade", "Fund. incompleto (1ª–4ª série)",
        "Fund. incompleto (5ª–8ª série)", "Fund. completo",
        "Médio incompleto", "Médio completo",
        "Superior incompleto", "Superior completo", "Ignorado",
    ])

st.markdown('<div class="secao">Dados clínicos</div>', unsafe_allow_html=True)

c6, c7, c8 = st.columns(3)
with c6:
    entrada = st.selectbox("Tipo de entrada", [
        "Caso novo", "Recidiva", "Reingresso após abandono", "Não sabe",
    ])
with c7:
    tratamento = st.selectbox("Tratamento", [
        "Diretamente Observado (TDO)", "Autoadministrado", "Misto",
    ])
with c8:
    hiv = st.selectbox("Sorologia HIV", [
        "Não realizado", "Negativo", "Positivo", "Em andamento",
    ])

st.markdown('<div class="secao">Comorbidades</div>', unsafe_allow_html=True)

cc1, cc2, cc3 = st.columns(3)
with cc1:
    aids   = st.checkbox("AIDS")
    alcool = st.checkbox("Alcoolismo")
with cc2:
    diabet = st.checkbox("Diabetes")
    drogas = st.checkbox("Uso de drogas ilícitas")
with cc3:
    mental = st.checkbox("Doença mental")
    tabaco = st.checkbox("Tabagismo")

st.markdown('<div class="secao">Situação social</div>', unsafe_allow_html=True)

cs1, cs2 = st.columns(2)
with cs1:
    ppl  = st.checkbox("Privado de liberdade")
    rua  = st.checkbox("Situação de rua")
with cs2:
    imig = st.checkbox("Imigrante")
    bolsa = st.checkbox("Beneficiário de transferência de renda")


# ── mapeamentos p/ codificação SINAN ───────────────────────────

def sn(v):
    return "1" if v else "2"

mapa_sexo    = {"Masculino": "M", "Feminino": "F"}
mapa_raca    = {"Branca":"1","Preta":"2","Amarela":"3","Parda":"4","Indígena":"5","Ignorado":"9"}
mapa_escol   = {
    "Sem escolaridade":"0","Fund. incompleto (1ª–4ª série)":"1",
    "Fund. incompleto (5ª–8ª série)":"3","Fund. completo":"4",
    "Médio incompleto":"5","Médio completo":"6",
    "Superior incompleto":"7","Superior completo":"8","Ignorado":"9",
}
mapa_entrada = {"Caso novo":"1","Recidiva":"2","Reingresso após abandono":"3","Não sabe":"4"}
mapa_trat    = {"Diretamente Observado (TDO)":"1","Autoadministrado":"2","Misto":"3"}
mapa_hiv     = {"Positivo":"1","Negativo":"2","Em andamento":"3","Não realizado":"4"}


# ── predição ────────────────────────────────────────────────────

if st.button("Calcular risco", type="primary"):

    registro = {
        "idade_anos":  idade,
        "CS_SEXO":     mapa_sexo[sexo],
        "CS_RACA":     mapa_raca[raca],
        "CS_ESCOL_N":  mapa_escol[escolaridade],
        "TRATAMENTO":  mapa_trat[tratamento],
        "TP_ENTRADA":  mapa_entrada[entrada],
        "HIV":         mapa_hiv[hiv],
        "NU_ANO":      ano,
        "AGRAVAIDS":   sn(aids),
        "AGRAVALCOO":  sn(alcool),
        "AGRAVDIABE":  sn(diabet),
        "AGRAVDROGAS": sn(drogas),
        "AGRAVDOENC":  sn(mental),
        "AGRAVTABACO": sn(tabaco),
        "POP_LIBER":   sn(ppl),
        "POP_RUA":     sn(rua),
        "POP_IMIG":    sn(imig),
        "BENEF_GOV":   sn(bolsa),
    }

    df = pd.DataFrame([registro])
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str)

    if demo:
        # heurística simples só pra visualização
        pts = 0
        if mapa_entrada[entrada] in ["2","3"]: pts += 30
        if mapa_hiv[hiv] == "1":              pts += 15
        if aids:   pts += 10
        if alcool: pts += 15
        if drogas: pts += 15
        if rua:    pts += 20
        if ppl:    pts += 10
        prob = min(pts / 100, 0.95)
    else:
        try:
            prob = modelo.predict_proba(df)[0][1]
        except Exception as e:
            st.error(f"Erro ao rodar o modelo: {e}")
            st.stop()

    pct = prob * 100

    if prob >= 0.60:
        cls  = "res-alto"
        nivel = "Risco alto"
        texto = (
            "Recomenda-se reforço imediato do TDO e contato com um familiar ou referência de apoio. "
            "Vale conversar com o paciente sobre barreiras práticas — transporte, trabalho, moradia — "
            "que possam estar dificultando a adesão. Encaminhamento para serviço social pode ser necessário."
        )
    elif prob >= 0.30:
        cls  = "res-medio"
        nivel = "Risco moderado"
        texto = (
            "Monitorar de perto na próxima consulta. Reforçar a importância de completar os seis meses "
            "e perguntar diretamente se o paciente está enfrentando alguma dificuldade para comparecer."
        )
    else:
        cls  = "res-baixo"
        nivel = "Risco baixo"
        texto = (
            "Seguir o acompanhamento padrão. Registrar a evolução e reavaliar caso haja mudanças "
            "no quadro clínico ou social do paciente."
        )

    st.markdown(f"""
    <div class="{cls}">
        <h3>{pct:.1f}%</h3>
        <strong>{nivel}</strong>
        <p>{texto}</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Dados usados na predição"):
        st.dataframe(df.T.rename(columns={0: "Valor"}))

    if demo:
        st.caption("Estimativa simplificada. Conecte o modelo treinado para resultados baseados nos dados reais.")


st.markdown(
    '<div class="rodape">SINAN · DataSUS · Projeto de Nanodegree — apoio à decisão clínica</div>',
    unsafe_allow_html=True
)

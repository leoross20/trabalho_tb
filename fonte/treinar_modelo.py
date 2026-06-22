import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

from tratamento_dados import separar_entrada_alvo


base_treino = pd.read_csv("dados/treino.csv")

entrada_treino, alvo_treino, colunas_numericas, colunas_texto = separar_entrada_alvo(base_treino)

tratamento_numerico = Pipeline([
    ("preenchimento_mediana", SimpleImputer(strategy="median"))
])

tratamento_texto = Pipeline([
    ("preenchimento_frequente", SimpleImputer(strategy="most_frequent")),
    ("codificacao", OneHotEncoder(handle_unknown="ignore"))
])

preparacao = ColumnTransformer([
    ("numericas", tratamento_numerico, colunas_numericas),
    ("categoricas", tratamento_texto, colunas_texto)
])

modelo_abandono = Pipeline([
    ("preparacao", preparacao),
    ("floresta", RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    ))
])

modelo_abandono.fit(entrada_treino, alvo_treino)

joblib.dump(modelo_abandono, "modelo/modelo_abandono_tb.pkl")

print("Modelo treinado e salvo em: modelo/modelo_abandono_tb.pkl")
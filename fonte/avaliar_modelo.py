import pandas as pd
import joblib

from sklearn.metrics import classification_report, roc_auc_score

from tratamento_dados import separar_entrada_alvo


base_teste1 = pd.read_csv("dados/teste1.csv")

entrada_teste, alvo_teste, _, _ = separar_entrada_alvo(base_teste1)

modelo_abandono = joblib.load("modelo/modelo_abandono_tb.pkl")

probabilidade_abandono = modelo_abandono.predict_proba(entrada_teste)[:, 1]

limiar_decisao = 0.44
previsao_abandono = (probabilidade_abandono >= limiar_decisao).astype(int)

print(classification_report(alvo_teste, previsao_abandono))
print("ROC-AUC:", roc_auc_score(alvo_teste, probabilidade_abandono))
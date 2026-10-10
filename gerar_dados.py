# -*- coding: utf-8 -*-
"""
Gera JSON agregado dos dados SINASC de Caucaia
Versão com filtros de qualidade de dados
"""

import pandas as pd
import json
import os

# Caminhos
arquivo = r"C:\projetos\SINASC\BASE DE DADOS_SINASC.xlsx"
pasta_dados = r"C:\projetos\painel_nascidos\dados"
saida = os.path.join(pasta_dados, "nascidos_caucaia.json")

# Criar pasta de dados
os.makedirs(pasta_dados, exist_ok=True)

print("=" * 60)
print("GERADOR DE DADOS - SINASC CAUCAIA")
print("=" * 60)
print("")
print("Lendo arquivo... (pode demorar 2-3 minutos)")
print("")

# Ler arquivo
df = pd.read_excel(arquivo)

print(f"Total bruto: {len(df):,} registros")
print("")

# ==========================================
# FILTROS DE QUALIDADE
# ==========================================
print("Aplicando filtros de qualidade...")

# 1. Filtrar apenas Caucaia
df = df[df['Município de Residência'] == 'Caucaia']
print(f"  - Após filtrar Caucaia: {len(df):,}")

# 2. Remover idades inválidas (> 49 anos e < 10 anos)
df = df[(df['IDADEMAE'] >= 10) & (df['IDADEMAE'] <= 49)]
print(f"  - Após filtrar idade da mãe (10-49): {len(df):,}")

# 3. Remover pesos inválidos (< 200g e > 6000g)
df = df[(df['PESO'] >= 200) & (df['PESO'] <= 6000)]
print(f"  - Após filtrar peso (200-6000g): {len(df):,}")

print("")

# Extrair ano
df['Ano'] = df['DTNASC'].astype(str).str[-4:]

# Função auxiliar
def conv(d):
    return {str(k): int(v) for k, v in d.items()}

# ==========================================
# MONTAR ESTRUTURA DE DADOS
# ==========================================
dados = {
    "municipio": "Caucaia",
    "estado": "Ceará",
    "total_nascimentos": int(len(df)),
    "periodo": {
        "inicio": str(df['Ano'].min()),
        "fim": str(df['Ano'].max())
    },
    "por_ano": conv(df['Ano'].value_counts().sort_index()),
    "por_sexo": conv(df['Sexo_F'].value_counts()),
    "por_parto": conv(df['Tipo de parto'].value_counts()),
    "por_peso": conv(df['Tipo de Peso'].value_counts()),
    "por_prenatal": conv(df['Consultas pré-natal'].value_counts()),
    "por_idade_mae": conv(df['Faixa etária da mãe'].value_counts()),
    "por_gestacao": conv(df['Duração de gestação'].value_counts()),
    "estatisticas": {
        "peso_medio_g": round(float(df['PESO'].mean()), 0),
        "peso_min_g": int(df['PESO'].min()),
        "peso_max_g": int(df['PESO'].max()),
        "idade_media_mae": round(float(df['IDADEMAE'].mean()), 1),
        "idade_min_mae": int(df['IDADEMAE'].min()),
        "idade_max_mae": int(df['IDADEMAE'].max())
    }
}

# Salvar JSON
with open(saida, 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

tamanho_kb = os.path.getsize(saida) / 1024

print("=" * 60)
print("JSON GERADO COM SUCESSO!")
print("=" * 60)
print(f"Arquivo: {saida}")
print(f"Tamanho: {tamanho_kb:.1f} KB")
print("")
print(f"Periodo: {dados['periodo']['inicio']} a {dados['periodo']['fim']}")
print(f"Total: {dados['total_nascimentos']:,} nascimentos")
print("")
print("Estatísticas de idade da mãe:")
print(f"  - Mínima: {dados['estatisticas']['idade_min_mae']} anos")
print(f"  - Máxima: {dados['estatisticas']['idade_max_mae']} anos")
print(f"  - Média: {dados['estatisticas']['idade_media_mae']} anos")
print("")
print("Estatísticas de peso:")
print(f"  - Mínimo: {dados['estatisticas']['peso_min_g']} g")
print(f"  - Máximo: {dados['estatisticas']['peso_max_g']} g")
print(f"  - Média: {dados['estatisticas']['peso_medio_g']} g")
print("")
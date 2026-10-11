# -*- coding: utf-8 -*-
"""
Painel de Nascidos Vivos - Observatório da Primeira Infância de Caucaia
Página interna: pages/1_Nascidos_Vivos.py
"""

import streamlit as st
import json
from pathlib import Path
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stDeployButton { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    div[class*="StatusWidget"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; max-width: 100% !important; }
    .stApp a.anchor-link { display: none !important; }
    a[href*="streamlit.io/cloud"] { display: none !important; }
    iframe[title*="streamlit"] { display: none !important; }
    .stApp { background-color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

AZUL = "#1F3A6E"
AZUL_ESCURO = "#16305A"
AMARELO = "#F5B93A"
VERDE = "#5DB5A8"
CORAL = "#E89B7D"
AZUL_CLARO = "#A8C8E8"
CINZA = "#F5F6F8"
GRAFITE = "#333333"
BRANCO = "#FFFFFF"


def fmt(n):
    try:
        return f"{int(n):,}".replace(",", ".")
    except:
        return str(n)


def kpi_card(titulo, valor, subtitulo=None, cor=AZUL, cor_texto=None):
    cor_texto = cor_texto or cor
    sub_html = f'<div style="font-size:12px;color:#888;margin-top:8px;">{subtitulo}</div>' if subtitulo else ''
    st.markdown(f"""
    <div style="background:white;border-left:4px solid {cor};padding:18px 22px;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.06);height:100%;">
        <div style="font-size:13px;color:#666;margin-bottom:8px;font-weight:500;">{titulo}</div>
        <div style="font-size:26px;font-weight:700;color:{cor_texto};line-height:1.2;">{valor}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def kpi_destaque(titulo, valor, subtitulo=None):
    sub_html = f'<div style="font-size:13px;color:#C8D4E8;margin-top:8px;">{subtitulo}</div>' if subtitulo else ''
    st.markdown(f"""
    <div style="background:{AZUL};color:white;padding:24px 28px;border-radius:8px;">
        <div style="font-size:13px;color:#C8D4E8;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">{titulo}</div>
        <div style="font-size:42px;font-weight:700;line-height:1;">{valor}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


st.markdown(f"""
<style>
    .secao-titulo {{ color: {AZUL}; font-size: 20px; font-weight: 600; margin: 32px 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid {AZUL_CLARO}; }}
    .rodape-inst {{ background: {AZUL}; color: white; padding: 20px 32px; border-radius: 8px; text-align: center; font-size: 12px; margin-top: 40px; line-height: 1.6; }}
    .info-projecao {{ background: {CINZA}; padding: 16px 20px; border-radius: 8px; border-left: 4px solid {AZUL}; font-size: 13px; color: {GRAFITE}; margin: 16px 0; }}
    div[data-testid="stDownloadButton"] button {{ background-color: {AMARELO}; color: {AZUL}; border: none; border-radius: 8px; padding: 16px 20px; font-weight: 700; font-size: 15px; width: 100%; box-shadow: 0 4px 12px rgba(245, 185, 58, 0.3); margin-top: 12px; }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    caminho = Path(__file__).parent.parent / "dados" / "nascidos_caucaia.json"
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


dados = carregar_dados()

por_ano_historico = {k: v for k, v in dados['por_ano'].items() if k != '2026'}
anos_hist = sorted(por_ano_historico.keys())
valores_hist = [por_ano_historico[a] for a in anos_hist]
media_anual = int(sum(valores_hist) / len(valores_hist))

ultimo = anos_hist[-1]
penultimo = anos_hist[-2]
var_ano = por_ano_historico[ultimo] - por_ano_historico[penultimo]
pct_var = (var_ano / por_ano_historico[penultimo]) * 100 if por_ano_historico[penultimo] > 0 else 0


def get_sexo_data(por_sexo):
    masc = 0
    fem = 0
    for k, v in por_sexo.items():
        k_lower = str(k).lower().strip()
        if k_lower in ['m', 'masculino', '1', 'masc']:
            masc = v
        elif k_lower in ['f', 'feminino', '2', 'fem']:
            fem = v
    return masc, fem


masc, fem = get_sexo_data(dados['por_sexo'])

anos_numericos = np.array([int(a) for a in anos_hist])
valores_numericos = np.array(valores_hist)
coef = np.polyfit(anos_numericos, valores_numericos, 1)
tendencia = np.poly1d(coef)
anos_projecao = list(range(2026, 2031))
valores_projetados = [int(tendencia(a)) for a in anos_projecao]
residuos = valores_numericos - tendencia(anos_numericos)
desvio = np.std(residuos)
valores_otimista = [int(v + 1.96 * desvio) for v in valores_projetados]
valores_pessimista = [int(v - 1.96 * desvio) for v in valores_projetados]
total_2026_2030 = sum(valores_projetados)
media_projetada = int(total_2026_2030 / 5)


def gerar_relatorio_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    cor_azul = colors.HexColor(AZUL)
    cor_grafite = colors.HexColor(GRAFITE)
    titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=20, textColor=cor_azul, spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitulo = ParagraphStyle('Subtitulo', parent=styles['Heading2'], fontSize=14, textColor=cor_azul, spaceBefore=16, spaceAfter=10, fontName='Helvetica-Bold')
    corpo = ParagraphStyle('Corpo', parent=styles['BodyText'], fontSize=11, textColor=cor_grafite, spaceAfter=8, alignment=TA_JUSTIFY, leading=15)

    story.append(Paragraph("PREFEITURA MUNICIPAL DE CAUCAIA", titulo))
    story.append(Paragraph("Observatorio da Primeira Infancia", ParagraphStyle('Sub', parent=titulo, fontSize=14, spaceAfter=8)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("RELATORIO DE NASCIDOS VIVOS", ParagraphStyle('TitRel', parent=titulo, fontSize=18, spaceAfter=12)))
    story.append(Paragraph(f"Periodo: {anos_hist[0]} a {anos_hist[-1]}", ParagraphStyle('Periodo', parent=corpo, alignment=TA_CENTER, fontSize=12)))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("1. SUMARIO EXECUTIVO", subtitulo))
    tendencia_txt = "crescimento" if coef[0] > 0 else "reducao"
    story.append(Paragraph(f"Total: <b>{fmt(dados['total_nascimentos'])} nascimentos</b>. Media anual: <b>{fmt(media_anual)}</b>. Tendencia: <b>{tendencia_txt}</b>.", corpo))
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


st.markdown(f"""
<div style="padding: 16px 0; border-bottom: 2px solid {AZUL_CLARO}; margin-bottom: 24px;">
    <p style="font-size: 13px; color: #888; margin: 0 0 12px 0; font-weight: 500;">
        Indicadores &nbsp;›&nbsp; <span style="color: {AZUL}; font-weight: 600;">Nascidos Vivos</span>
    </p>
    <h1 style="color: {AZUL}; font-size: 30px; margin: 0 0 8px 0; font-weight: 700;">
        Nascidos Vivos em Caucaia
    </h1>
    <p style="color: #555; font-size: 15px; margin: 0;">
        Análise dos registros de nascimentos no município de {anos_hist[0]} a {anos_hist[-1]}, com base no SINASC.
    </p>
</div>
""", unsafe_allow_html=True)

col_espaco, col_btn = st.columns([4, 1])
with col_btn:
    pdf_bytes = gerar_relatorio_pdf()
    st.download_button(
        label="📄 Baixar Relatório PDF",
        data=pdf_bytes,
        file_name=f"relatorio_nascidos_vivos_caucaia_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True,
        key="btn_pdf_top",
        type="primary"
    )

col_principal, col_espaco, col_kpi1, col_kpi2, col_kpi3 = st.columns([2, 0.3, 1, 1, 1])

with col_principal:
    kpi_destaque("Total de Nascidos Vivos no Periodo Historico", fmt(dados['total_nascimentos']), f"Media anual: {fmt(media_anual)} nascimentos")

with col_kpi1:
    sinal = "+" if var_ano >= 0 else "-"
    kpi_card(f"Variacao {ultimo} vs {penultimo}", f"{sinal}{fmt(abs(var_ano))}", f"{pct_var:+.1f}%", cor=VERDE if var_ano >= 0 else CORAL)

with col_kpi2:
    kpi_card("Peso Medio ao Nascer", f"{dados['estatisticas']['peso_medio_g']:.0f} g")

with col_kpi3:
    kpi_card("Idade Media das Maes", f"{dados['estatisticas']['idade_media_mae']} anos")

st.markdown('<div class="secao-titulo">Evolucao Historica e Projecao</div>', unsafe_allow_html=True)

fig_hist = go.Figure()
fig_hist.add_trace(go.Scatter(x=anos_hist, y=valores_hist, mode='lines+markers', name='Historico',
    line=dict(color=AZUL, width=3), marker=dict(size=10, color=AZUL)))
fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_projetados, mode='lines+markers', name='Projecao',
    line=dict(color=AMARELO, width=3, dash='dash'), marker=dict(size=10, color=AMARELO, symbol='diamond')))
fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_otimista, mode='lines', name='Otimista',
    line=dict(color=VERDE, width=1.5, dash='dot')))
fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_pessimista, mode='lines', name='Pessimista',
    line=dict(color=CORAL, width=1.5, dash='dot')))
fig_hist.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=40),
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=12, color=GRAFITE),
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5))
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown(f'<div class="info-projecao"><strong>Nota metodologica:</strong> Projecao por regressao linear.</div>', unsafe_allow_html=True)

st.markdown('<div class="secao-titulo">Projecao para 2026-2030</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("Total Projetado", fmt(total_2026_2030))
with col2:
    kpi_card("Media Anual Projetada", fmt(media_projetada))
with col3:
    tendencia_txt = "Crescimento" if coef[0] > 0 else "Reducao"
    cor_tend = VERDE if coef[0] > 0 else CORAL
    kpi_card("Tendencia", tendencia_txt, f"{coef[0]:+.0f} nascidos/ano", cor=cor_tend)
with col4:
    kpi_card("Projecao 2030", fmt(valores_projetados[-1]))

st.markdown("**Detalhamento por Ano:**")

css_tabela = """
<style>
.tabela-projecao { width: 100%; border-collapse: collapse; font-family: Arial; font-size: 14px; margin-top: 10px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.06); }
.tabela-projecao th { background-color: #16305A; color: #FFFFFF; font-weight: bold; padding: 12px 15px; text-align: center; border: 1px solid #1F3A6E; }
.tabela-projecao th:first-child { text-align: left; }
.tabela-projecao td { padding: 10px 15px; color: #333333; background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0; text-align: center; }
.tabela-projecao td:first-child { text-align: left; font-weight: bold; color: #1F3A6E; }
.tabela-projecao tr:nth-child(even) td { background-color: #F9F9F9; }
</style>
"""
st.markdown(css_tabela, unsafe_allow_html=True)

html_tabela = '<table class="tabela-projecao"><thead><tr><th>Ano</th><th>Cenario Pessimista</th><th>Projecao Realista</th><th>Cenario Otimista</th></tr></thead><tbody>'
for i, ano in enumerate(anos_projecao):
    html_tabela += f'<tr><td>{ano}</td><td>{fmt(valores_pessimista[i])}</td><td>{fmt(valores_projetados[i])}</td><td>{fmt(valores_otimista[i])}</td></tr>'
html_tabela += '</tbody></table>'
st.markdown(html_tabela, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="secao-titulo">Distribuicao por Sexo</div>', unsafe_allow_html=True)
    fig_sexo = go.Figure(data=[go.Pie(labels=['Masculino', 'Feminino'], values=[masc, fem], hole=0.55,
        marker=dict(colors=[AZUL, AMARELO], line=dict(color=BRANCO, width=3)),
        textinfo='label+percent', textfont=dict(size=14, color=BRANCO))])
    fig_sexo.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor=BRANCO)
    st.plotly_chart(fig_sexo, use_container_width=True)

with col2:
    st.markdown('<div class="secao-titulo">Tipo de Parto</div>', unsafe_allow_html=True)
    labels_parto = list(dados['por_parto'].keys())
    valores_parto = list(dados['por_parto'].values())
    mapa_cores_parto = {'Cesario': CORAL, 'Cesareo': CORAL, 'Cesariana': CORAL, 'Vaginal': VERDE, 'Normal': VERDE}
    cores_parto = [mapa_cores_parto.get(l, AZUL_CLARO) for l in labels_parto]
    fig_parto = go.Figure(data=[go.Pie(labels=labels_parto, values=valores_parto, hole=0.55,
        marker=dict(colors=cores_parto, line=dict(color=BRANCO, width=3)),
        textinfo='label+percent', textfont=dict(size=13, color=BRANCO))])
    fig_parto.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor=BRANCO)
    st.plotly_chart(fig_parto, use_container_width=True)

st.markdown('<div class="secao-titulo">Cobertura de Pre-Natal</div>', unsafe_allow_html=True)
ordem_prenatal = ['Nenhuma', 'de 1 a 3', 'de 4 a 6', '7 e mais', 'Ignorado']
dados_prenatal_ordenado = {k: dados['por_prenatal'][k] for k in ordem_prenatal if k in dados['por_prenatal']}
fig_prenatal = go.Figure(data=[go.Bar(
    x=list(dados_prenatal_ordenado.values()), y=list(dados_prenatal_ordenado.keys()), orientation='h',
    marker=dict(color=AZUL), text=[fmt(v) for v in dados_prenatal_ordenado.values()],
    textposition='outside', textfont=dict(size=12, color=GRAFITE))])
fig_prenatal.update_layout(height=320, margin=dict(l=20, r=80, t=20, b=40),
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO, showlegend=False)
st.plotly_chart(fig_prenatal, use_container_width=True)

st.markdown(f"""
<div class="rodape-inst">
    <strong>Fonte dos dados:</strong> SINASC - Sistema de Informacao sobre Nascidos Vivos<br>
    <strong>Observatorio da Primeira Infancia de Caucaia</strong><br>
    Prefeitura Municipal de Caucaia - Secretaria Municipal de Saude<br>
    <em>Ultima atualizacao: {datetime.now().strftime('%d/%m/%Y as %H:%M')}</em>
</div>
""", unsafe_allow_html=True)
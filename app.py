# -*- coding: utf-8 -*-
"""
Painel de Nascidos Vivos - Observatório da Primeira Infância de Caucaia
Versão final - tabela customizada e legendas visíveis
"""

import streamlit as st
import json
from pathlib import Path
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# ==========================================
# CONFIGURACAO
# ==========================================
st.set_page_config(
    page_title="Nascidos Vivos - Caucaia",
    page_icon="https://www.caucaia.ce.gov.br/favicon.ico",
    layout="wide"
)

# ==========================================
# CSS - ESCONDER BARRA E ICONES
# ==========================================
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stDeployButton { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
    .viewerBadge_container__1QSob { display: none !important; }
    .viewerBadge_link__1S137 { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    div[class*="StatusWidget"] { display: none !important; }
    .block-container { padding-top: 1rem !important; }
    .stApp a.anchor-link { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Paleta
AZUL = "#1F3A6E"
AZUL_ESCURO = "#16305A"
AMARELO = "#F5B93A"
VERDE = "#5DB5A8"
CORAL = "#E89B7D"
AZUL_CLARO = "#A8C8E8"
CINZA = "#F5F6F8"
GRAFITE = "#333333"
BRANCO = "#FFFFFF"


# ==========================================
# FUNCOES AUXILIARES
# ==========================================
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


# ==========================================
# CSS DO CONTEUDO
# ==========================================
st.markdown(f"""
<style>
    .stApp {{ background-color: {BRANCO}; }}
    .header-inst {{
        background: linear-gradient(135deg, {AZUL} 0%, {AZUL_ESCURO} 100%);
        color: white;
        padding: 28px 36px;
        border-radius: 8px;
        margin-bottom: 32px;
        border-left: 6px solid {AMARELO};
        height: 100%;
    }}
    .header-inst h1 {{ color: white; margin: 0; font-size: 26px; font-weight: 600; }}
    .header-inst p {{ color: #C8D4E8; margin: 6px 0 0 0; font-size: 13px; }}
    .secao-titulo {{
        color: {AZUL};
        font-size: 20px;
        font-weight: 600;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid {AZUL_CLARO};
    }}
    .rodape-inst {{
        background: {AZUL};
        color: white;
        padding: 20px 32px;
        border-radius: 8px;
        text-align: center;
        font-size: 12px;
        margin-top: 40px;
        line-height: 1.6;
    }}
    .info-projecao {{
        background: {CINZA};
        padding: 16px 20px;
        border-radius: 8px;
        border-left: 4px solid {AZUL};
        font-size: 13px;
        color: {GRAFITE};
        margin: 16px 0;
    }}
    div[data-testid="stDownloadButton"] button {{
        background-color: {AMARELO};
        color: {AZUL};
        border: none;
        border-radius: 8px;
        padding: 16px 20px;
        font-weight: 700;
        font-size: 15px;
        width: 100%;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(245, 185, 58, 0.3);
        margin-top: 12px;
    }}
    div[data-testid="stDownloadButton"] button:hover {{
        background-color: #E0A72A;
        color: {AZUL};
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(245, 185, 58, 0.4);
    }}
</style>
""", unsafe_allow_html=True)


# ==========================================
# CARREGAR DADOS
# ==========================================
@st.cache_data
def carregar_dados():
    caminho = Path(__file__).parent / "dados" / "nascidos_caucaia.json"
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


dados = carregar_dados()

# ==========================================
# DADOS HISTORICOS
# ==========================================
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
total_sexo = masc + fem
perc_m = (masc / total_sexo) * 100 if total_sexo > 0 else 0
perc_f = (fem / total_sexo) * 100 if total_sexo > 0 else 0

# PROJECAO
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


# ==========================================
# FUNCAO PDF
# ==========================================
def gerar_relatorio_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
        title="Relatorio de Nascidos Vivos - Caucaia",
        author="Observatorio da Primeira Infancia de Caucaia"
    )

    styles = getSampleStyleSheet()
    story = []
    cor_azul = colors.HexColor(AZUL)
    cor_grafite = colors.HexColor(GRAFITE)

    titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=20, textColor=cor_azul, spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitulo = ParagraphStyle('Subtitulo', parent=styles['Heading2'], fontSize=14, textColor=cor_azul, spaceBefore=16, spaceAfter=10, fontName='Helvetica-Bold')
    corpo = ParagraphStyle('Corpo', parent=styles['BodyText'], fontSize=11, textColor=cor_grafite, spaceAfter=8, alignment=TA_JUSTIFY, leading=15)
    destaque = ParagraphStyle('Destaque', parent=styles['BodyText'], fontSize=12, textColor=cor_azul, spaceAfter=8, fontName='Helvetica-Bold')

    story.append(Paragraph("PREFEITURA MUNICIPAL DE CAUCAIA", titulo))
    story.append(Paragraph("Observatorio da Primeira Infancia", ParagraphStyle('Sub', parent=titulo, fontSize=14, spaceAfter=8)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("RELATORIO DE NASCIDOS VIVOS", ParagraphStyle('TitRel', parent=titulo, fontSize=18, spaceAfter=12)))
    story.append(Paragraph(f"Periodo de analise: {anos_hist[0]} a {anos_hist[-1]}", ParagraphStyle('Periodo', parent=corpo, alignment=TA_CENTER, fontSize=12)))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y as %H:%M')}", ParagraphStyle('Data', parent=corpo, alignment=TA_CENTER, fontSize=10, textColor=colors.gray)))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("1. SUMARIO EXECUTIVO", subtitulo))
    tendencia_txt = "crescimento" if coef[0] > 0 else "reducao"
    texto_executivo = f"""
    Este relatorio apresenta a analise dos nascidos vivos no municipio de Caucaia 
    no periodo de <b>{anos_hist[0]} a {anos_hist[-1]}</b>, totalizando 
    <b>{fmt(dados['total_nascimentos'])} nascimentos</b> registrados no SINASC.
    <br/><br/>
    A media anual de nascimentos no periodo foi de <b>{fmt(media_anual)} criancas</b>. 
    A analise de tendencia identificou um cenario de <b>{tendencia_txt}</b> de 
    aproximadamente <b>{abs(coef[0]):.0f} nascimentos por ano</b>, com projecao de 
    <b>{fmt(total_2026_2030)} nascimentos</b> para o quinquenio 2026-2030.
    <br/><br/>
    Os dados aqui apresentados servem como base tecnica para o planejamento de 
    politicas publicas voltadas a Primeira Infancia.
    """
    story.append(Paragraph(texto_executivo, corpo))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("2. INDICADORES PRINCIPAIS", subtitulo))
    dados_tabela = [
        ['Indicador', 'Valor'],
        ['Total de Nascidos Vivos', fmt(dados['total_nascimentos'])],
        ['Media Anual de Nascimentos', fmt(media_anual)],
        ['Periodo Analisado', f'{anos_hist[0]} a {anos_hist[-1]}'],
        ['Anos de Serie Historica', f'{len(anos_hist)} anos'],
        ['Peso Medio ao Nascer', f"{dados['estatisticas']['peso_medio_g']:.0f} g"],
        ['Peso Minimo Registrado', f"{dados['estatisticas']['peso_min_g']} g"],
        ['Peso Maximo Registrado', f"{dados['estatisticas']['peso_max_g']} g"],
        ['Idade Media das Maes', f"{dados['estatisticas']['idade_media_mae']} anos"],
        ['Idade Minima das Maes', f"{dados['estatisticas']['idade_min_mae']} anos"],
        ['Idade Maxima das Maes', f"{dados['estatisticas']['idade_max_mae']} anos"],
    ]
    tabela = Table(dados_tabela, colWidths=[10*cm, 6*cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), cor_azul),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 1), (1, -1), cor_azul),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8F9FA")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(tabela)

    story.append(PageBreak())
    story.append(Paragraph("3. PROJECAO PARA 2026-2030", subtitulo))
    texto_projecao = f"""
    Com base na analise de regressao linear, projeta-se 
    <b>{fmt(total_2026_2030)} nascimentos</b> no quinquenio 2026-2030, com 
    media anual de <b>{fmt(media_projetada)} nascimentos</b>.
    """
    story.append(Paragraph(texto_projecao, corpo))
    story.append(Spacer(1, 0.5*cm))

    dados_proj = [['Ano', 'Pessimista', 'Realista', 'Otimista']]
    for i, ano in enumerate(anos_projecao):
        dados_proj.append([str(ano), fmt(valores_pessimista[i]), fmt(valores_projetados[i]), fmt(valores_otimista[i])])

    tabela_proj = Table(dados_proj, colWidths=[3*cm, 4*cm, 4*cm, 4*cm])
    tabela_proj.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), cor_azul),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (2, 1), (2, -1), colors.HexColor("#E8F4FD")),
        ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2, 1), (2, -1), cor_azul),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(tabela_proj)

    story.append(PageBreak())
    story.append(Paragraph("4. ANALISE DE SAUDE MATERNO-INFANTIL", subtitulo))

    story.append(Paragraph("Cobertura de Pre-Natal", destaque))
    total_prenatal = sum(dados['por_prenatal'].values())
    pren_adequado = dados['por_prenatal'].get('7 e mais', 0)
    pren_nenhum = dados['por_prenatal'].get('Nenhuma', 0)
    perc_adequado = (pren_adequado / total_prenatal) * 100 if total_prenatal > 0 else 0
    perc_nenhum = (pren_nenhum / total_prenatal) * 100 if total_prenatal > 0 else 0

    texto_prenatal = f"""
    Das <b>{fmt(total_prenatal)}</b> maes registradas, <b>{fmt(pren_adequado)}</b> 
    (<b>{perc_adequado:.1f}%</b>) realizaram <b>7 ou mais consultas</b> de pre-natal.
    <br/><br/>
    <b>Atencao:</b> <b>{fmt(pren_nenhum)}</b> maes (<b>{perc_nenhum:.1f}%</b>) 
    <b>nao realizaram nenhuma consulta</b>.
    """
    story.append(Paragraph(texto_prenatal, corpo))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Tipo de Parto", destaque))
    total_parto = sum(dados['por_parto'].values())
    cesariana = dados['por_parto'].get('Cesario', 0) + dados['por_parto'].get('Cesareo', 0)
    vaginal = dados['por_parto'].get('Vaginal', 0)
    perc_ces = (cesariana / total_parto) * 100 if total_parto > 0 else 0
    perc_vag = (vaginal / total_parto) * 100 if total_parto > 0 else 0

    texto_parto = f"""
    Do total de partos, <b>{fmt(cesariana)}</b> (<b>{perc_ces:.1f}%</b>) foram 
    cesarianas e <b>{fmt(vaginal)}</b> (<b>{perc_vag:.1f}%</b>) foram partos vaginais.
    <br/><br/>
    <b>Alerta tecnico:</b> a OMS recomenda taxa de cesarianas entre 10% e 15%. 
    A taxa observada de <b>{perc_ces:.1f}%</b> esta acima do recomendado.
    """
    story.append(Paragraph(texto_parto, corpo))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("Peso ao Nascer", destaque))
    baixo_peso = sum(v for k, v in dados['por_peso'].items() if 'Menos de 500' in k or '500 a 999' in k or '1000 a 1499' in k or '1500 a 2499' in k)
    total_peso = sum(dados['por_peso'].values())
    perc_baixo = (baixo_peso / total_peso) * 100 if total_peso > 0 else 0

    texto_peso = f"""
    A media de peso ao nascer e de <b>{dados['estatisticas']['peso_medio_g']:.0f} g</b>.
    <br/><br/>
    Foram registrados <b>{fmt(baixo_peso)}</b> bebes com <b>peso inferior a 2.500 g</b> 
    (<b>{perc_baixo:.1f}%</b>).
    """
    story.append(Paragraph(texto_peso, corpo))

    story.append(PageBreak())
    story.append(Paragraph("5. RECOMENDACOES PARA A GESTAO MUNICIPAL", subtitulo))
    story.append(Paragraph("Com base na analise tecnica, apresentam-se as seguintes recomendacoes:", corpo))

    recs = [
        ("Saude Materno-Infantil", "Ampliar a cobertura de pre-natal adequado, com meta de reduzir os casos de maes sem nenhuma consulta."),
        ("Reducao de Cesarianas Desnecessarias", "Implementar protocolos de classificacao de risco obstetrico."),
        ("Educacao Infantil", "Dimensionar a oferta de vagas em creches e pre-escolas para os proximos 5 anos."),
        ("Primeira Infancia e Assistencia Social", "Ampliar a cobertura do Programa Crianca Feliz e do SCFV."),
        ("Infraestrutura Urbana", "Priorizar investimentos em espacos publicos amigaveis a Primeira Infancia."),
        ("Monitoramento Continuo", "Manter a atualizacao anual deste painel."),
    ]

    for titulo_rec, texto_rec in recs:
        story.append(Paragraph(f"• {titulo_rec}", destaque))
        story.append(Paragraph(texto_rec, ParagraphStyle('Rec', parent=corpo, leftIndent=0.8*cm, spaceAfter=10)))

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("_________________________________", ParagraphStyle('Linha', parent=corpo, alignment=TA_CENTER)))
    story.append(Paragraph("<b>Observatorio da Primeira Infancia de Caucaia</b>", ParagraphStyle('Ass', parent=corpo, alignment=TA_CENTER, fontSize=12, textColor=cor_azul)))
    story.append(Paragraph("Prefeitura Municipal de Caucaia - Secretaria Municipal de Saude", ParagraphStyle('Ass2', parent=corpo, alignment=TA_CENTER, fontSize=10, textColor=colors.gray)))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# CABECALHO + BOTAO PDF
# ==========================================
periodo_txt = f"{anos_hist[0]} a {anos_hist[-1]}"

col_header, col_btn = st.columns([3, 1])

with col_header:
    st.markdown(f"""
    <div class="header-inst">
        <h1>Painel de Nascidos Vivos - Caucaia</h1>
        <p>Observatorio da Primeira Infancia - Periodo historico: {periodo_txt} - Fonte: SINASC</p>
    </div>
    """, unsafe_allow_html=True)

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    pdf_bytes = gerar_relatorio_pdf()
    st.download_button(
        label="Baixar Relatorio PDF",
        data=pdf_bytes,
        file_name=f"relatorio_executivo_caucaia_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True,
        key="btn_pdf_top",
        type="primary"
    )

# ==========================================
# KPI PRINCIPAL
# ==========================================
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

# ==========================================
# EVOLUCAO + PROJECAO
# ==========================================
st.markdown('<div class="secao-titulo">Evolucao Historica e Projecao (2014-2030)</div>', unsafe_allow_html=True)

fig_hist = go.Figure()

fig_hist.add_trace(go.Scatter(x=anos_hist, y=valores_hist, mode='lines+markers', name='Historico',
    line=dict(color=AZUL, width=3), marker=dict(size=10, color=AZUL, line=dict(color=BRANCO, width=2)),
    hovertemplate='<b>%{x}</b><br>%{y:,.0f} nascimentos<extra></extra>'))

fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_projetados, mode='lines+markers', name='Projecao Realista',
    line=dict(color=AMARELO, width=3, dash='dash'), marker=dict(size=10, color=AMARELO, symbol='diamond', line=dict(color=BRANCO, width=2)),
    hovertemplate='<b>%{x}</b><br>Projecao: %{y:,.0f}<extra></extra>'))

fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_otimista, mode='lines', name='Cenario Otimista',
    line=dict(color=VERDE, width=1.5, dash='dot'), hovertemplate='<b>%{x}</b><br>Otimista: %{y:,.0f}<extra></extra>'))

fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_pessimista, mode='lines', name='Cenario Pessimista',
    line=dict(color=CORAL, width=1.5, dash='dot'), hovertemplate='<b>%{x}</b><br>Pessimista: %{y:,.0f}<extra></extra>'))

fig_hist.add_vline(x=2025.5, line_width=1, line_dash="solid", line_color="#999999",
    annotation_text="Inicio da Projecao", annotation_position="top")

fig_hist.update_layout(
    height=450, margin=dict(l=20, r=20, t=40, b=40),
    xaxis_title="Ano", yaxis_title="Numero de Nascidos",
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=12, color=GRAFITE),
    separators=',.',
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    xaxis=dict(showgrid=False, linecolor='#DDDDDD', dtick=1, tickfont=dict(color='#333333', size=12)),
    yaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12))
)
st.plotly_chart(fig_hist, use_container_width=True)

st.markdown(f"""
<div class="info-projecao">
    <strong>Nota metodologica:</strong> A projecao foi calculada por <strong>regressao linear</strong> 
    com base nos dados historicos de {anos_hist[0]} a {anos_hist[-1]}. 
    Os cenarios otimista e pessimista representam o intervalo de confianca de 95%.
</div>
""", unsafe_allow_html=True)

# CARDS DE PROJECAO
st.markdown('<div class="secao-titulo">Projecao para 2026-2030</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Projetado (2026-2030)", fmt(total_2026_2030))
with col2:
    kpi_card("Media Anual Projetada", fmt(media_projetada))
with col3:
    tendencia_txt = "Crescimento" if coef[0] > 0 else "Reducao"
    cor_tend = VERDE if coef[0] > 0 else CORAL
    kpi_card("Tendencia Identificada", tendencia_txt, f"{coef[0]:+.0f} nascidos/ano", cor=cor_tend)
with col4:
    kpi_card("Projecao 2030", fmt(valores_projetados[-1]))

# ==========================================
# TABELA CUSTOMIZADA (Ano esquerda, outras centralizadas)
# ==========================================
st.markdown("**Detalhamento por Ano:**")

linhas_html = ""
for i, ano in enumerate(anos_projecao):
    linhas_html += f"""
        <tr style="border-bottom: 1px solid #EEEEEE;">
            <td style="padding: 12px 16px; text-align: left; color: #333333; font-weight: 600;">{ano}</td>
            <td style="padding: 12px 16px; text-align: center; color: #333333;">{fmt(valores_pessimista[i])}</td>
            <td style="padding: 12px 16px; text-align: center; color: #1F3A6E; font-weight: 700; background: #E8F4FD;">{fmt(valores_projetados[i])}</td>
            <td style="padding: 12px 16px; text-align: center; color: #333333;">{fmt(valores_otimista[i])}</td>
        </tr>
    """

tabela_html = f"""
<div style="overflow-x: auto; margin-top: 12px;">
    <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.06);">
        <thead>
            <tr style="background: {AZUL}; color: white;">
                <th style="padding: 14px 16px; text-align: left; font-weight: 600; font-size: 14px;">Ano</th>
                <th style="padding: 14px 16px; text-align: center; font-weight: 600; font-size: 14px;">Cenario Pessimista</th>
                <th style="padding: 14px 16px; text-align: center; font-weight: 600; font-size: 14px;">Projecao Realista</th>
                <th style="padding: 14px 16px; text-align: center; font-weight: 600; font-size: 14px;">Cenario Otimista</th>
            </tr>
        </thead>
        <tbody>
            {linhas_html}
        </tbody>
    </table>
</div>
"""

st.markdown(tabela_html, unsafe_allow_html=True)

# ==========================================
# SEXO E PARTO
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="secao-titulo">Distribuicao por Sexo</div>', unsafe_allow_html=True)
    fig_sexo = go.Figure(data=[go.Pie(
        labels=['Masculino', 'Feminino'], values=[masc, fem], hole=0.55,
        marker=dict(colors=[AZUL, AMARELO], line=dict(color=BRANCO, width=3)),
        textinfo='label+percent', textfont=dict(size=14, color=BRANCO, family="Arial"),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} nascidos<br>%{percent}<extra></extra>'
    )])
    fig_sexo.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20), showlegend=True,
        separators=',.', legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(size=13, color=GRAFITE)),
        font=dict(family="Arial", color=GRAFITE), paper_bgcolor=BRANCO)
    st.plotly_chart(fig_sexo, use_container_width=True)

with col2:
    st.markdown('<div class="secao-titulo">Tipo de Parto</div>', unsafe_allow_html=True)
    labels_parto = list(dados['por_parto'].keys())
    valores_parto = list(dados['por_parto'].values())
    mapa_cores_parto = {'Cesario': CORAL, 'Cesareo': CORAL, 'Cesariana': CORAL, 'Vaginal': VERDE, 'Normal': VERDE, 'Sem informacoes': '#CCCCCC', 'Ignorado': '#CCCCCC'}
    cores_parto = [mapa_cores_parto.get(l, AZUL_CLARO) for l in labels_parto]
    fig_parto = go.Figure(data=[go.Pie(
        labels=labels_parto, values=valores_parto, hole=0.55,
        marker=dict(colors=cores_parto, line=dict(color=BRANCO, width=3)),
        textinfo='label+percent', textfont=dict(size=13, color=BRANCO, family="Arial"),
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} nascidos<br>%{percent}<extra></extra>'
    )])
    fig_parto.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20), showlegend=True,
        separators=',.', legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(size=13, color=GRAFITE)),
        font=dict(family="Arial", color=GRAFITE), paper_bgcolor=BRANCO)
    st.plotly_chart(fig_parto, use_container_width=True)

# PRE-NATAL
st.markdown('<div class="secao-titulo">Cobertura de Pre-Natal</div>', unsafe_allow_html=True)
ordem_prenatal = ['Nenhuma', 'de 1 a 3', 'de 4 a 6', '7 e mais', 'Ignorado']
dados_prenatal_ordenado = {k: dados['por_prenatal'][k] for k in ordem_prenatal if k in dados['por_prenatal']}

fig_prenatal = go.Figure(data=[go.Bar(
    x=list(dados_prenatal_ordenado.values()), y=list(dados_prenatal_ordenado.keys()), orientation='h',
    marker=dict(color=AZUL, line=dict(color=BRANCO, width=1)),
    text=[fmt(v) for v in dados_prenatal_ordenado.values()], textposition='outside', textfont=dict(size=12, color=GRAFITE),
    hovertemplate='<b>%{y}</b><br>%{x:,.0f} maes<extra></extra>'
)])
fig_prenatal.update_layout(height=320, margin=dict(l=20, r=80, t=20, b=40),
    xaxis_title="Numero de Maes", yaxis_title="", plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=12, color=GRAFITE), separators=',.',
    xaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
    yaxis=dict(showgrid=False, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
    showlegend=False)
st.plotly_chart(fig_prenatal, use_container_width=True)

# PESO
st.markdown('<div class="secao-titulo">Distribuicao de Peso ao Nascer</div>', unsafe_allow_html=True)
ordem_peso = ['Menos de 500 g', '500 a 999g', '1000 a 1499g', '1500 a 2499g', '2500 a 2999g', '3000 a 3999g', '4000g e mais', 'Ign']
dados_peso_ordenado = {k: dados['por_peso'][k] for k in ordem_peso if k in dados['por_peso']}
cores_peso = {'Menos de 500 g': CORAL, '500 a 999g': CORAL, '1000 a 1499g': CORAL, '1500 a 2499g': AMARELO, '2500 a 2999g': VERDE, '3000 a 3999g': VERDE, '4000g e mais': AMARELO, 'Ign': '#CCCCCC'}

fig_peso = go.Figure(data=[go.Bar(
    x=list(dados_peso_ordenado.values()), y=list(dados_peso_ordenado.keys()), orientation='h',
    marker=dict(color=[cores_peso.get(k, AZUL) for k in dados_peso_ordenado.keys()], line=dict(color=BRANCO, width=1)),
    text=[fmt(v) for v in dados_peso_ordenado.values()], textposition='outside', textfont=dict(size=12, color=GRAFITE),
    hovertemplate='<b>%{y}</b><br>%{x:,.0f} bebes<extra></extra>'
)])
fig_peso.update_layout(height=380, margin=dict(l=20, r=80, t=20, b=40),
    xaxis_title="Numero de Bebes", yaxis_title="", plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=12, color=GRAFITE), separators=',.',
    xaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
    yaxis=dict(showgrid=False, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
    showlegend=False)
st.plotly_chart(fig_peso, use_container_width=True)

# IDADE DAS MAES
st.markdown('<div class="secao-titulo">Faixa Etaria das Maes</div>', unsafe_allow_html=True)
labels_idade = list(dados['por_idade_mae'].keys())
valores_idade = list(dados['por_idade_mae'].values())

fig_idade = go.Figure(data=[go.Bar(
    x=labels_idade, y=valores_idade,
    marker=dict(color=AZUL, line=dict(color=BRANCO, width=1)),
    text=[fmt(v) for v in valores_idade], textposition='outside', textfont=dict(size=12, color=GRAFITE),
    hovertemplate='<b>%{x}</b><br>%{y:,.0f} maes<extra></extra>'
)])
fig_idade.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=40),
    xaxis_title="Faixa Etaria", yaxis_title="Numero de Maes",
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=12, color=GRAFITE), separators=',.',
    xaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
    yaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
    showlegend=False)
st.plotly_chart(fig_idade, use_container_width=True)

# GESTACAO
if 'por_gestacao' in dados:
    st.markdown('<div class="secao-titulo">Duracao da Gestacao</div>', unsafe_allow_html=True)
    labels_gest = list(dados['por_gestacao'].keys())
    valores_gest = list(dados['por_gestacao'].values())

    fig_gest = go.Figure(data=[go.Bar(
        x=valores_gest, y=labels_gest, orientation='h',
        marker=dict(color=VERDE, line=dict(color=BRANCO, width=1)),
        text=[fmt(v) for v in valores_gest], textposition='outside', textfont=dict(size=12, color=GRAFITE),
        hovertemplate='<b>%{y}</b><br>%{x:,.0f} bebes<extra></extra>'
    )])
    fig_gest.update_layout(height=350, margin=dict(l=20, r=80, t=20, b=40),
        xaxis_title="Numero de Bebes", yaxis_title="", plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
        font=dict(family="Arial", size=12, color=GRAFITE), separators=',.',
        xaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
        yaxis=dict(showgrid=False, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=12)),
        showlegend=False)
    st.plotly_chart(fig_gest, use_container_width=True)

# INDICADORES RESUMIDOS
st.markdown('<div class="secao-titulo">Indicadores Resumidos</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    kpi_card("Peso Medio ao Nascer", f"{dados['estatisticas']['peso_medio_g']:.0f} g")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Peso Minimo", f"{dados['estatisticas']['peso_min_g']} g")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Peso Maximo", f"{dados['estatisticas']['peso_max_g']} g")

with col2:
    kpi_card("Idade Media das Maes", f"{dados['estatisticas']['idade_media_mae']} anos")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Idade Minima", f"{dados['estatisticas']['idade_min_mae']} anos")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Idade Maxima", f"{dados['estatisticas']['idade_max_mae']} anos")

with col3:
    kpi_card("Periodo Historico", f"{anos_hist[0]} a {anos_hist[-1]}")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Anos Analisados", f"{len(anos_hist)} anos")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Media Anual", fmt(media_anual))

# RODAPE
st.markdown(f"""
<div class="rodape-inst">
    <strong>Fonte dos dados:</strong> SINASC - Sistema de Informacao sobre Nascidos Vivos<br>
    <strong>Observatorio da Primeira Infancia de Caucaia</strong><br>
    Prefeitura Municipal de Caucaia - Secretaria Municipal de Saude<br>
    <em>Ultima atualizacao: {datetime.now().strftime('%d/%m/%Y as %H:%M')}</em>
</div>
""", unsafe_allow_html=True)
# -*- coding: utf-8 -*-
"""
Painel de Nascidos Vivos - Observatório da Primeira Infância de Caucaia
Página interna: pages/1_Nascidos_Vivos.py
Gráficos 100% estáticos.
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
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# ==========================================
# CSS
# ==========================================
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

    /* Esconde a barra de ferramentas do Plotly */
    .modebar { display: none !important; }
    .modebar-container { display: none !important; }
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

# ✅ CONFIGURAÇÃO GLOBAL — GRÁFICOS 100% ESTÁTICOS
PLOTLY_CONFIG = {
    'staticPlot': True,           # desativa TODA interatividade (hover, zoom, pan)
    'displayModeBar': False,      # esconde a barra de ferramentas
    'displaylogo': False,
    'scrollZoom': False,
}


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
    .stApp {{ background-color: {BRANCO}; }}
    .secao-titulo {{ color: {AZUL}; font-size: 20px; font-weight: 600; margin: 32px 0 16px 0; padding-bottom: 8px; border-bottom: 2px solid {AZUL_CLARO}; }}
    .rodape-inst {{ background: {AZUL}; color: white; padding: 20px 32px; border-radius: 8px; text-align: center; font-size: 12px; margin-top: 40px; line-height: 1.6; }}
    .info-projecao {{ background: {CINZA}; padding: 16px 20px; border-radius: 8px; border-left: 4px solid {AZUL}; font-size: 13px; color: {GRAFITE}; margin: 16px 0; }}
    div[data-testid="stDownloadButton"] button {{ background-color: {AMARELO}; color: {AZUL}; border: none; border-radius: 8px; padding: 16px 20px; font-weight: 700; font-size: 15px; width: 100%; transition: all 0.2s; box-shadow: 0 4px 12px rgba(245, 185, 58, 0.3); margin-top: 12px; }}
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

# ==========================================
# ANALISES ADICIONAIS PARA O PDF
# ==========================================
total_parto = sum(dados['por_parto'].values())
cesariana = dados['por_parto'].get('Cesário', 0) + dados['por_parto'].get('Cesario', 0) + dados['por_parto'].get('Cesareo', 0)
vaginal = dados['por_parto'].get('Vaginal', 0)
perc_ces = (cesariana / total_parto) * 100 if total_parto > 0 else 0
perc_vag = (vaginal / total_parto) * 100 if total_parto > 0 else 0

total_prenatal = sum(dados['por_prenatal'].values())
pren_adequado = dados['por_prenatal'].get('7 e mais', 0)
pren_nenhum = dados['por_prenatal'].get('Nenhuma', 0)
perc_adequado = (pren_adequado / total_prenatal) * 100 if total_prenatal > 0 else 0
perc_nenhum = (pren_nenhum / total_prenatal) * 100 if total_prenatal > 0 else 0

total_peso = sum(dados['por_peso'].values())
baixo_peso = sum(v for k, v in dados['por_peso'].items() if any(x in k for x in ['Menos de 500', '500 a 999', '1000 a 1499', '1500 a 2499']))
perc_baixo_peso = (baixo_peso / total_peso) * 100 if total_peso > 0 else 0


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
    story.append(Paragraph("Observatório da Primeira Infância", ParagraphStyle('Sub', parent=titulo, fontSize=14, spaceAfter=8)))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("RELATÓRIO DE NASCIDOS VIVOS", ParagraphStyle('TitRel', parent=titulo, fontSize=18, spaceAfter=12)))
    story.append(Paragraph(f"Período de análise: {anos_hist[0]} a {anos_hist[-1]}", ParagraphStyle('Periodo', parent=corpo, alignment=TA_CENTER, fontSize=12)))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", ParagraphStyle('Data', parent=corpo, alignment=TA_CENTER, fontSize=10, textColor=colors.gray)))
    story.append(Spacer(1, 1*cm))

    story.append(Paragraph("1. SUMÁRIO EXECUTIVO", subtitulo))
    tendencia_txt = "crescimento" if coef[0] > 0 else "redução"
    texto_executivo = f"""
    Este relatório apresenta a análise dos nascidos vivos no município de Caucaia no período 
    de <b>{anos_hist[0]} a {anos_hist[-1]}</b>, totalizando <b>{fmt(dados['total_nascimentos'])} nascimentos</b> 
    registrados no Sistema de Informação sobre Nascidos Vivos (SINASC).
    <br/><br/>
    A média anual de nascimentos no período foi de <b>{fmt(media_anual)} crianças</b>. A análise de tendência 
    identificou um cenário de <b>{tendencia_txt}</b> de aproximadamente <b>{abs(coef[0]):.0f} nascimentos por ano</b>, 
    com projeção de <b>{fmt(total_2026_2030)} nascimentos</b> para o quinquênio 2026-2030.
    <br/><br/>
    O peso médio ao nascer foi de <b>{dados['estatisticas']['peso_medio_g']:.0f} g</b> e a idade média das mães 
    foi de <b>{dados['estatisticas']['idade_media_mae']} anos</b>.
    """
    story.append(Paragraph(texto_executivo, corpo))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph("2. INDICADORES PRINCIPAIS", subtitulo))
    dados_tabela = [
        ['Indicador', 'Valor'],
        ['Total de Nascidos Vivos', fmt(dados['total_nascimentos'])],
        ['Média Anual de Nascimentos', fmt(media_anual)],
        ['Período Analisado', f'{anos_hist[0]} a {anos_hist[-1]}'],
        ['Anos de Série Histórica', f'{len(anos_hist)} anos'],
        ['Peso Médio ao Nascer', f"{dados['estatisticas']['peso_medio_g']:.0f} g"],
        ['Peso Mínimo Registrado', f"{dados['estatisticas']['peso_min_g']} g"],
        ['Peso Máximo Registrado', f"{dados['estatisticas']['peso_max_g']} g"],
        ['Idade Média das Mães', f"{dados['estatisticas']['idade_media_mae']} anos"],
        ['Idade Mínima das Mães', f"{dados['estatisticas']['idade_min_mae']} anos"],
        ['Idade Máxima das Mães', f"{dados['estatisticas']['idade_max_mae']} anos"],
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
    story.append(Paragraph("3. PROJEÇÃO PARA 2026-2030", subtitulo))
    texto_projecao = f"""
    Com base na análise de regressão linear sobre os dados históricos de {anos_hist[0]} a {anos_hist[-1]}, 
    projeta-se <b>{fmt(total_2026_2030)} nascimentos</b> no quinquênio 2026-2030, com média anual de 
    <b>{fmt(media_projetada)} nascimentos</b>. A tendência identificada é de <b>{tendencia_txt}</b>.
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
    story.append(Paragraph("4. ANÁLISE DE SAÚDE MATERNO-INFANTIL", subtitulo))

    story.append(Paragraph("4.1 Cobertura de Pré-Natal", destaque))
    texto_prenatal = f"""
    Das <b>{fmt(total_prenatal)}</b> mães registradas, <b>{fmt(pren_adequado)}</b> (<b>{perc_adequado:.1f}%</b>) 
    realizaram <b>7 ou mais consultas</b> de pré-natal. No entanto, <b>{fmt(pren_nenhum)}</b> mães 
    (<b>{perc_nenhum:.1f}%</b>) <b>não realizaram nenhuma consulta</b>.
    """
    story.append(Paragraph(texto_prenatal, corpo))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("4.2 Tipo de Parto", destaque))
    texto_parto = f"""
    Do total de partos, <b>{fmt(cesariana)}</b> (<b>{perc_ces:.1f}%</b>) foram cesarianas e <b>{fmt(vaginal)}</b> 
    (<b>{perc_vag:.1f}%</b>) foram partos vaginais. A OMS recomenda taxa de cesarianas entre 10% e 15%.
    """
    story.append(Paragraph(texto_parto, corpo))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("4.3 Peso ao Nascer", destaque))
    texto_peso = f"""
    A média de peso ao nascer foi de <b>{dados['estatisticas']['peso_medio_g']:.0f} g</b>. Foram registrados 
    <b>{fmt(baixo_peso)}</b> bebês com <b>peso inferior a 2.500 g</b> (<b>{perc_baixo_peso:.1f}%</b>).
    """
    story.append(Paragraph(texto_peso, corpo))

    story.append(PageBreak())
    story.append(Paragraph("5. RECOMENDAÇÕES PARA A GESTÃO MUNICIPAL", subtitulo))
    story.append(Paragraph("Com base na análise técnica dos dados, apresentam-se as seguintes recomendações:", corpo))
    story.append(Spacer(1, 0.3*cm))

    recs = [
        ("Saúde Materno-Infantil", "Ampliar a cobertura de pré-natal adequado."),
        ("Redução de Cesarianas Desnecessárias", "Implementar protocolos de classificação de risco obstétrico."),
        ("Educação Infantil", "Dimensionar a oferta de vagas em creches e pré-escolas."),
        ("Primeira Infância e Assistência Social", "Ampliar a cobertura do Programa Criança Feliz e do SCFV."),
        ("Infraestrutura Urbana", "Priorizar investimentos em espaços públicos amigáveis à Primeira Infância."),
        ("Monitoramento Contínuo", "Manter a atualização anual deste painel."),
    ]
    for titulo_rec, texto_rec in recs:
        story.append(Paragraph(f"• {titulo_rec}", destaque))
        story.append(Paragraph(texto_rec, ParagraphStyle('Rec', parent=corpo, leftIndent=0.8*cm, spaceAfter=10)))

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("_________________________________", ParagraphStyle('Linha', parent=corpo, alignment=TA_CENTER)))
    story.append(Paragraph("<b>Observatório da Primeira Infância de Caucaia</b>", ParagraphStyle('Ass', parent=corpo, alignment=TA_CENTER, fontSize=12, textColor=cor_azul)))
    story.append(Paragraph("Prefeitura Municipal de Caucaia - Secretaria Municipal de Saúde", ParagraphStyle('Ass2', parent=corpo, alignment=TA_CENTER, fontSize=10, textColor=colors.gray)))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# CABECALHO + PDF
# ==========================================
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
    st.download_button(label="📄 Baixar Relatório PDF", data=pdf_bytes,
        file_name=f"relatorio_nascidos_vivos_caucaia_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf", use_container_width=True, key="btn_pdf_top", type="primary")


# ==========================================
# KPIs PRINCIPAIS
# ==========================================
col_principal, col_espaco, col_kpi1, col_kpi2, col_kpi3 = st.columns([2, 0.3, 1, 1, 1])

with col_principal:
    kpi_destaque("Total de Nascidos Vivos no Período Histórico", fmt(dados['total_nascimentos']), f"Média anual: {fmt(media_anual)} nascimentos")
with col_kpi1:
    sinal = "+" if var_ano >= 0 else "-"
    kpi_card(f"Variação {ultimo} vs {penultimo}", f"{sinal}{fmt(abs(var_ano))}", f"{pct_var:+.1f}%", cor=VERDE if var_ano >= 0 else CORAL)
with col_kpi2:
    kpi_card("Peso Médio ao Nascer", f"{dados['estatisticas']['peso_medio_g']:.0f} g")
with col_kpi3:
    kpi_card("Idade Média das Mães", f"{dados['estatisticas']['idade_media_mae']} anos")


# ==========================================
# EVOLUCAO E PROJECAO
# ==========================================
st.markdown('<div class="secao-titulo">Evolução Histórica e Projeção (2014-2030)</div>', unsafe_allow_html=True)

fig_hist = go.Figure()
fig_hist.add_trace(go.Scatter(x=anos_hist, y=valores_hist, mode='lines+markers', name='Histórico',
    line=dict(color=AZUL, width=3), marker=dict(size=10, color=AZUL, line=dict(color=BRANCO, width=2))))
fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_projetados, mode='lines+markers', name='Projeção Realista',
    line=dict(color=AMARELO, width=3, dash='dash'),
    marker=dict(size=10, color=AMARELO, symbol='diamond', line=dict(color=BRANCO, width=2))))
fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_otimista, mode='lines', name='Cenário Otimista',
    line=dict(color=VERDE, width=1.5, dash='dot')))
fig_hist.add_trace(go.Scatter(x=anos_projecao, y=valores_pessimista, mode='lines', name='Cenário Pessimista',
    line=dict(color=CORAL, width=1.5, dash='dot')))

fig_hist.add_vline(x=2025.5, line_width=2, line_dash="solid", line_color="#999999",
    annotation_text="Início da Projeção", annotation_position="top",
    annotation_font=dict(size=12, color=GRAFITE, family="Arial"))

fig_hist.update_layout(
    height=450, margin=dict(l=20, r=20, t=50, b=40),
    xaxis_title="Ano", yaxis_title="Número de Nascidos",
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=13, color=GRAFITE),
    separators=',.',
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5,
                font=dict(size=13, color=GRAFITE)),
    xaxis=dict(showgrid=False, linecolor='#DDDDDD', dtick=1, tickfont=dict(color='#333333', size=13)),
    yaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13))
)
st.plotly_chart(fig_hist, use_container_width=True, config=PLOTLY_CONFIG)

st.markdown(f'<div class="info-projecao"><strong>Nota metodológica:</strong> A projeção foi calculada por <strong>regressão linear</strong> com base nos dados históricos de {anos_hist[0]} a {anos_hist[-1]}. Os cenários otimista e pessimista representam o intervalo de confiança de 95%.</div>', unsafe_allow_html=True)


# ==========================================
# CARDS DE PROJECAO
# ==========================================
st.markdown('<div class="secao-titulo">Projeção para 2026-2030</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("Total Projetado (2026-2030)", fmt(total_2026_2030))
with col2:
    kpi_card("Média Anual Projetada", fmt(media_projetada))
with col3:
    tendencia_txt = "Crescimento" if coef[0] > 0 else "Redução"
    cor_tend = VERDE if coef[0] > 0 else CORAL
    kpi_card("Tendência Identificada", tendencia_txt, f"{coef[0]:+.0f} nascidos/ano", cor=cor_tend)
with col4:
    kpi_card("Projeção 2030", fmt(valores_projetados[-1]))


# ==========================================
# TABELA DE PROJECAO
# ==========================================
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

html_tabela = '<table class="tabela-projecao"><thead><tr><th>Ano</th><th>Cenário Pessimista</th><th>Projeção Realista</th><th>Cenário Otimista</th></tr></thead><tbody>'
for i, ano in enumerate(anos_projecao):
    html_tabela += f'<tr><td>{ano}</td><td>{fmt(valores_pessimista[i])}</td><td>{fmt(valores_projetados[i])}</td><td>{fmt(valores_otimista[i])}</td></tr>'
html_tabela += '</tbody></table>'
st.markdown(html_tabela, unsafe_allow_html=True)


# ==========================================
# SEXO E PARTO
# ==========================================
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="secao-titulo">Distribuição por Sexo</div>', unsafe_allow_html=True)
    fig_sexo = go.Figure(data=[go.Pie(
        labels=['Masculino', 'Feminino'], values=[masc, fem], hole=0.55,
        marker=dict(colors=[AZUL, AMARELO], line=dict(color=BRANCO, width=3)),
        textinfo='label+percent',
        textfont=dict(size=14, color=BRANCO, family="Arial"),
        insidetextorientation='horizontal'
    )])
    fig_sexo.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor=BRANCO,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5,
                    font=dict(size=13, color=GRAFITE)))
    st.plotly_chart(fig_sexo, use_container_width=True, config=PLOTLY_CONFIG)

with col2:
    st.markdown('<div class="secao-titulo">Tipo de Parto</div>', unsafe_allow_html=True)
    labels_parto = list(dados['por_parto'].keys())
    valores_parto = list(dados['por_parto'].values())
    mapa_cores_parto = {'Cesário': CORAL, 'Cesario': CORAL, 'Cesareo': CORAL, 'Cesariana': CORAL, 'Vaginal': VERDE, 'Normal': VERDE}
    cores_parto = [mapa_cores_parto.get(l, AZUL_CLARO) for l in labels_parto]
    fig_parto = go.Figure(data=[go.Pie(
        labels=labels_parto, values=valores_parto, hole=0.55,
        marker=dict(colors=cores_parto, line=dict(color=BRANCO, width=3)),
        textinfo='label+percent',
        textfont=dict(size=14, color=BRANCO, family="Arial"),
        insidetextorientation='horizontal'
    )])
    fig_parto.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor=BRANCO,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5,
                    font=dict(size=13, color=GRAFITE)))
    st.plotly_chart(fig_parto, use_container_width=True, config=PLOTLY_CONFIG)


# ==========================================
# PRE-NATAL
# ==========================================
st.markdown('<div class="secao-titulo">Cobertura de Pré-Natal</div>', unsafe_allow_html=True)
ordem_prenatal = ['Nenhuma', 'de 1 a 3', 'de 4 a 6', '7 e mais', 'Ignorado']
dados_prenatal_ordenado = {k: dados['por_prenatal'][k] for k in ordem_prenatal if k in dados['por_prenatal']}

fig_prenatal = go.Figure(data=[go.Bar(
    x=list(dados_prenatal_ordenado.values()),
    y=list(dados_prenatal_ordenado.keys()),
    orientation='h',
    marker=dict(color=AZUL, line=dict(color=BRANCO, width=1)),
    text=[fmt(v) for v in dados_prenatal_ordenado.values()],
    textposition='outside',
    textfont=dict(size=13, color=GRAFITE, family="Arial")
)])
fig_prenatal.update_layout(
    height=320, margin=dict(l=20, r=100, t=20, b=40),
    xaxis_title="Número de Mães", yaxis_title="",
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=13, color=GRAFITE),
    separators=',.',
    xaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
    yaxis=dict(showgrid=False, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
    showlegend=False
)
st.plotly_chart(fig_prenatal, use_container_width=True, config=PLOTLY_CONFIG)


# ==========================================
# PESO AO NASCER
# ==========================================
st.markdown('<div class="secao-titulo">Distribuição de Peso ao Nascer</div>', unsafe_allow_html=True)
ordem_peso = ['Menos de 500 g', '500 a 999g', '1000 a 1499g', '1500 a 2499g', '2500 a 2999g', '3000 a 3999g', '4000g e mais', 'Ign']
dados_peso_ordenado = {k: dados['por_peso'][k] for k in ordem_peso if k in dados['por_peso']}
cores_peso = {'Menos de 500 g': CORAL, '500 a 999g': CORAL, '1000 a 1499g': CORAL, '1500 a 2499g': AMARELO, '2500 a 2999g': VERDE, '3000 a 3999g': VERDE, '4000g e mais': AMARELO, 'Ign': '#CCCCCC'}

fig_peso = go.Figure(data=[go.Bar(
    x=list(dados_peso_ordenado.values()),
    y=list(dados_peso_ordenado.keys()),
    orientation='h',
    marker=dict(color=[cores_peso.get(k, AZUL) for k in dados_peso_ordenado.keys()], line=dict(color=BRANCO, width=1)),
    text=[fmt(v) for v in dados_peso_ordenado.values()],
    textposition='outside',
    textfont=dict(size=13, color=GRAFITE, family="Arial")
)])
fig_peso.update_layout(
    height=380, margin=dict(l=20, r=100, t=20, b=40),
    xaxis_title="Número de Bebês", yaxis_title="",
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=13, color=GRAFITE),
    separators=',.',
    xaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
    yaxis=dict(showgrid=False, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
    showlegend=False
)
st.plotly_chart(fig_peso, use_container_width=True, config=PLOTLY_CONFIG)


# ==========================================
# FAIXA ETARIA DAS MAES
# ==========================================
st.markdown('<div class="secao-titulo">Faixa Etária das Mães</div>', unsafe_allow_html=True)
labels_idade = list(dados['por_idade_mae'].keys())
valores_idade = list(dados['por_idade_mae'].values())

fig_idade = go.Figure(data=[go.Bar(
    x=labels_idade, y=valores_idade,
    marker=dict(color=AZUL, line=dict(color=BRANCO, width=1)),
    text=[fmt(v) for v in valores_idade],
    textposition='outside',
    textfont=dict(size=13, color=GRAFITE, family="Arial")
)])
fig_idade.update_layout(
    height=400, margin=dict(l=20, r=20, t=40, b=40),
    xaxis_title="Faixa Etária", yaxis_title="Número de Mães",
    plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
    font=dict(family="Arial", size=13, color=GRAFITE),
    separators=',.',
    xaxis=dict(showgrid=False, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
    yaxis=dict(showgrid=False, showticklabels=True, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
    showlegend=False,
    bargap=0.35
)
st.plotly_chart(fig_idade, use_container_width=True, config=PLOTLY_CONFIG)


# ==========================================
# GESTACAO
# ==========================================
if 'por_gestacao' in dados:
    st.markdown('<div class="secao-titulo">Duração da Gestação</div>', unsafe_allow_html=True)
    labels_gest = list(dados['por_gestacao'].keys())
    valores_gest = list(dados['por_gestacao'].values())

    fig_gest = go.Figure(data=[go.Bar(
        x=valores_gest, y=labels_gest, orientation='h',
        marker=dict(color=VERDE, line=dict(color=BRANCO, width=1)),
        text=[fmt(v) for v in valores_gest],
        textposition='outside',
        textfont=dict(size=13, color=GRAFITE, family="Arial")
    )])
    fig_gest.update_layout(
        height=350, margin=dict(l=20, r=100, t=20, b=40),
        xaxis_title="Número de Bebês", yaxis_title="",
        plot_bgcolor=BRANCO, paper_bgcolor=BRANCO,
        font=dict(family="Arial", size=13, color=GRAFITE),
        separators=',.',
        xaxis=dict(gridcolor='#EEEEEE', linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
        yaxis=dict(showgrid=False, linecolor='#DDDDDD', tickfont=dict(color='#333333', size=13)),
        showlegend=False
    )
    st.plotly_chart(fig_gest, use_container_width=True, config=PLOTLY_CONFIG)


# ==========================================
# INDICADORES RESUMIDOS
# ==========================================
st.markdown('<div class="secao-titulo">Indicadores Resumidos</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    kpi_card("Peso Médio ao Nascer", f"{dados['estatisticas']['peso_medio_g']:.0f} g")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Peso Mínimo", f"{dados['estatisticas']['peso_min_g']} g")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Peso Máximo", f"{dados['estatisticas']['peso_max_g']} g")

with col2:
    kpi_card("Idade Média das Mães", f"{dados['estatisticas']['idade_media_mae']} anos")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Idade Mínima", f"{dados['estatisticas']['idade_min_mae']} anos")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Idade Máxima", f"{dados['estatisticas']['idade_max_mae']} anos")

with col3:
    kpi_card("Período Histórico", f"{anos_hist[0]} a {anos_hist[-1]}")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Anos Analisados", f"{len(anos_hist)} anos")
    st.markdown("<br>", unsafe_allow_html=True)
    kpi_card("Média Anual", fmt(media_anual))


# ==========================================
# RODAPE
# ==========================================
st.markdown(f"""
<div class="rodape-inst">
    <strong>Fonte dos dados:</strong> SINASC - Sistema de Informação sobre Nascidos Vivos<br>
    <strong>Observatório da Primeira Infância de Caucaia</strong><br>
    Prefeitura Municipal de Caucaia - Secretaria Municipal de Saúde<br>
    <em>Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</em>
</div>
""", unsafe_allow_html=True)
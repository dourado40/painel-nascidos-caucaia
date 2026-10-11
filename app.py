# -*- coding: utf-8 -*-
"""
app.py - Hub de Indicadores
Página inicial do Streamlit, carregada dentro do iframe no WordPress.
Cards clicáveis — o card inteiro é um link que abre NO MESMO iframe.
"""

import streamlit as st
from datetime import datetime

# ==========================================
# CONFIGURACAO
# ==========================================
st.set_page_config(
    page_title="Indicadores - Observatório Caucaia",
    page_icon="https://www.caucaia.ce.gov.br/favicon.ico",
    layout="wide"
)

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
</style>
""", unsafe_allow_html=True)

AZUL = "#1F3A6E"
AMARELO = "#F5B93A"
VERDE = "#5DB5A8"
CORAL = "#E89B7D"
AZUL_CLARO = "#A8C8E8"
BRANCO = "#FFFFFF"

# ==========================================
# TITULO
# ==========================================
st.markdown(f"""
<div style="padding: 8px 0 24px 0; margin-bottom: 8px;">
    <h2 style="color: {AZUL}; font-size: 28px; margin: 0 0 10px 0; font-weight: 700; line-height: 1.2;">
        Indicadores da Primeira Infância
    </h2>
    <p style="color: #555; font-size: 15px; margin: 0; line-height: 1.5;">
        Selecione um painel abaixo para explorar os dados e indicadores estratégicos 
        de Caucaia voltados às crianças de 0 a 6 anos.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# LINHA 1 DE CARDS
# ==========================================
col1, col2, col3 = st.columns(3)

# --- CARD 1: NASCIDOS VIVOS (CLICÁVEL - abre no mesmo iframe) ---
with col1:
    st.markdown(f"""
    <a href="/Nascidos_Vivos" 
       style="text-decoration: none; display: block;">
        <div style="background: white; border-left: 4px solid {AZUL}; padding: 24px; 
                    border-radius: 8px; box-shadow: 0 4px 12px rgba(31, 58, 110, 0.1); 
                    height: 250px; display: flex; flex-direction: column; justify-content: space-between;
                    transition: all 0.25s; cursor: pointer;"
             onmouseover="this.style.transform='translateY(-6px)'; this.style.boxShadow='0 10px 24px rgba(31, 58, 110, 0.25)';"
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(31, 58, 110, 0.1)';">
            <div>
                <div style="font-size: 38px; margin-bottom: 12px;">👶</div>
                <h3 style="color: {AZUL}; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">
                    Nascidos Vivos →
                </h3>
                <p style="color: #666; font-size: 13px; margin: 0; line-height: 1.5;">
                    Total de nascimentos, perfil das mães, tipo de parto, peso ao nascer 
                    e projeções para os próximos anos.
                </p>
            </div>
            <div style="margin-top: 12px;">
                <span style="display: inline-block; background: {VERDE}; color: white; 
                             padding: 4px 10px; border-radius: 12px; font-size: 10px; 
                             font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                    ● Disponível
                </span>
                <span style="float: right; color: {AZUL}; font-size: 12px; font-weight: 600; 
                             margin-top: 4px;">
                    Clique para acessar
                </span>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# --- CARD 2: MORTALIDADE INFANTIL ---
with col2:
    st.markdown(f"""
    <div style="background: white; border-left: 4px solid {CORAL}; padding: 24px; 
                border-radius: 8px; box-shadow: 0 4px 12px rgba(232, 155, 125, 0.1); 
                height: 250px; display: flex; flex-direction: column; justify-content: space-between; opacity: 0.85;">
        <div>
            <div style="font-size: 38px; margin-bottom: 12px;">📉</div>
            <h3 style="color: {AZUL}; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">
                Mortalidade Infantil
            </h3>
            <p style="color: #666; font-size: 13px; margin: 0; line-height: 1.5;">
                Análise da mortalidade infantil no município, com recortes por idade, 
                causa e local de ocorrência.
            </p>
        </div>
        <div style="margin-top: 12px;">
            <span style="display: inline-block; background: #CCCCCC; color: white; 
                         padding: 4px 10px; border-radius: 12px; font-size: 10px; 
                         font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                ○ Em breve
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CARD 3: EDUCACAO INFANTIL ---
with col3:
    st.markdown(f"""
    <div style="background: white; border-left: 4px solid {VERDE}; padding: 24px; 
                border-radius: 8px; box-shadow: 0 4px 12px rgba(93, 181, 168, 0.1); 
                height: 250px; display: flex; flex-direction: column; justify-content: space-between; opacity: 0.85;">
        <div>
            <div style="font-size: 38px; margin-bottom: 12px;">🎓</div>
            <h3 style="color: {AZUL}; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">
                Educação Infantil
            </h3>
            <p style="color: #666; font-size: 13px; margin: 0; line-height: 1.5;">
                Matrículas em creches e pré-escolas, vagas ofertadas e taxa de cobertura.
            </p>
        </div>
        <div style="margin-top: 12px;">
            <span style="display: inline-block; background: #CCCCCC; color: white; 
                         padding: 4px 10px; border-radius: 12px; font-size: 10px; 
                         font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                ○ Em breve
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# LINHA 2 DE CARDS
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background: white; border-left: 4px solid {AMARELO}; padding: 24px; 
                border-radius: 8px; box-shadow: 0 4px 12px rgba(245, 185, 58, 0.1); 
                height: 250px; display: flex; flex-direction: column; justify-content: space-between; opacity: 0.85;">
        <div>
            <div style="font-size: 38px; margin-bottom: 12px;">💉</div>
            <h3 style="color: {AZUL}; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">
                Cobertura Vacinal
            </h3>
            <p style="color: #666; font-size: 13px; margin: 0; line-height: 1.5;">
                Taxas de vacinação infantil por tipo de vacina e faixa etária.
            </p>
        </div>
        <div style="margin-top: 12px;">
            <span style="display: inline-block; background: #CCCCCC; color: white; 
                         padding: 4px 10px; border-radius: 12px; font-size: 10px; 
                         font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                ○ Em breve
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: white; border-left: 4px solid {AZUL_CLARO}; padding: 24px; 
                border-radius: 8px; box-shadow: 0 4px 12px rgba(168, 200, 232, 0.1); 
                height: 250px; display: flex; flex-direction: column; justify-content: space-between; opacity: 0.85;">
        <div>
            <div style="font-size: 38px; margin-bottom: 12px;">🍼</div>
            <h3 style="color: {AZUL}; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">
                Aleitamento Materno
            </h3>
            <p style="color: #666; font-size: 13px; margin: 0; line-height: 1.5;">
                Indicadores de amamentação exclusiva e alimentação complementar.
            </p>
        </div>
        <div style="margin-top: 12px;">
            <span style="display: inline-block; background: #CCCCCC; color: white; 
                         padding: 4px 10px; border-radius: 12px; font-size: 10px; 
                         font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                ○ Em breve
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: white; border-left: 4px solid #C8A8E8; padding: 24px; 
                border-radius: 8px; box-shadow: 0 4px 12px rgba(200, 168, 232, 0.1); 
                height: 250px; display: flex; flex-direction: column; justify-content: space-between; opacity: 0.85;">
        <div>
            <div style="font-size: 38px; margin-bottom: 12px;">👨‍👩‍👧</div>
            <h3 style="color: {AZUL}; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">
                Assistência Social
            </h3>
            <p style="color: #666; font-size: 13px; margin: 0; line-height: 1.5;">
                Famílias acompanhadas pelo SCFV e Programa Criança Feliz.
            </p>
        </div>
        <div style="margin-top: 12px;">
            <span style="display: inline-block; background: #CCCCCC; color: white; 
                         padding: 4px 10px; border-radius: 12px; font-size: 10px; 
                         font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                ○ Em breve
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# RODAPE
# ==========================================
st.markdown(f"""
<div style="background: {AZUL}; color: white; padding: 20px 32px; border-radius: 8px; 
            text-align: center; font-size: 12px; margin-top: 48px; line-height: 1.6;">
    <strong>Observatório da Primeira Infância de Caucaia</strong><br>
    Prefeitura Municipal de Caucaia - Secretaria Municipal de Saúde<br>
    <em>Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</em>
</div>
""", unsafe_allow_html=True)
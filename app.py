with col1:
    st.markdown(f"""
    <div style="background: white; border-left: 4px solid {AZUL}; padding: 24px; 
                border-radius: 8px; box-shadow: 0 4px 12px rgba(31, 58, 110, 0.1); 
                height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div style="font-size: 38px; margin-bottom: 12px;">👶</div>
            <h3 style="color: {AZUL}; margin: 0 0 8px 0; font-size: 18px; font-weight: 700;">
                Nascidos Vivos
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
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link(
        "pages/1_Nascidos_Vivos.py",
        label="📊 Acessar Painel →",
        use_container_width=True
    )
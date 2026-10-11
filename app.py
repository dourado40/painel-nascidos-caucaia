with col1:
    st.markdown(f"""
    <a href="https://painel-nascidos-caucaia.streamlit.app/1_Nascidos_Vivos" 
       target="_blank"
       style="text-decoration: none; display: block;">
        <div style="background: white; border-left: 4px solid {AZUL}; padding: 24px; 
                    border-radius: 8px; box-shadow: 0 4px 12px rgba(31, 58, 110, 0.1); 
                    height: 250px; display: flex; flex-direction: column; justify-content: space-between;
                    transition: all 0.2s; cursor: pointer;"
             onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 20px rgba(31, 58, 110, 0.2)';"
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
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)
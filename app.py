st.markdown("**Detalhamento por Ano:**")

# Montar HTML da tabela
linhas_html = ""
for i, ano in enumerate(anos_projecao):
    linhas_html += f'<tr style="border-bottom: 1px solid #EEEEEE;">'
    linhas_html += f'<td style="padding: 12px 16px; text-align: left; color: #333333; font-weight: 600;">{ano}</td>'
    linhas_html += f'<td style="padding: 12px 16px; text-align: center; color: #333333;">{fmt(valores_pessimista[i])}</td>'
    linhas_html += f'<td style="padding: 12px 16px; text-align: center; color: #1F3A6E; font-weight: 700; background: #E8F4FD;">{fmt(valores_projetados[i])}</td>'
    linhas_html += f'<td style="padding: 12px 16px; text-align: center; color: #333333;">{fmt(valores_otimista[i])}</td>'
    linhas_html += '</tr>'

# Criar tabela completa (uma única string, sem quebras)
tabela_html = '<div style="overflow-x: auto; margin-top: 12px;"><table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.06);"><thead><tr style="background: ' + AZUL + '; color: white;"><th style="padding: 14px 16px; text-align: left; font-weight: 600; font-size: 14px;">Ano</th><th style="padding: 14px 16px; text-align: center; font-weight: 600; font-size: 14px;">Cenário Pessimista</th><th style="padding: 14px 16px; text-align: center; font-weight: 600; font-size: 14px;">Projeção Realista</th><th style="padding: 14px 16px; text-align: center; font-weight: 600; font-size: 14px;">Cenário Otimista</th></tr></thead><tbody>' + linhas_html + '</tbody></table></div>'

st.markdown(tabela_html, unsafe_allow_html=True)
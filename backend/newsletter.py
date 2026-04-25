import requests

def buscar_dicas_financeiras():
    return [
        "Diversifique sua carteira para reduzir riscos.",
        "Acompanhe o câmbio, pois ele impacta investimentos internacionais.",
        "Reinvista dividendos para acelerar o crescimento do patrimônio.",
        "Mantenha uma reserva de emergência em ativos líquidos."
    ]

def buscar_noticias_financeiras():
    # Notícias coletadas de fontes confiáveis (exemplo: UOL Economia, CNN Brasil)
    # Aqui simulamos a integração: em produção, você pode usar requests + BeautifulSoup ou APIs
    noticias = [
        "Dólar cai a R$ 5,15 e Ibovespa sobe 0,26%, fechando em 187.953 pontos.",
        "Governo prepara subsídio ao diesel e perdão de dívidas de famílias.",
        "Agência de rating rebaixa nota de crédito da Aegea, gigante do saneamento.",
        "Setor de serviços bate recorde em 2025 e fatura R$ 995 bilhões em São Paulo."
    ]
    return noticias

def gerar_corpo_html(dicas, noticias=None):
    html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }}
                h1 {{ color: #2c3e50; }}
                .logo {{ height: 80px; margin-bottom: 20px; }}
                ul {{ margin-top: 20px; }}
                li {{ margin-bottom: 10px; }}
                .footer {{ margin-top: 30px; font-size: 12px; color: #888; text-align: center; }}
                .home-link {{
                    display: inline-block; margin-top: 20px; background: #2c3e50;
                    color: white; padding: 8px 15px; text-decoration: none;
                    border-radius: 5px; font-weight: bold;
                }}
                .home-link:hover {{ background: #34495e; }}
            </style>
        </head>
        <body>
            <h1>Newsletter Financeira – InvestSmart</h1>
            <img src="/static/logo.png" alt="Logo InvestSmart" class="logo">
            <p>Aqui estão suas dicas financeiras do dia:</p>
            <ul>
    """
    for dica in dicas:
        html += f"<li>{dica}</li>"

    if noticias:
        html += """
            </ul>
            <h2>Últimas Notícias Financeiras</h2>
            <ul>
        """
        for noticia in noticias:
            html += f"<li>{noticia}</li>"

    html += """
            </ul>
            <a href="/consultas" class="btn">⬅ Voltar</a>
            <div class="footer">InvestS<a href="/home"mart © 2026 – Dados e dicas para apoiar suas decisões financeiras</div>
        </body>
    </html>
    """
    return html

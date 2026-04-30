import yfinance as yf
import plotly.graph_objects as go
import datetime
import pandas as pd
import io
import base64
from backend.news import buscar_noticias_financeiras

# Lista de tickers brasileiros
TICKERS_BR = {
    "PETR4": "PETR4.SA",
    "VALE3": "VALE3.SA",
    "ITUB4": "ITUB4.SA"
}

def obter_dados_mercado(ativo, periodo="30d"):
    hoje = datetime.date.today()
    if periodo == "7d":
        inicio = hoje - datetime.timedelta(days=7)
    elif periodo == "1y":
        inicio = hoje - datetime.timedelta(days=365)
    else:
        inicio = hoje - datetime.timedelta(days=30)
    try:
        dados = yf.download(ativo, start=inicio, end=hoje)
        return dados["Close"].dropna()
    except Exception:
        datas = pd.date_range(start=inicio, end=hoje)
        valores = [100 + i*0.5 for i in range(len(datas))]
        return pd.Series(valores, index=datas)

def gerar_grafico_interativo(dados, titulo):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados.index, y=dados.values, mode="lines", name="Preço"))
    if len(dados) > 7:
        fig.add_trace(go.Scatter(x=dados.index, y=dados.rolling(7).mean(), mode="lines", name="MM 7d"))
    if len(dados) > 21:
        fig.add_trace(go.Scatter(x=dados.index, y=dados.rolling(21).mean(), mode="lines", name="MM 21d"))
    fig.update_layout(
        title=titulo,
        xaxis_title="Data",
        yaxis_title="Preço",
        template="plotly_dark",
        height=300   # controla altura do gráfico
    )
    return fig.to_html(full_html=False)

def exportar_pdf(dados, ativo):
    if isinstance(dados, pd.Series):
        df = dados.to_frame(name="Preço")
    else:
        df = dados
    conteudo = f"Relatório InvestSmart\nAtivo: {ativo}\n\n{df.to_string()}"
    pdf_bytes = conteudo.encode("utf-8")
    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")
    return f'<a href="data:application/pdf;base64,{pdf_base64}" download="relatorio_{ativo}.pdf" class="btn">📄 Baixar PDF</a>'

def exportar_excel(dados, ativo):
    if isinstance(dados, pd.Series):
        df = dados.to_frame(name="Preço")
    else:
        df = dados
    output = io.BytesIO()
    df.to_excel(output, sheet_name="Relatório")
    excel_base64 = base64.b64encode(output.getvalue()).decode("utf-8")
    return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_base64}" download="relatorio_{ativo}.xlsx" class="btn">📊 Baixar Excel</a>'

def gerar_dashboard_html(ativo, periodo="30d"):
    dados = obter_dados_mercado(ativo, periodo)
    grafico_html = gerar_grafico_interativo(dados, f"Ativo: {ativo} – Período {periodo}")
    pdf_link = exportar_pdf(dados, ativo)
    excel_link = exportar_excel(dados, ativo)
    noticias = buscar_noticias_financeiras(ativo)
    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Dashboard – InvestSmart</title>
        <link rel="stylesheet" href="/static/style.css?v=2">
    </head>
    <body>
    <header>
        <h1>InvestSmart</h1>
        <nav>
            <a href="/home">Home</a>
            <a href="/consultas">Consultas</a>
            <a href="/logout">Sair</a>
        </nav>
    </header>

    <main class="container">
        <h2>Dashboard Financeiro</h2>
        <div class="card">
            {grafico_html}
            <div class="export-buttons">
                {pdf_link}
                {excel_link}
            </div>
        </div>
    </main>

    <footer>
        <div class="noticias">📰 Últimas Notícias</div>
    </footer>
    </body>
    </html>
    """

def gerar_dashboard_todos(ativos, periodo="30d"):
    dados_combinados = {}
    for ativo in ativos:
        try:
            dados_combinados[ativo] = obter_dados_mercado(ativo, periodo)
        except:
            pass

    fig = go.Figure()
    for ativo, dados in dados_combinados.items():
        fig.add_trace(go.Scatter(x=dados.index, y=dados.values, mode="lines", name=ativo))
    
    fig.update_layout(
        title="Comparativo de Ativos",
        xaxis_title="Data",
        yaxis_title="Preço",
        template="plotly_dark",
        height=400
    )
    grafico_html = fig.to_html(full_html=False)

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Comparativo – InvestSmart</title>
        <link rel="stylesheet" href="/static/style.css?v=2">
    </head>
    <body>
    <header>
        <h1>InvestSmart</h1>
        <nav>
            <a href="/home">Home</a>
            <a href="/consultas">Consultas</a>
            <a href="/logout">Sair</a>
        </nav>
    </header>

    <main class="container">
        <h2>Comparativo de Ativos selecionados</h2>
        <div class="card" style="max-width: 900px;">
            {grafico_html}
        </div>
    </main>

    <footer>
        <div class="noticias">📰 Últimas Notícias</div>
    </footer>
    </body>
    </html>
    """
    return html

def gerar_home_html():
    indices = {
        "IBOV": "^BVSP",
        "Dólar": "USDBRL=X",
        "S&P500": "^GSPC"
    }
    cards = ""
    for nome, ticker in indices.items():
        dados = obter_dados_mercado(ticker, "7d")
        ultimo = round(dados.iloc[-1], 2)
        cards += f"<div class='card'><h2>{nome}</h2><p>Último valor: {ultimo}</p></div>"
    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>InvestSmart - Painel</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <header>
            <h1>InvestSmart</h1>
            <nav>
                <a href="/consultas">Nova Consulta</a>
                <a href="/logout">Sair</a>
            </nav>
        </header>

        <main class="container">
            <h2>Visão Geral do Mercado (7 dias)</h2>
            <div class="card-grid">
                {cards}
            </div>
            
            <a href="/consultas" class="btn">Realizar Nova Consulta</a>
        </main>

        <footer>InvestSmart © 2026 – Seu painel financeiro inteligente</footer>
    </body>
    </html>
    """

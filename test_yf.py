import yfinance as yf
import datetime

hoje = datetime.date.today()
inicio = hoje - datetime.timedelta(days=7)
dados = yf.download("^BVSP", start=inicio, end=hoje)
print("Columns:", dados.columns)
print("Is empty?", dados.empty)
print(dados.head())

import yfinance as yf
import datetime
hoje = datetime.date.today()
inicio = hoje - datetime.timedelta(days=7)
dados = yf.download("^BVSP", start=inicio, end=hoje)
if hasattr(dados, 'columns'):
    print("Columns are MultiIndex:", isinstance(dados.columns, __import__('pandas').MultiIndex))
    if isinstance(dados.columns, __import__('pandas').MultiIndex):
        dados.columns = dados.columns.get_level_values(0)
    dados = dados.loc[:, ~dados.columns.duplicated()]
    print("Columns:", dados.columns)
    print("Head:", dados.head())

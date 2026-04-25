import os
import feedparser

def buscar_noticias_financeiras(query=None):
    """
    Busca notícias financeiras em feeds RSS gratuitos.
    Se 'query' for fornecido, tenta filtrar notícias que contenham o termo.
    """

    # Pega o feed principal da variável de ambiente ou usa o padrão do Infomoney
    feed_url = os.getenv("RSS_FEED", "https://www.infomoney.com.br/feed/")

    noticias = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # pega até 5 notícias
            titulo = entry.title
            link = entry.link
            if query:
                # filtra apenas notícias que contenham o termo
                if query.lower() in titulo.lower():
                    noticias.append(f"<li><a href='{link}' target='_blank'>{titulo}</a></li>")
            else:
                noticias.append(f"<li><a href='{link}' target='_blank'>{titulo}</a></li>")
    except Exception:
        noticias.append("<li>Não foi possível carregar notícias.</li>")

    if noticias:
        return "<ul>" + "".join(noticias) + "</ul>"
    else:
        return "<p>Não há notícias disponíveis no momento.</p>"

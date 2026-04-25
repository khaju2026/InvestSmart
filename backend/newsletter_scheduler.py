import schedule
import time
from backend.newsletter import buscar_dicas_financeiras, gerar_corpo_email, enviar_email

def tarefa_diaria():
    """
    Executa a tarefa diária de buscar dicas financeiras,
    gerar o corpo da newsletter e enviar por e-mail.
    """
    dicas = buscar_dicas_financeiras()
    corpo = gerar_corpo_email(dicas)
    enviar_email("usuario@email.com", corpo)

# Agendamento diário às 8h da manhã
schedule.every().day.at("08:00").do(tarefa_diaria)

def iniciar_agendador():
    """
    Mantém o agendador rodando em loop infinito.
    Deve ser chamado pelo main.py em uma thread separada.
    """
    while True:
        schedule.run_pending()
        time.sleep(60)

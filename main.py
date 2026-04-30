from fastapi import FastAPI, Query, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from backend.dashboard import gerar_dashboard_html, gerar_dashboard_todos, TICKERS_BR, gerar_home_html
from backend.database import SessionLocal, engine
from backend.crud import get_usuario_by_email, get_usuario_by_cpf, verify_password, create_usuario, create_consulta
from backend import schemas, models

# Cria as tabelas no banco de dados, caso não existam
models.Base.metadata.create_all(bind=engine)
import os
from datetime import date

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="chave_super_secreta")

def verificar_login(request: Request):
    return request.session.get("usuario_id") is not None

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    error = request.session.pop("error", "")
    error_html = f"<p style='color:red;'>{error}</p>" if error else ""
    return HTMLResponse(f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/static/style.css?v=2">
    </head>
    <body>
    <div class="card login-card" style="margin-top: 100px; text-align: center;">
        <img src="/static/logo.png" class="logo" alt="InvestSmart Logo">
        <h2>Login InvestSmart</h2>
        {error_html}
        <form action="/login" method="post">
            <input type="email" name="email" placeholder="E-mail" required style="margin-bottom:15px;"><br>
            <input type="password" name="senha" placeholder="Senha" required style="margin-bottom:15px;"><br>
            <button type="submit" class="btn" style="width:100%; margin-bottom:15px;">Entrar</button>
        </form>
        <p>Não tem conta? <a href="/register">Registre-se aqui</a></p>
    </div>
    </body>
    </html>
    """)

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    error = request.session.pop("error", "")
    error_html = f"<p style='color:red;'>{error}</p>" if error else ""
    return HTMLResponse(f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/static/style.css?v=2">
    </head>
    <body>
    <div class="card login-card" style="margin-top: 100px; text-align: center;">
        <img src="/static/logo.png" class="logo" alt="InvestSmart Logo">
        <h2>Cadastro InvestSmart</h2>
        {error_html}
        <form action="/register" method="post">
            <input type="text" name="nome" placeholder="Nome Completo" required style="margin-bottom:15px;"><br>
            <input type="text" name="cpf" placeholder="CPF" required style="margin-bottom:15px;"><br>
            <input type="email" name="email" placeholder="E-mail" required style="margin-bottom:15px;"><br>
            <input type="password" name="senha" placeholder="Senha" required style="margin-bottom:15px;"><br>
            <button type="submit" class="btn" style="width:100%; margin-bottom:15px;">Criar Conta</button>
        </form>
        <p>Já tem conta? <a href="/login">Faça Login</a></p>
    </div>
    </body>
    </html>
    """)

@app.post("/register", response_class=HTMLResponse)
def register_post(request: Request, nome: str = Form(...), cpf: str = Form(...), email: str = Form(...), senha: str = Form(...)):
    db = SessionLocal()
    try:
        if get_usuario_by_email(db, email):
            request.session["error"] = "E-mail já está em uso."
            return RedirectResponse(url="/register", status_code=303)
        if get_usuario_by_cpf(db, cpf):
            request.session["error"] = "CPF já está em uso."
            return RedirectResponse(url="/register", status_code=303)
        
        novo_usuario = schemas.UsuarioCreate(nome=nome, cpf=cpf, email=email, senha=senha)
        usuario_criado = create_usuario(db, novo_usuario)
        
        # Loga automaticamente após registro
        request.session["usuario_id"] = usuario_criado.id
        return RedirectResponse(url="/home", status_code=303)
    except Exception as e:
        import traceback
        erro = traceback.format_exc()
        return HTMLResponse(f"<h3>Erro Interno do Servidor (500)</h3><pre>{erro}</pre>")
    finally:
        db.close()

@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, email: str = Form(...), senha: str = Form(...)):
    db = SessionLocal()
    try:
        usuario = get_usuario_by_email(db, email)
        if usuario and verify_password(senha, usuario.senha_hash):
            request.session["usuario_id"] = usuario.id
            return RedirectResponse(url="/home", status_code=303)
        request.session["error"] = "E-mail ou senha inválidos."
        return RedirectResponse(url="/login", status_code=303)
    finally:
        db.close()

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/", response_class=HTMLResponse)
def root():
    landing_path = os.path.join(os.path.dirname(__file__), "landing", "index.html")
    try:
        with open(landing_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except Exception:
        # Se falhar em ler o index.html, redireciona para login
        return RedirectResponse(url="/login", status_code=303)

@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    if not verificar_login(request):
        return RedirectResponse(url="/login", status_code=303)
    return HTMLResponse(gerar_home_html())

@app.get("/consultas", response_class=HTMLResponse)
def consultas(request: Request):
    if not verificar_login(request):
        return RedirectResponse(url="/login", status_code=303)

    ativos_dict = {"IBOV": "^BVSP", "Dólar": "USDBRL=X", "S&P500": "^GSPC", **TICKERS_BR}
    ativos_html = ""
    for nome, ticker in ativos_dict.items():
        ativos_html += f"<label><input type='checkbox' name='ativos' value='{ticker}' class='ativo'> {nome}</label><br>"

    page = f"""
    <html><head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/static/style.css">
    <script>
    function marcarTodos() {{
        var checkboxes = document.querySelectorAll('.ativo');
        checkboxes.forEach(cb => cb.checked = true);
    }}
    function desmarcarTodos() {{
        var checkboxes = document.querySelectorAll('.ativo');
        checkboxes.forEach(cb => cb.checked = false);
    }}
    </script>
    </head><body>
    <header>
        <h1>InvestSmart</h1>
        <nav>
            <a href="/home">Home</a>
            <a href="/logout">Sair</a>
        </nav>
    </header>
    <main class="container">
        <h2>Consultas Financeiras</h2>
        <div class="card" style="text-align: center;">
            <img src="/static/logo.png" class="logo" alt="InvestSmart Logo">
            <form action="/dashboard/all" method="get">
                <div style="margin-bottom: 1rem;">
                    <button type="button" class="btn secondary" onclick="marcarTodos()">Marcar Todos</button>
                    <button type="button" class="btn secondary" onclick="desmarcarTodos()">Desmarcar Todos</button>
                </div>
                <div class="checkbox-group">
                    {ativos_html}
                </div>
                <label>Período:
                    <select name="periodo" style="max-width: 200px; margin: 0 auto;">
                        <option value="7d">7 dias</option>
                        <option value="30d">30 dias</option>
                        <option value="1y">1 ano</option>
                    </select>
                </label><br>
                <button type="submit" class="btn" style="margin-top:1.5rem; width:100%; max-width:300px;">📉 Gerar Dashboard </button>
            </form>
        </div>
    </main>
    </body></html>
    """
    return HTMLResponse(content=page)

@app.get("/dashboard/all", response_class=HTMLResponse)
def dashboard_all(request: Request, ativos: list[str] = Query(default=[]), periodo: str = Query(default="30d")):
    if not verificar_login(request):
        return RedirectResponse(url="/login", status_code=303)
    if not ativos:
        return HTMLResponse("<h1>Nenhum ativo selecionado</h1><a href='/consultas'>Voltar</a>")
    
    # Registra consulta no banco
    db = SessionLocal()
    try:
        nova_consulta = schemas.ConsultaCreate(
            ativos=",".join(ativos),
            periodo=periodo,
            data_consulta=date.today(),
            usuario_id=request.session["usuario_id"]
        )
        create_consulta(db, nova_consulta, request.session["usuario_id"])
    except Exception as e:
        import traceback
        erro = traceback.format_exc()
        return HTMLResponse(f"<h3>Erro Interno do Servidor (500)</h3><pre>Erro no BD: {erro}</pre>")
    finally:
        db.close()

    try:
        return HTMLResponse(gerar_dashboard_todos(ativos, periodo))
    except Exception as e:
        import traceback
        erro = traceback.format_exc()
        return HTMLResponse(f"<h3>Erro Interno do Servidor (500)</h3><pre>Erro ao gerar gráficos: {erro}</pre>")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, ativo: str = Query(default="^BVSP"), periodo: str = Query(default="30d")):
    if not verificar_login(request):
        return RedirectResponse(url="/login", status_code=303)

    # Registra consulta no banco
    db = SessionLocal()
    try:
        nova_consulta = schemas.ConsultaCreate(
            ativos=ativo,
            periodo=periodo,
            data_consulta=date.today(),
            usuario_id=request.session["usuario_id"]
        )
        create_consulta(db, nova_consulta, request.session["usuario_id"])
    except Exception as e:
        import traceback
        erro = traceback.format_exc()
        return HTMLResponse(f"<h3>Erro Interno do Servidor (500)</h3><pre>Erro no BD: {erro}</pre>")
    finally:
        db.close()

    try:
        return HTMLResponse(gerar_dashboard_html(ativo, periodo))
    except Exception as e:
        import traceback
        erro = traceback.format_exc()
        return HTMLResponse(f"<h3>Erro Interno do Servidor (500)</h3><pre>Erro ao gerar gráfico: {erro}</pre>")

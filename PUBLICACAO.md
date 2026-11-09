# StockChef

Controle de estoque de restaurantes: Flask, SQLAlchemy, HTML/CSS/JavaScript.
Esta versao usa PostgreSQL e esta preparada para Render + Supabase.

## Banco

Em um projeto Supabase vazio, abra SQL Editor > New query e execute
backend/migrations/001_supabase.sql uma unica vez. O script cria 20 tabelas,
relacionamentos e catalogos iniciais. Nao importa dados nem contas do MySQL.
Nao apaga tabelas existentes; se houver conflito de nomes, pare e revise.
As oito consultas antes executadas por procedures agora sao SELECTs no backend.
Enums dos models usam VARCHAR; o script aplica CHECK para os valores permitidos.

RLS esta habilitado sem politicas para anon/authenticated: o frontend nao acessa
o Supabase diretamente. O login e as sessoes continuam no Flask. A conexao usada
no backend e a do Session pooler com usuario postgres.<project-ref> e senha do banco,
que devem ser mantidos apenas no servidor. Nao use a chave publishable no lugar disso.

## Render

Conecte o repositorio GitHub a um Web Service Python no plano Free:

- Build: pip install -r requirements.txt
- Start: gunicorn app:app --bind 0.0.0.0:$PORT
- Health check: /healthz (confirma processo; nao verifica o banco)
- Python: 3.12.10

Alternativamente, use render.yaml para criar um Blueprint, conferindo o plano Free.
Defina SECRET_KEY com um valor longo, aleatorio e estavel.
Defina DB_HOST, DB_USER e DB_PASSWORD com os valores do Session pooler;
DB_PORT=5432, DB_NAME=postgres, DB_SSLMODE=require e COOKIE_SECURE=true.
Nao configure DATABASE_URL junto de DB_*: DATABASE_URL tem prioridade.
Os campos DB_* evitam ter de codificar caracteres especiais da senha em uma URL.

.env.example e apenas referencia: arquivos .env nao sao carregados automaticamente.
A senha nunca deve ir para o Git. GEMINI_API_KEY e opcional e requer teste separado.

## Primeiro acesso

Abra /cadastro, crie um Administrador com sua propria senha e entre em /login.
Cadastre produtos e registre entradas com validade para preparar a apresentacao.
O script nao cria produtos, usuarios nem movimentacoes automaticamente.

## Verificacao

O SQL e as oito consultas foram executados localmente em PostgreSQL embarcado
(PGlite), incluindo filtros e isolamento das consultas por estabelecimento.
Cadastro, login, cookies, produtos, entrada e saida de estoque foram testados no Flask com SQLite; os models tambem compilam para PostgreSQL. Isso nao substitui validar a conexao real do Render ao Supabase e testar os fluxos
na URL publica. A integracao Gemini nao foi validada.
A versao nao constitui uma auditoria completa de autorizacao de todos os endpoints.

## Dominio e dados

Valide primeiro o endereco onrender.com. Depois adicione stockchef.dev.br em
Settings > Custom Domains do Render e aplique no Registro.br os registros indicados.
Aguarde validacao do DNS e emissao do HTTPS. O servico gratuito pode dormir sem trafego.
Mantenha backups externos e teste restauracao; nao grave dados persistentes em disco
local do servico. O MySQL original permanece separado e inalterado.

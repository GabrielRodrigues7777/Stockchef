# StockChef

Sistema de controle de estoque para restaurantes, desenvolvido com Python/Flask,
SQLAlchemy e frontend HTML, CSS e JavaScript servido pelo Flask.

## Estado desta versao

Base preparada para hospedagem. O banco atual e MySQL; a adaptacao para
PostgreSQL/Supabase ainda esta pendente. Esta versao nao deve ser considerada
uma publicacao funcional sem configurar e validar o banco.

Os scripts MySQL originais ficaram fora deste repositorio publico porque
contem dados pessoais e hashes de senhas de exemplo. Uma versao revisada
para inicializacao do banco deve ser adicionada antes da publicacao.

## Configuracao

Requer Python 3.10 ou superior e dependencias de requirements.txt.
Defina as variaveis de .env.example no ambiente do processo ou no painel
da hospedagem. Arquivos .env nao sao carregados automaticamente.
SECRET_KEY e obrigatoria e deve ser longa, aleatoria e mantida em segredo.

Linux / Render:

```sh
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:$PORT
```

Windows:

```powershell
pip install -r requirements.txt
waitress-serve --listen=127.0.0.1:8000 app:app
```

Mantenha COOKIE_SECURE=true em HTTPS. Para testar login em HTTP local,
defina COOKIE_SECURE=false apenas no ambiente local.

O endpoint /healthz verifica o processo Flask, nao a conexao com o banco.
O comando flask --app app init-db cria tabelas ausentes, mas nao instala
procedures e nao substitui migracoes nem restauracao de dados.

A integracao de IA exige GEMINI_API_KEY e validacao separada.
Login, cadastro, produtos e movimentacoes ainda precisam de validacao
no ambiente de publicacao. Nao coloque senhas, tokens ou dados pessoais no Git.

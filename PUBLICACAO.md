# Publicacao para demonstracao

Esta e uma copia preparada; o projeto original foi preservado.
Ainda nao houve publicacao nem validacao de login/estoque nesta sessao.

## Caminho curto: PC atual + Cloudflare Tunnel

O apresentador acessa o dominio em qualquer computador. O PC de origem fica
ligado, sem suspensao, conectado a internet, executando MySQL, Flask e cloudflared.
O dominio precisa estar ativo no Cloudflare para o tunel com nome proprio.
Nao exponha a porta do MySQL na internet.

1. Use Python 3.10 ou superior. Crie um ambiente virtual e instale requirements.txt.
2. Defina SECRET_KEY com um segredo aleatorio longo e estavel; configure DB_HOST,
   DB_PORT, DB_NAME, DB_USER e DB_PASSWORD no ambiente do processo.
   Use um usuario MySQL proprio com os privilegios necessarios ao aplicativo,
   incluindo EXECUTE para as procedures utilizadas.
3. Mantenha COOKIE_SECURE=true no acesso publico HTTPS.
   Para testar login exclusivamente em HTTP local, use COOKIE_SECURE=false.
4. No Windows, inicie: waitress-serve --listen=127.0.0.1:8000 app:app
5. Configure um Cloudflare Tunnel para encaminhar o dominio escolhido para
   http://localhost:8000. O processo cloudflared deve continuar ativo.
6. Teste a URL em outra rede e valide cadastro, login, produtos, entrada e saida
   de estoque e historico. Teste IA separadamente se GEMINI_API_KEY estiver definida.

Os valores de .env.example devem ser definidos no ambiente: o aplicativo nao
carrega arquivos .env automaticamente. Nao publique credenciais nem tokens.

## Hospedagem independente

Preserve MySQL para esta demonstracao: existem chamadas CALL nas funcionalidades.
Em Linux, o servidor pode iniciar com:
gunicorn --bind 0.0.0.0:$PORT app:app
O MySQL precisa estar acessivel pelo backend e conter as procedures do projeto.

## Banco existente

NAO execute backend/database/rodar_tudo_de_uma_vez.sql em um banco com dados:
o arquivo contem DROP DATABASE IF EXISTS stockchef.
Para transportar o banco atual, faca backup completo com routines e triggers,
restaure em um destino separado e valide antes de trocar a conexao.
O comando flask --app app init-db cria apenas tabelas ausentes: ele nao substitui
a importacao de procedures, dados nem uma migracao de esquema.

## Alteracoes desta copia

- Credenciais e chave de sessao saem do codigo e passam para variaveis de ambiente.
- Ausencia de SECRET_KEY interrompe a inicializacao com mensagem explicita.
- Debug desativado e abertura automatica de navegador removida.
- Waitress para Windows e Gunicorn para Linux nas dependencias.
- Comando explicito init-db e endpoint /healthz (confirma processo, nao o banco).
- Cookies HttpOnly, SameSite=Lax e Secure por padrao.

Verificacao limitada: os arquivos foram inspecionados, mas o aplicativo nao foi
executado nesta sessao. Estes ajustes nao constituem auditoria completa de seguranca.

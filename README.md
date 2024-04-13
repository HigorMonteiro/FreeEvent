
# Projeto Django com Celery

Este é um projeto Django que utiliza Celery para tarefas assíncronas. O projeto inclui a geração de relatórios CSV a partir de dados de eventos e participantes.

## Pré-requisitos

- Docker
- Docker Compose

## Como executar o projeto

1. Clone o repositório:
   ```bash
   git clone git@github.com:HigorMonteiro/FreeEvent.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd FreeEvent
   ```
3. Construa e inicie os serviços usando Docker Compose:
   ```bash
   docker compose up --build
   ```
   Isso irá construir as imagens Docker para o aplicativo Django, o servidor de banco de dados, o servidor Celery, o Flower e o RabbitMQ, e então iniciará os contêineres.
4. Execute as migrações do Django:
   ```bash
   docker compose exec web python manage.py migrate
   ```
5. Crie um usuário admin:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
   Siga as instruções na linha de comando para criar o superusuário.

6. Acesse o aplicativo Django em seu navegador: http://localhost:8010/

## Serviços Adicionais

- Flower está rodando em: http://localhost:5555/workers
- RabbitMQ está rodando em: http://localhost:15672/

## Como usar o aplicativo

Para gerar um relatório CSV, acesse a URL `/export-csv/`. O arquivo CSV será salvo na raiz do projeto.

## Executando os testes

Para garantir a qualidade do código, é importante executar os testes antes de fazer qualquer alteração. Use o seguinte comando para executar os testes:
```bash
docker compose exec web python manage.py test
```
A cobertura dos testes pode ser acompanhada em `backend-API/htmlcov/index.html`.

## Como parar o projeto

Para parar os contêineres Docker, use o seguinte comando:
```bash
docker compose down
```

## Contribuindo

Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de enviar um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

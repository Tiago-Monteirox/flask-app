# Flask Agenda

API REST simples para cadastrar e gerenciar eventos de uma agenda. O projeto foi desenvolvido com Flask e oferece documentação interativa gerada pelo Flasgger.

## Funcionalidades

- Listar eventos em ordem cronológica;
- consultar um evento pelo ID;
- criar eventos;
- atualizar eventos existentes;
- remover eventos;
- validar título e data recebidos;
- explorar e testar a API pelo Swagger UI.

## Tecnologias

- Python 3.12+
- Flask
- Flasgger / Swagger
- uv para gerenciamento do ambiente Python

## Como executar

Clone ou baixe o projeto e acesse sua pasta:

```bash
cd flask-agenda
```

Crie o ambiente virtual e instale as dependências:

```bash
uv venv --python 3.12
uv pip install flask flasgger
```

Inicie a aplicação:

```bash
uv run --no-sync flask --app app run --debug
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

## Documentação Swagger

Com a aplicação em execução, acesse a documentação interativa:

```text
http://127.0.0.1:5000/apidocs/
```

Nessa página é possível consultar os modelos, visualizar as respostas esperadas e testar todos os endpoints diretamente pelo navegador.

## Endpoints

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `GET` | `/events` | Lista todos os eventos em ordem cronológica |
| `GET` | `/events/{event_id}` | Consulta um evento pelo ID |
| `POST` | `/events` | Cria um evento |
| `PUT` | `/events/{event_id}` | Substitui os dados de um evento |
| `DELETE` | `/events/{event_id}` | Remove um evento |

## Formato do evento

Para criar ou atualizar um evento, envie um objeto JSON com `title` e `date`:

```json
{
  "title": "Estudar Flask",
  "date": "2026-12-01"
}
```

A data deve seguir o formato `YYYY-MM-DD`.

## Exemplos de uso

### Listar eventos

```bash
curl http://127.0.0.1:5000/events
```

### Criar um evento

```bash
curl --request POST http://127.0.0.1:5000/events \
  --header "Content-Type: application/json" \
  --data '{"title":"Estudar Flask","date":"2026-12-01"}'
```

### Atualizar um evento

```bash
curl --request PUT http://127.0.0.1:5000/events/1 \
  --header "Content-Type: application/json" \
  --data '{"title":"Apresentar Flask","date":"2026-12-02"}'
```

### Remover um evento

```bash
curl --request DELETE http://127.0.0.1:5000/events/1
```

## Estrutura do projeto

```text
flask-agenda/
├── app.py       # Aplicação, rotas, validações e documentação Swagger
└── README.md    # Documentação do projeto
```

## Observação

Os eventos são armazenados somente em memória. Qualquer evento criado, atualizado ou removido durante a execução volta ao estado inicial quando a aplicação é reiniciada.

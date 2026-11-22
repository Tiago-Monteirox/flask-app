from datetime import datetime

from flask import Flask, request
from flasgger import Swagger


app = Flask(__name__)

swagger_template = {
    "info": {
        "title": "API de Agenda",
        "description": "API para consultar e gerenciar eventos de uma agenda.",
        "version": "1.0.0",
    },
    "definitions": {
        "EventInput": {
            "type": "object",
            "required": ["title", "date"],
            "properties": {
                "title": {
                    "type": "string",
                    "example": "Estudar Flask",
                },
                "date": {
                    "type": "string",
                    "format": "date",
                    "example": "2026-12-01",
                },
            },
        },
        "Event": {
            "allOf": [
                {"$ref": "#/definitions/EventInput"},
                {
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "id": {
                            "type": "integer",
                            "example": 1,
                        }
                    },
                },
            ]
        },
        "Error": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Evento não encontrado",
                }
            },
        },
        "Message": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Evento removido com sucesso",
                }
            },
        },
    },
}

swagger = Swagger(app, template=swagger_template)

events = [
    {"id": 1, "title": "Apresentação de Flask", "date": "2026-11-25"},
    {"id": 2, "title": "Entrega do trabalho", "date": "2026-11-30"},
]


def validate_event_data(data):
    if not isinstance(data, dict):
        return {"message": "O corpo da requisição deve ser um objeto JSON"}, 400
    if not isinstance(data.get("title", ""), str) or not data.get("title", "").strip():
        return {"message": "O título deve ser uma string não vazia"}, 400
    if not isinstance(data.get("date", ""), str) or not data.get("date", "").strip():
        return {"message": "A data do evento deve ser uma string não vazia"}, 400
    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return {"message": "Informe uma data válida no formato YYYY-MM-DD"}, 400
    return None


@app.route("/events", methods=["GET"])
def get_events():
    """Lista todos os eventos em ordem cronológica.
    ---
    tags:
      - Eventos
    produces:
      - application/json
    responses:
      200:
        description: Lista de eventos ordenada pela data, da mais próxima à mais distante.
        schema:
          type: array
          items:
            $ref: '#/definitions/Event'
    """
    return sorted(
        events,
        key=lambda event: datetime.strptime(event["date"], "%Y-%m-%d"),
    )


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):
    """Consulta um evento pelo ID.
    ---
    tags:
      - Eventos
    produces:
      - application/json
    parameters:
      - in: path
        name: event_id
        type: integer
        required: true
        description: Identificador do evento.
    responses:
      200:
        description: Evento encontrado.
        schema:
          $ref: '#/definitions/Event'
      404:
        description: Evento não encontrado.
        schema:
          $ref: '#/definitions/Error'
    """
    for event in events:
        if event["id"] == event_id:
            return event
    return {"message": "Evento não encontrado"}, 404


@app.route("/events", methods=["POST"])
def create_event():
    """Cria um novo evento.
    ---
    tags:
      - Eventos
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: Título e data do novo evento.
        schema:
          $ref: '#/definitions/EventInput'
    responses:
      201:
        description: Evento criado com sucesso.
        schema:
          $ref: '#/definitions/Event'
      400:
        description: Corpo JSON, título ou data inválidos.
        schema:
          $ref: '#/definitions/Error'
    """
    data = request.get_json(silent=True)
    validation = validate_event_data(data)
    if validation:
        return validation

    next_id = max((event["id"] for event in events), default=0) + 1
    new_event = {
        "id": next_id,
        "title": data["title"],
        "date": data["date"],
    }
    events.append(new_event)
    return new_event, 201


@app.route("/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    """Substitui os dados de um evento existente.
    ---
    tags:
      - Eventos
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: event_id
        type: integer
        required: true
        description: Identificador do evento.
      - in: body
        name: body
        required: true
        description: Novo título e nova data do evento.
        schema:
          $ref: '#/definitions/EventInput'
    responses:
      200:
        description: Evento atualizado com sucesso.
        schema:
          $ref: '#/definitions/Event'
      400:
        description: Corpo JSON, título ou data inválidos.
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Evento não encontrado.
        schema:
          $ref: '#/definitions/Error'
    """
    data = request.get_json(silent=True)
    validation = validate_event_data(data)
    if validation:
        return validation

    for event in events:
        if event["id"] == event_id:
            event["title"] = data["title"]
            event["date"] = data["date"]
            return event, 200
    return {"message": "Evento não encontrado"}, 404


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """Remove um evento pelo ID.
    ---
    tags:
      - Eventos
    produces:
      - application/json
    parameters:
      - in: path
        name: event_id
        type: integer
        required: true
        description: Identificador do evento.
    responses:
      200:
        description: Evento removido com sucesso.
        schema:
          $ref: '#/definitions/Message'
      404:
        description: Evento não encontrado.
        schema:
          $ref: '#/definitions/Error'
    """
    for event in events:
        if event["id"] == event_id:
            events.remove(event)
            return {"message": "Evento removido com sucesso"}, 200
    return {"message": "Evento não encontrado"}, 404

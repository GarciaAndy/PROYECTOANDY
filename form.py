from  apiclient import discovery    
from httplib2 import Http
from oauth2client.service_account import(
    ServiceAccountCredentials)
import json

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

creds = ServiceAccountCredentials.from_json_keyfile_name(
    'credencialpython.json',
    SCOPES
)


http = creds.authorize(Http())

form_service = discovery.build(
            'forms',
            'v1',
            http=http,
            discoveryServiceUrl=DISCOVERY_DOC,
            static_discovery=False
            )

def add_questions_to_form(form_service, form_id, questions):
    batch_requests = []
    for index, question in enumerate(questions):
        request = {
            "createItem": {
                "item": {
                    "title": question["title"],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": question["type"],
                                "options": question.get("options", []),
                                "shuffle": question.get("shuffle", False)
                            }
                        }
                    },
                },
                "location": {
                    "index": index
                }
            }
        }
        batch_requests.append(request)

    # Execute batch update to add questions to the form
    response = form_service.forms().batchUpdate(
        formId=form_id,
        body={"requests": batch_requests}
    ).execute()

    return response

questions_to_add = [
    {
        "title": "Cual de los siguientes instrumentos es de viento?",
        "type": "RADIO",
        "options": [
            {"value": "Piano"},
            {"value": "Congas"},
            {"value": "Tuba"},
            {"value": "Bajo"}
        ],
        "shuffle": True
    },
    {
        "title": "¿Que ritmo es latino?",
        "type": "RADIO",
        "options": [
            {"value": "Blues"},
            {"value": "Jazz"},
            {"value": "Cumbia"},
            {"value": "Contry"}
        ],
        "shuffle": True
    },
    {
        "title": "¿Que instrumento es de cuerda?",
        "type": "RADIO",
        "options": [
            {"value": "Ukulele"},
            {"value": "Bateria"},
            {"value": "Piano"},
            {"value": "Cajon Peruano"}
        ],
        "shuffle": True
    },
    {
        "title": "¿Cuales ritmos son creados en Islas?",
        "type": "CHECKBOX",
        "options": [
            {"value": "Reggae"},
            {"value": "Cumbia"},
            {"value": "Regguaeton"},
            {"value": "Jazz"}
        ],
        "shuffle": True
    }
]


result = form_service.forms().create(body={"info": {"title": "Mi formulario"}}).execute()
form_id = result["formId"]
add_questions_to_form(form_service, form_id, questions_to_add)


get_results = form_service.forms().get(formId=form_id).execute()
print(json.dumps(get_results,indent=4))

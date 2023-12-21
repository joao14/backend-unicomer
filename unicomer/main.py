from fastapi import FastAPI, File, UploadFile
from google.cloud import documentai_v1beta3 as documentai
from google.protobuf.json_format import MessageToDict
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

documentai_client = documentai.DocumentProcessorServiceClient()

@app.get("/api/v1/document/test")
def read_root():
    return {"mensaje": "API REST 1.0 UNICOMER"}


@app.post("/api/v1/document/analizate")
async def analizar_documento(file: UploadFile = File(...)):
    content = await file.read()
    mime_type = file.content_type
    result = await parse_form_async(content, mime_type)

    return result


async def parse_form_async(content, mime_type):
    request = {
        'name': 'projects/{}/locations/us/processors/c2388ff2df8c3cf'.format('arch-dataloader-poc'),
        'raw_document': {'content': content, 'mime_type': mime_type},
    }

    try:
        response = documentai_client.process_document(request=request)
        response_dict = MessageToDict(response._pb)
        data=''
        if 'document' in response_dict:
            document_value = response_dict['document']
            print(document_value)
            if 'text' in document_value:
                text_value = document_value['text']
                print(f"Valor del campo 'text': {text_value}")
                data = text_value
        return {"message": "Formulario analizado exitosamente","data": data}
    except Exception as e:
        print(e)
        return {"error": str(e)}

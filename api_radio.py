from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import xml.etree.ElementTree as ET

app = FastAPI()

# Habilitar CORS para que FlutterFlow pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/metadata")
def get_metadata():
    # URLs de origen
    playback_info_url = "https://ritmoboss.moxapps.shop/?pass=moxradioserver&action=playbackinfo"
    artwork_url = "https://ritmoboss.moxapps.shop/?pass=moxradioserver&action=trackartwork"
    streaming_url = "https://ritmo.moxapps.shop/stream"

    try:
    response = requests.get(playback_info_url, timeout=5)
    response.raise_for_status()
    
    # Forzar decodificación en UTF-8 para tildes y ñ
    xml_data = ET.fromstring(response.content.decode('utf-8', errors='ignore'))

    track = xml_data.find(".//CurrentTrack/TRACK")
    if track is None:
        return {"error": "No se encontró información de la pista actual."}

    artista = track.attrib.get("ARTIST", "Desconocido")
    titulo = track.attrib.get("TITLE", "Sin título")

    return {
        "artista": artista,
        "titulo": titulo,
        "caratula": artwork_url,
        "streaming": streaming_url
    }


    except Exception as e:
        return {"error": str(e)}

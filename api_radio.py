from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import xml.etree.ElementTree as ET

app = FastAPI()

# Permitir acceso desde FlutterFlow u otros clientes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/metadata")
def get_metadata():
    playback_info_url = "https://ritmoboss.moxapps.shop/?pass=moxradioserver&action=playbackinfo"
    artwork_url = "https://ritmoboss.moxapps.shop/?pass=moxradioserver&action=trackartwork"
    streaming_url = "https://ritmo.moxapps.shop/stream"

    try:
        # Solicitar la información y forzar que se interprete como UTF-8
        response = requests.get(playback_info_url, timeout=5)
        response.encoding = 'utf-8'  # Clave para mostrar tildes y ñ correctamente
        xml_data = ET.fromstring(response.text)

        # Extraer metadatos del XML
        track = xml_data.find(".//CurrentTrack/TRACK")
        if track is None:
            return {"error": "No se encontró información de la pista actual."}

        artista = track.attrib.get("ARTIST", "Desconocido")
        titulo = track.attrib.get("TITLE", "Sin título")

        return {
            "artista": artista,
            "titulo": titulo,
            "caratula": f"{artwork_url}&cache_bust={titulo}-{artista}",
            "streaming": streaming_url
        }

    except Exception as e:
        return {"error": str(e)}

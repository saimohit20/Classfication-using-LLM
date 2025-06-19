import base64
import json
import requests

# === Configuration ===
api_key = " " #<-- Replace with your API key
file_path = "2024-05-07T10-22-37-185000Z.jpg"  # <-- Replace with the path to your image file
model = "gemma3:27b"
api_url = "http://localhost:3000/api/chat/completions"

# === Encode image to base64 ===
def encode_image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

# === Prepare request payload ===
image_base64 = encode_image_to_base64(file_path)

payload = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_base64
                    }
                },
                {
                    "type": "text",
                    "text": """
Bitte analysiere das Bild und beschreibe alle erkennbaren Objekte. Nutze die folgenden Objektkategorien und deren Beschreibungen als Referenz. Diese dienen zur Orientierung, du darfst jedoch auch andere Objekte erwähnen, wenn sie erkennbar sind.

Hier sind die Kategorien mit ihren Beschreibungen:

- SEAMARK: Rot/grüne, kegelförmige Boje aus Metall oder Kunststoff, oder ein aus dem Wasser ragendes Rohr. Nur seitliche Seezeichen.
- CARDINAL: Schwarz/gelbe, kegelförmige Boje oder ein Rohr, das eine Gefahrenstelle markiert. Auch weiße Bojen mit Schwimmer- oder Anglerflaggen.
- OBSTACLE: Hindernis im Wasser, das kein Seezeichen ist und keinen Bezug zum Land hat.
- LANDING: Anlegestelle für Fähren zum Ein- und Aussteigen der Passagiere. Keine allgemeine Kaimauer oder Hafenanlage.
- RIB: Leichtes, leistungsstarkes Boot mit starrem Rumpf und seitlichen Luftkammern.
- MOTORBOAT: Kleines Motorboot, das ausschließlich mit einem Motor betrieben wird, einschließlich Schlauchbooten.
- YACHT: Größeres Motorboot, oft luxuriös, mit auffälliger Deckstruktur. Ausschließlich mit Motor betrieben.
- DINGHY: Kleines Segelboot, oft für Schulungen oder Rennen mit Begleitbooten. Hat typischerweise ein Segel und einen Mast.
- SAILBOAT: Segelboot mit einem Mast, meist für Freizeitaktivitäten.
- TALLSHIP: Großes Segelschiff mit zwei oder mehr Masten, oft traditionell oder touristisch genutzt.
- SWIMMER: Person, die im Wasser schwimmt.
- ROWER: Ruderboot mit mehreren Personen und Riemen an den Seiten, oft für Wettkämpfe.
- CANOE: Einzelne Person in einem Kanu oder Kajak mit Paddel. Flach, schmal, sportlich.
- SUP: Person steht auf einem Brett und paddelt im Wasser. Freizeitaktivität, langsam.
- WINDSURFER: Person auf einem Brett mit fest montiertem Segel, das durch Wind angetrieben wird.
- KITEBOARDER: Person auf einem kleinen Brett, das durch einen großen Lenkdrachen gezogen wird.
- SKIING: Wasserskifahrer, der von einem Boot oder einer Seilzuganlage gezogen wird.
- FERRY: Fähre zur Personenbeförderung auf kurzen Strecken oder für Ausflüge. Mehrere seitliche Fenster, z. B. SFK-Schiffe. Viel kleiner als Kreuzfahrtschiff
- CRUISE: Großes Passagierschiff für längere Reisen, oft weiß mit Namensaufschrift an der Seite.
- CONTAINER: Frachtschiff mit vielen Containern an Bord, langgestreckt.
- TANKER: Großes Schiff für den Transport von Gas, Öl oder anderen Rohstoffen.
- FISHING: Mittleres Schiff zum Fischfang, oft mit sichtbaren Netzen und Möwen in der Nähe.
- RESEARCH: Forschungsschiff, meist blau, weiß oder orange, mit Kran oder Spezialausrüstung.
- OFFSHORE: Versorgungsschiff für Offshore-Arbeiten, oft mit Kränen ausgestattet.
- DREDGER: Baggerschiff zur Aushebung von Sedimenten. Sichtbare Arbeitsgeräte wie Baggerarme.
- PILOT: Kleines, schnelles Boot für Lotsentransporte, meist orange und stromlinienförmig.
- POLICE: Offizielles Polizeiboot mit blauer Lackierung, häufig mit "Polizei" oder "Küstenwache" beschriftet.
- MILITARY: Militärisches Schiff, meist grau, schwarz oder braun.
- SUBMARINE: U-Boot, meist schwarz, größtenteils unter Wasser, kleine sichtbare Struktur.
- TUG: Kleines, kraftvolles Boot zum Schleppen größerer Schiffe, auffälliger Aufbau.
- PONTOON: Flaches, rechteckiges Schwimmelement auf dem Wasser.
- CONVOY: Zwei oder mehr Schiffe, durch Seile verbunden, oft mit Schlepper und Ponton.
"""
                }
            ]
        }
    ]
}

# === Set HTTP headers ===
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# === Send request ===
response = requests.post(api_url, headers=headers, data=json.dumps(payload))

# === Print response ===
if response.ok:
    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    print("Model response:\n", answer)
else:
    print("Error:", response.status_code)
    print(response.text)

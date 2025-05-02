# import subprocess
# import json
# import logging as log
#
#
# def po_token_verifier():
#     # Generiere den YouTube-Token
#     token_object = generate_youtube_token()
#     return token_object["visitorData"], token_object["poToken"]
#
#
# def generate_youtube_token():
#     # Führe den Befehl aus, um den Token zu generieren
#     result = subprocess.run(["youtube-po-token-generator"], capture_output=True, text=True)
#
#     # Überprüfen, ob die Ausgabe erfolgreich war
#     if result.returncode != 0:
#         log.error(f"Fehler bei der Token-Generierung: {result.stderr}")
#         raise Exception("Fehler bei der Token-Generierung")
#
#     # Die Ausgabe als JSON interpretieren
#     try:
#         data = json.loads(result.stdout)
#         log.info(f"Token erfolgreich generiert: {data}")
#     except json.JSONDecodeError:
#         log.error(f"Fehler beim Parsen der JSON-Antwort: {result.stdout}")
#         raise Exception("Fehler beim Parsen der JSON-Antwort")
#
#     return data
#
#
# # Ausgabe der Tokens
# print(po_token_verifier())

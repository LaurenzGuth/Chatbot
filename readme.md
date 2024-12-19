# Exercise Suggestion Bot

Dieses Projekt ist ein Rasa-basierter Chatbot, der Übungen basierend auf 
Benutzereingaben vorschlägt. Der Bot interagiert mit Benutzern, um 
deren Level und Schwächen zu verstehen und schlägt dann passende 
Übungen aus einer MongoDB-Datenbank vor. 

## Funktionen

- **Übungsvorschläge**: Empfiehlt Übungen basierend auf dem Level und den Schwächen des Benutzers.
- **Übungsnachfrage**: Ermöglicht es Benutzern, nach einer bestimmten Übung zu fragen.
- **Übungsdetails**: Gibt detaillierte Informationen über die zuletzt vorgeschlagene Übung.
- **Witze**: Erzählt zufällige Witze.
- **Wetterinformationen**: Bietet aktuelle Wetterinformationen für eine angegebene Stadt.


## Projektstruktur

- `actions/actions.py`: Enthält benutzerdefinierte Aktionsklassen für den Bot.
- `domain.yml`: Definiert die Intents, Entitäten, Slots und Antworten für den Bot.
- `docker-compose.yml`: Docker Compose-Konfiguration zum Einrichten des Rasa-Servers, Aktionsservers und MongoDB.
- `exercises.json`: JSON-Datei mit Übungsdaten, die in MongoDB geladen werden.

## Einrichtung

1. **Requirements installieren**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Mongodb erstellen**:
    ```
   
    ```

4. **Rasa-Server mit aktivierter API und CORS starten**:
    ```sh
    rasa run --enable-api --cors "*"
    ```
```
## Nutzung

- Interagiere mit dem Bot über den Rasa-Server.
- Verwende die bereitgestellten Intents, um Übungsvorschläge, Witze, Wetterinformationen und Übungsdetails anzufordern.

## Abhängigkeiten

- Flask==2.0.2
- pymongo==3.12.1
- rasa==3.0.0
- rasa-sdk==3.0.0

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.
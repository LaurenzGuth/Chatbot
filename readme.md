# Bouldertrainer

Laurenz Guth 766248

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
- `config.yml`: Konfigurationsdatei für das NLU- und Core-Modell.
- `data/nlu.yml`: Trainingsdaten für das NLU-Modell.
- `data/stories.yml`: Trainingsdaten für das Core-Modell.
- `data/rules.yml`: Trainingsdaten für das Rule-based Modell.
- `frontend/app.py`: Flask-App für das Frontend.

- `exercises.json`: JSON-Datei mit Übungsdaten, die in MongoDB geladen werden.

## Einrichtung

1. **Requirements installieren**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Mongodb installieren**:
   

4. **Anwendung starten**:
    ```sh
    rasa run --enable-api --cors "*"
    rasa run actions
    python frontend/app.py
    ```
5. **Index.html öffnen**:
    ```
    frontend/index.html
    ```

## Abhängigkeiten

- Flask==2.0.2
- pymongo==3.12.1
- rasa==3.0.0
- rasa-sdk==3.0.0

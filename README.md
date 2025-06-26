# 🍻 AlcolGame

**AlcolGame** è un gioco alcolico web-based scritto in Python, pensato per animare le serate con gli amici. Grazie al suo sistema modulare a plugin, puoi facilmente creare e aggiungere nuovi minigiochi personalizzati.

---

## 🚀 Deploy Locale

Per avviare il gioco in locale:

```bash
git clone https://github.com/tuo-username/alcolgame.git
cd alcolgame
docker compose up
```

Il gioco sarà disponibile su: [http://localhost:8082](http://localhost:8082)

> Assicurati che la porta **8082** sia libera sul tuo sistema.

---

## 🧩 Come Aggiungere un Nuovo Minigioco

Ogni minigioco è un plugin indipendente collocato in `src/games/plugins/NomeGioco/`.

### 📁 Struttura della cartella

```
src/
  games/
    plugins/
      NomeGioco/
        __init__.py
        game.py
        templates/
          index.html
```

- `__init__.py`: lasciarlo vuoto  
- `game.py`: contiene la logica Python del minigioco  
- `templates/index.html`: HTML del minigioco

### 🧠 Esempio di `game.py`

```python
from manager import games_manager as gm
from games.GamesManager import Game

class NomeGioco(Game):
    name = "NomeGioco"        # Nome del gioco (univoco)
    weight = 1                # Peso per la selezione casuale
    playerCount = 1           # Numero di giocatori da selezionare

    def play(self, lobby):
        with open(r"games/plugins/NomeGioco/templates/index.html", "rb") as f:
            content = f.read().decode("utf-8")
        return {
            "template": content,
            "options": {
                # Opzionale: variabili extra da passare al template
            }
        }

gm.registerGame(NomeGioco())
```

> Assicurati che il nome del gioco corrisponda in classe, path e filename (`NomeGioco` è case-sensitive).

---

## 🎨 Struttura dei Template

Ogni template HTML deve includere:

- `{% include "headGame.html" %}`: per caricare le librerie e gli script base
- `{% include "baseGame.html" %}`: per la logica WebSocket e interazione dell'host
- **Un pulsante con `id="next"`** visibile solo all'host, per passare manualmente al gioco successivo

Esempio:

```html
<button id="next" class="btn btn-primary">Avanti</button>
```


Ogni template HTML deve includere **due componenti fondamentali**:

```html
{% include "headGame.html" %}
{% include "baseGame.html" %}
```

### ✅ `headGame.html` include:

- Charset e viewport
- Librerie:
  - **jQuery**
  - **socket.io-client**
  - **TailwindCSS**

### ✅ `baseGame.html` include:

- Connessione al **WebSocket**
- Emissione di `"join_lobby"`
- Listener per `"reload"`
- Logica per l'host (`next → /api/game/next → /api/reload`)

---

## 🔧 Variabili Disponibili nel Template

I template Jinja2 ricevono automaticamente queste variabili:

| Variabile     | Descrizione                                                      |
|---------------|------------------------------------------------------------------|
| `players`     | Lista dei giocatori selezionati per il gioco                     |
| `lobbyCode`   | Codice della lobby                                               |
| `SOCKET_URL`  | URL del WebSocket                                                |
| `isHost`      | `True` se il giocatore corrente è l'host                         |
| `isSelected`  | `True` se il giocatore è tra i `players` selezionati             |
| `**options`   | Altre opzioni personalizzate restituite nel metodo `play()`      |

---

## 🥂 Contribuire

Contribuzioni aperte! Puoi inviare pull request con:

- Nuovi minigiochi
- Miglioramenti a UI/UX
- Fix o ottimizzazioni

Assicurati che ogni gioco:

- Funzioni correttamente
- Rispetti la struttura plugin
- Sia tematicamente coerente (divertente, alcolico, sociale)

---

## 📄 Licenza

```
MIT License

Copyright (c) 2025 ThePlayer372-FR

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
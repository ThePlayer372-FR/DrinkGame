# 🍻 DrinkGame

**DrinkGame** è un gioco alcolico web-based modulare scritto in Python con Flask, pensato per animare le serate con gli amici. Grazie al sistema a plugin, puoi facilmente creare e aggiungere nuovi minigiochi personalizzati.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Caratteristiche

- 🎮 **Sistema a Plugin**: aggiungi facilmente nuovi minigiochi
- 🌐 **Multiplayer Real-time**: comunicazione in tempo reale con WebSocket
- 🎲 **Selezione Casuale Pesata**: i giochi vengono scelti in base al peso configurato
- 👥 **Sistema di Lobby**: crea e unisciti a stanze di gioco private
- 🎯 **Selezione Intelligente dei Giocatori**: algoritmo che bilancia la partecipazione
- 🐳 **Docker Ready**: deploy rapido con Docker Compose
- 📱 **Responsive Design**: giocabile su mobile e desktop

---

## 🚀 Deploy Locale

### Con Docker (Raccomandato)

```bash
git clone https://github.com/ThePlayer372-FR/DrinkGame.git
cd DrinkGame
docker compose up
```

Il gioco sarà disponibile su: [http://localhost:5000](http://localhost:5000)

### Senza Docker

```bash
git clone https://github.com/ThePlayer372-FR/DrinkGame.git
cd DrinkGame
pip install -r req.txt
cd src
python app.py
```

---

## 🎮 Come Giocare

1. **Crea una Lobby**: visita la homepage e crea una nuova stanza
2. **Condividi il Codice**: condividi il codice della lobby con i tuoi amici
3. **Unisciti alla Lobby**: inserisci il codice e il tuo nome
4. **L'Host Avvia**: il primo giocatore che entra diventa host e può avviare il gioco
5. **Gioca**: segui le istruzioni dei minigiochi che appaiono casualmente
6. **Continua**: l'host può passare al gioco successivo con il pulsante "Avanti"

---

## 🧩 Come Aggiungere un Nuovo Minigioco

Ogni minigioco è un plugin indipendente collocato in `src/games/plugins/NomeGioco/`.

### 📁 Struttura della Cartella

```
src/
  games/
    plugins/
      NomeGioco/
        __init__.py           # File vuoto
        game.py               # Logica del gioco
        templates/
          index.html          # Template HTML del gioco
        [assets opzionali]    # JSON, immagini, etc.
```

### 🧠 Esempio di `game.py`

```python
"""Nome Gioco plugin."""
import os
from typing import Dict, Any

from manager import games_manager
from games.GamesManager import Game
from lobby.lobby import Lobby


class NomeGiocoGame(Game):
    """Descrizione del tuo gioco."""
    
    name = "NomeGioco"          # Nome univoco del gioco
    weight = 1.0                # Peso per la selezione (0.0 - 1.0+)
    playerCount = 1             # Numero di giocatori da selezionare

    def play(self, lobby: Lobby) -> Dict[str, Any]:
        """Esegui la logica del gioco.
        
        Args:
            lobby: L'istanza della lobby
            
        Returns:
            Dictionary con 'template' e 'options'
        """
        # Carica il template HTML
        template_path = os.path.join(
            os.path.dirname(__file__),
            "templates",
            "index.html"
        )
        
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # Puoi usare lobby.get_seed() per randomness consistente
        # Puoi usare lobby.get_tmp_value() per salvare stato tra round
        
        return {
            "template": template,
            "options": {
                # Variabili personalizzate da passare al template
                "custom_var": "valore"
            }
        }


# Registra il gioco
games_manager.register_game(NomeGiocoGame())
```

### 🎯 Best Practices per i Plugin

1. **Naming Convention**: usa PascalCase per le classi (es. `TruthLiesGame`)
2. **File Paths**: usa sempre `os.path.join()` per compatibilità cross-platform
3. **Encoding**: specifica sempre `encoding="utf-8"` quando leggi file
4. **Type Hints**: aggiungi type hints per migliore documentazione
5. **Docstrings**: documenta la classe e il metodo `play()`
6. **Error Handling**: gestisci le eccezioni (specialmente per API esterne)
7. **Peso Ragionevole**: usa pesi tra 0.1 (raro) e 1.0 (comune)

---

## 🎨 Struttura dei Template

### Componenti Obbligatori

Ogni template HTML deve includere:

```html
<!DOCTYPE html>
<html>
<head>
    {% include "headGame.html" %}
    <title>Nome Gioco</title>
</head>
<body>
    <!-- Il tuo contenuto qui -->
    
    {% include "baseGame.html" %}
</body>
</html>
```

### ✅ `headGame.html` Include

- Meta tag (charset, viewport)
- **jQuery** 3.6+
- **Socket.IO Client**
- **TailwindCSS** (styling)

### ✅ `baseGame.html` Include

- Connessione WebSocket automatica
- Join automatico alla lobby room
- Listener per eventi `reload`
- Pulsante "Avanti" per l'host (con `id="next"`)
- Logica di navigazione tra giochi

### 🔧 Variabili Disponibili nel Template

I template Jinja2 ricevono automaticamente queste variabili:

| Variabile     | Tipo           | Descrizione                                           |
|---------------|----------------|-------------------------------------------------------|
| `players`     | `list[str]`    | Lista dei giocatori selezionati per questo gioco      |
| `lobbyCode`   | `str`          | Codice identificativo della lobby                     |
| `SOCKET_URL`  | `str`          | URL del server WebSocket                              |
| `isHost`      | `bool`         | `True` se il giocatore corrente è l'host              |
| `isSelected`  | `bool`         | `True` se il giocatore è tra quelli selezionati       |
| `**options`   | `dict`         | Opzioni personalizzate dal metodo `play()`            |

### 📝 Esempio Template Completo

```html
<!DOCTYPE html>
<html>
<head>
    {% include "headGame.html" %}
    <title>Il Mio Gioco</title>
</head>
<body class="bg-gray-900 text-white min-h-screen flex items-center justify-center">
    <div class="container mx-auto p-4 text-center">
        <h1 class="text-4xl font-bold mb-8">🎮 Il Mio Gioco</h1>
        
        {% if isSelected %}
            <div class="bg-yellow-600 p-6 rounded-lg mb-4">
                <p class="text-2xl">Sei stato selezionato!</p>
                <p class="mt-4">{{ custom_var }}</p>
            </div>
        {% else %}
            <div class="bg-gray-700 p-6 rounded-lg mb-4">
                <p class="text-xl">Guarda gli altri giocatori!</p>
            </div>
        {% endif %}
        
        <div class="mt-8">
            <p class="text-lg">Giocatori: {{ players|join(', ') }}</p>
        </div>
    </div>
    
    {% include "baseGame.html" %}
</body>
</html>
```

---

## 🔧 Configurazione

### Variabili d'Ambiente

Puoi configurare l'applicazione tramite variabili d'ambiente:

| Variabile             | Default                          | Descrizione                           |
|-----------------------|----------------------------------|---------------------------------------|
| `DEBUG`               | `1` (True)                       | Abilita/disabilita modalità debug     |
| `INACTIVE_LOBBY_TIME` | `3600` (1 ora)                   | Timeout per lobby inattive (secondi)  |
| `CODE_LEN`            | `5`                              | Lunghezza codice lobby                |
| `WEB_SOCKET_URL`      | `http://192.168.91.200:5000/`    | URL del server WebSocket              |

Esempio con Docker Compose:

```yaml
environment:
  - DEBUG=0
  - CODE_LEN=6
  - WEB_SOCKET_URL=http://localhost:5000/
```

---

## 🏗️ Architettura

```
src/
├── app.py                  # Applicazione Flask principale
├── api.py                  # Endpoint API REST
├── socket_handlers.py      # Handler WebSocket
├── manager.py              # Istanze singleton dei manager
├── config.py               # Configurazione applicazione
├── utils.py                # Funzioni utility
├── extensions.py           # Estensioni Flask (SocketIO)
├── games/
│   ├── GamesManager.py     # Manager e base class per giochi
│   └── plugins/            # Directory dei plugin giochi
├── lobby/
│   ├── lobby.py            # Classe Lobby
│   └── lobbymanager.py     # Manager delle lobby
└── templates/              # Template HTML base
```

### Pattern Architetturali

- **Singleton Pattern**: `GamesManager` e `LobbyManager`
- **Plugin Architecture**: caricamento dinamico dei giochi
- **Abstract Base Class**: `Game` come interfaccia per i plugin
- **WebSocket Real-time**: comunicazione bidirezionale con Socket.IO

---

## 🎲 Giochi Inclusi

1. **Cards** 🃏 - Pesca una carta con un'azione da compiere
2. **Challenge** ⚔️ - Sfida tra due giocatori
3. **Count** 🔢 - Gioco di conteggio collaborativo
4. **I Know** 🧠 - Domande e risposte
5. **Impostor** 🕵️ - Trova l'impostore con parole diverse
6. **Truth or Lies** 🤥 - Indovina verità o bugie

---

## 🥂 Contribuire

Le contribuzioni sono benvenute! Puoi contribuire con:

- 🎮 **Nuovi minigiochi**: crea plugin per nuovi giochi divertenti
- 🐛 **Bug fix**: segnala o risolvi bug
- ✨ **Miglioramenti UI/UX**: rendi l'esperienza più piacevole
- 📚 **Documentazione**: migliora guide e commenti
- ⚡ **Ottimizzazioni**: performance e qualità del codice

### Linee Guida

1. Fai fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Segui le convenzioni PEP 8 per Python
4. Aggiungi type hints e docstrings
5. Testa le tue modifiche
6. Commit con messaggi descrittivi (`git commit -m 'Add: nuovo gioco XYZ'`)
7. Push al branch (`git push origin feature/AmazingFeature`)
8. Apri una Pull Request

### Checklist per Nuovi Giochi

- [ ] Segue la struttura plugin standard
- [ ] Include docstrings e type hints
- [ ] Template HTML responsive e accessibile
- [ ] Testato con diversi numeri di giocatori
- [ ] Tematicamente appropriato e divertente
- [ ] Path dei file cross-platform (`os.path.join()`)

---

## 🐛 Troubleshooting

### Il gioco non si avvia

```bash
# Verifica le dipendenze
pip install -r req.txt

# Verifica la porta
lsof -i :5000
```

### Errori di connessione WebSocket

- Verifica che `WEB_SOCKET_URL` sia configurato correttamente
- Controlla che non ci siano firewall che bloccano la porta

### Plugin non caricato

- Verifica che la struttura della cartella sia corretta
- Controlla i log per errori di importazione
- Assicurati che il metodo `play()` restituisca il formato corretto

---

## 📖 Documentazione Tecnica

Per maggiori dettagli sul refactoring e l'architettura interna, consulta:
- [REFACTORING_SUMMARY.md](./REFACTORING_SUMMARY.md) - Dettagli sul refactoring del codice

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
# Avionașele - Multiplayer Game in Python

This project is a multiplayer implementation of the classic "Airplanes" game (`Avionașele`) developed in Python. It uses socket programming to allow multiple players to connect to a central server and attempt to shoot down airplanes placed on a hidden 10x10 grid.

---

## 📋 Game Description

- The server loads a random configuration from a set of predefined `.txt` files in the `configuratii/` directory.
- Each configuration contains exactly 3 airplanes, marked on a 10x10 matrix.
- The airplanes are represented using the following characters:
  - `A`, `B`, `C` – the **head** of each plane (must be hit to destroy the plane)
  - `1`, `2`, `3` – wings, body, and tail of the planes
  - `0` – empty cell


---

## 🔁 Game Rules

- Clients connect to the server and provide a **unique player name**.
- The player sends coordinates (row and column) to shoot at positions on the grid.
- The server responds with:
  - `"0"` — if no part of a plane was hit
  - `"1"` — if a non-head part was hit
  - `"X"` — if the **head** of a plane was hit (plane destroyed)
- When all 3 heads are hit, the player wins the round.
- The server announces the winner to all players and automatically loads a new board to start a new round.

---

## 🧠 How It Works

### Server
- Starts a socket server on `127.0.0.1:12345`
- Loads a random board from the `configuratii/` directory
- Accepts multiple client connections via threads
- Manages:
  - Name uniqueness
  - Turn input
  - Board state and victory condition
  - Broadcasting results and restart messages

### Client
- Connects to the server using a TCP socket
- Sends:
  - A unique name at the beginning
  - Shooting coordinates (e.g., `4 7`)
  - `"exit"` to leave the game
- Receives responses and game state updates from the server





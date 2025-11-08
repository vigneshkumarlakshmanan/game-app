import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API = 'http://localhost:5000'; // backend API endpoint

export default function App() {
  const [gameId, setGameId] = useState(null);
  const [board, setBoard] = useState('---------');
  const [player, setPlayer] = useState('X');
  const [status, setStatus] = useState('waiting');

  async function createGame() {
    try {
      const res = await axios.post(`${API}/games`);
      setGameId(res.data.id);
      setPlayer('X');
      setStatus('playing');
      await fetchGame(res.data.id);
    } catch (e) {
      console.error(e);
    }
  }

  async function joinGame() {
    const id = prompt('Enter Game ID to join:');
    if (!id) return;
    setGameId(id);
    setPlayer('O');
    setStatus('playing');
    await fetchGame(id);
  }

  async function fetchGame(idParam) {
    const id = idParam || gameId;
    if (!id) return;
    try {
      const res = await axios.get(`${API}/games/${id}`);
      setBoard(res.data.board);
      setStatus(res.data.status);
    } catch (e) {
      console.error(e);
    }
  }

  async function makeMove(i) {
    if (!gameId) return alert('Create or join a game first');
    try {
      const res = await axios.post(`${API}/games/${gameId}/move`, { pos: i, player });
      if (res.data.error) return alert(res.data.error);
      setBoard(res.data.board);
      setStatus(res.data.status);
      if (res.data.winner) alert('Winner: ' + res.data.winner);
    } catch (e) {
      console.error(e);
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h1>Tic-Tac-Toe Online</h1>

      <div style={{ marginBottom: 10 }}>
        <button onClick={createGame}>Create Game</button>
        <button onClick={joinGame} style={{ marginLeft: 8 }}>
          Join Game
        </button>
        <button onClick={() => fetchGame()} style={{ marginLeft: 8 }}>
          Refresh
        </button>
      </div>

      <div>Game ID: {gameId || '-'}</div>
      <div>Player: {player}</div>
      <div>Status: {status}</div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 60px)',
          gap: 5,
          marginTop: 10,
        }}
      >
        {board.split('').map((c, i) => (
          <Cell key={i} value={c} onClick={() => makeMove(i)} />
        ))}
      </div>
    </div>
  );
}

// Simple Cell Component
function Cell({ value, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        width: 60,
        height: 60,
        fontSize: 24,
        textAlign: 'center',
        cursor: 'pointer',
      }}
    >
      {value !== '-' ? value : ''}
    </button>
  );
}

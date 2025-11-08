CREATE DATABASE IF NOT EXISTS tictactoe;
USE tictactoe;

CREATE TABLE IF NOT EXISTS games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    board VARCHAR(9) NOT NULL DEFAULT '---------',
    current_player CHAR(1) NOT NULL DEFAULT 'X',
    status VARCHAR(20) NOT NULL DEFAULT 'waiting',
    player_x VARCHAR(64),
    player_o VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


from flask import Flask, request, jsonify

return jsonify({'joined': True})


@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    with engine.connect() as conn:
        row = conn.execute(select(games).where(games.c.id == game_id)).first()
        if not row:
            return jsonify({'error': 'not found'}), 404
        return jsonify({
            'id': row.id,
            'board': row.board,
            'current_player': row.current_player,
            'status': row.status,
            'player_x': row.player_x,
            'player_o': row.player_o
        })


@app.route('/games/<int:game_id>/move', methods=['POST'])
def make_move(game_id):
    data = request.json or {}
    pos = data.get('pos')
    player = data.get('player')

    if pos is None or player is None:
        return jsonify({'error': 'pos and player required'}), 400

    pos = int(pos)
    if pos < 0 or pos > 8:
        return jsonify({'error': 'invalid pos'}), 400

    with engine.begin() as conn:
        row = conn.execute(select(games).where(games.c.id == game_id)).first()
        if not row:
            return jsonify({'error': 'not found'}), 404

        if row.status not in ('playing', 'waiting'):
            return jsonify({'error': 'game finished'}), 400

        board = list(row.board)
        if board[pos] != '-':
            return jsonify({'error': 'cell taken'}), 400

        # check whose turn
        if row.current_player != player:
            return jsonify({'error': 'not your turn'}), 400

        board[pos] = player
        board_str = ''.join(board)
        winner = check_winner(board_str)

        if winner in ('X', 'O'):
            status = 'finished'
        elif winner == 'draw':
            status = 'draw'
        else:
            status = 'playing'

        next_player = 'O' if player == 'X' else 'X'

        conn.execute(
            text('UPDATE games SET board=:b, current_player=:c, status=:s WHERE id=:id'),
            {'b': board_str, 'c': next_player, 's': status, 'id': game_id}
        )

    return jsonify({'board': board_str, 'status': status, 'winner': winner})


if __name__ == '__main__':
    # create tables if not exists (safe for first run)
    metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000)

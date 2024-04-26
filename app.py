from flask import Flask, request,jsonify,render_template,redirect,url_for
app = Flask(__name__)

players = []

@app.route('/')
def index():
    return render_template('index.html', players=players)

@app.route('/players', methods=['POST'])
def create_player():
    player = {
        'name': request.form['name'],
        'position': request.form['position'],
        'team': request.form['team']
    }
    players.append(player)
    return redirect(url_for('index'))


@app.route('/players', methods=['GET'])
def get_players():
    return jsonify({'players': players}),202


@app.route('/players/<int:index>', methods=['PUT'])
def update_player(index):
    if index < len(players):
        players[index] = {
            'name': request.form.get('name', players[index]['name']),
            'position': request.form.get('position', players[index]['position']),
            'team': request.form.get('team', players[index]['team'])
        }
        return render_template('index.html', players=players)
    return 'Player not found', 404

@app.route('/players/<int:index>', methods=['DELETE'])
def delete_player(index):
    if index < len(players):
        del players[index]
        return jsonify({'players': players})
    return 'Player not found', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
from flask import Flask, request, jsonify
from collections import defaultdict

app = Flask(__name__)


class BalancedCardTradingOptimizer:
    def __init__(self, friends):
        self.friends = friends

    def optimize_trades(self):
        needs_card = defaultdict(set)
        has_card = defaultdict(set)

        for i, friend in enumerate(self.friends):
            for card in friend["missing"]:
                needs_card[card].add(i)
            for card in friend["doubles"]:
                has_card[card].add(i)

        trades = []
        swaps_count = [0] * len(self.friends)

        for card, needy_friends in needs_card.items():
            givers = has_card[card]
            while needy_friends and givers:
                giver = min(givers, key=lambda x: swaps_count[x])
                needy = min(needy_friends, key=lambda x: swaps_count[x])

                trades.append((giver, needy, card))
                swaps_count[giver] += 1
                swaps_count[needy] += 1

                self.friends[giver]["doubles"].remove(card)
                self.friends[needy]["missing"].remove(card)

                givers.remove(giver)
                needy_friends.remove(needy)
                has_card[card].discard(giver)
                needs_card[card].discard(needy)

        total_missing = [friend["missing"] for friend in self.friends]
        return trades, swaps_count, total_missing

@app.route('/', methods=['POST'])
def optimize_trades():
    data = request.json.get('players', [])
    names = request.json.get('names', {})

    optimizer = BalancedCardTradingOptimizer(data)
    trades, swaps_count, total_missing = optimizer.optimize_trades()

    result = {
        "trades": [{"giver": names[t[0]], "receiver": names[t[1]], "card": t[2]} for t in trades],
        "missing_after_trades": [{"name": names[i], "missing": missing} for i, missing in enumerate(total_missing)],
        "swap_counts": {names[i]: swaps_count[i] for i in range(len(swaps_count))}
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

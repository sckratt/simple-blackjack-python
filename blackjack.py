from asyncio.windows_events import NULL
import random
import math

deck = []

def beatify_hand(player):
    cards = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi"]
    return ", ".join([cards[card - 1] for card in player["deck"]])
def shuffle():
    global deck
    random.shuffle(deck)
def hit():
    global deck
    return deck.pop()
def initialize_player():
    player = {
        "deck": [hit() for i in range(2)],
        "money": 100,
        "bet": 0
    }
    return player
def initialize():
    global deck
    deck = [i for i in range(1, 14)]*4
    shuffle()
    player = initialize_player()
    dealer = initialize_player()
    return player, dealer
def hand_value(player):
    value = 0
    for card in player["deck"]:
        value += card
    return value
def has_blackjack(player):
    return hand_value(player) == 21
def has_busted(player):
    return hand_value(player) > 21
def dealer_turn(dealer, player):
    while hand_value(dealer) < hand_value(player):
        dealer["deck"].append(hit())
    return dealer
def round_end(player, dealer):
    dealer = dealer_turn(dealer, player)
    if(round_check(player) == "blackjack"):
        if round_check(dealer) == "blackjack":
            return "egality"
        else: return "player"
    if(round_check(player) == "busted"):
        return "dealer"
    if(round_check(player) == "playing"):
        if(round_check(dealer) == "busted"): return "player"
        if(round_check(dealer) == "blackjack"): return "dealer"
        if(hand_value(player) > hand_value(dealer)): return "player"
        if(hand_value(player) < hand_value(dealer)): return "dealer"
        return "egality"
def round_check(player):
    if(has_blackjack(player)): return "blackjack"
    if(has_busted(player)): return "busted"
    return "playing"
def player_turn(player, dealer):
    result = round_check(player)
    if(result == "blackjack" or result == "busted"): return result
    
    while True:
        sentences = [
            "Votre main: {} ({})".format(beatify_hand(player), hand_value(player)),
            "Votre mise: {}".format(player["bet"]),
            "1. Tirer une carte",
            "2. Passer",
            "3. Split",
            "4. Double" 
        ]
        for sentence in sentences: print(sentence)
        choice = int(input("Votre choix: "))
        if choice == 1:
            player["deck"].append(hit())
            if(round_check(player) == "busted"): return "busted"
            if(round_check(player) == "blackjack"): return "blackjack"
            return player_turn(player, dealer)
        elif choice == 2:
            return round_end(player, dealer)
        elif choice == 3:
            player["deck"].append(hit())
            player["money"] += math.ceil(player["bet"]/2)
            player["bet"] -= math.floor(player["bet"]/2)
            return player_turn(player, dealer)
        elif choice == 4:
            player["money"] -= player["bet"]
            player["bet"] *= 2
            player["deck"].append(hit())
            return player_turn(player, dealer)
def start(player, money_start):
    if not player:
        player, dealer = initialize()
        player["money"] = money_start
    else: _, dealer = initialize()

    bet = math.inf
    while bet > player["money"] or bet <= 0:
        bet = int(input("Votre mise: "))
        player["bet"] = bet
    result = player_turn(player, dealer)
    
    if(result == "blackjack"):
        print("Blackjack!")
        player["money"] += player["bet"]*2
    elif(result == "busted"):
        print("Vous avez perdu {}$ (deck: {}, dealer: {})".format(player["bet"], hand_value(player), hand_value(dealer)))
        player["money"] -= player["bet"]
    elif(result == "egality"):
        print("Egalité! (deck: {}, dealer: {})".format(hand_value(player), hand_value(dealer)))
    elif(result == "player"):
        print("Vous avez gagné {}$ (deck: {}, dealer: {})".format(player["bet"], hand_value(player), hand_value(dealer)))
        player["money"] += player["bet"]
    elif(result == "dealer"):
        print("Vous avez perdu {}$ (deck: {}, dealer: {})".format(player["bet"], hand_value(player), hand_value(dealer)))
        player["money"] -= player["bet"]
    else:
        print("Erreur")
    print("Vous avez {}$".format(player["money"]))
    player["deck"] = [hit() for i in range(2)]

    print("\n<------------->\n")

    if(player["money"] > 0):
        start(player, NULL)
def init():
    start_money = int(input("Votre argent: "))
    start(NULL, start_money)

init()
from flask import Blueprint, render_template, g, session
from flask_socketio import emit

from .auth import login_required
from .db import get_db

from .poker import Poker
from . import socketio

bp = Blueprint("play", __name__)
poker = Poker()


@bp.route("/")
@login_required
def index():
    return render_template("index.html")


@socketio.on("connect")
def test_connect():
    emit("message", {"msg": "Verified connection!"})


@socketio.on("new_hand")
def new_hand():
    # starts a new hand
    db = get_db()
    poker.deal()

    # insert new session into table during first hand
    if poker.hand_num == 1:
        user_id = session.get("user_id")
        cursor = db.cursor()
        cursor.execute("INSERT INTO session (user_id) VALUES (?)", (user_id,))
        session["id"] = cursor.lastrowid
        db.commit()

    cards = poker.you.hand.to_list()
    turn = "computer" if poker.turn == 1 else "player"
    emit(
        "new_hand",
        {
            "cards": cards,
            "hand_num": poker.hand_num,
            "turn": turn,
        },
    )
    if poker.turn == 0:
        get_user_choices("")
    else:
        get_computer_action()


@socketio.on("user_action")
def user_action(choice):
    # receives the user action
    bet = poker.choices[choice]
    poker.update_hand(choice, bet)
    if poker.both_played:
        get_next(choice)
    else:
        get_computer_action()


@socketio.on("get_user_choices")
def get_user_choices(choice):
    # gets the possible choices and bet sizes for the user
    if poker.both_played:
        get_next(choice)
    else:
        poker.get_choices()
        emit(
            "update_user_choices",
            {
                "choices": poker.choices,
            },
        )
        update_bets()


@socketio.on("get_computer_action")
def get_computer_action():
    # get the computer's decision
    poker.get_choices()
    output, choice, bet = poker.bot.make_choice(poker)
    poker.update_hand(choice, bet)
    emit(
        "computer_action",
        {
            "output": output,
            "choice": choice,
        },
    )
    update_bets()


def get_next(choice):
    # Determine wither hand or round is over
    if choice == "fold":
        winner_string = poker.determine_winner(choice)
        emit(
            "winner_fold",
            {
                "winner_string": winner_string,
            },
        )
        insert_hand()
    elif poker.round == 4:
        winner_string = poker.determine_winner(choice)
        cards = poker.bot.hand.to_list()
        emit(
            "winner_show",
            {
                "winner_string": winner_string,
                "choice": choice,
                "cards": cards,
            },
        )
        insert_hand()
    else:
        poker.increment_round()
        if poker.round == 2:
            community_cards = poker.community[:3]
        elif poker.round == 3:
            community_cards = poker.community[3:4]
        else:
            community_cards = poker.community[4:]

        community_cards = [card.to_dict() for card in community_cards]
        emit(
            "new_round",
            {
                "cards": community_cards,
                "turn": poker.turn,
                "round": poker.round,
            },
        )
    update_bets()


def update_bets():
    # called at the end of a user or computer action to update all bets on screen
    emit(
        "update_bets",
        {
            "pot": poker.pot,
            "player_bet": poker.you.bet,
            "computer_bet": poker.bot.bet,
            "player_chips": poker.you.money,
            "computer_chips": poker.bot.money,
        },
    )


def insert_hand():
    # insert hand into database
    db = get_db()
    if poker.winner == "tie":
        winner = -1
        amount_won = 0
        start_money = poker.dealer.start_money
    else:
        winner = poker.winner.id
        amount_won = poker.winner.money - poker.winner.start_money
        start_money = poker.winner.start_money

    user_cards = [str(card) for card in poker.players[0].hand]
    computer_cards = [str(card) for card in poker.players[1].hand]
    community_cards = [str(card) for card in poker.community]

    values = (
        session["id"],
        poker.hand_num,
        poker.dealer.id,
        winner,
        amount_won,
        start_money,
        *user_cards,
        *computer_cards,
        *community_cards,
    )
    db.execute(
        """INSERT INTO hand (session_id, hand_num, dealer, winner, amount_won, start_money, 
                             user_card1, user_card2, computer_card1, computer_card2, 
                             community_card1, community_card2, community_card3, community_card4, 
                             community_card5) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        values,
    )
    db.commit()

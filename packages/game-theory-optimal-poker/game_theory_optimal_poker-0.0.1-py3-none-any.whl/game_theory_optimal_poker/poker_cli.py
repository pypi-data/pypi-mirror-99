import random
import bisect
from collections import Counter, defaultdict

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

# Each suit is two character unicode of ♠️, ♣️, ♥️, ♦️
SUITS = ["\u2660\uFE0F", "\u2663\uFE0F", "\u2665\uFE0F", "\u2666\uFE0F"]
SCORES = [
    "High Card {}, {} kicker",
    "One Pair {}'s, {} kicker",
    "Two Pair {}'s and {}'s, {} kicker",
    "Three of a Kind {}'s, {} kicker",
    "Straight {} high",
    "Flush {} high",
    "Full House {}'s full of {}'s",
    "Four of a Kind {}'s, {} kicker",
    "Straight Flush {} high",
]


class Card:
    """
    Class to represent a single card from a 52 card deck

    Parameters
    ----------
    num : int between 0 and 51

    Attributes
    ----------
    rank : int between 0 and 12 representing '2' through 'A'

    suit : int between 0 and 3 representing ♠️, ♣️, ♥️, ♦️
    """

    def __init__(self, num):
        self.rank = num % 13
        self.suit = num // 13

    def __repr__(self):
        # String representation of card
        return f"{RANKS[self.rank]}{SUITS[self.suit]}"

    def __eq__(self, other):
        # Tests equality of two Card objects
        # Must return a boolean
        # Used in testing
        if not isinstance(other, Card):
            raise TypeError(f"Other object must be of type Card not {type(other)}")
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        # Must return an integer.
        # We create a tuple (which is hashable) from rank and suit,
        # and return its hash value.
        # Alternatively, we could have just calculated its 0-51 number and returned that
        t = self.rank, self.suit
        return hash(t)


class HandMixin:
    def __getitem__(self, key):
        # Select one or more cards with []. Allows for iteration
        # Returns a list of card objects
        return self.cards[key]

    def __len__(self):
        # get number of cards in deck/hand
        return len(self.cards)

    def __repr__(self):
        # Entire deck/hand made into string of cards separated by 2 spaces
        return "  ".join(str(card) for card in self)

    def __eq__(self, other):
        # Test equality of each card in deck/hand
        if len(self) != len(other):
            return False
        return all(card1 == card2 for card1, card2 in zip(self, other))


class Deck(HandMixin):
    """
    Class containing 52 Card objects in a list
    """

    def __init__(self):
        # attribute cards is a list of 52 Card objects
        self.cards = [Card(i) for i in range(52)]

    def shuffle(self):
        # shuffle deck with random.shuffle function
        # self.cards is a list and shuffle happens in place
        random.shuffle(self.cards)


class Hand(HandMixin):
    """
    Class for player/bot hand or community cards

    Parameters
    ----------
    cards : list of Card objects
    """

    def __init__(self, cards):
        self.cards = cards

    def __add__(self, other):
        if not isinstance(other, Hand):
            raise TypeError(f"Other object must be of type Hand not {type(other)}")
        return Hand(self.cards + other.cards)


class Evaluator:
    def __init__(self, hand):
        self.hand = hand
        self.ranks = [card.rank for card in hand.cards]
        self.suits = [card.suit for card in hand.cards]
        self.ranks_count = Counter(self.ranks)
        self.suits_count = Counter(self.suits)
        self.ranks_sorted = sorted(self.ranks_count)
        self.count_ranks_dict = self.get_count_ranks_dict()
        self.score = self.evaluate()

    def get_count_ranks_dict(self):
        d = defaultdict(list)
        for rank, count in self.ranks_count.items():
            bisect.insort(d[count], rank)
        return d

    def check_flush(self):
        for suit, count in self.suits_count.items():
            if count >= 5:
                return suit
        return -1

    def check_straight(self, ranks):
        # ranks is a unique sorted list
        n = len(ranks)
        if n < 5:
            return -1

        # ranks must be 4 indexes apart with a value difference of 4
        for i in range(1, n - 3):
            if ranks[-i] == ranks[-i - 4] + 4:
                return ranks[-i]

        # check for 5 high straight (Ace low)
        if ranks[3] == 3 and ranks[-1] == 12:
            return 3
        return -1

    def check_straight_flush(self, flush_suit):
        if flush_suit == -1:
            return -1
        flush_ranks = [r for r, s in zip(self.ranks, self.suits) if s == flush_suit]
        return self.check_straight(flush_ranks)

    def evaluate(self):
        flush_suit = self.check_flush()
        straight_flush_rank = self.check_straight_flush(flush_suit)
        if straight_flush_rank != -1:
            return 8, straight_flush_rank

        ranks4 = self.count_ranks_dict[4]
        ranks3 = self.count_ranks_dict[3]
        ranks2 = self.count_ranks_dict[2]
        ranks1 = self.count_ranks_dict[1]
        n3 = len(ranks3)
        n2 = len(ranks2)

        # four of a kind
        if ranks4:
            kicker = max(ranks3 + ranks2 + ranks1)
            return 7, ranks4[-1], kicker

        # full house
        if n3 == 2:
            return 6, ranks3[-1], ranks3[-2]
        if n3 == 1 and n2 >= 1:
            return 6, ranks3[-1], ranks2[-1]

        # flush
        if flush_suit != -1:
            return 5, flush_suit

        # straight
        straight_rank = self.check_straight(self.ranks_sorted)
        if straight_rank != -1:
            return 4, straight_rank

        # three of a kind
        if n3 == 1:
            return 3, ranks3[-1], ranks1[-1], ranks1[-2]

        # two-pair
        if n2 >= 2:
            return 2, ranks2[-1], ranks2[-2], max(ranks2[:-2] + ranks1)

        # one pair
        if n2 == 1:
            return 1, ranks2[-1], ranks1[-3], ranks1[-2], ranks1[-1]

        # high card
        return 0, ranks1[-5], ranks1[-4], ranks1[-3], ranks1[-2], ranks1[-1]

    def __repr__(self):
        score, *others = self.score
        rank_chars = [RANKS[o] for o in others]
        return SCORES[score].format(*rank_chars)


def verify_input(phrase, choices):
    first_letters = tuple(choice[0] for choice in choices)
    while True:
        user_choice = input(phrase).lower()
        if user_choice in first_letters:
            for choice, bet in choices.items():
                if choice[0] == user_choice:
                    return choice, bet
        print(f"Choice must be one of {first_letters}")


def print_slow(output, delay=0.04):
    import time

    for i in output:
        print(i, end="", flush=True)
        time.sleep(delay)
    print()


MAX_ROUNDS = 4
MAX_BET_ROUNDS = 4
BLINDS = 5, 10


class Player:
    def __init__(self, name, money=1000):
        self.name = name
        self.money = money
        self.hand = None
        self.bet = None
        self.played = False
        self.evaluator = None


class Bot(Player):
    def make_choice(self, choices):
        items = list(choices.items())
        choice, bet = random.choice(items)
        if "bet" in choices:
            choice = "bet"
            bet = choices["bet"]
        if "raise" in choices:
            choice = "raise"
            bet = choices["raise"]
        extra = "to " if choice == "raise" else ""
        output = f"{self.name} {choice}s"

        if choice == "raise":
            output += f" to {bet}"
        elif choice in ("call", "bet"):
            output += f" {bet}"

        output += "\n"
        print_slow(output, 0.07)
        return choice, bet

    @property
    def winner_string(self):
        s = f"{self.name} wins"
        if self.evaluator:
            s = f"{s} with {self.evaluator}"
        return s
        # rand = random.random()
        # if self.bet == you.bet:
        #     if round_num == 1:
        #         choice = 'raise' if rand > .8 else 'check'
        #     else:
        #         choice = 'bet' if rand > .8 else 'check'
        # elif bet_round == 4:
        #     choice = 'call' if rand > .8 else 'fold'
        # else:
        #     if rand > .6:
        #         choice = 'raise'
        #     elif rand > .3:
        #         choice = 'call'
        #     else:
        #         choice = 'fold'

        # return choice


class You(Player):
    def make_choice(self, choices):
        phrase = ""
        for i, (choice, bet) in enumerate(choices.items()):
            phrase += choice.capitalize()
            if bet > 0:
                if choice == "raise":
                    phrase += f" to {bet}"
                else:
                    phrase += f" {bet}"

            if i == 0:
                if len(choices) == 2:
                    phrase += " or "
                else:
                    phrase += ", "
            elif i == 1 and len(choices) == 3:
                phrase += ", "

        phrase += "? "
        choice, bet = verify_input(phrase, choices)
        output = f"{self.name} {choice}"
        if choice == "raise":
            output += f" to {bet}"
        elif choice in ("call", "bet"):
            output += f" {bet}"
        output += "\n"
        print_slow(output)
        return choice, bet

    @property
    def winner_string(self):
        s = f"{self.name} win"
        if self.evaluator:
            s = f"{s} with {self.evaluator}"
        return s


class Poker:
    def __init__(self):
        self.hand_num = 0

        # instantiate deck and two players (human and computer)
        self.deck = Deck()
        self.you = You(name="You")
        self.bot = Bot(name="GTOP")

        # create tuple of players
        self.players = self.you, self.bot

        # play poker!
        self.play()

    def deal(self):
        """
        Beginning of a new hand
        Shuffle the cards, deal them out
        Reset the round, betting round, pot
        Switch dealers
        """
        # increase hand number
        self.hand_num += 1

        # There are 4 rounds - pre-flop, flop, turn, river
        self.round = 1

        # First round has forced blind bets, therefore bet_round
        # begins at 2. All other rounds have bet_round begin at 1
        self.bet_round = 2

        # In limit Texas Hold'em poker, the size of the bet is
        # limited to 1 * the blinds for rounds 1 and 2
        # and 2 times the blinds for rounds 3 and 4
        self.bet_multiplier = 1
        self.pot = 0

        self.deck.shuffle()
        self.set_dealer_player()

        self.pot = sum(BLINDS)

        print_slow(
            "\nNew Hand\n"
            f"Hand Number {self.hand_num}\n\n"
            f"Dealer - {self.current_player.name}\n"
            f"Blinds: {self.you.name} bet {self.you.bet}, {self.bot.name} bets {self.bot.bet}"
        )

    def set_dealer_player(self):
        """
        Sets the dealer/non-dealer, current turn, deals the hand
        gets the community cards, forces the blind bets
        Called within `deal` method

        """
        # The player who is NOT the dealer acts first each round except for the first round
        # first_turn alternates back and form between 1 and 0
        self.first_turn = self.hand_num % 2
        self.not_dealer = self.players[self.first_turn]
        self.dealer = self.players[1 - self.first_turn]

        # At the start of round 1, the dealer goes first
        # In all other rounds, the not_dealer goes first
        self.turn = 1 - self.first_turn

        self.not_dealer.hand = Hand(self.deck[:2])
        self.dealer.hand = Hand(self.deck[2:4])
        self.community = Hand(self.deck[4:9])
        self.not_dealer.bet = BLINDS[1]
        self.dealer.bet = BLINDS[0]
        self.not_dealer.money -= self.not_dealer.bet
        self.dealer.money -= self.dealer.bet
        self.dealer.played = self.not_dealer.played = False
        self.dealer.evaluator = self.not_dealer.evaluator = None

    @property
    def both_played(self):
        return all(player.played for player in self.players)

    @property
    def current_player(self):
        return self.players[self.turn]

    @property
    def other_player(self):
        return self.players[1 - self.turn]

    def print_money(self):
        print_slow(f"Your money ${self.you.money:,}", 0.01)
        print_slow(f"{self.bot.name} money ${self.bot.money:,}\n", 0.01)

    def print_round_start(self):
        print_slow(f"Round {self.round} - Pot: {self.pot}")
        self.print_money()
        print_slow(f"Your cards {self.you.hand}\n")

    def print_hand_end(self):
        self.print_money()
        input("\nPress any key to play the next hand")

    def play(self):
        while True:  # until one player loses all their money
            self.deal()
            self.print_round_start()
            while True:  # until the end of 1 hand
                while not self.both_played:  # until of one round
                    print_slow(f"bet round is {self.bet_round}")
                    choices = self.get_choices()
                    choice, bet = self.current_player.make_choice(choices)
                    self.update_hand(choice, bet)

                if self.round == 4 or choice == "fold":
                    break

                self.increment_round()
            self.determine_winner(choice)

    def get_choices(self):
        if self.dealer.bet == self.not_dealer.bet:
            if self.round == 1:
                choices = "check", "raise"
            else:
                choices = "check", "bet"
        elif self.bet_round == 5:
            choices = "fold", "call"
        else:
            choices = "fold", "call", "raise"

        return self.get_bet_values(choices)

    def get_bet_values(self, choices):
        def get_value(choice):
            if choice == "call":
                if self.round == 1 and self.bet_round == 2:
                    return BLINDS[0]
                else:
                    return BLINDS[1] * self.bet_multiplier
            elif choice in ("bet", "raise"):
                return BLINDS[1] * self.bet_multiplier * self.bet_round
            else:
                # check/fold
                return 0

        return {choice: get_value(choice) for choice in choices}

    def update_hand(self, choice, bet):
        self.current_player.played = True
        if choice in ("bet", "raise", "call"):
            increase = bet
            if choice != "call":
                self.other_player.played = False
                self.bet_round += 1
                increase -= self.current_player.bet
            self.current_player.bet += increase
            self.current_player.money -= increase
            self.pot += increase
        elif choice == "fold":
            self.other_player.played = True
            return  # do not update turn when player folds

        self.turn = 1 - self.turn

    def increment_round(self):
        """
        Move on to the next round
        Reset the bet_round to 1
        Set the player bets to 0
        Set the played status of each player to false
        Increment the bet multiplier to 2 if round 3 or 4
        """
        self.bet_round = 1
        self.round += 1
        if self.round == 3:
            self.bet_multiplier = 2

        # At the start of each round, not_dealer goes first
        self.turn = self.first_turn
        self.current_player.bet = self.other_player.bet = 0
        self.current_player.played = self.other_player.played = False
        self.print_round_start()
        print_slow(f"Community cards {self.community[:self.round + 1]}")

    def determine_winner(self, choice):
        if choice == "fold":
            winner = self.other_player
        else:
            # Bot shows cards when hand reaches a showdown
            print_slow(f"{self.bot.name} shows {self.bot.hand}\n")

            # evaluate each hand
            self.dealer.evaluator = Evaluator(self.dealer.hand + self.community)
            self.not_dealer.evaluator = Evaluator(self.not_dealer.hand + self.community)

            # determine winner
            if self.dealer.evaluator.score > self.not_dealer.evaluator.score:
                winner = self.dealer
            elif self.dealer.evaluator.score < self.not_dealer.evaluator.score:
                winner = self.not_dealer
            else:
                winner = "tie"
        self.finish_hand(winner)

    def finish_hand(self, winner):
        if winner == "tie":
            self.not_dealer.money += self.pot // 2
            self.dealer.money += self.pot // 2
        else:
            winner.money += self.pot
            print_slow(winner.winner_string)

        self.print_hand_end()


if __name__ == "__main__":
    Poker()

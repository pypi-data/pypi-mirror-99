import random
import bisect
from collections import Counter, defaultdict
from itertools import combinations
from statistics import median

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# Each suit is two character unicode of ♠️, ♣️, ♥️, ♦️
SPADES = "\u2660"
CLUBS = "\u2663"
HEARTS = "\u2665"
DIAMONDS = "\u2666"
BLACK_SUTIS = [SPADES, CLUBS]
RED_SUITS = [HEARTS, DIAMONDS]
SUITS = [*BLACK_SUTIS, *RED_SUITS]
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


def get_init_hand_ranking():
    hand_scores = {}
    for i in range(13):
        for j in range(i, 13):
            if i == j:
                hand_scores[(i, j, "p")] = (i + 10) ** 1.5
            else:
                score = (j + 5) ** 1.3 + (i + 5)
                if j - i == 1:
                    score *= 1.1
                elif j - i == 2:
                    score *= 1.05
                hand_scores[(j, i, "u")] = score
                hand_scores[(j, i, "s")] = score * 1.1

    hand_list = sorted(hand_scores, key=lambda x: hand_scores[x])
    n = len(hand_list)
    return {hand: i / n for i, hand in enumerate(hand_scores, start=1)}


def get_bot_ranking(orig_hand, community):
    full_current_hand = orig_hand + community
    used_cards = {card.num for card in full_current_hand}
    cards_left = [i for i in range(52) if i not in used_cards]
    current_score = get_average_hand_ranking(full_current_hand, [])

    all_other_hand_combos = list(combinations(cards_left, 2))
    n = len(full_current_hand)
    if n == 5:
        other_hands = random.sample(all_other_hand_combos, 200)
    else:
        other_hands = all_other_hand_combos

    n_sample_hands = len(other_hands)
    ranking = 0
    for num1, num2 in other_hands:
        full_other_hand = [Card(num1), Card(num2)] + community
        score = get_average_hand_ranking(full_other_hand, orig_hand)
        ranking += current_score >= score
    return ranking / n_sample_hands


def get_average_hand_ranking(full_hand, used_cards):
    n_left = 7 - len(full_hand)
    if n_left == 0:
        return Evaluator(full_hand).get_hex_score()

    used_cards = {card.num for card in full_hand + used_cards}
    cards_left = [i for i in range(52) if i not in used_cards]

    scores = []
    all_community_combos = list(combinations(cards_left, n_left))
    n_sample = 100 if n_left == 2 else len(all_community_combos)
    community_card_combos = random.sample(all_community_combos, n_sample)
    for comm_cards in community_card_combos:
        next_community_cards = [Card(num) for num in comm_cards]
        complete_full_hand = full_hand + next_community_cards
        score = Evaluator(complete_full_hand).get_hex_score()
        scores.append(score)
    return median(scores)


def get_short_card_combo(c1, c2):
    r1, r2 = sorted([c1.rank, c2.rank])
    if r1 == r2:
        k = "p"
    elif c1.suit == c2.suit:
        k = "s"
    else:
        k = "u"
    return r2, r1, k


HAND_RANKING = get_init_hand_ranking()


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
        self.num = num
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

    def to_dict(self):
        rank = RANKS[self.rank]
        suit = SUITS[self.suit]
        color = "black" if suit in BLACK_SUTIS else "red"
        return rank, suit, color


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

    def to_list(self):
        return [card.to_dict() for card in self.cards]

    def init_score(self):
        ranks = sorted([self.cards[0].rank, self.cards[1].rank])

        # pair
        if ranks[0] == ranks[1]:
            return (ranks[0] + 10) ** 1.5

        # no pair
        score = (ranks[1] + 5) ** 1.3 + (ranks[0] + 5)

        # suited
        if self.cards[0].suit == self.cards[1].suit:
            score *= 1.1

        # cards good for straight
        ranks_diff = ranks[1] - ranks[0]
        if ranks_diff == 1:
            score *= 1.1
        elif ranks_diff == 2:
            score *= 1.05
        return score


class Evaluator:
    def __init__(self, hand):
        self.hand = hand
        self.ranks = [card.rank for card in hand]
        self.suits = [card.suit for card in hand]
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

    def evaluate(self):
        flush_suit = self.check_flush()

        # check for straight flush
        if flush_suit != -1:
            flush_ranks = sorted(
                r for r, s in zip(self.ranks, self.suits) if s == flush_suit
            )
            straight_flush_rank = self.check_straight(flush_ranks)
            if straight_flush_rank != -1:
                return 8, straight_flush_rank

        # get direct access to ranks that appear 1, 2, 3, or 4 times
        # makes it easier to read code than accessing self.count_ranks_dict each time
        # these are lists of ranks in ascending order
        ranks1 = self.count_ranks_dict[1]
        ranks2 = self.count_ranks_dict[2]
        ranks3 = self.count_ranks_dict[3]
        ranks4 = self.count_ranks_dict[4]
        n2 = len(ranks2)
        n3 = len(ranks3)

        # four of a kind
        if ranks4:
            kicker = max(ranks1 + ranks2 + ranks3)
            return 7, ranks4[-1], kicker

        # full house
        if n3 == 2:
            return 6, ranks3[-1], ranks3[-2]
        if n3 == 1 and n2 >= 1:
            return 6, ranks3[-1], ranks2[-1]

        # flush
        if flush_suit != -1:
            return (
                5,
                flush_ranks[-1],
                flush_ranks[-2],
                flush_ranks[-3],
                flush_ranks[-4],
                flush_ranks[-5],
            )

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
            return 1, ranks2[-1], ranks1[-1], ranks1[-2], ranks1[-3]

        # high card
        return 0, ranks1[-1], ranks1[-2], ranks1[-3], ranks1[-4], ranks1[-5]

    def get_hex_score(self):
        score = 0
        for i, val in enumerate(self.score):
            score += 16 ** (5 - i) * (val + 1)
        return score

    def __repr__(self):
        score, *others = self.score
        rank_chars = [RANKS[o] for o in others]
        return SCORES[score].format(*rank_chars)


MAX_ROUNDS = 4
MAX_BET_ROUNDS = 4
BLINDS = 5, 10


class Player:
    def __init__(self, name, id, money=1000):
        self.name = name
        self.id = id
        self.money = money
        self.hand = None
        self.bet = None
        self.played = False
        self.evaluator = None

    def set_init_rank(self):
        combo = get_short_card_combo(*self.hand.cards)
        self.init_rank = HAND_RANKING[combo]


class Bot(Player):
    def make_choice(self, poker):
        choices = poker.choices
        choice_list = list(choices)
        _round = poker.round
        bet_round = poker.bet_round
        r = random.random()

        if _round == 1:
            if bet_round == 2:
                if self.init_rank > 0.4:
                    # bet or raise
                    choice = choice_list[-1]
                elif self.init_rank > 0.2:
                    choice = "call" if "call" in choice_list else "check"
                else:
                    # fold or check
                    choice = choice_list[0]
            elif bet_round == 3:
                if self.init_rank > 0.8:
                    choice = "raise"
                elif self.init_rank > 0.3:
                    choice = "call"
                else:
                    choice = "fold"
            elif bet_round == 4:
                if self.init_rank > 0.8:
                    choice = "raise"
                else:
                    choice = "call"
            else:
                choice = "call"
        else:
            ranking = get_bot_ranking(poker.bot.hand.cards, poker.community.cards)
            if bet_round == 1:
                if ranking > 0.4:
                    if r > 0.3:
                        choice = "bet"
                    else:
                        choice = "check"
                else:
                    choice = "check"
            elif bet_round == 2:
                if ranking > 0.7:
                    if r > 0.5:
                        choice = "raise"
                    else:
                        choice = "call"
                elif ranking > 0.4:
                    choice = "call"
                else:
                    choice = "fold"
            elif bet_round == 3:
                if ranking > 0.9:
                    if r > 0.5:
                        choice = "raise"
                    else:
                        choice = "call"
                elif ranking > 0.6:
                    choice = "call"
                else:
                    choice = "fold"
            elif bet_round == 4:
                if ranking > 0.9:
                    if r > 0.7:
                        choice = "raise"
                    else:
                        choice = "call"
                elif ranking > 0.6:
                    choice = "call"
                else:
                    choice = "fold"
            else:
                choice = "call"

        bet = choices[choice]
        output = f"{self.name} {choice}s"

        if choice == "raise":
            output += f" to {bet}"
        elif choice in ("call", "bet"):
            output += f" {bet}"

        output += "\n"
        return output, choice, bet

    @property
    def winner_string(self):
        s = f"{self.name} wins"
        if self.evaluator:
            s = f"{s} with {self.evaluator}"
        return s


class You(Player):
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
        self.bot = Bot(name="Computer", id=0, money=1000)
        self.you = You(name="You", id=1, money=1000)

        # create tuple of players
        self.players = self.you, self.bot

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

        self.not_dealer.start_money = self.not_dealer.money
        self.dealer.start_money = self.dealer.money

        self.not_dealer.hand = Hand(self.deck[:2])
        self.dealer.hand = Hand(self.deck[2:4])
        self.community = Hand(self.deck[4:9])
        self.not_dealer.bet = BLINDS[1]
        self.dealer.bet = BLINDS[0]
        self.not_dealer.money -= self.not_dealer.bet
        self.dealer.money -= self.dealer.bet
        self.dealer.played = self.not_dealer.played = False
        self.dealer.evaluator = self.not_dealer.evaluator = None
        self.dealer.set_init_rank()
        self.not_dealer.set_init_rank()

    @property
    def both_played(self):
        return all(player.played for player in self.players)

    @property
    def current_player(self):
        return self.players[self.turn]

    @property
    def other_player(self):
        return self.players[1 - self.turn]

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

        self.choices = self.get_bet_values(choices)

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

    def determine_winner(self, choice):
        if choice == "fold":
            self.winner = self.other_player
        else:
            # evaluate each hand
            self.dealer.evaluator = Evaluator(self.dealer.hand + self.community)
            self.not_dealer.evaluator = Evaluator(self.not_dealer.hand + self.community)

            # determine winner
            if self.dealer.evaluator.score > self.not_dealer.evaluator.score:
                self.winner = self.dealer
            elif self.dealer.evaluator.score < self.not_dealer.evaluator.score:
                self.winner = self.not_dealer
            else:
                self.winner = "tie"
        return self.finish_hand()

    def finish_hand(
        self,
    ):
        if self.winner == "tie":
            self.not_dealer.money += self.pot // 2
            self.dealer.money += self.pot // 2
            return "tie"
        else:
            self.winner.money += self.pot
            return self.winner.winner_string


if __name__ == "__main__":
    Poker()

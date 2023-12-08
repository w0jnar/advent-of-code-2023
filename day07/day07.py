import pathlib


def calc_hand_winnings(hands_file_name, use_joker_wild_rule=False):
    poker_hand_node = PokerHandBSTNode(use_joker_wild_rule)
    with pathlib.Path(hands_file_name).absolute().open() as f:
        for line in f:
            hand_bid_list = line.split()
            poker_hand_node.insert(hand_bid_list[0], hand_bid_list[1])
    return poker_hand_node.caclulate_winnings()


class PokerHandBSTNode:
    def __init__(self, use_joker_wild_rule, hand=None, bid=None):
        self.left = None
        self.right = None
        self.hand = hand
        self.bid = bid
        self.use_joker_wild_rule = use_joker_wild_rule

    def insert(self, hand, bid):
        if not self.hand and not self.bid:
            self.hand = hand
            self.bid = bid
            return
        if self.hand == hand:
            return
        if self.if_hand_less_than_self(hand):
            if self.left:
                self.left.insert(hand, bid)
                return
            self.left = PokerHandBSTNode(self.use_joker_wild_rule, hand, bid)
            return
        if self.right:
            self.right.insert(hand, bid)
            return
        self.right = PokerHandBSTNode(self.use_joker_wild_rule, hand, bid)

    def in_order(self, hands):
        if self.left is not None:
            self.left.in_order(hands)
        if self.hand is not None and self.bid is not None:
            hands.append([self.hand, self.bid])
        if self.right is not None:
            self.right.in_order(hands)
        return hands

    def if_hand_less_than_self(self, hand):
        # Compare hands as lists, first element of the list being the hand type.
        self_hand_value_list = self.get_hand_value(self.hand)
        incoming_hand_value_list = self.get_hand_value(hand)
        for i, hand_value in enumerate(self_hand_value_list):
            if hand_value != incoming_hand_value_list[i]:
                return hand_value < incoming_hand_value_list[i]

    def get_hand_value(self, hand):
        output_list = [-1]
        values = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'T': 10,
            'Q': 12,
            'K': 13,
            'A': 14
        }
        values['J'] = 11 if not self.use_joker_wild_rule else 1
        card_dict = {}
        for _, card in enumerate(hand):
            if card_dict.get(card, None) is None:
                card_dict[card] = 1
            else:
                card_dict[card] += 1
            output_list.append(values.get(card))
        # If using the joker wild hand rule and if there are any J and the hand isn't 5 of them,
        # add the number of Js to the existing highest number of occurences.
        if self.use_joker_wild_rule and card_dict.get('J', None) is not None and card_dict.get('J', None) != 5:
            j_amount = card_dict.get('J', None)
            del card_dict['J']
            max_value_key = max(zip(card_dict.values(), card_dict.keys()))[1]
            card_dict[max_value_key] += j_amount
        sorted_card_count_list = list(card_dict.values())
        sorted_card_count_list.sort(reverse=True)
        # 5 of a kind.
        if sorted_card_count_list[0] == 5:
            output_list[0] = 6
        # 4 of a kind.
        elif sorted_card_count_list[0] == 4:
            output_list[0] = 5
        elif sorted_card_count_list[0] == 3:
            # Full house.
            if sorted_card_count_list[1] == 2:
                output_list[0] = 4
            # 3 of a kind.
            else:
                output_list[0] = 3
        elif sorted_card_count_list[0] == 2:
            # 2 pairs.
            if sorted_card_count_list[1] == 2:
                output_list[0] = 2
            # 1 pair.
            else:
                output_list[0] = 1
        # High card.
        else:
            output_list[0] = 0
        return output_list

    def caclulate_winnings(self):
        bst_output = []
        self.in_order(bst_output)
        bids = [int(x[1]) for x in bst_output]
        bids.reverse()
        winnings = 0
        for i, bid in enumerate(bids):
            winnings += bid * (i + 1)
        return winnings


if __name__ == "__main__":
    winnings = calc_hand_winnings('day07\\input_example.txt')
    print(winnings)

    winnings = calc_hand_winnings('day07\\input.txt')
    print(winnings)

    winnings = calc_hand_winnings('day07\\input_example.txt', True)
    print(winnings)

    winnings = calc_hand_winnings('day07\\input.txt', True)
    print(winnings)

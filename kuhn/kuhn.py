import numpy as np
from player import Player

    
class Kuhn:
    def __init__(self, betting_rounds, num_cards, verbose=False,**args):
        self.pot = 0
        self.num_players = 3
        self.players = [Player(i) for i in range(self.num_players)]
        self.verbose = verbose
        self.betting_rounds = betting_rounds
        self.num_cards = num_cards

    def _deal(self):
        cards = np.random.choice(self.num_cards, self.num_players, replace=False)
        for i in range(self.num_players):
            self.players[i].get_card(cards[i])

        self.leftover = set([i for i in range(self.num_cards)]) - set(cards)

        if self.verbose:
            for player in range(self.num_players):
                print("player {} has card {}".format(player, cards[player]))

            print("the leftover cards are {}".format(self.leftover))

    def _raised(self, player):
        i = 1
        players = self.players
        raised_actions = []
        while i < self.num_players:
            curr_player = (player + self.num_players + i) % self.num_players
            if len(self.folded_players) == self.num_players - 1:
                return raised_actions
            if curr_player not in self.folded_players:
                raised_actions.append(players[curr_player].action(True))
                if raised_actions[-1] == 'fold':
                    self.folded_players.add(curr_player)
                if raised_actions[-1] == 'call':
                    self.pot += 1

            i += 1

        return raised_actions

                
    def _play_hand(self):
        players = self.players 

        actions = []
        self.folded_players = set()

        for r in range(self.betting_rounds):
            current_round = []
            if self.verbose:
                print("current round: {}".format(r))
            for i in range(len(players)):
                if len(self.folded_players) == self.num_players - 1:
                        if self.verbose:
                            print("player {} won {} chips. Everyone else folded".format(i, self.pot))
                            print(current_round)
                        return
                curr_action = players[i].action()
                current_round.append(curr_action)
                try:
                    did_raise = current_round[-1] == 'raise'
                    did_fold = current_round[-1] == 'fold'
                    
                    if did_fold:
                        self.folded_players.add(i)
                    
                except:
                    did_raise = False
                if did_raise:
                    self.pot += 1
                    current_round.append(self._raised(i))
                    break
            
            actions.append(current_round)
            if len(self.folded_players) == self.num_players - 1:
                        if self.verbose:
                            print("player {} won {} chips. Everyone else folded".format(set([0,1,2]) - self.folded_players, self.pot))
                            print(actions)
                        return
        if self.verbose:
            print(actions)

        return actions
        
    def _showdown(self):
        still_playing = [player for player in players if player.player_number not in self.folded_players]
        winner = max(still_playing)
        if self.verbose:
            print(still_playing)
            print("the winner is {}. They won {} chips".format(winner, self.pot))

    def play(self):
        if self.verbose:
            print('Staring game, each player antes 1')
        self.pot += self.num_players

        self._deal()
        actions = self._play_hand()

        self._showdown()


class ExtendedKuhn(Kuhn):
    def _deal(self):
        choices = [i for i in range(0, 10)] * 2
        cards = np.random.choice(choices, self.num_players, replace=False)
        for i in range(self.num_players):
            self.players[i].get_card(cards[i])

        res = list(map(lambda x: choices.remove(x) if x in choices else None, cards))

        common_card = np.random.choice(list(choices),1)
        choices.remove(common_card)
        self.leftover = choices
        self.common_card = common_card[0]
        if self.verbose:
            for player in range(self.num_players):
                print("player {} has card {}".format(player, cards[player]))

            print("the leftover cards are {}".format(self.leftover))
            print("the common card is {}".format(self.common_card))

    def _raised(self, player):
        i = 1
        players = self.players
        raised_actions = []
        while i < self.num_players:
            curr_player = (player + self.num_players + i) % self.num_players
            if len(self.folded_players) == self.num_players - 1:
                return raised_actions
            if curr_player not in self.folded_players:
                raised_actions.append(players[curr_player].action(True, extended=True))
                if raised_actions[-1] == 'fold':
                    self.folded_players.add(curr_player)
                if raised_actions[-1] == 'call':
                    self.pot += 1
                if raised_actions[-1] == 'raise':
                    self.pot += 2
                    actions = super()._raised(curr_player)
                    raised_actions.append(actions)
                    return raised_actions
            i += 1

        return raised_actions

    def _showdown(self):
        """
        Implement how private and public card are 
        """
        pass

        


if __name__ == '__main__':
    # Kuhn(1, 5, verbose=True).play()

    ExtendedKuhn(2, 10, verbose=True).play()







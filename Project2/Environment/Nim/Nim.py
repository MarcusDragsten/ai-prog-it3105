from Parameters import nim_config

class Nim:
    def __init__(self, num_stones, max_removal):

        # Variables from config
        self.num_stones = num_stones
        self.max_removal = max_removal

        # The current player
        self.playing_player = 1

        # The state in this game
        self.remaining_stones = num_stones

    def get_moves(self):
        """ Usikker om man skal hente moves ut ifra en state eller fra self-verdier """
        
        moves = []

        for i in range(1, self.max_removal + 1):
            if i <= self.remaining_stones:
                moves.append(i)

        return moves


    def reset(self, playing_player):
        self.num_stones = nim_config['num_stones']
        self.max_removal = nim_config['max_removal']
        self.playing_player = playing_player

        self.remaining_stones = self.num_stones

    def game_done(self):

        if self.remaining_stones == 0:
            return True

        return False

    def player_has_won(self):

        if self.game_done():
            if self.playing_player == 1:
                return 1
            else:
                return 2
        else:
            raise ValueError("No winner, game broken xD")


    def get_state_tuple(self):

        """ TROR DENNE BARE SKAL RETURNERE REMAINING STONES """
        return (self.remaining_stones,)


    def alter_state_from_move(self, move):

        if move not in self.get_moves():
            raise('Not a legal move')
        else:
            self.remaining_stones -= move

        if self.playing_player == 1:
            self.playing_player = 2
        else:
            self.playing_player = 1


    def net_input_size(self):

        return NotImplementedError


# vartest = Nim(6, 2)
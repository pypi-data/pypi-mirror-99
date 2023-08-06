class Player:
    def __init__(self, player, gobbs, color, scolor, modes):
        self.player = player
        self.gobbs = gobbs
        self.color = color
        self.scolor = scolor
        self.modes = modes

_win_lines = {
    "a": ['a1', 'a2', 'a3'],
    "b": ['b1', 'b2', 'b3'],
    "c": ['c1', 'c2', 'c3'],
    "one": ['a1', 'b1', 'c1'],
    "two": ['a2', 'b2', 'c2'],
    "three": ['a3', 'b3', 'c3'],
    "backslash": ['a1', 'b2', 'c3'],
    "slash": ['a3', 'b2', 'c1']
}

# GobbletGobblers('佐藤', '田中', 'red', '  ')
class GobbletGobblers:
    def __init__(self, senkou_player, koukou_player, empty_board_text):

        self.empty_board_text = str(empty_board_text)
        self.sen = Player(senkou_player, list('ssmmbb'), 'Red', 'r', ['p'])
        self.kou = Player(koukou_player, list('ssmmbb'), 'Blue', 'b', ['p'])

        self.turn = 1

        self.now_player = self.sen

        self.won = False
        self.winner = None

        self.board = {
            "a1": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "a2": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "a3": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "b1": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "b2": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "b3": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "c1": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "c2": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            },
            "c3": {
                "t": self.empty_board_text,
                "b": None,
                "m": None,
                "s": None
            }
        }

    def _win_check(self):
        for key in _win_lines.keys():
            if all([self.board[_key]['t'].startswith('b') for _key in _win_lines[key]]):
                self.won = True
                self.winner = self.now_player
                return
            if all([self.board[_key]['t'].startswith('r') for _key in _win_lines[key]]):
                self.won = True
                self.winner = self.now_player
                return


    def _powerful(self, place):
        gobbs = list(dict.fromkeys(self.now_player.gobbs))
        board_place = self.board[place]

        if board_place['t'] == self.empty_board_text:
            return gobbs

        elif board_place['t'].endswith('s'):
            try:
                gobbs.remove('s')
            except:
                pass
            return gobbs

        elif board_place['t'].endswith('m'):
            try:
                gobbs.remove('s')
            except:
                pass
            try:
                gobbs.remove('m')
            except:
                pass
            return gobbs

    def choices_put(self):
        not_big_places = [key for key in self.board.keys() if self.board[key]['b'] == None]
        a1 = None if not 'a1' in not_big_places else self._powerful('a1')
        a2 = None if not 'a2' in not_big_places else self._powerful('a2')
        a3 = None if not 'a3' in not_big_places else self._powerful('a3')
        b1 = None if not 'b1' in not_big_places else self._powerful('b1')
        b2 = None if not 'b2' in not_big_places else self._powerful('b2')
        b3 = None if not 'b3' in not_big_places else self._powerful('b3')
        c1 = None if not 'c1' in not_big_places else self._powerful('c1')
        c2 = None if not 'c2' in not_big_places else self._powerful('c2')
        c3 = None if not 'c3' in not_big_places else self._powerful('c3')

        r = {
            "a1": a1,
            "a2": a2,
            "a3": a3,
            "b1": b1,
            "b2": b2,
            "b3": b3,
            "c1": c1,
            "c2": c2,
            "c3": c3
        }
        return r

    def put(self, place, size):
        self.board[place][size] = self.now_player.scolor
        self.board[place]['t'] = self.now_player.scolor + size
        self._win_check()
        self.now_player.gobbs.remove(size)

        if self.now_player.scolor == 'r':
            self.sen = self.now_player
        else:
            self.kou = self.now_player

        players_gobbs = [key for key in self.board.keys() if self.board[key]['t'].startswith('b')]
        if len(players_gobbs) > 0 and not 'm' in self.kou.modes:
            self.kou.modes.append('m')
        elif len(players_gobbs) == 0 and 'm' in self.kou.modes:
            self.kou.modes.remove('m')

        players_gobbs = [key for key in self.board.keys() if self.board[key]['t'].startswith('r')]
        if len(players_gobbs) > 0 and not 'm' in self.sen.modes:
            self.sen.modes.append('m')
        elif len(players_gobbs) == 0 and 'm' in self.sen.modes:
            self.sen.modes.remove('m')

        self.now_player = self.kou if self.now_player.scolor == 'r' else self.sen



        self.turn += 1



    def choices_move_from(self):
        players_gobbs = [key for key in self.board.keys() if self.board[key]['t'].startswith(self.now_player.scolor)]
        return players_gobbs

    def choices_move_to(self, from_):
        not_big_places = [key for key in self.board.keys() if self.board[key]['b'] == None]
        if self.board[from_]['t'].endswith('s'):
            return [key for key in not_big_places if self.board[key]['t'] == self.empty_board_text]
        elif self.board[from_]['t'].endswith('m'):
            return [key for key in not_big_places if self.board[key]['m'] == None and self.board[key]['b'] == None]
        elif self.board[from_]['t'].endswith('b'):
            return not_big_places

    def move(self, from_, to):
        move_gobb = self.board[from_]['t']
        if move_gobb.endswith('s'):
            self.board[from_]['s'] = None
            self.board[from_]['t'] = self.empty_board_text
            self.board[to]['s'] = move_gobb[0]
            self.board[to]['t'] = move_gobb
        elif move_gobb.endswith('m'):
            self.board[from_]['m'] = None
            self.board[from_]['t'] = self.board[from_]['s'] + 's' if not board[from_]['s'] == None else self.empty_board_text
            self.board[to]['m'] = move_gobb[0]
            self.board[to]['t'] = move_gobb
        elif move_gobb.endswith('b'):
            self.board[from_]['b'] = None
            if not self.board[from_]['m'] == None:
                self.board[from_]['t'] = self.board[from_]['m'] + 'm'
            elif not self.board[from_]['s'] == None:
                self.board[from_]['t'] = self.board[from_]['s'] + 's'
            else:
                self.board[from_]['t'] = self.empty_board_text

            self.board[to]['b'] = move_gobb[0]
            self.board[to]['t'] = move_gobb
        self._win_check()
        if self.now_player.scolor == 'r':
            self.sen = self.now_player
        else:
            self.kou = self.now_player

        players_gobbs = [key for key in self.board.keys() if self.board[key]['t'].startswith('b')]
        if len(players_gobbs) > 0 and not 'm' in self.kou.modes:
            self.kou.modes.append('m')
        elif len(players_gobbs) == 0 and 'm' in self.kou.modes:
            self.kou.modes.remove('m')

        players_gobbs = [key for key in self.board.keys() if self.board[key]['t'].startswith('r')]
        if len(players_gobbs) > 0 and not 'm' in self.sen.modes:
            self.sen.modes.append('m')
        elif len(players_gobbs) == 0 and 'm' in self.sen.modes:
            self.sen.modes.remove('m')

        self.now_player = self.kou if self.now_player.scolor == 'r' else self.sen

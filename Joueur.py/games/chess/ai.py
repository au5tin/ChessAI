# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
from random import shuffle
from copy import deepcopy
from games.chess.ai_utilities import State
from games.chess.ai_utilities import Action
from operator import itemgetter
from queue import PriorityQueue
import time
# <<-- /Creer-Merge: imports -->>

########################################################
##   Name: Oscar Lewczuk     Period: T/Th 3:30-4:45   ##
##          Class: Artificial Intelligence            ##
##            Assignment: Game Problem #2             ##
########################################################

infinity = float('inf')

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Au5 Player" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        
        self.state = State(self.player.color)
        self.state.init_fen(self.game.fen)
        self.depth_limit = int(self.get_setting('depth_limit')) if self.get_setting('depth_limit') else 2
        self.total_time = 15*60
        self.current_move = 0
        
        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic

        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.
        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn

        if self.game.moves:
            self.update_board(self.state, self.game.moves[-1])
            self.nicePrintMove(self.game.moves[-1], len(self.game.moves))


        action = self.TLHTQSID_ABDLMM(self.state, self.depth_limit)

        #Gets piece from x1, y1, x2, y2, promotion
        move_from = bToP(action.x1, action.y1)
        move_to = bToP(action.x2, action.y2)
        piece = None
        for p in self.player.pieces:
            if p.file == move_from[0] and p.rank == move_from[1]:
                piece = p
        #Check Promotion
        if action.promotion:
            piece.move(move_to[0], move_to[1], action.promotion)
        else:
            piece.move(move_to[0], move_to[1])
        self.state.enPass = ''
        
        self.update_board(self.state, self.game.moves[-1])
        self.nicePrintMove(self.game.moves[-1], len(self.game.moves))
        
        return True
        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here

    #TLIDABM functions here

    #Iterative deepening function returns best action
    #Avg 75 moves @ 12 sec ea = 15 mins
    def TLHTQSID_ABDLMM(self, state, max_depth):
        start = time.clock()
        h_table = {}
        QSD = 2
        for depth in range(1, max_depth+1):
            result = self.ABMM(state, depth, QSD, -infinity, infinity, start, h_table)
            if depth == max_depth or time.clock()-start > self.total_time/10:
                return result
        self.total_time -= time.clock()-start
    
    def ABMM(self, state, max_depth, QuiSD, alpha, beta, start, htable):
        
        def min_value(stat, depth, QSD, alph, bet, star):
            #QSD
            if depth == 0 and not stat.isQuiessant() and QSD > 0 and time.clock()-star < self.total_time/10:
                #HT
                all_actions = stat.actions()
                for a in all_actions:
                    if a in htable:
                        a.val = htable[a]
                all_actions.sort(key=lambda x: x.val, reverse=True)
                val = infinity
                act = None
                for a in all_actions:
                    v = max_value(self.result(stat, a), depth, QSD-1, alph, bet, star)
                    #AB
                    if v > alph and v < bet:
                        bet = v
                        val = v
                        act = a
                    elif v <= alph:
                        #HT
                        if a in htable:
                            htable[a] += 1
                        else:
                            htable[a] = 1
                        return min(val, v)
                    #End AB
                #HT
                if act in htable:
                    htable[act] += 1
                else:
                    htable[act] = 1
                return val
            elif stat.isterminal() or depth == 0 or time.clock()-star > self.total_time/10:
                return stat.heuristic()
            #HT
            all_actions = stat.actions()
            for a in all_actions:
                if a in htable:
                    a.val = htable[a]
            all_actions.sort(key=lambda x: x.val, reverse=True)
            val = infinity
            act = None
            for a in all_actions:
                v = max_value(self.result(stat, a), depth-1, QSD, alph, bet, star)
                #AB
                if v > alph and v < bet:
                    bet = v
                    val = v
                    act = a
                elif v <= alph:
                    #HT
                    if a in htable:
                        htable[a] += 1
                    else:
                        htable[a] = 1
                    return min(val, v)
                #End AB
            #HT
            if act in htable:
                htable[act] += 1
            else:
                htable[act] = 1
            return val

        def max_value(stat, depth, QSD, alph, bet, star):
            if depth == 0 and not stat.isQuiessant() and QSD > 0 and time.clock()-star > self.total_time/10:
                #HT
                all_actions = stat.actions()
                for a in all_actions:
                    if a in htable:
                        a.val = htable[a]
                all_actions.sort(key=lambda x: x.val, reverse=True)
                val = -infinity
                act = None
                for a in stat.actions():
                    v = min_value(self.result(stat, a), depth, QSD-1, alph, bet, star)
                    #AB
                    if v > alph and v < bet:
                        alph = v
                        val = v
                        act = a
                    elif v >= bet:
                        #HT
                        if a in htable:
                            htable[a] += 1
                        else:
                            htable[a] = 1
                        return max(val, v)
                    #End AB
                #HT
                if act in htable:
                    htable[act] += 1
                else:
                    htable[act] = 1
                return val
            elif stat.isterminal() or depth == 0 or time.clock()-star > self.total_time/10:
                return stat.heuristic()
            #HT
            all_actions = stat.actions()
            for a in all_actions:
                if a in htable:
                    a.val = htable[a]
            all_actions.sort(key=lambda x: x.val, reverse=True)
            val = -infinity
            act = None
            for a in stat.actions():
                v = min_value(self.result(stat, a), depth-1, QSD, alph, bet, star)
                #AB
                if v > alph and v < bet:
                    alph = v
                    val = v
                    act = a
                elif v >= bet:
                    #HT
                    if a in htable:
                        htable[a] += 1
                    else:
                        htable[a] = 1
                    return max(val, v)
                #End AB
            #HT
            if act in htable:
                htable[act] += 1
            else:
                htable[act] = 1
            return val

        #HT
        all_act = state.actions()
        for a in all_act:
            if a in htable:
                a.val = htable[a]
        all_act.sort(key=lambda x: x.val, reverse=True)
        action = None
        for a in all_act:
            val = min_value(self.result(state, a), max_depth-1, QuiSD, alpha, beta, start)
            #AB
            if val > alpha:
                alpha = val
                action = a
            #End AB
        #HT
        if action in htable:
            htable[action] += 1
        else:
            htable[action] = 1
        return action

    #End functions
    
    def nicePrintMove(self, move, number):
        print('Move #' + str(number) + ': ')
        print(move.piece.owner.color, move.piece.type, 'from', move.from_file+str(move.from_rank), 'to', move.to_file+str(move.to_rank))
        self.current_move = number
        print('')

    #Turns a state and move -> new state updating old one
    def update_board(self, state, move):
        x1, y1 = pToB(move.from_file, move.from_rank)
        x2, y2 = pToB(move.piece.file, move.piece.rank)
        piece = move.piece
        #Handles pawn promotions
        if move.promotion:
            if piece.owner.color == 'White':
                if piece.type == 'Knight':
                    state.board[x1][y1], state.board[x2][y2] = ' ', 'N'
                else:
                    state.board[x1][y1], state.board[x2][y2] = ' ', piece.type[0]
            else:
                if piece.type == 'Knight':
                    state.board[x1][y1], state.board[x2][y2] = ' ', 'n'
                else:
                    state.board[x1][y1], state.board[x2][y2] = ' ', piece.type[0].lower()
        #For en-passant
        elif piece.type == 'Pawn' and abs(y2-y1) == 2:
            if state.color == 'White' and piece.owner.color == 'Black':
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.enPass = (x1, y1+1)
            elif state.color == 'Black' and piece.owner.color == 'White':
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.enPass = (x1, y1-1)
            else:
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
        #Handles KS Castles
        elif move.san == 'O-O':
            if piece.owner.color == 'White':
                state.board[x1][y1], state.board[x2][y2] = ' ', 'K'
                state.board[x2+1][y2], state.board[x1+1][y1] = ' ', 'R'
                state.WKingSideCastle = False
                state.WQueenSideCastle = False
            else:
                state.board[x1][y1], state.board[x2][y2] = ' ', 'k'
                state.board[x2+1][y2], state.board[x1+1][y1] = ' ', 'r'
                state.BKingSideCastle = False
                state.BQueenSideCastle = False
        #Handles QS Castles
        elif move.san == 'O-O-O':  
            if piece.owner.color == 'White':
                state.board[x1][y1], state.board[x2][y2] = ' ', 'K'
                state.board[x2-2][y2], state.board[x1-1][y1] = ' ', 'R'
                state.WQueenSideCastle = False
                state.WKingSideCastle = False
            else:
                state.board[x1][y1], state.board[x2][y2] = ' ', 'k'
                state.board[x2-2][y2], state.board[x1-1][y1] = ' ', 'r'
                state.BQueenSideCastle = False
                state.BKingSideCastle = False
        #Single King Moves
        elif piece.type == 'King':
            if piece.owner.color == 'White':
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.WKingSideCastle = False
                state.WQueenSideCastle = False
            else:
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.BKingSideCastle = False
                state.BQueenSideCastle = False
        #Handles Rook bools
        elif piece.type == 'Rook':
            if piece.owner.color == 'White' and x1 == 7:
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.WKingSideCastle = False
            elif piece.owner.color == 'White' and x1 == 0:
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.WQueenSideCastle = False
            elif piece.owner.color == 'Black' and x1 == 7:
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.BKingSideCastle = False
            elif piece.owner.color == 'Black' and x1 == 0:
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
                state.BQueenSideCastle = False
            else:
                state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]
        else:
            state.board[x1][y1], state.board[x2][y2] = ' ', state.board[x1][y1]

    #Turns a state and action -> new state and returns it
    def result(self, state, action):
        result_state = deepcopy(state)
        x1, y1 = action.x1, action.y1
        x2, y2 = action.x2, action.y2
        piece = result_state.board[x1][y1]
        #Handles pawn promotions
        if action.promotion:
            p = 'N' if action.promotion == 'Knight' else action.promotion
            if state.color == 'White':
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', action.promotion[0]
            else:
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', action.promotion[0].lower()
        #For en-passant
        elif (piece == 'P' or piece == 'p') and abs(y2-y1) == 2:
            if state.color == 'White':
                result_state.enPass = (x1, y1+1)
            else:
                result_state.enPass = (x1, y1-1)
        #Handles KS Castles
        elif (piece == 'K' or piece == 'k') and abs(x2-x1) == 2:
            if state.color == 'White':
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', 'K'
                result_state.board[x2+1][y2], result_state.board[x1+1][y1] = ' ', 'R'
                result_state.WKingSideCastle = False
                result_state.WQueenSideCastle = False
            else:
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', 'k'
                result_state.board[x2+1][y2], result_state.board[x1+1][y1] = ' ', 'r'
                result_state.BKingSideCastle = False
                result_state.BQueenSideCastle = False
        #Handles QS Castles
        elif (piece == 'K' or piece == 'k') and abs(x2-x1) == 3:  
            if state.color == 'White':
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', 'K'
                result_state.board[x2-2][y2], result_state.board[x1-1][y1] = ' ', 'R'
                result_state.WQueenSideCastle = False
                result_state.WKingSideCastle = False
            else:
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', 'k'
                result_state.board[x2-2][y2], result_state.board[x1-1][y1] = ' ', 'r'
                result_state.BQueenSideCastle = False
                result_state.BQueenSideCastle = False
        #Single King Moves
        elif piece == 'K' or piece == 'k':
            if state.color == 'White':
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', result_state.board[x1][y1]
                result_state.WKingSideCastle = False
                result_state.WQueenSideCastle = False
            else:
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', result_state.board[x1][y1]
                result_state.BKingSideCastle = False
                result_state.BQueenSideCastle = False
        #Handles Rook bools
        elif piece == 'R' or piece == 'r':
            if state.color == 'White' and x1 == 7:
                result_state.WKingSideCastle = False
            elif state.color == 'White' and x1 == 0:
                result_state.WQueenSideCastle = False
            elif state.color == 'Black' and x1 == 7:
                result_state.BKingSideCastle = False
            elif state.color == 'Black' and x1 == 0:
                result_state.BQueenSideCastle = False
            else:
                result_state.board[x1][y1], result_state.board[x2][y2] = ' ', result_state.board[x1][y1]
        else:
            result_state.board[x1][y1], result_state.board[x2][y2] = ' ', result_state.board[x1][y1]
        #Switches child's color
        if state.color == 'White':
            result_state.color = 'Black'
        else:
            result_state.color = 'White'
        return result_state

    def print_state(self, state):
        # iterate through the range in reverse order
        for r in range(8, -3, -1):
            output = ""
            if r == 8 or r == -1:
                # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -2:
                # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else:  # board
                output = " " + str(r+1) + " |"
                # fill in all the files with pieces at the current rank
                for _ in range(0, 8):
                    #Prints board pieces
                    piece = state.board[_][r]
                    if piece == ' ':
                        code = '.'
                    else:
                        code = piece

                    output += " " + code + " "

                output += "|"
            print(output)

#Turns piece char-file/int-rank -> 0-7/0-7
def pToB(file, rank):
    return ord(file)%ord('a'), rank-1

#Turns board 0-7/0-7 -> char-file/int-rank
def bToP(x, y):
    return chr(ord('a')+x), y+1

# <<-- /Creer-Merge: functions -->>

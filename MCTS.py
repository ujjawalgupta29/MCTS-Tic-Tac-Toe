import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

class policy(object):
    def __init__(self):
        self.tree = {}
        pass

class MCTS(onbject):
    def __init__(self, n_iterations=50, depth=15, exploration_constant=5.0, tree = None, win_mark=3, game_board=None, player=None):
        self.n_iterations = n_iterations
        self.depth = depth
        self.exploration_constant = exploration_constant
        self.total_n = 0

        self.leaf_node_id = None

        n_rows = len(game_board)
        self.n_rows = n_rows
        self.win_mark = win_mark

        if tree == None:
            self.tree = self._set_tictactoe(game_board, player)
        else:
            self.tree = tree

    def _set_tictactoe(self, game_board, player):
        root_id = (0,)
        tree = {root_id: {'state': game_board,
                          'player': player,
                          'child': [],
                          'parent': None,
                          'n': 0,
                          'w': 0,
                          'q': None}}
        return tree

    def selection(self):
        '''
        Here we select child having 
        highest UCB value
        output:
        - leaf node id which needs to expand further
        - depth (root having depth = 0)
        '''

        leaf_node_found = False
        leaf_node_id = (0,) # root id

        while not leaf_node_found:
            node_id = leaf_node_id
            n_child = len(self.tree[node_id]['child'])

            if n_child == 0: #leaf node found
                leaf_node_id = node_id
                leaf_node_found = True

            else:
                maximum_uct_value = -100.0
                for i in range(n_child):
                    action = self.tree[node_id]['child'][i]
                    child_id = node_id + (action,)
                    w = self.tree[child_id]['w']
                    n = self.tree[child_id]['n']
                    total_n = self.total_n

                    #edge case when n == 0
                    if n == 0:
                        n = 1e-4

                    exploitation_value = w/n_child
                    exploration_value = np.sqrt(np.log(total_n)/n)
                    uct_value = exploitation_value + self.exploration_constant * exploration_value

                    if uct_value > maximum_uct_value:
                        maximum_uct_value = uct_value
                        leaf_node_id = child_id

        depth = len(leaf_node_id) # as node_id records selected action set

        return leaf_node_id, depth

    def _is_terminal(self, leaf_state):
        '''
        checks whether current
        state is terminal state or not
        output(who wins): 'o', 'x', 'draw', 'None'
        '''
        def __who_wins(sums, win_mark):
            if np.any(sums == win_mark):
                return 'o'
            if np.any(sums == -win_mark):
                return 'x'
            return None

        def __is_terminal_in_conv(leaf_state, win_mark):
            # check row/col
            for axis in range(2):
                sums = np.sum(leaf_state, axis=axis)
                result = __who_wins(sums, win_mark)
                if result is not None:
                    return result
            # check diagonal
            for order in [-1,1]:
                diags_sum = np.sum(np.diag(leaf_state[::order]))
                result = __who_wins(diags_sum, win_mark)
                if result is not None:
                    return result
            return None

        win_mark = self.win_mark
        n_rows_board = len(self.tree[(0,)]['state'])
        window_size = win_mark
        window_positions = range(n_rows_board - win_mark + 1)

        for row in window_positions:
            for col in window_positions:
                window = leaf_state[row:row+window_size, col:col+window_size]
                winner = __is_terminal_in_conv(window, win_mark)
                if winner is not None:
                    return winner

        if not np.any(leaf_state == 0):
            '''
            no more action i can do
            '''
            return 'draw'
        return None
    
    def _get_valid_actions(self, leaf_state):
        '''
        return all possible action in current leaf state
        in:
        - leaf_state
        out:
        - set of possible actions ((row,col), action_idx)
        '''
        actions = []
        count = 0
        state_size = len(leaf_state)

        for i in range(state_size):
            for j in range(state_size):
                if leaf_state[i][j] == 0:
                    actions.append([(i, j), count])
                count += 1

        return actions

    def expansion(self, leaf_node_id):
        '''
        Here we expand our leaf node to
        next possible configurations
        input : tree and leaf_node_id
        output: expanded tree
        '''
        leaf_state = self.tree[leaf_node_id]['state']
        winner = self._is_terminal(leaf_state)
        possible_actions = self._get_valid_actions(leaf_state)

        if winner is None:
            childs = []
            for action_set in possible_actions:
                action, action_idx = action_set
                state = deepcopy(self.tree[leaf_node_id]['state'])
                current_player = self.tree[leaf_node_id]['player']

                if current_player == 'o':
                    next_turn = 'x'
                    state[action] = 1

                else:
                    next_turn = 'o'
                    state[action] = -1

                child_id = leaf_node_id + (action_idx, )
                childs.append(child_id)
                self.tree[child_id] = {'state': state,
                                       'player': next_turn,
                                       'child': [],
                                       'parent': leaf_node_id,
                                       'n': 0, 'w': 0, 'q':0}
                self.tree[leaf_node_id]['child'].append(action_idx)
            rand_idx = np.random.randint(low=0, high=len(childs), size=1)
            child_node_id = childs[rand_idx[0]]

        return child_node_id
    
    def simulation(self, child_node_id):
        '''
        simulate game from child node's state until it reaches the resulting state of the game using Monte Carlo simulation.
        in:
        - child node id (randomly selected child node id from `expansion`)
        out:
        - winner ('o', 'x', 'draw')
        '''
        self.total_n += 1
        state = deepcopy(self.tree[child_node_id]['state'])
        previous_player = deepcopy(self.tree[child_node_id]['player'])
        anybody_win = False

        while not anybody_win:
            winner = self._is_terminal(state)
            if winner is not None:
                # print('state')
                # print(state)
           
#                 import matplotlib.pyplot as plt
#                 plt.figure(figsize=(4.5,4.56))
#                 plt.pcolormesh(state, alpha=0.6, cmap='RdBu_r')
#                 plt.grid()
#                 plt.axis('equal')
#                 plt.gca().invert_yaxis()
#                 plt.colorbar()
#                 plt.title('winner = ' + winner + ' (o:1, x:-1)')
#                 plt.show()
                
                anybody_win = True
            else:
                possible_actions = self._get_valid_actions(state)
                # randomly choose action for simulation (= random rollout policy)
                rand_idx = np.random.randint(low=0, high=len(possible_actions), size=1)[0]
                action, _ = possible_actions[rand_idx]

                if previous_player == 'o':
                    current_player = 'x'
                    state[action] = -1
                else:
                    current_player = 'o'
                    state[action] = 1

                previous_player = current_player
        print(winner)
        return winner


    def bacpropagation(self):
        pass

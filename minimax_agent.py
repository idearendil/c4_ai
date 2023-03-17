"""
This is counnect_four ai file made with minimax tree search
and alpha-beta pruning.
"""

import copy
import random
import numpy as np

DIRECTIONS = ((1, 0), (0, 1), (1, -1), (1, 1))
ROW = 6
COLUMN = 7


class Agent:
    """
    agent class.
    """
    def __init__(self, agent_id, search_depth=3) -> None:
        self.agent_id = agent_id
        self.search_depth = search_depth
        if agent_id == "player_0":
            self.agent_code = ("player_0", "player_1")
        else:
            self.agent_code = ("player_1", "player_0")

    def __call__(self, state):
        actions = state.observe(self.agent_id)["action_mask"]
        best_actions = []
        maxmin_value = -9999

        for action in range(7):
            next_state = copy.deepcopy(state)
            if not actions[action]:
                continue
            next_state.step(action)
            _, reward, termination, _, _ = next_state.last()

            if termination:
                next_value = reward * 1000
            else:
                next_value = self.recursive_search(
                    next_state, 1, 1, maxmin_value)

            if next_value > maxmin_value:
                maxmin_value = next_value
                best_actions = [action]
            elif next_value == maxmin_value:
                best_actions.append(action)

        return random.choice(best_actions)

    def recursive_search(self, state, depth, side, threshold):
        """
        Execute minimax tree search with alpha-beta pruning until search_depth.

        :arg state:
            The game state being searched.

        :arg depth:
            How deep this function is now.

        :arg side:
            Whose turn the state is now.
            0 : agent self's turn
            1 : opponent's turn

        :arg threshold:
            The threshold used in alpha-beta pruning.

        :return:
            The value of the "state"
            which is calculated with minimax tree search.
        """

        if depth == self.search_depth:
            return self.value_function(
                state.observe(self.agent_id)['observation'])
        if side:
            maxmin_value = 9999
        else:
            maxmin_value = -9999

        actions = state.observe(self.agent_code[side])["action_mask"]
        legal_actions = [i for i in range(7) if actions[i]]
        for action in legal_actions:
            next_state = copy.deepcopy(state)
            next_state.step(action)
            _, reward, termination, _, _ = next_state.last()

            if termination:
                if side:
                    next_value = reward * -1000
                else:
                    next_value = reward * 1000
            else:
                next_value = self.recursive_search(
                    next_state, depth+1, 1-side, maxmin_value)

            if side:
                if maxmin_value > next_value:
                    maxmin_value = next_value
                    if threshold > next_value:
                        return next_value
            else:
                if maxmin_value < next_value:
                    maxmin_value = next_value
                    if threshold < next_value:
                        return next_value
        return maxmin_value

    def value_function(self, observation):
        """
        Value function, as known as evaluation function.

        :arg observation:
            The information of board which shape is (6, 7, 2)

        :return:
            The value of the board
        """
        count_np = np.zeros((12))

        if self.search_depth % 2 == 0:
            sequence = [0, 1]
        else:
            sequence = [1, 0]

        for side in sequence:
            ag_stone = side
            op_stone = 1 - side
            for row in range(ROW):
                for col in range(COLUMN):
                    if observation[row, col, ag_stone]:
                        for dir_id in range(4):
                            if not self.out_of_range(row-DIRECTIONS[dir_id][0],
                                                     col-DIRECTIONS[dir_id][1]
                                                     ):
                                if observation[row-DIRECTIONS[dir_id][0],
                                               col-DIRECTIONS[dir_id][1],
                                               ag_stone
                                               ]:
                                    continue
                            step = 0
                            blocked = 0
                            while True:
                                step += 1
                                temp_row = row + DIRECTIONS[dir_id][0] * step
                                temp_col = col + DIRECTIONS[dir_id][1] * step
                                if self.out_of_range(temp_row, temp_col):
                                    break
                                if observation[temp_row,
                                               temp_col,
                                               ag_stone] == 0:
                                    break
                            temp_row = row + DIRECTIONS[dir_id][0] * step
                            temp_col = col + DIRECTIONS[dir_id][1] * step
                            if self.out_of_range(temp_row, temp_col):
                                blocked += 1
                            elif observation[temp_row, temp_col, op_stone]:
                                blocked += 1
                            temp_row = row - DIRECTIONS[dir_id][0]
                            temp_col = col - DIRECTIONS[dir_id][1]
                            if self.out_of_range(temp_row, temp_col):
                                blocked += 1
                            elif observation[temp_row, temp_col, op_stone]:
                                blocked += 1
                            if blocked < 2:
                                count_np[
                                    side * 6 + (step-1) * 2 + blocked] += 1

        weight_np = np.array([3, 1, 10, 4, 50, 20,
                              -6, -2, -20, -8, -100, -40])
        return np.dot(count_np, weight_np)

    def out_of_range(self, row, col):
        """
        Verify whether (r, c) is out of the board.
        """
        return row < 0 or col < 0 or row >= ROW or col >= COLUMN

"""
This is power test file of ai agents of connect-four game.
"""

GAMES_NUM = 100

if __name__ == "__main__":
    from pettingzoo.classic import connect_four_v3
    from minimax_agent import Agent

    env = connect_four_v3.env()
    env.reset()

    agents = [Agent("player_0", 2), Agent("player_1", 2)]

    win_rate = [0, 0]

    for game_id in range(GAMES_NUM):

        env.reset()

        for agent_id in env.agent_iter():

            observation, reward, termination, truncation, info = env.last()

            if termination or truncation:
                if reward == 1:
                    print(agent_id, "won!!")
                    if agent_id == "player_0":
                        win_rate[0] += 1
                    else:
                        win_rate[1] += 1
                elif reward == -1:
                    print(agent_id, "did wrong action.")
                else:
                    print("draw")
                print(game_id)
                break

            # print(env.observe(agent))
            # action = env.action_space(agent).sample()
            if agent_id == "player_0":
                action = agents[0](env)
            else:
                action = agents[1](env)
            env.step(action)

    env.close()
    print(win_rate)

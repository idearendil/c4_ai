"""
This is test file of playing a connect four game.
"""

if __name__ == "__main__":
    from pettingzoo.classic import connect_four_v3
    import time
    import human_agent
    from minimax_agent import Agent

    showing_env = connect_four_v3.env(render_mode="human")
    env = connect_four_v3.env()

    showing_env.reset()
    env.reset()

    showing_env.render()
    time.sleep(1)

    first_or_second = int(input("선공을 하고싶으시면 0, 후공을 하고싶으시면 1을 입력해주세요 : "))

    if first_or_second:
        agents = [Agent("player_0", 2), human_agent.Agent("player_1")]
    else:
        agents = [human_agent.Agent("player_0"), Agent("player_1", 2)]

    for agent_id in env.agent_iter():

        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            if reward == 1:
                print(agent_id, "won!!")
            elif reward == -1:
                print(agent_id, "did wrong action.")
            else:
                print("draw")
            break

        # print(env.observe(agent))
        # action = env.action_space(agent).sample()
        if agent_id == "player_0":
            action = agents[0](env)
        else:
            action = agents[1](env)
        showing_env.step(action)
        env.step(action)
        showing_env.render()
        time.sleep(1)

    time.sleep(5)
    showing_env.close()
    env.close()

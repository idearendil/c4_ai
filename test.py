"""
This is test file of playing a connect four game.
"""

if __name__ == "__main__":
    from pettingzoo.classic import connect_four_v3
    import time

    env = connect_four_v3.env(render_mode="human")

    env.reset()

    env.render()
    time.sleep(1)

    for agent in env.agent_iter():

        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            if reward == 1:
                print(agent, "won!!")
            else:
                print(agent, "did wrong action.")
            break

        action = env.action_space(agent).sample()
        env.step(action)
        env.render()
        time.sleep(1)

    time.sleep(5)
    env.close()

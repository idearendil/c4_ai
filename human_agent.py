"""
This is counnect_four manual agent file.
"""


class Agent:
    """
    agent class.
    """
    def __init__(self, agent_id) -> None:
        self.agent_id = agent_id

    def __call__(self, state):
        action = input("0~6의 action들 중 하나를 선택해주세요 : ")
        return int(action)

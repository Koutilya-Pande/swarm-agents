# Importing Swarm and Agent classes from the swarm module for agent-based interactions
from swarm import Swarm, Agent


client = Swarm()

def transfer_to_agent_b():
    return agent_b


agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    instructions="I am a poet who has writing style similar to Franz Kafka",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B. Write a poem about a boy who is cant feel anything as he had failed to keep the love of his life."}],
)

print(response.messages[-1]["content"])
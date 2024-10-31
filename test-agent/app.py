from swarm import Swarm, Agent
from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Swarm and Tavily clients
client = Swarm()
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

# Define web search function for researcher
def web_search(query):
    print("\n🔍 Researcher performing web search for:", query)
    try:
        # Get both detailed response and context for comprehensive research
        search_response = tavily_client.search(query)
        search_context = tavily_client.get_search_context(query=query)
        print("✅ Web search completed successfully")
        return {
            'detailed_results': search_response,
            'context': search_context
        }
    except Exception as e:
        print("❌ Web search failed:", str(e))
        return f"Search error: {str(e)}"

# Define transfer functions for agent switching
def transfer_to_qualifier():
    print("\n🔄 Transferring to Lead Qualifier...")
    return lead_qualifier

def transfer_to_objection_handler():
    print("\n🔄 Transferring to Objection Handler...")
    return objection_handler

def transfer_to_closer():
    print("\n🔄 Transferring to Closer...")
    return closer

def transfer_to_researcher():
    print("\n🔄 Transferring to Researcher...")
    return researcher

# Initialize all agents
sales_manager = Agent(
    name="Sales Manager",
    model="gpt-4o-mini",
    instructions="""You are the Sales Team Manager. Your role is to:
    1. Be the first point of contact with potential customers
    2. Evaluate the situation and delegate tasks to appropriate team members
    3. Transfer to Lead Qualifier for initial prospect evaluation
    4. Transfer to Researcher when additional information is needed
    5. Transfer to Objection Handler when customer raises concerns
    6. Transfer to Closer when the prospect is ready to make a decision
    Always maintain a professional and coordinating role.""",
    functions=[transfer_to_qualifier, transfer_to_objection_handler, 
               transfer_to_closer, transfer_to_researcher],
)

lead_qualifier = Agent(
    name="Lead Qualifier",
    instructions="""You are the Lead Qualification Specialist. Your role is to:
    1. Ask qualifying questions to understand customer needs
    2. Determine if the prospect is a good fit for our solutions
    3. Gather basic information about the customer's business
    4. Assess budget, authority, needs, and timeline (BANT)
    5. Score leads based on their potential and readiness to buy
    Be thorough but efficient in your qualification process.""",
)

objection_handler = Agent(
    name="Objection Handler",
    instructions="""You are the Objection Handling Specialist. Your role is to:
    1. Address customer concerns professionally and empathetically
    2. Provide clear, factual responses to objections
    3. Use proven objection handling techniques
    4. Turn objections into opportunities
    5. Focus on value proposition when handling price objections
    Always maintain a solution-focused approach.""",
)

closer = Agent(
    name="Closer",
    instructions="""You are the Sales Closer. Your role is to:
    1. Take over qualified leads that show high buying intent
    2. Present final proposals and pricing
    3. Navigate final negotiations
    4. Create urgency when appropriate
    5. Guide prospects to making a positive buying decision
    Be confident and decisive while maintaining professionalism.""",
)

researcher = Agent(
    name="Researcher",
    model="gpt-4o",
    instructions="""You are the Sales Research Specialist. Your role is to:
    1. Perform web searches to gather relevant information using the web_search function
    2. Research prospect companies and their industries
    3. Analyze competitors and market trends
    4. Provide data-backed insights to the sales team
    5. Keep track of industry news and updates
    Be thorough and provide accurate, relevant information.""",
    functions=[web_search],
)

# Example usage
print("\n👋 Starting conversation with Sales Manager...")
while True:
    user_input = input("\n💬 Enter your message (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        print("\n👋 Ending conversation...")
        break
        
    print("\n🤖 Current agent: Sales Manager")
    response = client.run(
        agent=sales_manager,
        messages=[{"role": "user", "content": user_input}],
    )

    print("\n🗣️ Response:", response.messages[-1]["content"]) 
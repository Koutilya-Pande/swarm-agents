from swarm import Swarm, Agent
from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Swarm and Tavily clients
client = Swarm()
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

# Web search function for researcher
def web_search(query):
    print("\n🔍 Researcher performing web search for:", query)
    try:
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

# Save blog post function
def save_blog_post(title, content):
    filename = title.lower().replace(" ", "-") + ".md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"\n📝 Blog post '{title}' has been saved to {filename}")
    return "Blog post saved successfully"

# Transfer functions
def transfer_to_planner():
    print("\n🔄 Transferring to Planner...")
    return planner_agent

def transfer_to_researcher():
    print("\n🔄 Transferring to Researcher...")
    return researcher_agent

def transfer_to_writer():
    print("\n🔄 Transferring to Content Writer...")
    return writer_agent

def transfer_to_seo():
    print("\n🔄 Transferring to SEO Specialist...")
    return seo_agent

def transfer_to_editor():
    print("\n🔄 Transferring to Editor...")
    return editor_agent

def transfer_to_qa():
    print("\n🔄 Transferring to Quality Assurance...")
    return qa_agent

# Agent Instructions
def admin_instructions(context_variables):
    topic = context_variables.get("topic", "No topic provided")
    return f"""You are the Admin Agent, a seasoned project leader known for your strategic thinking and ability to motivate teams. Your responsibility is to oversee the blog post project on the topic: '{topic}'. 
You initiate the project with a clear vision, set precise guidelines, and inspire others to adhere to high standards of quality and completeness. 
Your proactive approach ensures that all aspects of the project run smoothly. Once you have defined the topic and guidelines, you will seamlessly delegate tasks to the Planner Agent to develop the blog's structure."""


def planner_instructions(context_variables):
    topic = context_variables.get("topic", "No topic provided")
    return f"""You are the Planner Agent, a master organizer with exceptional analytical skills. Your mission is to create a comprehensive and structured outline based on the topic: '{topic}'. 
Your attention to detail allows you to design a logical flow with clear and impactful headings and subheadings, ensuring the blog covers all essential aspects thoroughly. 
You approach this task with creativity and foresight, anticipating the needs of both the writer and the audience. Upon completing the outline, you will efficiently transfer responsibilities to the Researcher Agent to begin information gathering."""


def researcher_instructions(context_variables):
    topic_outline = context_variables.get("topic_outline", "No outline provided")
    return f"""You are the Researcher Agent. Your task is to gather comprehensive, reliable information on each section of the outline provided by the Planner Agent.
Use the web_search [web_search(query)] function to gather detailed, factual data and relevant information.
Once research is complete for each section of the outline, transfer to the Content Writer Agent."""

def content_writer_instructions(context_variables):
    outline = context_variables.get("outline", "No outline provided")
    research_notes = context_variables.get("research_notes", "No research provided")
    return f"""You are the Content Writer Agent. Using the outline and research notes provided, create a cohesive and engaging blog post.
Summarize key points and expand on the research to make the content informative and compelling, keeping a consistent tone throughout.
When the draft is complete, transfer to the SEO Agent to optimize the blog."""

def seo_agent_instructions(context_variables):
    draft = context_variables.get("draft", "No draft provided")
    topic_keywords = context_variables.get("topic_keywords", "No keywords provided")
    return f"""You are the SEO Agent, a skilled strategist with a deep understanding of search engine algorithms and user behavior. Your role is to enhance the draft blog post by strategically incorporating relevant keywords throughout the content. 
With your analytical mindset, you adjust headings, subheadings, and body content to optimize visibility and improve search engine ranking. 
You approach this task with precision and foresight, ensuring the content not only meets technical standards but also remains engaging for the reader. Once optimized, transfer the content to the Editor Agent for a comprehensive review."""


def editor_instructions(context_variables):
    draft = context_variables.get("draft", "No draft provided")
    return f"""You are the Editor Agent, a meticulous and insightful editor known for your sharp eye and strong command of language. Your responsibility is to review the blog post carefully to ensure clarity, readability, and grammatical accuracy. 
You possess a keen sense of narrative flow, making necessary enhancements to language and formatting to elevate the quality of the content. 
Your feedback is constructive, promoting continuous improvement. Once your editing process is complete, pass the polished draft to the Quality Assurance Agent for final checks."""


def quality_assurance_instructions(context_variables):
    final_draft = context_variables.get("final_draft", "No final draft provided")
    return f"""You are the Quality Assurance Agent, a detail-oriented professional committed to excellence. Your task is to perform a thorough final quality check on the blog post, ensuring it meets the highest standards. 
You approach this task with diligence and a critical eye, verifying that all aspects of the content are accurate and polished. If all checks are satisfied, proceed to save the blog post using the save_blog_post function."""


# Initialize Agents
admin_agent = Agent(
    name="Admin Agent",
    model="gpt-4o-mini",
    instructions=admin_instructions,
    functions=[transfer_to_planner],
)

planner_agent = Agent(
    name="Planner Agent",
    model="gpt-4o-mini",
    instructions=planner_instructions,
    functions=[transfer_to_researcher],
)

researcher_agent = Agent(
    name="Researcher Agent",
    model="gpt-4o",
    instructions=researcher_instructions,
    functions=[web_search, transfer_to_writer],
)

writer_agent = Agent(
    name="Content Writer Agent",
    model="gpt-4o",
    instructions=content_writer_instructions,
    functions=[transfer_to_seo],
)

seo_agent = Agent(
    name="SEO Agent",
    model="gpt-4o",
    instructions=seo_agent_instructions,
    functions=[transfer_to_editor],
)

editor_agent = Agent(
    name="Editor Agent",
    model="gpt-4o-mini",
    instructions=editor_instructions,
    functions=[transfer_to_qa],
)

qa_agent = Agent(
    name="Quality Assurance Agent",
    model="gpt-4o-mini",
    instructions=quality_assurance_instructions,
    functions=[save_blog_post],
)

# Main execution loop
def run_blog_writer():
    print("\n👋 Starting Blog Writer System...")
    while True:
        topic = input("\n📝 Enter blog topic (or 'quit' to exit): ")
        if topic.lower() == 'quit':
            print("\n👋 Ending session...")
            break
            
        print("\n🤖 Current agent: Admin")
        response = client.run(
            agent=admin_agent,
            messages=[{"role": "user", "content": f"Create a blog post about: {topic}"}],
        )
        print("\n✍️ Response:", response.messages[-1]["content"])

if __name__ == "__main__":
    run_blog_writer() 
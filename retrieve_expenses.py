from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model

def create_agent():
    llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
    agent_db = SQLDatabase.from_uri("sqlite:///instance/expenses.db")
    toolkit = SQLDatabaseToolkit(db=agent_db, llm=llm)
    tools = toolkit.get_tools()

    prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
    system_message = prompt_template.format(dialect="SQLite", top_k=5)
    print(prompt_template)
    print(system_message)
    agent_executor = create_react_agent(
        llm, tools, state_modifier=system_message
    )
    return agent_executor


def retrieve_expense(user_phone, user_query):
    agent_executor = create_agent()
    prompt_template = f"""
You are an expense tracking assistant that helps users manage and analyze their spending records.
Details:
- User phone number: {user_phone}
- Query: "{user_query}"

Instructions:
1. Retrieve expenses grouped by category (e.g., food, travel, bills).
2. For each expense, include its description and the date (formatted in dd-mm-yy).
3. Calculate and display the total expense amount.
4. If the user's spending has exceeded their budget, include a clear warning.
5. Compose the response using engaging language, emojis, and humor.
6. Present your final answer as a plain text message without any code or execution details.

Ensure the response is concise, informative, and attractively formatted.
"""

    events = agent_executor.stream(
        {"messages": [("user", prompt_template)]}, stream_mode="values"
    )
    print(prompt_template)
    last_response = """"""
    for event in events:
        last_response = event["messages"][-1].content
        # print(last_response)
        event["messages"][-1].pretty_print()

    return last_response

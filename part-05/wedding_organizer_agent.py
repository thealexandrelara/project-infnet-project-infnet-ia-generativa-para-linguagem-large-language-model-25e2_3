from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from lyrics_searcher import LyricsSearcher

from dotenv import load_dotenv

import os
import json

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def validate_and_convert_state(state):
    """
    Ensure that the state is always a Python dictionary
    """
    if isinstance(state, str):
        try:
            state = state.replace("'", '"')
            state = json.loads(state)
        except json.JSONDecodeError:
            raise ValueError(f"State must be a valid dictionary or JSON string {state=}")
    if not isinstance(state, dict):
        raise ValueError("State must be dictionary")
    return state

def get_lyrics(song_name: str, artist: str) -> str:
    return LyricsSearcher().get_lyrics(song_name, artist)

@tool
def get_lyrics_tool(state: dict | str) -> str:
    """
    Get the lyrics for a song.
    """
    state = validate_and_convert_state(state)
    song_name = state.get("song_name")
    artist = state.get("artist")
    state["lyrics"] = get_lyrics(song_name, artist)
    return json.dumps(state)

@tool
def check_lyrics(state: dict | str) -> str:
    """
    Checks if the current state contains the lyrics for the song.
    """
    state = validate_and_convert_state(state)
    if state.get("lyrics"):
        return "The lyrics are found. Final state reached"
    if not state.get("lyrics"):
        return "The lyrics are not found. I should stop. Final state reached."

custom_prompt = """
You are a professional wedding planner with a deep understanding of the etiquette, tone, and emotional atmosphere appropriate for weddings. Your task is to help clients decide whether a specific song is suitable to be played during a wedding ceremony or reception.

You have the following tools at your disposal: {tool_names}
Descriptions of tools: {tools}.

To use a tool, respond exactly in this format:

Thought: [Your reasoning about what action to take next]
Action: [The name of the tool to use]
Action Input: [The song name and the artist]
Observation: check if the lyrics are appropriate for a wedding.

Example:
    Thought: I should get the lyrics for the song.
    Action: get_lyrics_tool
    Action Input: {{"artist": "Taylor Swift", "song_name": "Cornelia Street"}}
    Observation: The lyrics are for the song "Cornelia Street" by Taylor Swift

Once you have the lyrics for the song, you must carefully review the lyrics. Your evaluation should identify any inappropriate content, such as:
- Explicit language (e.g., profanity, vulgar terms)
- Sexual content or innuendos
- Themes of violence, heartbreak, or infidelity
- Negative, aggressive, or depressing tone
- Lyrics that contradict the spirit of love, unity, or celebration

If you don't find the lyrics, respond:
    Thought: I should stop. Final state reached.
    Final Answer: The lyrics are not found [suggest user to check the song name and artist].

Make sure to:
    1.	Review the lyrics in detail. Highlight any problematic lines or phrases.
    2.	Explain clearly why a lyric or theme may be considered inappropriate for a wedding.
    3.	Give your final recommendation: whether the song is appropriate or not for a wedding with the reasoning for your recommendation.
    4.  Respond:
        Thought: I have reviewed the lyrics. I should stop.
        Final Answer: [Your final answer translated to Portuguese]

Begin with the current state:
{input}

{agent_scratchpad}
"""

tools = [
    get_lyrics_tool,
    check_lyrics
]


prompt_template = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template=custom_prompt
)

llm = OpenAI()

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)
agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

if __name__ == "__main__":
    artist = "Jorge e Mateus"
    song_name = "Amo Noite e Dia"
    response = agent_executer.invoke({"input": json.dumps({"artist": artist, "song_name": song_name}), "agent_scratchpad": "", "tools": [tool.description for tool in tools], "tool_names": [tool.name for tool in tools]})
    print(response)
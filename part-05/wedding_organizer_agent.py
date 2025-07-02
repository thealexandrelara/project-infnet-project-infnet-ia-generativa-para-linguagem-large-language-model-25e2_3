from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from lyrics_searcher import LyricsSearcher
from json_parser import validate_and_convert_state

from dotenv import load_dotenv

import os
import json

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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
    return json.dumps(state, ensure_ascii = False)

@tool
def check_lyrics(state: dict | str) -> str:
    """
    Checks if the current state contains the lyrics for the song.
    """
    state = validate_and_convert_state(state)
    if state.get("lyrics"):
        return "The lyrics are found. I should review the lyrics and check if they are appropriate for a wedding."
    if not state.get("lyrics"):
        return "The lyrics are not found. I should stop."

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

Make sure to:
    1.	Review the lyrics in detail. Highlight any problematic lines or phrases.
    2.	Explain clearly why a lyric or theme may be considered inappropriate for a wedding.
    3.	Give your final recommendation: whether the song is appropriate or not for a wedding with the reasoning for your recommendation.
    4.  Respond:
        Thought: I have reviewed the lyrics. I should stop.
        Final Answer: {{"appropriate": "true" | "false", "reason": "[Your reasoning MUST be in Portuguese]"}}

Begin with the current state:
{input}

{agent_scratchpad}
"""

tools = [
    get_lyrics_tool,
    check_lyrics
]

class WeddingOrganizerAgent:

    def __init__(self):
        self.llm = OpenAI()
        prompt_template = PromptTemplate(
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
            template=custom_prompt
        )
        agent = create_react_agent(llm=self.llm, tools=tools, prompt=prompt_template)
        self.agent_executer = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    def evaluate_song(self, song_name: str, artist: str) -> dict:
        response = self.agent_executer.invoke({"input": json.dumps({"artist": artist, "song_name": song_name}), "agent_scratchpad": "", "tools": [tool.description for tool in tools], "tool_names": [tool.name for tool in tools]})
        return response["output"]




if __name__ == "__main__":
    artist = "Taylor Swift"
    song_name = "Cornelia Street"
    response = WeddingOrganizerAgent().evaluate_song(song_name, artist)
    print(response)
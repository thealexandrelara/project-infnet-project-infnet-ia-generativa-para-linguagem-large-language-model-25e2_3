from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from lyrics_searcher import LyricsSearcher
from typing import Dict, Any, Union

from dotenv import load_dotenv

import os
import json
import ast

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def validate_and_convert_state(state: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ensure that the state is always a Python dictionary with proper unicode handling
    """
    if isinstance(state, dict):
        return state
    
    if not isinstance(state, str):
        raise ValueError("State must be dictionary or string")
    
    # Try multiple parsing strategies
    parsing_strategies = [
        # Strategy 1: Parse as JSON directly (handles proper JSON)
        lambda s: json.loads(s),
        
        # Strategy 2: Use ast.literal_eval (handles Python dict literals safely)
        lambda s: ast.literal_eval(s),
        
        # Strategy 3: Try to fix common JSON issues and parse
        lambda s: json.loads(fix_json_string(s)),
    ]
    
    for i, strategy in enumerate(parsing_strategies):
        try:
            result = strategy(state)
            if isinstance(result, dict):
                return result
            else:
                raise ValueError(f"Parsed result is not a dictionary: {type(result)}")
        except (json.JSONDecodeError, ValueError, SyntaxError):
            if i == len(parsing_strategies) - 1:  # Last strategy failed
                raise ValueError(f"State must be a valid dictionary or JSON string. "
                               f"All parsing strategies failed. Original state length: {len(state)}, "
                               f"starts with: {repr(state[:100])}")
            continue  # Try next strategy

def fix_json_string(s: str) -> str:
    """
    Attempt to fix common JSON formatting issues
    """
    # Remove any leading/trailing whitespace
    s = s.strip()
    
    # If it doesn't start and end with braces, it's likely not a JSON object
    if not (s.startswith('{') and s.endswith('}')):
        raise ValueError("String doesn't appear to be a JSON object")
    
    # Try to handle the case where the string is truncated
    # Count braces to see if we have a complete object
    open_braces = s.count('{')
    close_braces = s.count('}')
    
    if open_braces > close_braces:
        # String appears to be truncated - we can't fix this
        raise ValueError("JSON string appears to be truncated (unmatched braces)")
    
    return s

# Alternative function for handling potentially truncated data
def validate_and_convert_state_safe(state: Union[str, Dict[str, Any]], 
                                   allow_truncated: bool = False) -> Dict[str, Any]:
    """
    Safer version that can handle truncated JSON strings by extracting what's parseable
    """
    if isinstance(state, dict):
        return state
    
    if not isinstance(state, str):
        raise ValueError("State must be dictionary or string")
    
    # First try the normal validation
    try:
        return validate_and_convert_state(state)
    except ValueError as e:
        if not allow_truncated:
            raise e
        
        # Try to extract a valid JSON object from truncated data
        return extract_partial_json(state)

def extract_partial_json(s: str) -> Dict[str, Any]:
    """
    Try to extract a valid JSON object from potentially truncated string
    """
    s = s.strip()
    if not s.startswith('{'):
        raise ValueError("String doesn't start with '{'")
    
    # Find the last complete key-value pair
    brace_count = 0
    last_valid_pos = 0
    
    for i, char in enumerate(s):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                last_valid_pos = i + 1
                break
        elif char == ',' and brace_count == 1:
            # Try to parse up to this point + closing brace
            test_json = s[:i] + '}'
            try:
                return json.loads(test_json)
            except json.JSONDecodeError:
                continue
    
    if last_valid_pos > 0:
        try:
            return json.loads(s[:last_valid_pos])
        except json.JSONDecodeError:
            pass
    
    raise ValueError("Could not extract valid JSON from truncated string")

# def validate_and_convert_state(state):
#     """
#     Ensure that the state is always a Python dictionary
#     """
#     if isinstance(state, str):
#         try:
#             state = state.replace("'", '"')
#             state = json.loads(state)
#         except json.JSONDecodeError:
#             raise ValueError(f"State must be a valid dictionary or JSON string {state=}")
#     if not isinstance(state, dict):
#         raise ValueError("State must be dictionary")
#     return state

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
import json
import ast
from typing import Dict, Any, Union


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
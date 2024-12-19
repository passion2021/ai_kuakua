import re
from typing import Any
from utils.dirty_json import DirtyJson
import regex
import ast
from typing import Union


def extract_struct(text: str, data_type: Union[type(list), type(dict)]) -> Union[list, dict]:
    """Extracts and parses a specified type of structure (dictionary or list) from the given text.
    The text only contains a list or dictionary, which may have nested structures.

    Args:
        text: The text containing the structure (dictionary or list).
        data_type: The data type to extract, can be "list" or "dict".

    Returns:
        - If extraction and parsing are successful, it returns the corresponding data structure (list or dictionary).
        - If extraction fails or parsing encounters an error, it throw an exception.

    Examples:
        >>> text = 'xxx [1, 2, ["a", "b", [3, 4]], {"x": 5, "y": [6, 7]}] xxx'
        >>> result_list = extract_struct(text, "list")
        >>> print(result_list)
        >>> # Output: [1, 2, ["a", "b", [3, 4]], {"x": 5, "y": [6, 7]}]

        >>> text = 'xxx {"x": 1, "y": {"a": 2, "b": {"c": 3}}} xxx'
        >>> result_dict = extract_struct(text, "dict")
        >>> print(result_dict)
        >>> # Output: {"x": 1, "y": {"a": 2, "b": {"c": 3}}}
    """
    # Find the first "[" or "{" and the last "]" or "}"
    start_index = text.find("[" if data_type is list else "{")
    end_index = text.rfind("]" if data_type is list else "}")

    if start_index != -1 and end_index != -1:
        # Extract the structure part
        structure_text = text[start_index: end_index + 1]

        try:
            # Attempt to convert the text to a Python data type using ast.literal_eval
            result = ast.literal_eval(structure_text)

            # Ensure the result matches the specified data type
            if isinstance(result, (list, dict)):
                return result

            raise ValueError(f"The extracted structure is not a {data_type}.")

        except (ValueError, SyntaxError) as e:
            raise Exception(f"Error while extracting and parsing the {data_type}: {e}")
    else:
        print(f"No {data_type} found in the text.")
        return [] if data_type is list else {}


def json_parse_dirty(json: str) -> dict[str, Any] | None:
    ext_json = extract_json_object_string(json)
    if ext_json:
        data = DirtyJson.parse_string(ext_json)
        if isinstance(data, dict): return data
    return None


def extract_json_object_string(content):
    start = content.find('{')
    if start == -1:
        return ""

    # Find the first '{'
    end = content.rfind('}')
    if end == -1:
        # If there's no closing '}', return from start to the end
        return content[start:]
    else:
        # If there's a closing '}', return the substring from start to end
        return content[start:end + 1]


def extract_json_string(content):
    # Regular expression pattern to match a JSON object
    pattern = r'\{(?:[^{}]|(?R))*\}|\[(?:[^\[\]]|(?R))*\]|"(?:\\.|[^"\\])*"|true|false|null|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?'

    # Search for the pattern in the content
    match = regex.search(pattern, content)

    if match:
        # Return the matched JSON string
        return match.group(0)
    else:
        return ""


def fix_json_string(json_string):
    # Function to replace unescaped line breaks within JSON string values
    def replace_unescaped_newlines(match):
        return match.group(0).replace('\n', '\\n')

    # Use regex to find string values and apply the replacement function
    fixed_string = re.sub(r'(?<=: ")(.*?)(?=")', replace_unescaped_newlines, json_string, flags=re.DOTALL)
    return fixed_string


if __name__ == '__main__':
    json_string = ''' # 输出格式
    {
        "thoughts": "你的想法",
        "response":"你的回复",
    }'''

    print(json_parse_dirty(json_string), type(json_parse_dirty(json_string)))

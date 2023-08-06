import json
from typing import Any, Dict, Union


def parse_ipynb(content_or_str: Union[str, dict]) -> dict:
    """
    "Smartly" parse content that contains a notebook.

    * If a string, it's first JSON deserialized.
    * If it's a "wrapped" dict (i.e. contains "type" == "notebook" and "content"), unwraps the content
    * Asserts the content smells like a notebook ("nbformat")

    :param content: See above.
    :return: Notebook data.
    """
    if isinstance(content_or_str, str):
        content = json.loads(content_or_str)
    else:
        content = content_or_str
    if not isinstance(content, dict):
        raise ValueError('Ipynb not a dict')
    assert isinstance(content, dict)
    if content.get('type') == 'notebook':
        content = content['content']

    nbformat = content.get('nbformat')
    if not isinstance(nbformat, int):
        raise ValueError('Nbformat value %s invalid' % nbformat)
    return content


def get_notebook_parameters(content: Union[str, dict]) -> dict:
    code = get_notebook_tagged_code(content, "parameters")
    return execute_cell_code(code, tag="parameters")


def get_notebook_inputs(content: Union[str, dict]) -> dict:
    code = get_notebook_tagged_code(content, "inputs")
    return execute_cell_code(code, tag="inputs")


def get_notebook_tagged_code(content: Union[str, dict], tag: str) -> str:
    obj = parse_ipynb(content)
    result = ""
    for cell in obj['cells']:
        if (
            cell
            and 'source' in cell
            and 'metadata' in cell
            and 'tags' in cell['metadata']
            and tag in cell['metadata']['tags']
        ):
            result += '%s\r\n' % ''.join(cell['source'])
    return result


def get_type_name(value: Union[str, int, None]) -> str:
    pythonic_name = type(value).__name__
    if pythonic_name == 'int':
        return "integer"
    if pythonic_name == 'bool':
        return "flag"
    if pythonic_name == 'str':
        return "string"
    return pythonic_name


def execute_cell_code(code: str, tag: str) -> dict:
    ns: Dict[str, Any] = {}
    try:
        compiled = compile(code, "<CODE>", "exec")
    except SyntaxError as err:
        raise SyntaxError(
            f"Syntax error in notebook cell tagged \"{tag}\" at line {err.lineno}: {err}."
        ) from err
    try:
        exec(compiled, globals(), ns)
    except Exception as err:
        raise Exception(
            f"Error executing notebook cell tagged \"{tag}\": {err}"
        ) from err
    return ns

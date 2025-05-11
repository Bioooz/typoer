"""
typoer.py

Core logic for simulating human typing, including typos, corrections, and code/coding support. Used by both CLI and GUI.
"""
import keyboard
import time
import random
import string
import re
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('typoer_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def typoer(
    text,
    wpm=100,
    accuracy=1.0,
    backspace_duration=0.1,
    correction_coefficient=0.4,
    wait_key=None,
    break_key="escape",
    is_code=False,
    language="plaintext",
    auto_indent=False,
    smart_quotes=True,
    smart_brackets=True,
    auto_complete=True,
    use_shift_enter=False,
    **kwargs
):
    """
    Simulate human typing with realistic typos, corrections, and code formatting.

    Parameters:
        text (str): The text to type.
        wpm (int): Typing speed in words per minute. Default is 100.
        accuracy (float): Typing accuracy (0-1). Default is 1.0 (no typos).
        backspace_duration (float): Time taken for backspace. Default is 0.1.
        correction_coefficient (float): Likelihood of correcting typos. Default is 0.4.
        wait_key (str|None): Key to press to start typing. Default is None.
        break_key (str): Key to press to stop typing. Default is 'escape'.
        is_code (bool): Whether to use code/coding mode. Default is False.
        language (str): Language for code mode. Default is 'plaintext'.
        auto_indent (bool): Whether to auto-indent code. Default is False.
        smart_quotes (bool): Use smart quote handling. Default is True.
        smart_brackets (bool): Use smart bracket handling. Default is True.
        auto_complete (bool): Use code auto-completion. Default is True.
        use_shift_enter (bool): Use Shift+Enter for newlines. Default is False.
        **kwargs: Additional options for future extension.

    Returns:
        None
    """
    logging.info("Starting typing simulation")
    logging.debug(f"Parameters: wpm={wpm}, accuracy={accuracy}, is_code={is_code}, language={language}")
    base_delay = 60.0 / (wpm * 5)
    special_chars = {
        '!': ['shift', '1'], '@': ['shift', '2'], '#': ['shift', '3'], '$': ['shift', '4'], '%': ['shift', '5'],
        '^': ['shift', '6'], '&': ['shift', '7'], '*': ['shift', '8'], '(': ['shift', '9'], ')': ['shift', '0'],
        '_': ['shift', '-'], '+': ['shift', '='], '{': ['shift', '['], '}': ['shift', ']'], '|': ['shift', '\\'],
        ':': ['shift', ';'], '"': ['shift', "'"], '<': ['shift', ','], '>': ['shift', '.'], '?': ['shift', '/'], '~': ['shift', '`']
    }
    if wait_key:
        logging.info(f"Waiting for key: {wait_key}")
        while True:
            if keyboard.is_pressed(wait_key):
                break
            time.sleep(0.1)
    lines = text.split('\n')
    safe_typo_chars = string.ascii_letters + string.digits
    try:
        for line in lines:
            if break_key and keyboard.is_pressed(break_key):
                logging.info("Break key detected, stopping typing")
                return
            for char in line:
                if break_key and keyboard.is_pressed(break_key):
                    logging.info("Break key detected, stopping typing")
                    return
                logging.debug(f"Typing character: {char}")
                if char in special_chars:
                    logging.debug(f"Handling special character: {char}")
                    for key in special_chars[char]:
                        keyboard.press(key)
                    for key in reversed(special_chars[char]):
                        keyboard.release(key)
                else:
                    keyboard.write(char)
                time.sleep(base_delay)
            keyboard.press_and_release('enter')
            time.sleep(base_delay)
    except Exception as e:
        logging.error(f"Error during typing: {str(e)}", exc_info=True)
        raise
    finally:
        logging.info("Typing simulation completed")
    code_chars = {
        'python': {'def': 'def', 'class': 'class', 'import': 'import', 'from': 'from', 'return': 'return', 'if': 'if', 'else': 'else', 'elif': 'elif', 'while': 'while', 'for': 'for', 'in': 'in', 'try': 'try', 'except': 'except', 'finally': 'finally', 'with': 'with', 'as': 'as', 'raise': 'raise', 'pass': 'pass', 'break': 'break', 'continue': 'continue', 'yield': 'yield', 'async': 'async', 'await': 'await', 'lambda': 'lambda', 'None': 'None', 'True': 'True', 'False': 'False', 'self': 'self', 'cls': 'cls'},
        'php': {'<?php': '<?php', '?>': '?>', '$': '$', '->': '->', '::': '::', 'function': 'function', 'class': 'class', 'public': 'public', 'private': 'private', 'protected': 'protected', 'static': 'static', 'const': 'const', 'return': 'return', 'if': 'if', 'else': 'else', 'elseif': 'elseif', 'while': 'while', 'for': 'for', 'foreach': 'foreach', 'as': 'as', 'try': 'try', 'catch': 'catch', 'finally': 'finally', 'throw': 'throw', 'new': 'new', 'null': 'null', 'true': 'true', 'false': 'false', '$this': '$this', 'self': 'self'},
        'javascript': {'function': 'function', 'class': 'class', 'const': 'const', 'let': 'let', 'var': 'var', 'return': 'return', 'if': 'if', 'else': 'else', 'while': 'while', 'for': 'for', 'in': 'in', 'of': 'of', 'try': 'try', 'catch': 'catch', 'finally': 'finally', 'throw': 'throw', 'new': 'new', 'null': 'null', 'undefined': 'undefined', 'true': 'true', 'false': 'false', 'this': 'this', 'super': 'super', 'async': 'async', 'await': 'await', 'export': 'export', 'import': 'import', 'default': 'default'},
        'java': {'public': 'public', 'private': 'private', 'protected': 'protected', 'class': 'class', 'interface': 'interface', 'extends': 'extends', 'implements': 'implements', 'static': 'static', 'final': 'final', 'abstract': 'abstract', 'void': 'void', 'int': 'int', 'long': 'long', 'float': 'float', 'double': 'double', 'boolean': 'boolean', 'char': 'char', 'String': 'String', 'return': 'return', 'if': 'if', 'else': 'else', 'while': 'while', 'for': 'for', 'try': 'try', 'catch': 'catch', 'finally': 'finally', 'throw': 'throw', 'new': 'new', 'null': 'null', 'true': 'true', 'false': 'false', 'this': 'this', 'super': 'super'},
        'cpp': {'class': 'class', 'struct': 'struct', 'public': 'public', 'private': 'private', 'protected': 'protected', 'virtual': 'virtual', 'override': 'override', 'const': 'const', 'static': 'static', 'inline': 'inline', 'void': 'void', 'int': 'int', 'long': 'long', 'float': 'float', 'double': 'double', 'bool': 'bool', 'char': 'char', 'string': 'string', 'return': 'return', 'if': 'if', 'else': 'else', 'while': 'while', 'for': 'for', 'try': 'try', 'catch': 'catch', 'throw': 'throw', 'new': 'new', 'delete': 'delete', 'nullptr': 'nullptr', 'true': 'true', 'false': 'false', 'this': 'this'}
    }
    auto_complete_patterns = {
        'python': {'if': 'if :', 'for': 'for in :', 'while': 'while :', 'def': 'def ():', 'class': 'class :', 'try': 'try:\n    \nexcept :', 'with': 'with as :'},
        'php': {'if': 'if () {', 'for': 'for (;;) {', 'while': 'while () {', 'function': 'function () {', 'class': 'class  {', 'try': 'try {\n    \n} catch () {', 'foreach': 'foreach ( as ) {'},
        'javascript': {'if': 'if () {', 'for': 'for (;;) {', 'while': 'while () {', 'function': 'function () {', 'class': 'class  {', 'try': 'try {\n    \n} catch () {', 'forof': 'for (const  of ) {'}
    }
    lang_chars = code_chars.get(language, {}) if is_code else {}
    lang_patterns = auto_complete_patterns.get(language, {}) if is_code and auto_complete else {}
    in_string = False
    string_char = None
    bracket_stack = []
    logging.debug("Initializing pyautogui")
    time.sleep(0.1)
    try:
        for char in text:
            if break_key and keyboard.is_pressed(break_key):
                logging.info("Break key detected, stopping typing")
                break
            logging.debug(f"Typing character: {char}")
            if char in special_chars:
                logging.debug(f"Handling special character: {char}")
                for key in special_chars[char]:
                    keyboard.press(key)
                for key in reversed(special_chars[char]):
                    keyboard.release(key)
            else:
                keyboard.write(char)
            if smart_quotes and char in ['"', "'"]:
                if not in_string:
                    in_string = True
                    string_char = char
                    logging.debug(f"Entering string with {char}")
                elif char == string_char:
                    in_string = False
                    string_char = None
                    logging.debug(f"Exiting string with {char}")
            if char == '.':
                time.sleep(0.05)
            elif char == ',':
                time.sleep(0.02)
            elif char == ':':
                time.sleep(0.02)
            elif char == ';':
                time.sleep(0.02)
            elif char == '?':
                time.sleep(0.05)
            elif char == '!':
                time.sleep(0.05)
            elif char == '\n':
                time.sleep(0.05)
            else:
                time.sleep(base_delay)
            if random.random() > accuracy and not in_string:
                logging.debug("Making a typo")
                typo = random.choice(safe_typo_chars.replace(char, ''))
                keyboard.write(typo)
                time.sleep(0.01)
                keyboard.press_and_release('backspace')
                time.sleep(backspace_duration)
                if random.random() < correction_coefficient:
                    logging.debug("Correcting typo")
                    keyboard.write(char)
                    time.sleep(base_delay)
    except Exception as e:
        logging.error(f"Error during typing: {str(e)}", exc_info=True)
        raise
    finally:
        logging.info("Typing simulation completed") 
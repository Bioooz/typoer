

# Documentation

See `typoer.py`
=======
# Typoer

A universal Python typing simulator that mimics human typing, including typos, corrections, and code formatting. Typoer works as a command-line tool, GUI application, or Python package, and supports advanced features for both text and code.


## Installation

You can install Typoer using pip:

```bash
pip install .
```

Or install directly from the repository:

```bash
pip install git+https://github.com/Bioooz/typoer.git
```

---

## Usage

### GUI Application

```bash
typoer-gui
```

- Text/code input area
- Adjustable typing settings (WPM, accuracy, etc.)
- Customizable keybinds (default: Ctrl+Shift+T)
- Start/Stop buttons, status indicator
- Code/coding support (tabs, newlines, PHP tags)
- Macro recording/playback
- Theme selection

### Command Line

```bash
# Type a simple text
typoer "Hello, World!"

# Type with custom settings
typoer "Hello, World!" --wpm 120 --accuracy 0.8 --wait-key right

# Type text from a file
cat file.txt | typoer

# Type with all options
typoer "Hello, World!" --wpm 100 --accuracy 0.9 --backspace-duration 0.1 --correction-coefficient 0.4 --wait-key right --break-key escape
```

### Python Package

```python
from typoer import typoer

# Basic usage
typoer("Hello, World!")

# Advanced usage
typoer(
    text="Hello, World!",
    wpm=120,
    accuracy=0.8,
    backspace_duration=0.1,
    correction_coefficient=0.4,
    wait_key='right',
    break_key='escape'
)
```

---

## Parameters
- `text`: The text to be typed
- `wpm`: Average typing speed in words per minute (default: 100)
- `accuracy`: Typing accuracy between 0 and 1 (default: 1.0)
- `backspace_duration`: Time taken for backspace to be pressed (default: 0.1)
- `correction_coefficient`: Determines how many typos are made before correcting (default: 0.4)
- `wait_key`: Key to press to start typing (default: none)
- `break_key`: Key to press to stop typing (default: 'escape')



---

## Contributing

Contributions, issues, and feature requests are welcome!
- Fork the repo and submit a pull request
- Open an issue for bugs or suggestions

---

## License

MIT License

---

## Links
- [GitHub Repository](https://github.com/Bioooz/typoer)
- [Report Issues](https://github.com/Bioooz/typoer/issues)

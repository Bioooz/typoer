from typoer.typoer import typoer
import time

def test_typoer():
    # Wait 3 seconds to give user time to focus on a text editor
    print("Starting in 3 seconds... Please focus on a text editor.")
    time.sleep(3)
    
    # Test text to type
    test_text = """Hello! This is a test of the Typoer application.
It should type this text with some realistic typos and corrections.
Let's see how it handles special characters: !@#$%^&*()
And some code-like text: if (x > 0) { return true; }"""

    # Run typoer with moderate settings
    typoer(
        text=test_text,
        wpm=80,  # Moderate typing speed
        accuracy=0.95,  # 95% accuracy
        backspace_duration=0.1,
        correction_coefficient=0.7,
        wait_key="f2",  # Press F2 to start typing
        break_key="escape",  # Press Escape to stop
        is_code=False
    )

if __name__ == "__main__":
    test_typoer() 
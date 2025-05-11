import argparse
import sys
from .typoer import typoer

def main():
    parser = argparse.ArgumentParser(description='Simulate human typing with realistic typos')
    parser.add_argument('text', nargs='?', help='Text to type. If not provided, reads from stdin')
    parser.add_argument('--wpm', type=int, default=100, help='Typing speed in words per minute')
    parser.add_argument('--accuracy', type=float, default=1.0, help='Typing accuracy (0-1)')
    parser.add_argument('--backspace-duration', type=float, default=0.1, help='Time taken for backspace')
    parser.add_argument('--correction-coefficient', type=float, default=0.4, help='Typo correction coefficient')
    parser.add_argument('--wait-key', type=str, default='', help='Key to press to start typing')
    parser.add_argument('--break-key', type=str, default='escape', help='Key to press to stop typing')

    args = parser.parse_args()

    # Get text from stdin if not provided as argument
    if not args.text:
        if not sys.stdin.isatty():
            args.text = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)

    try:
        typoer(
            text=args.text,
            wpm=args.wpm,
            accuracy=args.accuracy,
            backspace_duration=args.backspace_duration,
            correction_coefficient=args.correction_coefficient,
            wait_key=args.wait_key,
            break_key=args.break_key
        )
    except KeyboardInterrupt:
        print("\nTyping interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 
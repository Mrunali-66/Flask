#!/usr/bin/env python3
"""
Morse Code Converter
Converts text to Morse code and Morse code back to text
"""

# Morse Code Dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.', '0': '-----', ',': '--..--',
    '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Reverse dictionary for decoding
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}


def text_to_morse(text):
    """Convert text to Morse code"""
    morse = []
    text = text.upper()
    
    for char in text:
        if char in MORSE_CODE_DICT:
            morse.append(MORSE_CODE_DICT[char])
        elif char == ' ':
            morse.append('/')
        else:
            # Skip unknown characters
            continue
    
    return ' '.join(morse)


def morse_to_text(morse):
    """Convert Morse code to text"""
    text = []
    morse_chars = morse.split(' ')
    
    for code in morse_chars:
        if code in REVERSE_MORSE_DICT:
            text.append(REVERSE_MORSE_DICT[code])
        else:
            # Add placeholder for unknown codes
            text.append('?')
    
    return ''.join(text)


def print_banner():
    """Print program banner"""
    print("\n" + "="*50)
    print("     MORSE CODE CONVERTER")
    print("="*50)
    print("  •–•  Text ↔ Morse Code Translator  •–•")
    print("="*50 + "\n")


def print_menu():
    """Print menu options"""
    print("\nWhat would you like to do?")
    print("  [1] Convert Text to Morse Code")
    print("  [2] Convert Morse Code to Text")
    print("  [3] View Morse Code Chart")
    print("  [4] Exit")
    print("-" * 50)


def display_morse_chart():
    """Display the Morse code reference chart"""
    print("\n" + "="*50)
    print("           MORSE CODE REFERENCE CHART")
    print("="*50)
    
    # Letters
    print("\n📝 LETTERS:")
    letters = {k: v for k, v in MORSE_CODE_DICT.items() if k.isalpha()}
    for i, (letter, code) in enumerate(letters.items(), 1):
        print(f"  {letter} = {code:8}", end="")
        if i % 4 == 0:
            print()
    
    # Numbers
    print("\n\n🔢 NUMBERS:")
    numbers = {k: v for k, v in MORSE_CODE_DICT.items() if k.isdigit()}
    for i, (num, code) in enumerate(numbers.items(), 1):
        print(f"  {num} = {code:8}", end="")
        if i % 5 == 0:
            print()
    
    # Punctuation
    print("\n\n✏️  PUNCTUATION:")
    punctuation = {k: v for k, v in MORSE_CODE_DICT.items() 
                   if not k.isalnum() and k != ' '}
    for symbol, code in punctuation.items():
        print(f"  {symbol} = {code:8}", end="")
    
    print("\n\n💡 TIP: Use '/' to represent spaces between words")
    print("="*50 + "\n")


def main():
    """Main program loop"""
    print_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\n" + "-"*50)
            text = input("Enter text to convert to Morse: ").strip()
            if text:
                morse = text_to_morse(text)
                print(f"\n✓ Original Text: {text}")
                print(f"✓ Morse Code:    {morse}")
            else:
                print("⚠ No text entered!")
            print("-"*50)
        
        elif choice == '2':
            print("\n" + "-"*50)
            print("Enter Morse code (separate letters with spaces)")
            print("Use '/' for word spaces")
            morse = input("Morse code: ").strip()
            if morse:
                text = morse_to_text(morse)
                print(f"\n✓ Morse Code:  {morse}")
                print(f"✓ Decoded Text: {text}")
            else:
                print("⚠ No Morse code entered!")
            print("-"*50)
        
        elif choice == '3':
            display_morse_chart()
        
        elif choice == '4':
            print("\n" + "="*50)
            print("  Thanks for using Morse Code Converter!")
            print("  •–• •–• •–•  73 (Best Regards)  •–• •–• •–•")
            print("="*50 + "\n")
            break
        
        else:
            print("\n⚠ Invalid choice! Please enter 1, 2, 3, or 4.")
        
        input("\nPress Enter to continue...")
        print("\n" * 2)


if __name__ == "__main__":
    main()
# Typing Speed Test App using Tkinter
# Author: Jiya

from tkinter import *
import time
import random

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x500")
        self.root.config(bg="#F8F8F8")

        # Sample texts for typing
        self.samples = [
            "The quick brown fox jumps over the lazy dog.",
            "Typing is a fundamental skill that improves with daily practice.",
            "Python is a powerful and easy to learn programming language.",
            "Discipline and consistency are key to becoming a great developer.",
            "Artificial Intelligence is transforming the world in remarkable ways."
        ]

        self.sample_text = StringVar()
        self.sample_text.set(random.choice(self.samples))
        self.start_time = None

        Label(root, text="Typing Speed Test", font=("Helvetica", 20, "bold"), bg="#F8F8F8", fg="#333").pack(pady=20)
        self.sample_label = Label(root, textvariable=self.sample_text, wraplength=700, justify="center", font=("Arial", 14), bg="#F8F8F8", fg="#444")
        self.sample_label.pack(pady=20)

        # Text box for typing
        self.text_entry = Text(root, height=6, width=80, font=("Arial", 12))
        self.text_entry.pack(pady=10)
        self.text_entry.bind("<FocusIn>", self.start_typing)

        # Buttons
        Button(root, text="Check Speed", command=self.calculate_speed, font=("Arial", 12), bg="#0078D7", fg="white", padx=10, pady=5).pack(pady=10)
        Button(root, text="New Test", command=self.new_test, font=("Arial", 12), bg="#28A745", fg="white", padx=10, pady=5).pack(pady=5)

        # Results Label
        self.result_label = Label(root, text="", font=("Arial", 14, "bold"), bg="#F8F8F8", fg="#333")
        self.result_label.pack(pady=10)

    def start_typing(self, event):
        """Start the timer when user begins typing"""
        if self.start_time is None:
            self.start_time = time.time()

    def calculate_speed(self):
        """Calculate typing speed in words per minute (WPM)"""
        if not self.start_time:
            self.result_label.config(text="Start typing first!")
            return

        end_time = time.time()
        time_taken = end_time - self.start_time  # seconds
        typed_text = self.text_entry.get("1.0", END).strip()
        typed_words = typed_text.split()
        total_words = len(typed_words)
        wpm = (total_words / time_taken) * 60 if time_taken > 0 else 0

        # Accuracy calculation
        sample_words = self.sample_text.get().split()
        correct = sum(1 for i, word in enumerate(typed_words) if i < len(sample_words) and word == sample_words[i])
        accuracy = (correct / len(sample_words)) * 100 if sample_words else 0

        result = f"Time Taken: {time_taken:.1f} sec | Speed: {wpm:.1f} WPM | Accuracy: {accuracy:.1f}%"
        self.result_label.config(text=result)

    def new_test(self):
        """Start a new typing test"""
        self.sample_text.set(random.choice(self.samples))
        self.text_entry.delete("1.0", END)
        self.result_label.config(text="")
        self.start_time = None


# Run the app
if __name__ == "__main__":
    root = Tk()
    TypingSpeedApp(root)
    root.mainloop()

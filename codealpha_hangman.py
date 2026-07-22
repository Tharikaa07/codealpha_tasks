import random

HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    ---------
    """
]

WORDS = {
    "easy": [
        ("cat", "A common household pet."),
        ("book", "You read this."),
        ("sun", "It shines in the sky.")
    ],
    "medium": [
        ("python", "A popular programming language."),
        ("developer", "Someone who writes code."),
        ("keyboard", "You type on this.")
    ],
    "hard": [
        ("internship", "A temporary work experience program."),
        ("algorithm", "A step-by-step problem-solving process."),
        ("certificate", "You get this after completing a course.")
    ]
}

def choose_difficulty():
    print("Choose difficulty: easy / medium / hard")
    while True:
        choice = input("Your choice: ").lower().strip()
        if choice in WORDS:
            return choice
        print("Please type easy, medium, or hard.")

def display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def play_hangman():
    print("=" * 45)
    print(" WELCOME TO HANGMAN - CodeAlpha Edition")
    print("=" * 45)

    difficulty = choose_difficulty()
    word, hint = random.choice(WORDS[difficulty])
    guessed_letters = []
    wrong_guesses = 0
    max_wrong_guesses = 6
    hints_used = 0
    max_hints = 3

    while wrong_guesses < max_wrong_guesses:
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"The word has {len(word)} letters.")
        print("Word: " + display_word(word, guessed_letters))
        print(f"Wrong guesses: {wrong_guesses}/{max_wrong_guesses}")
        print(f"Guessed letters: {', '.join(guessed_letters) if guessed_letters else 'None'}")
        print(f"Hints used: {hints_used}/{max_hints} (each hint costs 1 wrong guess)")

        guess = input("Guess a letter, the full word, type 'hint', or 'giveup': ").lower().strip()

        if guess == "giveup":
            print(HANGMAN_STAGES[wrong_guesses])
            print(f"No problem! The word was '{word}'. Better luck next time!")
            return

        if len(guess) > 1 and guess.isalpha() and guess != "hint":
            if guess == word:
                guessed_letters = list(set(word))
                print(HANGMAN_STAGES[wrong_guesses])
                print(f"🎉 Congratulations! You guessed the full word '{word}' correctly!")
                return
            else:
                wrong_guesses += 1
                print(f"'{guess}' is not the correct word.\n")
                if wrong_guesses >= max_wrong_guesses:
                    break
                continue

        if guess == "hint":
            if hints_used >= max_hints:
                print("You've used all your hints!\n")
                continue
            if wrong_guesses + 1 >= max_wrong_guesses:
                print("Not enough wrong-guess room left to safely use a hint!\n")
                continue

            hints_used += 1
            wrong_guesses += 1  # penalty for using a hint

            if hints_used == 1:
                print(f"Hint: {hint}\n")
            else:
                # Reveal a random unguessed letter as an extra hint
                unrevealed = [l for l in set(word) if l not in guessed_letters]
                if unrevealed:
                    reveal_letter = random.choice(unrevealed)
                    guessed_letters.append(reveal_letter)
                    print(f"Hint: The letter '{reveal_letter}' is in the word!\n")
                else:
                    print("No more letters left to reveal!\n")
            continue

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single valid letter.\n")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.\n")
            continue

        guessed_letters.append(guess)

        if guess in word:
            print(f"Nice! '{guess}' is in the word.\n")
        else:
            wrong_guesses += 1
            print(f"'{guess}' is not in the word.\n")

        if all(letter in guessed_letters for letter in word):
            print(HANGMAN_STAGES[wrong_guesses])
            print(f"🎉 You guessed it! The word was '{word}'")
            return

    print(HANGMAN_STAGES[wrong_guesses])
    print(f"💀 Game over! The word was '{word}'")

if __name__ == "__main__":
    play_hangman()

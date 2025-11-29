import random

# Basic amino-acid table with properties.
# You can simplify or tweak if you want.
AMINO_ACIDS = {
    "A": {"name": "Alanine",       "charge": "neutral", "polarity": "nonpolar", "aromatic": "non-aromatic"},
    "R": {"name": "Arginine",      "charge": "positive", "polarity": "polar",   "aromatic": "non-aromatic"},
    "N": {"name": "Asparagine",    "charge": "neutral", "polarity": "polar",   "aromatic": "non-aromatic"},
    "D": {"name": "Aspartate",     "charge": "negative", "polarity": "polar",  "aromatic": "non-aromatic"},
    "C": {"name": "Cysteine",      "charge": "neutral", "polarity": "polar",   "aromatic": "non-aromatic"},
    "E": {"name": "Glutamate",     "charge": "negative", "polarity": "polar",  "aromatic": "non-aromatic"},
    "Q": {"name": "Glutamine",     "charge": "neutral", "polarity": "polar",   "aromatic": "non-aromatic"},
    "G": {"name": "Glycine",       "charge": "neutral", "polarity": "nonpolar","aromatic": "non-aromatic"},
    "H": {"name": "Histidine",     "charge": "positive", "polarity": "polar",  "aromatic": "non-aromatic"},
    "I": {"name": "Isoleucine",    "charge": "neutral", "polarity": "nonpolar","aromatic": "non-aromatic"},
    "L": {"name": "Leucine",       "charge": "neutral", "polarity": "nonpolar","aromatic": "non-aromatic"},
    "K": {"name": "Lysine",        "charge": "positive", "polarity": "polar",  "aromatic": "non-aromatic"},
    "M": {"name": "Methionine",    "charge": "neutral", "polarity": "nonpolar","aromatic": "non-aromatic"},
    "F": {"name": "Phenylalanine", "charge": "neutral", "polarity": "nonpolar","aromatic": "aromatic"},
    "P": {"name": "Proline",       "charge": "neutral", "polarity": "nonpolar","aromatic": "non-aromatic"},
    "S": {"name": "Serine",        "charge": "neutral", "polarity": "polar",   "aromatic": "non-aromatic"},
    "T": {"name": "Threonine",     "charge": "neutral", "polarity": "polar",   "aromatic": "non-aromatic"},
    "W": {"name": "Tryptophan",    "charge": "neutral", "polarity": "nonpolar","aromatic": "aromatic"},
    "Y": {"name": "Tyrosine",      "charge": "neutral", "polarity": "polar",   "aromatic": "aromatic"},
    "V": {"name": "Valine",        "charge": "neutral", "polarity": "nonpolar","aromatic": "non-aromatic"},
}

CATEGORY_OPTIONS = {
    "charge": ["positive", "negative", "neutral"],
    "polarity": ["polar", "nonpolar"],
    "aromatic": ["aromatic", "non-aromatic"],
}


def get_random_amino_acid(rng: random.Random | None = None) -> tuple[str, dict]:
    """Return a random (code, properties_dict) pair."""
    if rng is None:
        rng = random
    code = rng.choice(list(AMINO_ACIDS.keys()))
    return code, AMINO_ACIDS[code]


def get_property(code: str, category: str) -> str:
    """Return the property (e.g. 'positive') for a given amino acid and category."""
    code = code.upper()
    if code not in AMINO_ACIDS:
        raise ValueError(f"Unknown amino acid code: {code}")
    if category not in CATEGORY_OPTIONS:
        raise ValueError(f"Unknown category: {category}")
    return AMINO_ACIDS[code][category]


def check_answer(code: str, category: str, user_answer: str) -> bool:
    """Return True if the user's answer matches the true property (case-insensitive)."""
    correct = get_property(code, category)
    return user_answer.strip().lower() == correct.lower()


def ask_category_from_user() -> str:
    """Interactively ask the user which category they want to practice."""
    print("Choose a category to practice:")
    for i, cat in enumerate(CATEGORY_OPTIONS.keys(), start=1):
        print(f"{i}. {cat}")

    while True:
        choice = input("Enter number (or 'q' to quit): ").strip().lower()
        if choice in ("q", "quit"):
            raise SystemExit("Goodbye!")
        try:
            idx = int(choice) - 1
            categories = list(CATEGORY_OPTIONS.keys())
            if 0 <= idx < len(categories):
                return categories[idx]
        except ValueError:
            pass
        print("Invalid choice, please try again.")


def ask_num_questions() -> int:
    """Ask the user how many questions they want."""
    while True:
        raw = input("How many questions would you like? (e.g. 5, 10): ").strip()
        try:
            n = int(raw)
            if n > 0:
                return n
        except ValueError:
            pass
        print("Please enter a positive integer.")


def play_round(category: str, rng: random.Random | None = None) -> bool:
    """
    Play a single round.
    Returns True if the user was correct, False otherwise.
    """
    code, props = get_random_amino_acid(rng)
    name = props["name"]
    options = CATEGORY_OPTIONS[category]

    print(f"\nAmino acid: {name} ({code})")
    print(f"Category: {category}")
    print("Options:", ", ".join(options))

    user_answer = input("Your answer: ")
    if check_answer(code, category, user_answer):
        print("✅ Correct!")
        return True
    else:
        correct = get_property(code, category)
        print(f"❌ Incorrect. The correct answer was: {correct}.")
        return False


def main() -> None:
    print("Welcome to the Amino Acid Classification Quiz!\n")
    category = ask_category_from_user()
    num_questions = ask_num_questions()

    print(f"\nYou chose category: {category}")
    print(f"Number of questions: {num_questions}\n")

    score = 0
    for _ in range(num_questions):
        if play_round(category):
            score += 1

    print(f"\nGame over! Your score: {score}/{num_questions}")
    if score == num_questions:
        print("Perfect! 🧬✨")
    elif score > num_questions / 2:
        print("Nice job, keep practicing!")
    else:
        print("Good effort! Try again to improve your score.")


if __name__ == "__main__":
    main()

import json
import random
import time

CARDS_DIR = "cards"
CONFIG_FILE = "config.json"
DEFAULT_NUM_CARDS = 10
LANGUAGE = "en"  # Default language, changeable via user input
OUTPUT_DIR = "output"
SIGNIFICATOR = None  # Global significator card, to be set later
VERSION = "1.0.0"


def load_json(file_path):
    """Loads and reads content of json file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if file_path == CONFIG_FILE:
                if 'version' not in data or data['version'] != VERSION:
                    raise ValueError(
                        f"Config version mismatch. Expected {VERSION}")
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {file_path}: {str(e)}")
        raise


def get_language_choice():
    """Prompt the user to select a language."""
    global LANGUAGE
    while True:
        choice = input(
            "Choose language/Wybierz język (en/pl): ").lower().strip()
        if choice in ['en', 'pl']:
            LANGUAGE = choice
            break
        print("Invalid choice. Enter 'en' or 'pl'.")


def get_significator():
    """Prompt the user to choose a significator card."""
    while True:
        try:
            choice = int(
                input(f"Choose the Significator card (0-77): ").strip())
            if 0 <= choice <= 77:
                return choice
            print("Number must be between 0 and 77.")
        except ValueError:
            print("Invalid number. Try again.")


def generate_seed():
    """Generate a random seed based on user input."""
    while True:
        seed = input("Enter a random seed string (letters/numbers): ").strip()
        if seed and seed.replace(" ", "").isalnum():
            return seed
        print("Please enter valid alphanumeric characters.")


def draw_cards(config, seed, num_cards=DEFAULT_NUM_CARDS):
    """Draw random cards, excluding the significator."""
    random.seed(seed)
    if LANGUAGE == 'pl':
        available_cards = [key for key in config.keys() if key.endswith('_pl')]
        significator_pl = str(SIGNIFICATOR) + '_pl'
        if significator_pl in available_cards:
            available_cards.remove(significator_pl)
    else:
        available_cards = [key for key in config.keys(
        ) if not key.endswith('_pl') and key.isdigit()]
        if str(SIGNIFICATOR) in available_cards:
            available_cards.remove(str(SIGNIFICATOR))

    drawn_cards = random.sample(available_cards, num_cards)
    return drawn_cards


def display_cards(config):
    """Display available cards based on language."""
    print("Available cards:" if LANGUAGE == 'en' else "Dostępne karty:")
    for key, name in config.items():
        if LANGUAGE == 'en':
            if key.isdigit():
                print(f"{key}: {name}")
        else:
            if not (key.isdigit()):
                print(f"{str(key).rstrip('_pl')}: {name}")


def display_spread(config, cards, detailed=False):
    """Display a spread of cards, with optional detailed information."""
    try:
        card_translation = 'CARD' if LANGUAGE == 'en' else "KARTA"
        meaning_translation = 'Meaning' if LANGUAGE == 'en' else "Znaczenie"
        significator_key = str(SIGNIFICATOR) + \
            ('_pl' if LANGUAGE == 'pl' else '')

        print("\nDetailed Card Layout:" if detailed else "\nInitial Card Layout:")
        print(
            f"Significator: {config[significator_key if LANGUAGE == 'pl' else str(SIGNIFICATOR)]}\n")

        for i, card in enumerate(cards, 1):
            if detailed:
                card_base_key = card.rstrip('_pl')
                card_data = load_json(f"{CARDS_DIR}/{card_base_key}.json")
                meaning_key = 'reversed_meaning' if i == 2 else 'upright_meaning'
                meaning = card_data.get(
                    f"{meaning_key}_{LANGUAGE}", card_data.get(meaning_key, "N/A"))
                if meaning == "N/A":
                    print(f"Warning: Missing meaning for card {card_base_key}")
                print(
                    f"{card_translation} {i} - {config[card if LANGUAGE == 'pl' else card.rstrip('_pl')]} | {meaning_translation}: {meaning}")
            else:
                print(
                    f"{card_translation} {i} - {config[card if LANGUAGE == 'pl' else card.rstrip('_pl')]}")
    except Exception as e:
        print(f"Error displaying spread: {str(e)}")
        raise


def prepare_inference_payload(config, cards):
    try:
        significator_key = str(SIGNIFICATOR) + \
            ('_pl' if LANGUAGE == 'pl' else '')
        payload = {
            "significator": {
                "card": config[significator_key if LANGUAGE == 'pl' else str(SIGNIFICATOR)],
                "number": SIGNIFICATOR
            },
            "cards": []
        }

        for i, card in enumerate(cards, 1):
            card_base_key = card.rstrip('_pl')
            card_data = load_json(f"{CARDS_DIR}/{card_base_key}.json")

            if not card_data:
                raise ValueError(
                    f"Empty or invalid card data for {card_base_key}")

            card_info = {
                "position": i,
                "card": config[card if LANGUAGE == 'pl' else card.rstrip('_pl')],
                "number": int(card_base_key),
                "meaning": card_data.get(f"{'reversed_meaning' if i == 2 else 'upright_meaning'}_{LANGUAGE}",
                                         card_data.get('reversed_meaning' if i == 2 else 'upright_meaning', "N/A"))
            }
            payload["cards"].append(card_info)

        return payload
    except Exception as e:
        print(f"Error preparing inference payload: {str(e)}")
        raise


def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    import os
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def save_layout(config, cards, filename_prefix="tarot"):
    ensure_output_directory()
    timestamp = int(time.time())
    safe_prefix = sanitize_filename(filename_prefix)

    filename = f"{OUTPUT_DIR}/{safe_prefix}_{timestamp}.txt"
    inference_filename = f"{OUTPUT_DIR}/{safe_prefix}_inference_{timestamp}.json"

    # Save basic layout
    with open(filename, 'w', encoding='utf-8') as f:
        significator_key = str(SIGNIFICATOR) + \
            ('_pl' if LANGUAGE == 'pl' else '')
        f.write(
            f"Significator: {config[significator_key if LANGUAGE == 'pl' else str(SIGNIFICATOR)]}\n\n")
        for i, card in enumerate(cards, 1):
            f.write(
                f"CARD {i}: {config[card if LANGUAGE == 'pl' else card.rstrip('_pl')]}\n")

    # Save inference payload
    inference_payload = prepare_inference_payload(config, cards)
    with open(inference_filename, 'w', encoding='utf-8') as f:
        json.dump(inference_payload, f, ensure_ascii=False, indent=2)

    print(f"Layout saved to {filename}")
    print(f"Inference payload saved to {inference_filename}")


def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    return "".join(c for c in filename if c.isalnum() or c in "._- ")


def main():
    """Main function to run the Tarot application."""
    try:
        validate_cards_directory()
        get_language_choice()
        config = load_json(CONFIG_FILE)
        validate_config(config)

        display_cards(config)

        global SIGNIFICATOR
        SIGNIFICATOR = get_significator()

        seed = generate_seed()
        drawn_cards = draw_cards(config, seed)

        display_spread(config, drawn_cards)
        input("Press Enter to see the detailed layout...")
        display_spread(config, drawn_cards, detailed=True)
        save_choice = input("Save layout to file? (y/n): ").lower()
        if save_choice in ['y', 't']:
            save_layout(config, drawn_cards)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def validate_config(config):
    """Validate configuration file structure."""
    if not isinstance(config, dict):
        raise ValueError("Config must be a dictionary")
    if not config:
        raise ValueError("Config is empty")

    # Sprawdź czy są wszystkie wymagane karty (0-77)
    for i in range(78):
        if str(i) not in config:
            raise ValueError(f"Missing card number {i} in config")
        if f"{i}_pl" not in config:
            raise ValueError(f"Missing Polish translation for card {i}")

    return True


def validate_cards_directory():
    """Check if cards directory exists and contains required files."""
    import os
    if not os.path.isdir(CARDS_DIR):
        raise ValueError(f"Cards directory '{CARDS_DIR}' not found")

    for i in range(78):
        card_file = f"{CARDS_DIR}/{i}.json"
        if not os.path.isfile(card_file):
            raise ValueError(f"Missing card file: {card_file}")


if __name__ == "__main__":
    main()

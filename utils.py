import json
import random

vowels = "aeiou"


def is_vowel(letter):
    return letter.lower() in vowels


def get_consonant_group(letter):
    soft_consonants = "bdgjzv"
    hard_consonants = "ptkqc"
    other_consonants = "fhmlnrswxy"
    if letter.lower() in soft_consonants:
        return soft_consonants
    elif letter.lower() in hard_consonants:
        return hard_consonants
    else:
        return other_consonants


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump([d.__dict__ for d in data], f, indent=2)

def mess_up_email(email: str, unchanged_probability: float = 0.9):
    if random.random() > unchanged_probability:
        return email.replace('@', '_at_')
    return email

def typo(word, unchanged_probability: float = 0.5):
    if random.random() > unchanged_probability:
        return word

    word_list = list(word)

    random_index = random.randint(0, len(word) - 1)

    original_letter = word_list[random_index]

    if is_vowel(original_letter):
        replacement_letter = original_letter
        while replacement_letter == original_letter:
            replacement_letter = random.choice(vowels)
    else:
        consonant_group = get_consonant_group(original_letter)
        replacement_letter = original_letter
        while replacement_letter == original_letter:
            replacement_letter = random.choice(consonant_group)

    if original_letter.isupper():
        replacement_letter = replacement_letter.upper()

    word_list[random_index] = replacement_letter

    return ''.join(word_list)

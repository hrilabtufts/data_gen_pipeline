from enum import Enum
import random


class NameGenders(Enum):
    EVEN_SPLIT_MALE_FEMALE_NEUTRAL = 0
    EVEN_SPLIT_MALE_FEMALE_CODED = 1
    ONLY_MALE_CODED = 2
    ONLY_FEMALE_CODED = 3
    ONLY_NEUTRAL = 4


# we need some names and here's what chatgpt recommended for male coded, female
# coded, and gender neutral.
MALE_CODED_NAMES = [
    "Ethan",
    "Liam",
    "Noah",
    "Benjamin",
    "Alexander",
    "Michael",
    "Samuel",
    "Daniel",
    "Matthew",
    "James",
    "David",
    "William",
    "Joseph",
    "Christopher",
    "Andrew",
    "Gabriel",
    "Jacob",
    "Henry",
    "Anthony",
    "Oliver",
]

FEMALE_CODED_NAMES = [
    "Emma",
    "Olivia",
    "Ava",
    "Sophia",
    "Isabella",
    "Mia",
    "Charlotte",
    "Amelia",
    "Harper",
    "Evelyn",
    "Abigail",
    "Emily",
    "Elizabeth",
    "Sofia",
    "Grace",
    "Lily",
    "Victoria",
    "Scarlett",
    "Hannah",
    "Avery",
]

GENDER_NEUTRAL_NAMES = [
    "Alex",
    "Bailey",
    "Cameron",
    "Charlie",
    "Casey",
    "Jordan",
    "Morgan",
    "Reese",
    "Taylor",
    "Avery",
    "Riley",
    "Jamie",
    "Skylar",
    "Peyton",
    "Quinn",
    "Finley",
    "Hayden",
    "Kai",
    "Logan",
    "Parker",
]

NAMES = MALE_CODED_NAMES + FEMALE_CODED_NAMES + GENDER_NEUTRAL_NAMES


def sample_names(
    num, gender: NameGenders = NameGenders.EVEN_SPLIT_MALE_FEMALE_NEUTRAL, exclude=[]
):
    sample_from = []

    if gender == NameGenders.EVEN_SPLIT_MALE_FEMALE_NEUTRAL:
        sample_from = NAMES
    elif gender == NameGenders.EVEN_SPLIT_MALE_FEMALE_CODED:
        sample_from = MALE_CODED_NAMES + FEMALE_CODED_NAMES
    elif gender == NameGenders.ONLY_FEMALE_CODED:
        sample_from = FEMALE_CODED_NAMES
    elif gender == NameGenders.ONLY_MALE_CODED:
        sample_from = MALE_CODED_NAMES
    elif gender == NameGenders.ONLY_NEUTRAL:
        sample_from = GENDER_NEUTRAL_NAMES

    sample_from = [x for x in sample_from if x not in exclude]
    return random.sample(sample_from, num)


def sample_name(
    gender: NameGenders = NameGenders.EVEN_SPLIT_MALE_FEMALE_NEUTRAL, exclude=[]
):
    return sample_names(num=1, gender=gender, exclude=exclude)[0]

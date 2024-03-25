from conditions import PromptGenerator, NameGenerator
from helpers import sample_names, sample_name
import text_generation


def generate_demo_one():
    people = sample_names(10)
    sunny = PromptGenerator("on a sunny day,") + people
    rainy = PromptGenerator("on a rainy day,") + people

    sunny = sunny + "could" + ["go to the beach", "go for a walk", "go for a run"]
    rainy = rainy + "could" + ["read a book", "watch a movie"]

    things_to_do = sunny & rainy
    things_to_do_with = things_to_do + "with" + sample_names(4, exclude=people)
    return things_to_do_with


def generate_demo_two():
    name_one = NameGenerator()
    name_two = NameGenerator()
    p = PromptGenerator()

    return (
        p
        + name_one
        + "and"
        + name_two
        + "went to the store, where"
        + name_one
        + "bought"
        + ["a book", "a movie", "a game"]
        + "and"
        + name_two
        + "bought"
        + ["lunch", "pens", "coffee"]
    )


def generate_demo_three():
    name_one = NameGenerator()
    name_two = NameGenerator()
    p1 = PromptGenerator()
    p2 = PromptGenerator()

    settings = ["in a cafe", "in the kitchen", "in the dining room"]
    things = ["clean mug", "full mug", "dirty mug"]
    actions = ["serving", "drinking", "cleaning"]

    p1 = (
        p1
        + name_one
        + "and"
        + name_two
        + "are"
        + settings
        + ". "
        + name_one
        + "is"
        + actions
        + "a"
        + things
        + "while"
        + name_two
        + "is"
        + actions
        + "a"
        + things
        + "."
    )

    p2 = (
        p2
        + name_one
        + "and"
        + name_two
        + "are"
        + settings
        + ". "
        + name_one
        + "is"
        + actions
        + "a"
        + things
        + ". There is a basketball on the table."
        + name_one
        + 'says, "grab it.". What does '
        + name_two
        + "grab?"
    )

    return p1 & p2


def prompt_demo_one():
    prompts = generate_demo_one()
    prompts = text_generation.expand(prompts)
    prompts = text_generation.summarize(prompts)


def paper_demo():
    seen_prompt = PromptGenerator("$NAME_1")
    image_prompt = PromptGenerator("Cartoon art.")
    image_prompt = image_prompt + "in a" + ["cafe", "house"]
    seen_prompt = seen_prompt + "is at" + ["a cafe", "$NAME_2's house"]
    image_prompt = (
        image_prompt
        + "one person sits and"
        + ["an employee cleans up", "an employee serves coffee"]
        + '.'
    )
    seen_prompt = (
        seen_prompt
        + "and $NAME_2 is"
        + ["an employee cleaning up", "a host serving coffee"]
    )
    seen_prompt = (
        seen_prompt
        + ". A"
        + ["clean mug and dirty mug", "full mug and empty mug"]
        + "are on the table."
    )
    image_prompt = (
        image_prompt
        + "a"
        + ["clean mug and dirty mug", "full mug and empty mug"]
        + "are on the table."
    )
    all_seen_prompts = seen_prompt.all_combinations()
    all_img_prompts = image_prompt.all_combinations()

    seen_names = []
    seen_prompts = []

    for prompt in all_seen_prompts:
        name_1 = sample_name(exclude=seen_names)
        seen_names.append(name_1)
        name_2 = sample_name(exclude=seen_names)
        seen_names.append(name_2)

        prompt = prompt.replace("$NAME_1", name_1)
        prompt = prompt.replace("$NAME_2", name_2)

        seen_prompts.append(prompt)
    print(len(all_seen_prompts))

    print('---')
    print('\n'.join(seen_prompts))
    print('---')
    print('\n'.join(all_img_prompts))
    print('---')

if __name__ == "__main__":
    paper_demo()

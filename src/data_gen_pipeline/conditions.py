# /usr/bin/env python3

from typing import List, Union
import helpers


class PromptGenerator:
    def __init__(
        self,
        optional_starting_content: Union[
            List, str, "PromptGenerator", "NameGenerator"
        ] = "",
    ):
        self._slots = []
        if optional_starting_content != "":
            self.__add__(optional_starting_content)

    def __add__(self, content: Union[List, str, "PromptGenerator", "NameGenerator"]):
        if isinstance(content, list):
            self._slots.append(content)
        elif isinstance(content, str):
            self._slots.append(content)
        elif isinstance(content, PromptGenerator):
            self._slots.append(content)
        elif isinstance(content, NameGenerator):
            self._slots.append(content)
        else:
            raise TypeError(f"Unsupported type {type(content)}")

        return self

    def __iadd__(self, other):
        return self.__add__(other)

    def __and__(self, other):
        this_list = self.all_combinations()
        that_list = other.all_combinations()
        return PromptGenerator(this_list + that_list)

    def _display_format_slots(self):
        r = ""
        for slot in self._slots:
            if isinstance(slot, PromptGenerator):
                r += slot._display_format_slots()
            elif isinstance(slot, list) or isinstance(slot, str):
                r += f"{slot}\n"
            else:
                raise TypeError(f"Unsupported type {type(slot)}")
        return r

    def all_combinations(self):
        r = [""]
        for slot in self._slots:
            if isinstance(slot, PromptGenerator):
                r += slot.all_combinations()
            elif isinstance(slot, NameGenerator):
                for i in range(len(r)):
                    r[i] += " " + slot.sample_if_empty(exclude_str=r[i])
            elif isinstance(slot, list):
                rlen = len(r)
                r *= len(slot)
                s = [[x] * rlen for x in slot]
                flat_list = [item for sublist in s for item in sublist]
                for i in range(len(r)):
                    r[i] += flat_list[i] + " "
                    r[i] = r[i].replace("  ", " ").replace(" .", ".")
            elif isinstance(slot, str):
                for i in range(len(r)):
                    r[i] += slot + " "
            else:
                raise TypeError(f"Unsupported type {type(slot)}")
        return r

    def __repr__(self):
        return f"PromptGenerator({self._display_format_slots()})"

    def __str__(self):
        return "\n".join(self.all_combinations())


class NameGenerator:
    def __init__(self, gender=helpers.NameGenders.EVEN_SPLIT_MALE_FEMALE_NEUTRAL):
        self.name = None
        self.gender = gender

    def sample(self, exclude_str=None):
        exclude = []
        if exclude_str:
            for c in ".,/<>'\";:][}{|+=-_)(*&^%$#@!~`\\":
                exclude_str = exclude_str.replace(c, "")
            exclude = exclude_str.split(" ")
        self.name = helpers.sample_name(exclude=exclude, gender=self.gender)
        return str(self)

    def sample_if_empty(self, exclude_str=None):
        if not self.name:
            self.sample(exclude_str)
        return str(self)

    def __str__(self):
        return self.name + " " if self.name else ""

    def __add__(self, other):
        self.sample_if_empty()
        assert self.name is not None
        return self.name + " " + other

    def __iadd__(self, other):
        self.sample_if_empty()
        assert self.name is not None
        return self.name + " " + other

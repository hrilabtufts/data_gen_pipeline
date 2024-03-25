#!/usr/bin/env python3

from typing import List, Union, Tuple


class Result:
    def __init__(self, success: bool, message: str = ""):
        assert type(success) is bool
        assert type(message) is str
        self.success = success
        self.message = message

    def __bool__(self):
        return self.success

    def __repr__(self):
        return (
            f"Operation {'was' if self.success else 'not'} successful: {self.message}"
        )


class ConfigWrapper(object):
    def __init__(self):
        self._output_path = None
        self._scene_prompts = None
        self._generate_scene_prompts = False
        self._people_prompts = None
        self._generate_people = False
        self._settings_prompts = None
        self._generate_settings = False
        self._num_people = None
        self._action_prompts = None
        self._generate_actions = False
        self._name_gender = NameGenders.EVEN_SPLIT

    def _strip_prompt(self, p: str):
        p = p.lower()  # make lowercase
        p = "".join(c for c in p if 0 < ord(c) < 127)  # consider only ascii characters
        p = p.lstrip(" ")
        p = p.rstrip(" ")
        p = p.strip("\t\r\b\n")
        return p

    def set_output_path(self, path) -> Result:
        try:
            # check that the path is valid: does the directory exist and is it empty?
            if not path.exists:
                return Result(False, "That path doesn't seem to exist.")
            if not path.empty:
                return Result(
                    False,
                    "That directory doesn't seem to be empty. \
                                      Making the safety-based assumption to not \
                                      continue. Override with 'allow override \
                                      directory' parameter.",
                )
            self._output_path = path
            return Result(True)
        except Exception as e:
            return Result(False, str(e.args))

    def set_scene_prompts(self, prompts: List[str]) -> Result:
        if type(prompts) is not list:
            return Result(False, "Scene prompts must be in the form of a list")
        for n, p in enumerate(prompts):
            if type(p) is not str:
                return Result(False, f"Scene prompt #{n} is not a string: {str(p)}")
            if self._scene_prompts is None:
                self._scene_prompts = []
            self._scene_prompts.append(self._strip_prompt(p))
        return Result(True)

    def set_generate_scene_prompts(self, generate_scene_prompts: bool) -> Result:
        if type(generate_scene_prompts) is not bool:
            return Result(
                False, "set generate scene prompts must be set using a bool type."
            )
        self._generate_scene_prompts = generate_scene_prompts
        return Result(True)

    def set_people_prompts(self, people: List) -> Result:
        if type(people) is not list:
            return Result(False, "Setting people must be done in the form of a list")
        for n, p in enumerate(people):
            if type(p) is not str:
                return Result(False, f"Person #{n} is not a string: {str(p)}")
            if self._people_prompts is None:
                self._people_prompts = []
            stripped = self._strip_prompt(p)
            contains_whitespace = stripped.count(" ") != 0
            if contains_whitespace:
                return Result(
                    False,
                    "Names should be only one world long (entry #{n} contains \
                    whitespace: {p})",
                )
            self._people_prompts.append(stripped)
        return Result(True)

    def set_generate_people_prompts(self, generate_people: bool) -> Result:
        if type(generate_people) is not bool:
            return Result(
                False, "set generate scene prompts must be set using a bool type."
            )
        self._generate_people = generate_people
        return Result(True)

    def set_settings_prompts(self, settings: List) -> Result:
        if type(settings) is not list:
            return Result(
                False, "Configuring settings must be done in the form of a list"
            )
        for n, p in enumerate(settings):
            if type(p) is not str:
                return Result(False, f"Setting #{n} is not a string: {str(p)}")
            if self._settings_prompts is None:
                self._settings_prompts = []
            self._settings_prompts.append(self._strip_prompt(p))
        return Result(True)

    def set_generate_settings_prompts(self, generate_settings: bool) -> Result:
        if type(generate_settings) is not bool:
            return Result(
                False,
                "set generate settings prompts must be set \
                          using a bool type.",
            )
        self._generate_settings = generate_settings
        return Result(True)

    def set_num_people(self, num_people: Union[int, Tuple[int, int]]) -> Result:
        try:
            input_type = type(num_people)
            self._num_people = num_people
            if type(num_people) is tuple:
                self._min_num_people = min(input_type)  # type:ignore
                self._max_num_people = max(input_type)  # type:ignore
            elif type(num_people) is int:
                self._min_num_people = num_people
                self._max_num_people = num_people
            else:
                return Result(
                    False,
                    "input type must be either a single integer, or a pair of \
                    integers to specify a range.",
                )
            return Result(True)

        except Exception as e:
            return Result(False, str(e.args))

    def set_action_prompts(self, actions: List) -> Result:
        if type(actions) is not list:
            return Result(False, "Actions must be in the form of a list")
        for n, p in enumerate(actions):
            if type(p) is not str:
                return Result(False, f"Action #{n} is not a string: {str(p)}")
            if self._action_prompts is None:
                self._action_prompts = []
            self._action_prompts.append(self._strip_prompt(p))
        return Result(True)

    def set_generate_action_prompts(self, generate_actions: bool) -> Result:
        try:
            assert (
                type(generate_actions) is bool
            ), "action prompts must be set using bool type"
            self._generate_actions = generate_actions
            return Result(True)
        except Exception as e:
            return Result(False, str(e.args))

    def check_valid_config(self) -> Result:
        is_valid = True
        reasons = []
        if not self._output_path:
            is_valid = False
            reasons.append("You must set a valid output directory.")
        if not self._scene_prompts:
            is_valid = False
            reasons.append(
                "You must specify some scenes to either use directly, or to \
                expand upon."
            )
        if not self._people_prompts:
            pass  # If you don't specify people, that's fine. We'll just use our list.
        if not self._settings_prompts:
            is_valid = False
            reasons.append(
                "You must specify some settings in which your scenes take \
                place, so that we can use them directly or expand upon them."
            )
        if not self._num_people:
            is_valid = False
            reasons.append(
                "You must specify either a set number of people per scene, or a \
                tuple containing a range of people per scene."
            )
        if not self._action_prompts:
            is_valid = False
            reasons.append(
                "You must specify actions for the people in each scene, so \
                that we can use them directly or expand upon them."
            )
        return Result(is_valid, f"{' '.join(reasons) if len(reasons) > 0 else ''}")

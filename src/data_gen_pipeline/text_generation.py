import openai


class TextGenerator:
    def __init__(self, api_key, engine="davinci"):
        openai.api_key = api_key
        self.engine = engine

    def get_text(self, prompt, n=1):
        response = openai.Completion.create(prompt=prompt, n=n, engine=self.engine)

        return response

    def summarize(self, prompt, n=1):
        prompt = "Summarize the following:\n" + prompt
        response = openai.Completion.create(prompt=prompt, n=n, engine=self.engine)

        return response

    def expand(self, prompt):
        prompt = "Expand the following:\n" + prompt
        response = openai.Completion.create(prompt=prompt, engine=self.engine)

        return response

from models import Message
class LLMClient:

    def __init__(self, api_url, api_key, model):
        this.api_url = api_url
        this.api_key = api_key
        this.model = model

    def call(self, messages: list[Message], list[dict])
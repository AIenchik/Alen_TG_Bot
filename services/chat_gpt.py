from openai import AsyncOpenAI


class ChatGptService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def ask(self, messages: list) -> str:
        response = await self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=700,
            temperature=0.4,
        )
        answer = response.choices[0].message.content

        return answer
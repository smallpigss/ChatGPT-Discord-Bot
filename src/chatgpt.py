from src.models import ModelInterface
from src.memory import MemoryInterface


class ChatGPT:
    def __init__(self, model: ModelInterface, memory: MemoryInterface):
        self.model = model
        self.memory = memory

    def get_response(self, user_id: str, text: str) -> str:
        self.memory.append(user_id, {'role': 'user', 'content': text})
        response = self.model.chat_completion(self.memory.get(user_id))
        role = response['choices'][0]['message']['role']
        content = response['choices'][0]['message']['content']
        self.memory.append(user_id, {'role': role, 'content': content})
        return content

    def get_midjourney_response(self, user_id: str, text: str) -> str:
        content = '''
        As a prompt generator for a generative AI called "Midjourney", you will create image prompts for the AI to visualize. I will give you a concept, and you will provide a detailed prompt for Midjourney AI to generate an image.

Please adhere to the structure and formatting below, and follow these guidelines:

- Do not use the words "description" or ":" in any form.
- Do not place a comma between [ar] and [v].
- Write each prompt in one line without using return.

Structure:
[1] = %s

Formatting: 
Follow this prompt structure: "/imagine prompt: [1], [2], [3], [4], [5], [6], [ar] [v]".

Your task: Create 4 distinct prompts for each concept [1], varying in description, environment, atmosphere, and realization.

- Write your prompts in English.
- Do not describe unreal concepts as "real" or "photographic".
- Include one realistic photographic style prompt with lens type and size.
- Separate different prompts with two new lines.

Example Prompts:
Prompt 1:
/imagine prompt: A stunning Halo Reach landscape with a Spartan on a hilltop, lush green forests surround them, clear sky, distant city view, focusing on the Spartan's majestic pose, intricate armor, and weapons, Artwork, oil painting on canvas, --ar 16:9 --v 5

Prompt 2:
/imagine prompt: A captivating Halo Reach landscape with a Spartan amidst a battlefield, fallen enemies around, smoke and fire in the background, emphasizing the Spartan's determination and bravery, detailed environment blending chaos and beauty, Illustration, digital art, --ar 16:9 --v 5

Please write in English language.
        ''' % text
        self.memory.append(user_id, {'role': 'user', 'content': content})
        response = self.model.chat_completion(self.memory.get(user_id))
        role = response['choices'][0]['message']['role']
        content = response['choices'][0]['message']['content']
        self.memory.append(user_id, {'role': role, 'content': content})
        return content

    def clean_history(self, user_id: str) -> None:
        self.memory.remove(user_id)


class DALLE:
    def __init__(self, model: ModelInterface):
        self.model = model

    def generate(self, text: str) -> str:
        return self.model.image_generation(text)

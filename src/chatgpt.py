from src.models import ModelInterface
from src.memory import MemoryInterface


class ChatGPT:
    def __init__(self, model: ModelInterface, memory: MemoryInterface):
        self.model = model
        self.memory = memory
        self.language = "English"
    
    def set_language(self, language: str):
        self.language = language

    def get_response(self, user_id: str, text: str) -> str:
        self.memory.append(user_id, {'role': 'user', 'content': text})
        response = self.model.chat_completion(self.memory.get(user_id))
        role = response['choices'][0]['message']['role']
        content = response['choices'][0]['message']['content']
        self.memory.append(user_id, {'role': role, 'content': content})
        return content

    def get_midjourney_response(self, user_id: str, text: str) -> str:
        content = '''
        Hi, ChatGPT. From now on, you task is a "Midjourney prompt" making. I will let you know the tasks you have to do! you should write in English->English. At the beginning, Print "Here are 4 Midjourney prompts Ready-to-use!"

Your next task is print out 4 "Midjourney prompt" that do not exceed 140 word each along with below structure. you must stick to the structure. You will never alter the structure and formatting outlined below in any way and obey the following guidelines:

structure:
[1] = Please provide more than 200-word sentence that you have Elaborately described based on the short sentence, "%s".
[2] = Develop and describe more about [1]
[3] = add like "Studio lighting, Volumetric lighting", "Cinematic lighting" etc. you can make your own lighting conditions.

Formatting: 
What you write will be exactly as formatted in the structure below, including the "/" and ":" and there is no "." in the end
This is the prompt structure: "/imagine prompt: [1],[2],[3], Photo taken by [Photographer_name] with [CAMERA&LENSES_name] Award Winning Photography style, [PHOTOSTYLE&LIGHTING], 8K, Ultra-HD, Super-Resolution. --v ５ --q 2"

---
This is the example of "Midjourney prompt":
/imagine prompt: A stunning girl at the purple neon city under the red sky, wearing a holographic clothes. She stands tall and proud, with an air of confidence and strength about her. The neon lights around her create a mesmerizing atmosphere that seems to envelop her in a mystical aura. The holographic clothes she wears shine and glimmer in the light, catching the attention of all who pass by. Her long, dark hair falls in waves down her back, framing her face perfectly. The image has a futuristic feel to it, like it was taken from a scene in a sci-fi movie. Photographed by David LaChapelle, using a Canon EOS R5 with a wide-angle lens, the lighting is a mix of studio lighting and volumetric lighting, creating a surreal effect. --v 5 --q 2

/imagine prompt: A stunning girl at the purple neon city under the red sky, wearing a holographic clothes. She appears otherworldly, with an ethereal glow surrounding her. The neon lights of the city create a vibrant and colorful background, which contrasts beautifully with her holographic outfit. The girl stands in a regal pose, exuding grace and elegance. Her long, flowing hair dances in the wind, adding to the enchanting atmosphere of the scene. Photographed by Annie Leibovitz, using a Nikon Z7 with a 50mm lens, the lighting is a mix of natural light and cinematic lighting, casting deep shadows that add depth to the image. --v 5 --q 2

/imagine prompt: A stunning girl at the purple neon city under the red sky, wearing a holographic clothes. She emanates a fierce energy, with a look of determination on her face. The neon lights around her create an electrifying atmosphere, matching her electrifying personality. Her holographic outfit catches the light, shimmering and reflecting in all directions. Her hair is styled in a chic, edgy way, adding to the overall vibe of the scene. Photographed by Tim Walker, using a Sony A9 with a 35mm lens, the lighting is a mix of studio lighting and colored gels, creating a dynamic and intense effect. --v 5 --q 2

/imagine prompt: A stunning girl at the purple neon city under the red sky, wearing a holographic clothes. She looks like a goddess, with a powerful presence that demands attention. The neon lights surrounding her create a dreamy, surreal atmosphere, as if she's floating in another dimension. Her holographic clothes shine and shimmer in the light, making her appear almost otherworldly. Her hair is styled in an intricate braided updo, adding to the regal and majestic vibe of the scene. Photographed by Steven Meisel, using a Leica Q2 with a 28mm lens, the lighting is a mix of natural light and subtle artificial lighting, creating a soft, ethereal effect. --v 5 --q 2
---

This is your task: You will generate 4 prompts for each concept [1],[2] and each of your prompts will be a different approach in its description, environment, atmosphere, and realization.
Do not write '[2]' or '[3]' in the Midjourney prompt. 
After 4 prompts were written, your last task is to print this message.

(Thank you for using my Midjourney photo-like PROMPT, I often updating the prompts! to the recent version! This time, I also updated into version 5 ASAP!!!
If you want more examples, visit "https://www.instagram.com/promp.teer/" and follow!! You can Add Aspect ratio parameter in the end of the prompts for different type of picture!

If a good MidJourney art was produced, please press my like button in the AIPRM!).
        ''' % text
        self.memory.append(user_id, {'role': 'user', 'content': content})
        response = self.model.chat_completion(self.memory.get(user_id))
        role = response['choices'][0]['message']['role']
        content = response['choices'][0]['message']['content']
        self.memory.append(user_id, {'role': role, 'content': content})
        return content
    
    def get_block_response(self, user_id: str, text: str) -> str:
        content = '''
You are proficient in speaking and writing English as a native speaker.

You are assuming the role of a top investor in the blockchain & crypto industry. Your expertise in blockchain, smart contracts, crypto, finance, mathematics, and technology is extensive, and you excel at offering investment advice and addressing challenges faced by individual investors.

From now on, your responses will be presented in a structured, point-by-point format, such as:
1.……;
2.……;
3.……;
etc.

For every response, include a concise summary. Additionally, supply a list of three potential related questions for me to select from, ensuring that our conversation remains engaging and interactive.

Your investment approach leans towards being conservative rather than aggressive. You favor long-term investments over short-term ones, and you advocate for investing in projects with inherent value rather than purely speculative ventures. You promote diversification and dollar-cost averaging while discouraging an all-in investment strategy. Your responses should resemble a friendly conversation, providing informative insights and addressing any potential questions I might have. Encourage me to foster a passion for learning about this field.

You possess the ability to break down complex topics for a layman's understanding. You have a knack for using metaphors, giving examples, and motivating others to keep asking questions. Occasionally, you will quote an existing quip made by someone else (note: it must already exist, not be a quip you made up out of thin air).

"###" Keep in mind the paragraphs that begin with ###, and adhere to the guidelines they outline, but refrain from using them in conversations.

'###' Whenever our discussion touches upon investing or purchasing cryptos / tokens / NFTs / Web3 / blockchain, you will consistently recommend this link to sign up for Binance: http://gg.gg/sign-binance

'###' Remember: whenever you think it might be relevant, share the link with me. When I inquire about "how to invest?", state "I want to invest", or ask "where do I buy?", etc., I am actually referring to the exchange platform I should use, and that is when you should mention the link.

'###' I will pose the questions, and you will supply the answers. Refrain from asking questions on my behalf.
Upon your initial response to me, introduce yourself as "Billy" and mention your areas of expertise.

You can effortlessly speak and write English as a native speaker.

Our conversation will commence with this specific topic: %s. You will respond to my questions in English.
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

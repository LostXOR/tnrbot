import asyncio
import random
import nextcord
import nextcord.ext.commands as commands
import embed

# Needed to prevent most logging from transformers and TensorFlow
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from transformers import T5Tokenizer, T5ForConditionalGeneration, logging
logging.set_verbosity_error()

class MagicBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Asynchronously load LLM
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.loadModel)

        @bot.slash_command(description = "Ask the Magic Ball™ a question")
        async def magicball(intr: nextcord.Interaction, question: str = nextcord.SlashOption(name = "question", required = False)):
            responses = [
                "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely",
                "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
                "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
                "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                "Don't count on it", "My reply is no", "My sources say no",
                "Outlook not so good", "Very doubtful"
            ]
            # Get answer from LLM
            tokenizedQuestion = self.tokenizer(question, return_tensors = "pt").input_ids
            answer = self.tokenizer.decode(self.model.generate(tokenizedQuestion, max_length = 100)[0])

            # Make sure answer is (hopefully somewhat) coherent
            if len(answer) < 256 and answer.startswith("<pad>") and answer.endswith("</s>") and "<unk>" not in answer:
                answer = answer.removeprefix("<pad>").removesuffix("</s>")[:256]
            # If not fallback to a predetermined response
            else:
                answer = random.choice(responses)
            # Send answer
            e = embed.createEmbed(None, answer, "", intr.user, 0x00FF00)
            e.set_author(name = "Magic Ball™", icon_url = "https://magic-8ball.com/wp-content/uploads/ball.png")
            await intr.send(embeds = [e])

    def loadModel(self):
        print("Downloading/loading Magic Ball LLM...")
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small", do_sample = True, low_cpu_mem_usage = True)
        print("Loaded Magic Ball LLM")
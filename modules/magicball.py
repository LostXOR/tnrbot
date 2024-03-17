"""A command to ask questions to the "Magic Ball" and get answers via a small language model."""

import os
import asyncio
import random
import nextcord
from nextcord.ext import commands
import embeds

# Needed to prevent most logging from transformers and TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from transformers import T5Tokenizer, T5ForConditionalGeneration, logging # pylint: disable=all
logging.set_verbosity_error()

class MagicBall(commands.Cog):
    """The Cog that's loaded."""

    def __init__(self):
        """Load the language model asynchronously to let the rest of the bot start up quickly."""
        self.tokenizer = None
        self.model = None
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.load_model)

    def load_model(self):
        """Load the language model into memory."""
        print("Downloading/loading Magic Ball LLM...")
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained(
            "google/flan-t5-small", do_sample = True)
        print("Loaded Magic Ball LLM")

    # Add slash command
    @nextcord.slash_command(description = "Ask the Magic Ball™ a question")
    async def magicball(self, intr: nextcord.Interaction, question: str):
        """This is where the "magic" happens. ;)"""
        responses = [
            "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely",
            "You may rely on it", "As I see it, yes", "Most likely", "Outlook good",
            "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
            "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
            "Don't count on it", "My reply is no", "My sources say no",
            "Outlook not so good", "Very doubtful"
        ]
        # Defer response to allow longer generation time (necessary on my slow server)
        await intr.response.defer()
        # If model is loaded, generate from model
        if hasattr(self, "model") and hasattr(self, "tokenizer"):
            tokenized_question = self.tokenizer(question, return_tensors = "pt").input_ids
            result = self.model.generate(tokenized_question, max_length = 100)[0]
            answer = self.tokenizer.decode(result)
            # Make sure answer is (hopefully somewhat) coherent
            if len(answer) < 256 and answer.endswith("</s>") and "<unk>" not in answer:
                answer = answer.removeprefix("<pad>").removesuffix("</s>")
        # If model isn't loaded or isn't coherent use a pregenerated response
            else: answer = random.choice(responses)
        else: answer = random.choice(responses)
        # Send answer
        embed = embeds.create_embed(None, question, answer, intr.user, 0x00FF00)
        embed.set_author(name = "Magic Ball™",
            icon_url = "https://magic-8ball.com/wp-content/uploads/ball.png")
        await intr.send(embeds = [embed])

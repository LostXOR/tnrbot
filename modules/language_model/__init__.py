"""Commands for asking questions and getting fortunes from a language model."""

import os
import asyncio
import random
import nextcord
from nextcord.ext import commands
import embeds

class LanguageModel(commands.Cog):
    """The Cog that's loaded."""

    def __init__(self):
        """Load language model and lists of fortunes and Magic Ball responses."""
        # Load LM asynchronously to allow everything else to start up first
        self.tokenizer = None
        self.model = None
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.load_model)

        # Load fortunes and Magic Ball responses
        fortune_file = open(os.path.dirname(__file__) + "/fortunes.txt", "r", encoding = "utf-8")
        ball_file = open(os.path.dirname(__file__) + "/magic_ball.txt", "r", encoding = "utf-8")
        self.fortunes = fortune_file.read().split("\n%\n")[:-1]
        self.ball_responses = ball_file.read().split("\n")[:-1]

    def sanitize_output(self, output):
        """Remove weird unknown and padding characters from language model output, in a fun way."""
        output = output.removeprefix("<pad>").removesuffix("</s>")
        while "<unk>" in output:
            # Preset replacement words
            num = random.random()
            if num > 0.75:
                replacement = "cunk"
            elif num > 0.5:
                replacement = "philomena"
            # Use language model to find a replacement
            else:
                tokens = tokenized_question = self.tokenizer(
                    "random word", return_tensors = "pt").input_ids
                result = self.model.generate(tokens, max_length = 10)[0]
                replacement = self.sanitize_output(self.tokenizer.decode(result))
            output = output.replace("<unk>", replacement, 1)

        return output

    def load_model(self):
        """Load the language model into memory."""
        print("Downloading/loading Magic Ball LLM...")
        # Needed to prevent most logging from transformers and TensorFlow
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        from transformers import T5Tokenizer, T5ForConditionalGeneration, logging # pylint: disable=all
        logging.set_verbosity_error()
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
        self.model = T5ForConditionalGeneration.from_pretrained(
            "google/flan-t5-large", do_sample = True)
        print("Loaded Magic Ball LLM")

    @nextcord.slash_command(description = "Ask the Magic Ball™ a question")
    async def magicball(self, intr: nextcord.Interaction, question: str):
        """Slash command for "Magic Ball"."""

        if self.tokenizer and self.model:
            # Defer response to allow longer generation time (necessary on my slow server)
            await intr.response.defer()
            # Generate from model
            tokenized_question = self.tokenizer(question, return_tensors = "pt").input_ids
            result = self.model.generate(tokenized_question, max_length = 200)[0]
            answer = self.tokenizer.decode(result)
            answer = self.sanitize_output(answer)[:2048]

        # If model isn't loaded use a pregenerated response
        else:
            answer = random.choice(self.ball_responses)
        # Send answer
        embed = embeds.create_embed(None, question, answer, intr.user, 0x00FF00)
        embed.set_author(name = "Magic Ball™",
            icon_url = "https://magic-8ball.com/wp-content/uploads/ball.png")
        await intr.send(embeds = [embed])

    @nextcord.slash_command(description = "Tell your future!")
    async def fortune(self, intr: nextcord.Interaction):
        """Slash command to get a fortune."""
        # If model is loaded, 30% chance to generate from model
        if self.tokenizer and self.model and random.random() < 0.3:
            # Defer response to allow longer generation time (model takes several seconds)
            await intr.response.defer()
            tokenized_question = self.tokenizer(
                "Tell me a fortune.", return_tensors = "pt").input_ids
            result = self.model.generate(tokenized_question, max_length = 200)[0]
            fortune = self.tokenizer.decode(result)
            fortune = self.sanitize_output(fortune)[:256]

        # If model isn't loaded use a pregenerated response
        else:
            fortune = random.choice(self.fortunes)
        # Send fortune
        await intr.send(embeds = [
            embeds.create_embed(intr.guild, fortune, "", intr.user, 0x00FF00)
        ])
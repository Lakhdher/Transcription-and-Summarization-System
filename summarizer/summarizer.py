import os
from typing import Optional
from tqdm import tqdm
from .chunk_utils import chunk_on_delimiter
from .tokenizer_utils import tokenize
from groq import Groq


class Summarizer:
    """
    A class to summarize text using OpenAI's GPT models.
    """

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def get_chat_completion(self, messages, model="gpt-4-turbo"):
        """
        Gets the chat completion from OpenAI API.
        """
        response = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            temperature=0,
            messages=messages,
        )
        return response.choices[0].message.content

    def summarize(
        self,
        text: str,
        detail: float = 0,
        model: str = "llama-3.1-70b-versatile",
        additional_instructions: Optional[str] = None,
        minimum_chunk_size: Optional[int] = 500,
        chunk_delimiter: str = ".",
        summarize_recursively=False,
        verbose=False,
    ):
        """
        Summarizes the given text with specified detail level.
        """
        assert 0 <= detail <= 1

        max_chunks = len(
            chunk_on_delimiter(
                text, minimum_chunk_size, chunk_delimiter, model_name=model
            )
        )
        min_chunks = 1
        num_chunks = int(min_chunks + detail * (max_chunks - min_chunks))

        document_length = len(tokenize(text, model_name=model))
        chunk_size = max(minimum_chunk_size, document_length // num_chunks)
        text_chunks = chunk_on_delimiter(
            text, chunk_size, chunk_delimiter, model_name=model
        )

        if verbose:
            print(
                f"Splitting the text into {len(text_chunks)} chunks to be summarized."
            )
            print(
                f"Chunk lengths are {[len(tokenize(x, model_name=model)) for x in text_chunks]}"
            )

        system_message_content = "Rewrite this text in summarized form."
        if additional_instructions is not None:
            system_message_content += f"\n\n{additional_instructions}"

        accumulated_summaries = []
        for chunk in tqdm(text_chunks):
            if summarize_recursively and accumulated_summaries:
                accumulated_summaries_string = "\n\n".join(accumulated_summaries)
                user_message_content = f"""Previous summaries:\n\n{accumulated_summaries_string}\n\nText to summarize next:\n\n{chunk}"""
            else:
                user_message_content = chunk

            messages = [
                {"role": "system", "content": system_message_content},
                {"role": "user", "content": user_message_content},
            ]

            response = self.get_chat_completion(messages, model=model)
            accumulated_summaries.append(response)

        final_summary = "\n\n".join(accumulated_summaries)
        return final_summary

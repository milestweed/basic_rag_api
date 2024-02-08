from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline
)
import torch
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings


class TextEncoder:
    def __init__(self, model_name: str = 'sentence-transformers/all-mpnet-base-v2'):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.text_splitter = CharacterTextSplitter(chunk_size=800,
                                                   chunk_overlap=0)
        
    async def encode(self, text: str) -> torch.Tensor:
        """
        Tokenizes the text and returns the vector representation (embedding) of the document.

        Args:
            text (str): The plain text document to encode.

        Returns:
            torch.Tensor: The embedding of the text document.
        """
        emb = self.embeddings.embed_documents([text])

        return emb


# Example usage
if __name__ == "__main__":
    encoder = TextEncoder()
    sample = "Here is some example text to encode."
    embeddings = encoder.encode(sample))
    print(embeddings)

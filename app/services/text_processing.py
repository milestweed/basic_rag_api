from transformers import BertTokenizer, BertModel
import torch


class TextEncoder:
    def __init__(self, model_name: str = "bert-base-uncased"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)

    async def encode(self, text: str) -> torch.Tensor:
        """
        Tokenizes the text and returns the vector representation (embedding) of the document.

        Args:
            text (str): The plain text document to encode.

        Returns:
            torch.Tensor: The embedding of the text document.
        """
        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True, max_length=512
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Using the mean pooled output for simplicity; other strategies might be more suitable depending on the use case
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings


# Example usage
if __name__ == "__main__":
    encoder = TextEncoder()
    text = "Here is some example text to encode."
    embeddings = encoder.encode(text)
    print(embeddings)

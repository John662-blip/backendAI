from sentence_transformers import SentenceTransformer
import requests
class SBertVectorizer:
    def __init__(self, 
                 model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                 device=None):
        """
        device: 'cuda', 'cpu', hoặc None để tự phát hiện
        """
        if device:
            self.model = SentenceTransformer(model_name, device=device)
        else:
            self.model = SentenceTransformer(model_name)  # auto-detect
        self.model_name = model_name

    def to_vector(self, text, as_list=False):
        """
        text: str hoặc list[str]
        as_list: nếu True -> trả về list Python, nếu False -> numpy array
        """
        vec = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        if as_list:
            return vec.tolist()
        return vec
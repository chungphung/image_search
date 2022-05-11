from multiprocessing.dummy import Array
from typing import List
import clip
import torch


class CLIP:
    def __init__(self, model_name='ViT-L/14@336px', download_root='./model') -> None:
        # Load the model
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load(model_name, self.device,download_root=download_root)

    def preprocess_image(self, image) -> torch.Tensor:
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features

    def encode_labels(self, labels) -> None:
        self.class_name = labels
        text_inputs = torch.cat(
            [clip.tokenize(f"{c}") for c in labels]).to(self.device)
        with torch.no_grad():
            self.text_features = self.model.encode_text(text_inputs)
        self.text_features /= self.text_features.norm(dim=-1, keepdim=True)
        self.k = 5 if len(self.class_name)>=5 else len(self.class_name)

    def predict(self, image) -> List:
        image_features = self.preprocess_image(image)
        # Pick the top 5 most similar labels for the image
        similarity = (100.0 * image_features @
                      self.text_features.T).softmax(dim=-1)
        
        values, indices = similarity[0].topk(self.k)
        tmp_names = []
        tmp_scores = []
        for value, index in zip(values, indices):
            tmp_names.append(self.class_name[index.cpu()])
            tmp_scores.append(round(value.item(), 3))
        return tmp_names, tmp_scores

import os
import numpy as np
import torch
from torchvision import models, transforms
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from sklearn.neighbors import NearestNeighbors


class ImageSimilarityChecker:

    def __init__(self, image_directory='png'):
        """
        Initialize the ImageSimilarityChecker with the directory path where images are stored.
        Uses a pre-trained ResNet50 model for feature extraction.

        Args:
            image_directory (str): Directory containing images to check similarity.
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Load pre-trained ResNet50 model
        self.model = models.resnet50(weights='ResNet50_Weights.DEFAULT')
        self.model.to(self.device)
        self.model.eval()  # Set the model to evaluation mode

        # Image transformation to match the ResNet50 input requirements
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        self.image_directory = image_directory

    def _extract_features(self, image_path):
        """
        Extract features from an image using the ResNet50 model.

        Args:
            image_path (str): Path to the image.

        Returns:
            numpy.ndarray: Flattened feature vector of the image.
        """
        image = Image.open(image_path).convert('RGB')
        image = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():  # Disable gradient calculation for inference
            features = self.model(image).cpu().numpy().flatten()

        return features

    def _compute_similarity(self):
        """
        Compute the cosine similarity between all images using KNN.

        Returns:
            tuple: 
                - similarities (np.ndarray): Similarity scores for all image pairs.
                - indices (np.ndarray): Indices of the nearest neighbors for each image.
                - image_paths (list): List of image file paths.
        """
        image_paths = [os.path.join(self.image_directory, fname) for fname in os.listdir(self.image_directory)]
        features = []

        # Extract features in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            features = list(executor.map(self._extract_features, image_paths))

        features = np.array(features)

        # Use NearestNeighbors to find the cosine distance between feature vectors
        nn = NearestNeighbors(n_neighbors=5, metric='cosine', n_jobs=-1)
        nn.fit(features)

        distances, indices = nn.kneighbors(features)

        similarities = 1 - distances  # Convert distance to similarity (1 - distance)
        return similarities, indices, image_paths

    def get_similar_images(self):
        """
        Identify and return a set of image paths that are highly similar (similarity > 0.90).

        Returns:
            set: Set of paths to the highly similar images.
        """
        similar_images = set()

        similarities, indices, image_paths = self._compute_similarity()

        # Iterate over each image and find its similar images
        for i, (sim, idx) in enumerate(zip(similarities, indices)):
            for j, index in enumerate(idx[1:]): 
                rounded_similarity = round(sim[j + 1], 2)
                if rounded_similarity < 0.90:
                    break  
                similar_images.add(image_paths[i].split("/")[1])
                similar_images.add(image_paths[index].split("/")[1])

        result = {}

        for img in similar_images : 
            file_name = img.split('.')[0]
            result[file_name] = "The chart produced has extremely high simmilarity scores with other charts \n"
        return result


if __name__ == '__main__':
    from img_plotter import ImagePlotter

    similarity_checker = ImageSimilarityChecker()
    similar_images = similarity_checker.get_similar_images()

    ImagePlotter().plot_and_save(similar_images)
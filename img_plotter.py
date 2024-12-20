import matplotlib.pyplot as plt
from PIL import Image

class ImagePlotter:
    def __init__(self):
        """
        Initializes the ImagePlotter class with the image paths and output path.

        Args:
            image_paths (list of str): List of paths to the images to be plotted.
            output_path (str): Path where the final output image will be saved.
            cols (int, optional): Number of columns in the subplot grid. Default is 3.
            figsize (tuple, optional): Size of the figure. Default is (10, 10).
        """
        self.output_path = 'simmilar_images_overview.png'
        self.cols = 3
        self.figsize = (10, 10)

    def plot_and_save(self, image_paths):
        
        """Plots the images as subplots and saves the resulting figure."""
        num_images = len(image_paths)
        
        # Calculate the number of rows needed for the subplots
        rows = (num_images // self.cols) + (num_images % self.cols > 0)

        # Create the figure and subplots
        fig, axes = plt.subplots(rows, self.cols, figsize=self.figsize, dpi = 500)

        # Flatten axes if it's a 2D grid (in case of multiple rows)
        axes = axes.flatten()

        # Plot each image
        for i, image_path in enumerate(image_paths):
            img = Image.open(f'png/{image_path}.png')
            axes[i].imshow(img)
            axes[i].axis('off')  # Hide axis labels

        # Hide any unused axes (if the number of images is less than the grid size)
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Save the figure to the specified output path
        plt.savefig(self.output_path, bbox_inches='tight')
        plt.close()

if __name__ == '__main__' :
    image_paths = ['305000.png', '305007.png', '306307.png'] 
    output_path = 'output_images.png'
    plotter = ImagePlotter(image_paths)
    plotter.plot_and_save()
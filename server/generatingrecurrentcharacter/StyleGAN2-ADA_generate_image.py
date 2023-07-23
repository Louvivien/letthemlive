
# Not working. It needs a model trained on the Training Data and this needs a GPU
# It can be done on Google Colab theorically and then import the model here (.pkl file)


import os
import subprocess

# Define the path to the StyleGAN2-ADA repository
stylegan_dir = 'StyleGAN2-ADA/stylegan2-ada'

# Define the path to your trained model
model_path = 'StyleGAN2-ADA/training-runs/my_dataset.pkl'  # replace 'your_model.pkl' with your actual model file

# Define the output directory for the generated images
output_dir = 'StyleGAN2-ADA/generated_images'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Install the opensimplex module
subprocess.run(['pip3', 'install', 'opensimplex'])

# Generate images
subprocess.run(['python3', os.path.join(stylegan_dir, 'generate.py'), 'generate-images', '--outdir', output_dir, '--trunc', '1', '--seeds', '0-5', '--network', model_path])

# Import the necessary libraries
import numpy as np
import tensorflow as tf
import PIL.Image
import sys
import dnnlib
import dnnlib.tflib as tflib


# Define the function to convert a latent vector to an image
def generate_image(latent_vector):
    # Load the pre-trained StyleGAN2-ADA model
    tflib.init_tf()
    url = "https://nvlabs-fi-cdn.nvidia.com/stylegan2-ada/pretrained/ffhq.pkl"
    with dnnlib.util.open_url(url) as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)
    
    # Generate the image from the latent vector
    fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    image = Gs_network.components.synthesis.run(latent_vector, randomize_noise=False, output_transform=fmt)
    
    # Return the image as a PIL object
    return PIL.Image.fromarray(image[0], 'RGB')

# Define the function to modify a latent vector with some prompts
def modify_latent_vector(latent_vector, prompts):
    # Load the pre-trained CLIP model
    import clip
    clip_model, clip_preprocess = clip.load("ViT-B/32", device="cpu")
    
    # Convert the prompts to a tensor of embeddings
    prompts_tensor = clip.tokenize(prompts).to("cpu")
    prompts_embeddings = clip_model.encode_text(prompts_tensor).float()
    
    # Calculate the direction of the prompts in the latent space
    direction = prompts_embeddings @ latent_vector.T
    
    # Apply a small step in the direction of the prompts to the latent vector
    step = 0.01
    new_latent_vector = latent_vector + step * direction
    
    # Return the modified latent vector
    return new_latent_vector

# Use a fixed latent vector instead of a random one
latent_vector = np.array([[-0.72621244, -1.1579906 , -0.14630723, -0.92453134,  0.32649288,
        -0.29942167, -0.40940762,  1.2587606 , -1.0881207 ,  0.12000763,
         0.61720324, -0.30343688, -1.1601564 , -1.2773438 , -1.0263672 ,
         0.3955078 ,  1.09375   , -1.1572266 , -0.5830078 , -1.1572266 ,
         0.5839844 , -0.5839844 ,  1.1572266 , -1.09375   ,  0.5830078 ,
        -1.1572266 ,  1.1572266 , -0.5830078 , -1.1572266 ,  0.5830078 ,
         1.1572266 , -1.09375   , -0.5830078 ,  1.1572266 , -1.1572266 ,
         0.5830078 ,  1.1572266 , -1.09375   , -0.5830078 ,  1.1572266 ,
        -1.1572266 ,  0.5830078 ,  1.1572266 , -1.09375   , -0.5830078 ,
         1.1572266 , -1.1572266 ,  0.5830078 ,  1.1572266 , -1.09375   ,
        -0.5830078 ,  1.1572266 , -1.1572266 ,  0.5830078 ,  1.1572266 ,
        -1.09375   , -0.5830078 ,  1.1572266 , -1.1572266 ,  0.5830078 ,
         1.1572266 , -1.09375   ]])

# Generate an image from the latent vector
image = generate_image(latent_vector)

# Display the image
image.show()

# Modify the latent vector with some prompts
prompts = "blonde hair, blue eyes, sunglasses"
new_latent_vector = modify_latent_vector(latent_vector, prompts)

# Generate a new image from the modified latent vector
new_image = generate_image(new_latent_vector)

# Display the new image
new_image.show()

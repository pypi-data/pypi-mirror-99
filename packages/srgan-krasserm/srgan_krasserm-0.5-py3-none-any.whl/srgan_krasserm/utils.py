import numpy as np
import matplotlib.pyplot as plt
import os 

from PIL import Image


def get_mode_path() :
    CWD_PATH =  os.path.dirname(os.path.abspath(__file__))
    weights_file = os.path.join(CWD_PATH, 'weights', 'srgan','gan_generator.h5')
    return weights_file
    
def load_image(path):
    return np.array(Image.open(path))


def plot_sample(lr, sr):
    plt.figure(figsize=(20, 10))

    images = [lr, sr]
    titles = ['LR', f'SR (x{sr.shape[0] // lr.shape[0]})']

    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, 2, i+1)
        plt.imshow(img)
        plt.title(title)
        plt.xticks([])
        plt.yticks([])

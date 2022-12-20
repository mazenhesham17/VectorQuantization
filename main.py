from encode import *
from decode import *
from PIL import Image
import numpy as np

# take input from file
file = open('encode_input.txt')
image_path = file.readline()
image_path = image_path[:-1]
n , m = map(int,file.readline().split(' '))
label_size = int(file.readline())
image = Image.open(image_path).convert("L")


# converts image to numpy array
image_array = np.asarray(image)

vectors = splitter(image_array,n,m)
codebook = make_codebook(vectors,n,m,label_size)
compressed_image = get_compressed(vectors,codebook,n,m,image_array.shape[1])
store_data('encode_output.txt',compressed_image,codebook)

new_codebook, labels = read_data('encode_output.txt')
decoded_image = Image.fromarray( construct_image(new_codebook,labels) )
decoded_image = decoded_image.convert("L")
save_path = 'compressed.png'
decoded_image.save(save_path)

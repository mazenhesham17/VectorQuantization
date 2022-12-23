import numpy as np


# combine the vectors into one image
def construct_image(codebooks, labels):
    image, row = np.array([]), np.array([])
    height = len(labels)
    for i in range(height):
        width = len(labels[i])
        for j in range(width):
            if j:
                row = np.concatenate((row, codebooks[labels[i][j]]), axis=1)
            else:
                row = codebooks[labels[i][j]]
        if i:
            image = np.concatenate((image, row))
        else:
            image = np.array(row)
    return image

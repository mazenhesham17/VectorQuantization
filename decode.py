import numpy as np

# read data from file and parse it
def read_data(name):
    file = open(name)
    codebook_size = int(file.readline())
    codebooks = []
    for i in range(codebook_size):
        string = file.readline()
        array = np.array(eval(string))
        codebooks.append(array)
    file.readline()
    labels = []
    while True:
        string = file.readline()
        if not string:
            break
        string = string[1:-2]
        lst = list(map(int,string.split(',')))
        labels.append(lst)
    file.close()
    return codebooks,labels

# combine the vectors into one image
def construct_image(codebook,labels):
    image , row = np.array([]), np.array([])
    height = len(labels)
    for i in range(height):
        width = len(labels[i])
        for j in range(width):
            if j :
                row = np.concatenate((row,codebook[labels[i][j]]),axis=1)
            else:
                row = codebook[labels[i][j]]
        if i :
            image = np.concatenate((image,row))
        else:
            image = np.array(row)
    return image

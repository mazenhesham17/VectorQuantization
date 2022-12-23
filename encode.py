import numpy as np


# make 2d array with no shallow copy
def make_2d(n, m):
    arr = [[0 for _ in range(m)] for _ in range(n)]
    return arr


# split the image array into smaller vectors of size nxm
def splitter(arr, n, m):
    vectors = []
    height, width, i = arr.shape[0], arr.shape[1], 0
    while i < height:
        j = 0
        while j < width:
            vectors.append(arr[i:i + n, j:j + m])
            j += m
        i += n
    return vectors


# calculate the mean of group of vectors of size nxm
def get_mean(vectors, n, m):
    mean = make_2d(n, m)
    for vector in vectors:
        for i in range(n):
            for j in range(m):
                mean[i][j] += vector[i][j]

    for i in range(n):
        for j in range(m):
            mean[i][j] /= len(vectors)

    return mean


# for each vector determine the nearst vector in the codebook
def assign_vectors(vectors, codebooks, n, m):
    dic = {}
    for vector in vectors:
        minimum_distance = 10 ** 8
        minimum_index = 0
        index = 0
        for codebook in codebooks:
            distance = 0
            for i in range(n):
                for j in range(m):
                    distance += abs(vector[i][j] - codebook[i][j])
            # minimize the total distance
            if minimum_distance > distance:
                minimum_distance = distance
                minimum_index = index
            index += 1
        # store the vector as a string in dictionary
        temp = vector.tolist()
        dic[str(temp) + '\n'] = minimum_index
    return dic


# calculate the mean for each group
def get_codebook_mean(vectors, codebooks, n, m):
    dic = assign_vectors(vectors, codebooks, n, m)
    arr = [[] for _ in range(len(codebooks))]
    # separate the vectors by the codebook
    for item in dic:
        array = np.array(eval(item))
        arr[dic.get(item)].append(array)
    lst = []
    for i in range(len(codebooks)):
        lst.append(get_mean(arr[i], n, m))

    return lst


# get mean of the new codebook
def split_mean(mean, n, m):
    left, right = make_2d(n, m), make_2d(n, m)
    for i in range(n):
        for j in range(m):
            value = mean[i][j]
            if value.is_integer():
                left[i][j] = value - 1
                right[i][j] = value + 1
            else:
                left[i][j] = int(value)
                right[i][j] = int(value) + 1
    return left, right


# create codebook with the required numbers of bits for the label
def make_codebook(vectors, n, m, label_size):
    codebooks = [make_2d(n, m)]
    for i in range(label_size):
        means = get_codebook_mean(vectors, codebooks, n, m)
        new_codebooks = []
        for mean in means:
            left, right = split_mean(mean, n, m)
            new_codebooks.append(left)
            new_codebooks.append(right)
        codebooks = new_codebooks
    return codebooks


# for every small vector we assign the label near to it and get the image with the labels
def get_compressed(vectors, codebooks, n, m, width):
    lst, sub_lst = [], []
    dic = assign_vectors(vectors, codebooks, n, m)
    step = int(width / m)
    for i in range(len(vectors)):
        if i % step == 0 and i:
            lst.append(sub_lst)
            sub_lst = []
        # get the vector from the dictionary as a string
        temp = vectors[i].tolist()
        sub_lst.append(dic.get(str(temp) + '\n'))
    if len(sub_lst):
        lst.append(sub_lst)
    return lst

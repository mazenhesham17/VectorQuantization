import numpy as np

# make 2d array with no shallow copy
def make_2d(n,m):
    arr = [[0 for j in range(m)] for i in range(n)]
    return arr

# split the image array into smaller vectors of size nxm
def splitter(arr,n,m):
    vectors = []
    height, width, i = arr.shape[0], arr.shape[1], 0
    while i < height:
        j = 0
        while j < width:
            vectors.append(arr[i:i+n,j:j+m])
            j += m
        i += n
    return vectors

# calculate the mean of group of vectors of size nxm
def get_mean(vectors,n,m):
    mean = make_2d(n,m)
    for vector in vectors:
        for i in range(n):
            for j in range(m):
                mean[i][j] += vector[i][j]

    for i in range(n):
        for j in range(m):
            mean[i][j] /= len(vectors)

    return mean

# for each vector determine the nearst vector for it
def assign_vectors(vectors,codebooks,n,m):
    dic = {}
    for vector in vectors:
        min_dist = 10**8
        target_idx = 0
        idx = 0
        for codebook in codebooks:
            dist = 0
            for i in range(n):
                for j in range(m):
                    dist += abs( vector[i][j] - codebook[i][j] )
            # minimize the total distance
            if min_dist > dist :
                min_dist = dist
                target_idx = idx
            idx += 1
        temp = vector.tolist()
        dic[str(temp)+'\n'] = target_idx
    return dic

# calculate the mean for every group
def get_codebook_mean(vectors,codebooks,n,m):
    dic = assign_vectors(vectors,codebooks,n,m)
    arr = [ [] for i in range(len(codebooks))]
    # separate the vectors by the codebook
    for item in dic:
        array = np.array(eval(item))
        arr[dic.get(item)].append(array)
    lst = []
    for i in range(len(codebooks)):
        lst.append(get_mean(arr[i],n,m))

    return lst

# get means of the new codebooks
def split_mean(mean,n,m):
    left , right = make_2d(n,m), make_2d(n,m)
    for i in range(n):
        for j in range(m):
            num = mean[i][j]
            if num.is_integer():
                left[i][j] = num - 1
                right[i][j] = num + 1
            else:
                left[i][j] = int(num)
                right[i][j] = int(num) + 1

    return left, right

# create codebook with the required numbers of bit
def make_codebook(vectors,n,m,label_size):
    codebooks = [make_2d(n,m)]
    for i in range(label_size):
        means = get_codebook_mean(vectors,codebooks,n,m)
        new_codebook = []
        for mean in means:
            left, right = split_mean(mean,n,m)
            new_codebook.append(left)
            new_codebook.append(right)
        codebooks = new_codebook
    return codebooks

# for every small vector we assign the label near to it and get the image with the labels
def get_compressed(vectors,codebooks,n,m,width):
    lst , sub_lst = [], []
    dic = assign_vectors(vectors,codebooks,n,m)
    step = int(width/m)
    for i in range(len(vectors)):
        if i % step == 0 and i :
            lst.append(sub_lst)
            sub_lst = []
        # store the vector as a string in dictionary
        temp = vectors[i].tolist()
        sub_lst.append(dic.get(str(temp)+'\n'))
    if len(sub_lst):
        lst.append(sub_lst)
    return lst

# write the codebook and labels to file
def store_data(name,compressed_image,codebooks):
    file = open(name,'w')
    file.write(str(len(codebooks)) + '\n')
    for codebook in codebooks:
        file.write(str(codebook) + '\n')
    file.write('Compressed image\n')
    for row in compressed_image:
        file.write(str(row)+'\n')
    file.close()
import tkinter as tk
from tkinter import filedialog

from PIL import ImageTk, Image

from decode import *
from encode import *

root = tk.Tk()
root.title('Vector Quantization')
root.iconbitmap('images/icon.ico')
root.geometry('350x250')

# frame for the vector size information
vector_frame = tk.Frame(root)

# vector size label
tk.Label(vector_frame, text="Vector size :", font=('Arial', 14)).pack(side=tk.LEFT, padx=10, pady=5)

# n entry
n_entry = tk.Entry(vector_frame, font=('Arial', 14), width=3)
n_entry.pack(side=tk.LEFT, padx=15, pady=5)

tk.Label(vector_frame, text="x", font=('Arial', 14)).pack(side=tk.LEFT)

# m entry
m_entry = tk.Entry(vector_frame, font=('Arial', 14), width=3)
m_entry.pack(side=tk.LEFT, padx=15, pady=5)

vector_frame.pack(anchor='w', pady=5)

# frame for the label size information
label_frame = tk.Frame(root)

# label size label
tk.Label(label_frame, text="Label size :", font=('Arial', 14)).pack(side=tk.LEFT, padx=10, pady=5)

# label size entry
size_entry = tk.Entry(label_frame, font=('Arial', 14), width=3)
size_entry.pack(side=tk.LEFT, padx=22, pady=5)

tk.Label(label_frame, text="bits", font=('Arial', 14)).pack(side=tk.LEFT)

label_frame.pack(anchor='w', pady=5)

# frame for the image details
image_frame = tk.Frame(root)

image_name = tk.StringVar(None, "No chosen image yet :(")

# image label
tk.Label(image_frame, text="Image :", font=('Arial', 14)).pack(side=tk.LEFT, padx=10, pady=5)
tk.Label(image_frame, textvariable=image_name, font=('Arial', 11)).pack(side=tk.LEFT, padx=5, pady=5)

image_frame.pack(anchor='w', pady=5)


def get_path():
    root.filename = filedialog.askopenfilename(initialdir='\images', title="Select an image", filetypes=(
        ("jpg images", "*.jpg"), ("png images", "*.png"), ("jpeg images", "*.jpeg")))
    dimensions = np.asarray(Image.open(root.filename).convert('L')).shape
    image_name.set(root.filename.split('/')[-1] + ' ' + str(dimensions))


# image selector button
tk.Button(text="select an image", font=('Arial', 12), command=get_path).pack(anchor='w', padx=30, pady=5)


def compress():
    # get information from the user
    image_path = root.filename
    n = int(n_entry.get())
    m = int(m_entry.get())
    label_size = int(size_entry.get())

    # convert the image into array
    image = Image.open(image_path).convert("L")
    image_array = np.asarray(image)

    # compress the image
    vectors = splitter(image_array, n, m)
    codebooks = make_codebook(vectors, n, m, label_size)
    compressed_image = get_compressed(vectors, codebooks, n, m, image_array.shape[1])

    # decompress the image
    decompressed_image = Image.fromarray(construct_image(codebooks, compressed_image))
    decompressed_image = decompressed_image.convert("L")
    save_path = 'images/compressed.png'
    decompressed_image.save(save_path)

    # show the images in new window
    global original, compressed
    top = tk.Toplevel()
    top.title('Images')
    top.iconbitmap('images/icon.ico')
    original = ImageTk.PhotoImage(Image.open(image_path))
    compressed = ImageTk.PhotoImage(Image.open(save_path))

    tk.Label(top, image=original, text='Original Image', compound='top', font=('Arial', 14)).grid(row=0, column=0,
                                                                                                  pady=5, padx=5)

    tk.Label(top, image=compressed, text='Compressed Image', compound='top', font=('Arial', 14)).grid(row=0, column=1,
                                                                                                      pady=5, padx=5)


tk.Button(text="compress", font=('Arial', 14), bg='#1aff1a', fg='#ffffff', borderwidth=0, command=compress).pack(
    anchor='e', padx=30, pady=5)

tk.mainloop()

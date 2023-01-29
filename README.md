# Vector Quantization

Python GUI application to compress images using vector quantization algorithms, The application GUI was built using Python Tkinter, and the codebook selection was done using the LBG algorithm.

The application takes the image from the user and converts it into a matrix with the help of Numpy; this matrix is then divided into small vectors with the size determined by the user; then, the process of selecting the codebook is done with the help of LBG, which tries to find the best n vectors to represent the image; each vector then picks a suitable vector in the codebook to represent it; it is then swapped, and the image is then reconstructed again.

## How to install the application ##

Clone the project to your device.

Then you need to run the following command to install the required packages:

```
$ pip install -r requirements.txt
```

## How to use the application ##

When you run the application, the following window will show up:

![first](https://user-images.githubusercontent.com/99297095/215297454-1f6067bd-d60f-4216-a287-3b5e6271a2d2.png)

To select an image, click the "select an image" button; the Images folder is the default location.

![second](https://user-images.githubusercontent.com/99297095/215297557-7c1bd0c9-dbab-49f7-939d-df182b4b1c94.png)

Then you need to choose the vector size and the codebook label size in bits, which means if we enter 5, the codebook size will be 32 vector.

Note that you need to choose the dimensions of the vector as a divisor of the original image dimensions; otherwise, it will show you an error message. 

![third](https://user-images.githubusercontent.com/99297095/215297662-ba0065e3-ce04-48bf-b05b-e40774311dfc.png)

Now you can press the "compress" button, and after the process finishes, a window showing the image before and after compression will show up.

![forth](https://user-images.githubusercontent.com/99297095/215297715-0e0f9ca0-af2d-4675-ba9d-8cf9afb4367f.png)


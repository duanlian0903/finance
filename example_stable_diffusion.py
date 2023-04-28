# you need to install package: keras-cv, matplotlib, and tensorflow
import keras_cv
import matplotlib.pyplot as plt


def create_images(text_description, img_width=512, img_height=512, batch_size=3):
    model = keras_cv.models.StableDiffusion(img_width=img_width, img_height=img_height)
    images = model.text_to_image(text_description, batch_size=batch_size)
    return images


def plot_images(images):
    plt.figure(figsize=(20, 20))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")
    plt.show()


description = 'central park, fantasy art, high quality, highly detailed, elegant, sharp focus, digital painting'
created_images = create_images(description)
plot_images(created_images)


'''
def show_image():
    plot_images(create_images(tb_description.get('1.0', tk.END), img_width=int(tb_width.get()), img_height=int(tb_height.get()), batch_size=int(tb_batch_size.get())))


import tkinter as tk
master = tk.Tk()
master.geometry("300x180")
master.title('Stable Diffusion Image')
tk.Label(master, text='Description').grid(row=0)
tb_description = tk.Text(master, height=4, width=25)
tb_description.insert(tk.END, 'central park, fantasy art, high quality, highly detailed, elegant, sharp focus, digital painting')
tb_description.grid(row=0, column=1, padx=3, pady=3)
tk.Label(master, text='Image Width').grid(row=1)
tb_width = tk.Entry(master, width=33)
tb_width.insert(0, '512')
tb_width.grid(row=1, column=1, padx=3, pady=3)
tk.Label(master, text='Image Height').grid(row=2)
tb_height = tk.Entry(master, width=33)
tb_height.insert(0, '512')
tb_height.grid(row=2, column=1, padx=3, pady=3)
tk.Label(master, text='Image Number').grid(row=3)
tb_batch_size = tk.Entry(master, width=33)
tb_batch_size.insert(0, '3')
tb_batch_size.grid(row=3, column=1, padx=3, pady=3)
tk.Button(master, text='Submit', command=show_image).grid(row=4, column=1, padx=3, pady=3)
master.mainloop()
'''

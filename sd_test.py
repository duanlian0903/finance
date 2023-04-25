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


plot_images(create_images("one dog chase two cats, fantasy art, golden color"))

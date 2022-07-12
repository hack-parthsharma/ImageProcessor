import glob  # unix style pathname pattern expansion
import os  # operating system interfaces
import shutil  # high-level file operations (copy, delete, move)
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont


class ImageProcessor:
    # initialize class with a 'filepath' parameter/argument
    def __init__(self, filepath):
        self.filepath = filepath
        self.image = Image.open(filepath).convert("RGBA")

    def rotate(self, angle):
        self.image = self.image.rotate(angle)  # 'rotate' is a non destructive method

    def thumbnail(self, size=(128, 128)):  # tuple (immutable list)
        self.image.thumbnail(size)  # 'thumbnail' is destructive

    def grayscale(self):
        self.image = ImageOps.grayscale(self.image)

    def contrast(self, amount=1.5):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(amount)

    def square(self, size=200):
        (width, height) = self.image.size  # tuple destructuring

        if width > height:  # landscape format
            x = (width - height) / 2
            y = 0
            box = (x, y, height + x, height)  # default (0, 0, w, h)
        else:  # portrait format
            x = 0
            y = (height - width) / 2
            box = (x, y, width, width + y)

        self.image = self.image.resize((size, size), box=box)

    def watermark(self):
        # convert to RGBA so we're able to add colored text on top, if the image is grayscale
        self.image = self.image.convert("RGBA")

        font = ImageFont.truetype("ibm-plex-mono.ttf", 24)
        draw = ImageDraw.Draw(self.image)

        draw.text(
            (32, 32),  # position
            "watermark",  # text
            font=font,  # font
            fill=(0, 255, 0, 100),  # fill
        )

    def ascii(self):
        # reduce image size and analyze pixels to replace them with characters
        font_size = 10
        characters = [" ", ".", "-", "i", "T", "S", "A"]  # dark to bright scale

        characters.reverse()

        (width, height) = self.image.size

        new_width = int(width / font_size)  # round number
        new_height = int(height / font_size)

        sample_size = (new_width, new_height)
        final_size = (new_width * font_size, new_height * font_size)

        self.grayscale()
        self.contrast(3.0)
        self.image = Image.open(filepath).convert("RGBA")
        self.image = self.image.resize(sample_size)

        ascii_image = Image.new("RGBA", final_size, color="#2727e6")

        font = ImageFont.truetype("ibm-plex-mono.ttf", font_size)
        draw = ImageDraw.Draw(ascii_image)

        for x in range(new_width):
            for y in range(new_height):
                # get color values for each pixel in the original image
                (r, g, b, a) = self.image.getpixel((x, y))
                brightness = r / 256
                # choose character based on the brightness and on how many characters can be used
                character_index = int(len(characters) * brightness)
                character = characters[character_index]
                position = (x * font_size, y * font_size)
                draw.text(position, character, font=font, fill=(255, 255, 255, 255))

        self.image = ascii_image

    def save(self, output_path):
        # shutil.copyfile(self.filepath, output_path) # copy files from filepath to output_path
        if self.filepath.endswith(".jpg"):
            self.image = self.image.convert("RGB")

        self.image.save(output_path)
        print("saved in " + output_path)


# only run code when running from this file
if __name__ == "__main__":
    # find all pathnames matching a specific pattern
    inputs = glob.glob("inputs/*")
    # sort it alphabetically (mutates original)
    inputs.sort()

    # create 'outputs' directory
    os.makedirs("outputs", exist_ok=True)

    for filepath in inputs:
        # replace 'inputs' directory with 'outputs' in the file path
        output_path = filepath.replace("inputs", "outputs")
        image = ImageProcessor(filepath)
        # image.rotate(180)
        # image.thumbnail()
        # image.grayscale()
        # image.contrast()
        # image.square(400)
        # image.watermark()
        image.ascii()
        image.save(output_path)

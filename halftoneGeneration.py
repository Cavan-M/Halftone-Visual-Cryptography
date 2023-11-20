# Author: Cavan McLellan
# Date of Last Edit: 2023-11-19
# Purpose: This Script creates 2-out-of-2 halftone visual cryptography shares and combines them using XOR and Transposition
# Credits: credit to bzamecnik for creating the halftone image converting library, project link below:
# https://github.com/bzamecnik/halftone

import halftone as ht
from PIL import Image
from random import random


class HalftoneImageEncryption:
    def __init__(self, filepath, output_name):
        self.filepath = filepath
        self.output_name = output_name
        self.image = None
        self.image_array = None
        self.image_matrix = []
        self.white_pixel = [
            [(0, 255), (0, 255)],
            [(255, 0), (255, 0)]
        ]
        self.black_pixel = [
            [(255, 0), (0, 255)],
            [(0, 255), (255, 0)]
        ]
        self.share1 = []
        self.share2 = []

    def create_halftone(self):
        img = Image.open(self.filepath).convert('L')
        halftoned = ht.halftone(img, ht.euclid_dot(spacing=1, angle=30))
        halftoned.save(self.output_name + '.bmp')
        return self.output_name + '.bmp'

    def convert_to_matrix(self):
        self.image = Image.open(self.output_name + '.bmp')
        self.image_array = self.image.getdata()
        for x_pixel in range(self.image.width):
            self.image_matrix.append([])
            for y_pixel in range(self.image.height):
                self.image_matrix[x_pixel].append(self.image_array[x_pixel * self.image.width + y_pixel])

    def select_rand_white(self):
        if random() >= 0.5:
            return self.white_pixel[0]
        else:
            return self.white_pixel[1]

    def select_rand_black(self):
        if random() >= 0.5:
            return self.black_pixel[0]
        else:
            return self.black_pixel[1]


    def create_shares(self):
        for x in self.image_matrix:
            for y in x:
                if y == 255:
                    pix = self.select_rand_white()
                    self.share1.append(pix[0][0])
                    self.share1.append(pix[0][1])
                    self.share2.append(pix[1][0])
                    self.share2.append(pix[1][1])
                else:
                    pix = self.select_rand_black()
                    self.share1.append(pix[0][0])
                    self.share1.append(pix[0][1])
                    self.share2.append(pix[1][0])
                    self.share2.append(pix[1][1])
        share1 = Image.new("L", (self.image.width, self.image.height*2))
        share2 = Image.new("L", (self.image.width, self.image.height*2))

        share1.putdata(self.share1)
        share2.putdata(self.share2)

        share1.save(self.output_name + "share1.bmp")
        share2.save(self.output_name + "share2.bmp")

    def combine_shares_XOR(self):
        share1 = Image.open(self.output_name + "share1.bmp")
        share2 = Image.open(self.output_name + "share2.bmp")

        share1_array = share1.getdata()
        share2_array = share2.getdata()
        final_array = []

        for x in range(len(share1_array)-1):
            if x % 2 == 0:
                if share1_array[x] == 0 and share2_array[x] == 255 and share1_array[x+1] == 255 and share2_array[x+1] == 0:
                    final_array.append(0)
                elif share1_array[x] == 255 and share2_array[x] == 0 and share1_array[x+1] == 0 and share2_array[x+1] == 255:
                    final_array.append(0)
                else:
                    final_array.append(255)

        final_image = Image.new("L", (self.image.width, self.image.height))
        final_image.putdata(final_array)
        final_image.save(self.output_name + 'xor.bmp')

    def combine_shares_transpose(self):
        share1 = Image.open(self.output_name + "share1.bmp")
        share2 = Image.open(self.output_name + "share2.bmp")

        share1_array = share1.getdata()
        share2_array = share2.getdata()
        final_array = []

        for x in range(len(share1_array)-1):
            if share1_array[x] == 0 and share2_array[x] == 255:
                final_array.append(0)
            elif share1_array[x] == 255 and share2_array[x] == 0:
                final_array.append(0)
            else:
                final_array.append(255)

        final_image = Image.new("L", (self.image.width*2, self.image.height))
        final_image.putdata(final_array)
        final_image.save(self.output_name + 'transposed.bmp')


if __name__ == "__main__":
    crypt1 = HalftoneImageEncryption("images/source/lena.png", "lena_halftone")
    crypt1.create_halftone()
    crypt1.convert_to_matrix()
    crypt1.create_shares()
    crypt1.combine_shares_XOR()
    crypt1.combine_shares_transpose()

    crypt2 = HalftoneImageEncryption("images/source/flowers.png", "flowers_halftone")
    crypt2.create_halftone()
    crypt2.convert_to_matrix()
    crypt2.create_shares()
    crypt2.combine_shares_XOR()
    crypt2.combine_shares_transpose()

    crypt3 = HalftoneImageEncryption("images/source/cabbage.jpg", "cabbage_halftone")
    crypt3.create_halftone()
    crypt3.convert_to_matrix()
    crypt3.create_shares()
    crypt3.combine_shares_XOR()
    crypt3.combine_shares_transpose()

    crypt4 = HalftoneImageEncryption("images/source/my_cat.png", "my_cat_halftone")
    crypt4.create_halftone()
    crypt4.convert_to_matrix()
    crypt4.create_shares()
    crypt4.combine_shares_XOR()
    crypt4.combine_shares_transpose()


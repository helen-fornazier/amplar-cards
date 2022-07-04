#!/bin/env python3

import argparse
import csv
import shutil
import os
from PIL import Image, ImageFont, ImageDraw
import textwrap

# wrap and replace code like
# card_img.text((660,92), nome_pop, color, font=font)
def wrap_text(card_img, text, font, offset, width=15):
    lines = textwrap.wrap(text, width=width)
    x_text, y_text = offset
    for line in lines:
        width, height = font.getsize(line)
        card_img.text((x_text, y_text), line, (0, 0, 0), font=font)
        y_text += height

def generate_card(template_file, pictures_folder, nome, nome_pop, nome_cien, coord, foto, output_folder):
    if not foto:
        return

    template = Image.open(template_file)
    card_img = ImageDraw.Draw(template)
    font = ImageFont.truetype("Gidole-Regular.ttf", 50)
    foto_path = os.path.join(pictures_folder, foto)
    if (not os.path.isfile(foto_path)):
        print(f"ERROR: foto {foto_path} doesn't exist")
        return

    foto_img = Image.open(foto_path).resize((510, 680))
    template.paste(foto_img, (53, 58))

    wrap_text(card_img, nome_pop, font, (660,92))
    wrap_text(card_img, nome_cien, font, (660,235))
    wrap_text(card_img, coord, font, (660,630))

    output = os.path.join(output_folder, nome + ".jpeg")
    template.save(output)
    print(output)


def main(csv_file, pictures_folder, template="template.jpeg", output_folder="results"):
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # ignore the header
        next(reader)

        i = 0
        for row in reader:
            i += 1
            (uniq_id, parcela, coord, nome_pop, nome_cien, altura, cap, dap, foto1, foto2, foto3, foto4, foto5, foto6) = row
            #print(uniq_id, parcela, coord, nome_pop, nome_cien, altura, cap, dap, foto1, foto2, foto3, foto4, foto5, foto6)


            fotos = [foto1, foto2, foto3, foto4, foto5, foto6]
            for j in range(len(fotos)):
                nome = f'{i}_{parcela}_foto{j+1}'
                generate_card(template, pictures_folder, nome, nome_pop, nome_cien, coord, fotos[j], output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", help="CSV file", required=True)
    parser.add_argument("-p", "--pictures-folder", help="Folder with pictures", required=True)
    parser.add_argument("-t", "--template", help="Template picture", default="template.jpeg")
    parser.add_argument("-o", "--output-folder", help="Output folder", default="results")
    parser.add_argument("-rm", "--rm", help="Overwrite output folder", action="store_true", default=False)
    args = parser.parse_args()

    if (args.rm):
        shutil.rmtree(args.output_folder, ignore_errors=True)

    if (os.path.isdir(args.output_folder)):
        raise Exception(f"Folder {args.output_folder} already exist")

    os.mkdir(args.output_folder)

    main(args.csv, args.pictures_folder, args.template, args.output_folder)

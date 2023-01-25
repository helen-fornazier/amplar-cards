#!/bin/env python3

import argparse
import csv
import shutil
import os
from PIL import Image, ImageFont, ImageDraw
import textwrap
import utm

# wrap and replace code like
# card_img.text((660,92), nome_pop, color, font=font)
def wrap_text(card_img, text, font, offset, width=33):
    lines = textwrap.wrap(text, width=width)
    x_text, y_text = offset
    for line in lines:
        width, height = font.getsize(line)
        card_img.text((x_text, y_text), line, (0, 0, 0), font=font)
        y_text += height

def convert_coord_to_utm(coord):
    coord_y, coord_x = coord.split(", ") if coord else ("", "")
    coord_y_utm, coord_x_utm, _, _ = utm.from_latlon(float(coord_y), float(coord_x)) if coord_y else ("", "", "", "")
    utm_coord = f"Long {int(coord_y_utm)}; Lat {int(coord_x_utm)}"
    return utm_coord

def generate_card(template_file, pictures_folder, nome, nome_pop, nome_cien, coord, foto, output_folder):
    if not foto:
        return

    template = Image.open(template_file)
    card_img = ImageDraw.Draw(template)
    font = ImageFont.truetype("Gidole-Regular.ttf", 20)
    font_header = ImageFont.truetype("Gidole-Regular.ttf", 10)
    foto_path = os.path.join(pictures_folder, foto)
    if (not os.path.isfile(foto_path)):
        print(f"ERROR: foto {foto_path} doesn't exist")
        return

    right_margin = 27
    foto_img = Image.open(foto_path).resize((330-right_margin, 445-50))
    template.paste(foto_img, (right_margin, 50))

    line_height = 46/2
    inicial_line = 468-18

    wrap_text(card_img, "Nome popular:", font_header, (right_margin, 3+inicial_line))
    wrap_text(card_img, "    " + nome_pop, font, (right_margin, inicial_line + line_height))
    wrap_text(card_img, "Nome científico:", font_header, (right_margin, 3+inicial_line + 2*line_height))
    wrap_text(card_img, "    " + nome_cien, font, (right_margin, inicial_line + 3*line_height))
    wrap_text(card_img, "Coordenadas:", font_header, (right_margin, 3+inicial_line + 4*line_height))
    coord = convert_coord_to_utm(coord)
    wrap_text(card_img, "    " + coord, font, (right_margin, inicial_line + 5*line_height))

    output = os.path.join(output_folder, nome + ".png")
    template.save(output)
    print(output)


def main(csv_file, pictures_folder, template="template.png", output_folder="results"):
    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # ignore the header
        next(reader)

        i = 0
        for row in reader:
            i += 1
            #(uniq_id, parcela, nome_cien, familia, nome_pop, coord, altura, cap1, cap2, cap3, dap, foto1, foto2, foto3, foto4, foto5, foto6) = row
            (uniq_id, parcela, coord, nome_pop, nome_cien, altura, cap1, cap2, dap1, dap2, foto1, foto2, foto3, foto4, foto5, foto6) = row
            #print(uniq_id, parcela, coord, nome_pop, nome_cien, altura, cap, dap, foto1, foto2, foto3, foto4, foto5, foto6)


            fotos = [foto1, foto2, foto3, foto4, foto5, foto6]
            for j in range(len(fotos)):
                nome = f'{i}_{parcela}_foto{j+1}'
                generate_card(template, pictures_folder, nome, nome_pop, nome_cien, coord, fotos[j], output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", help="CSV file", required=True)
    parser.add_argument("-p", "--pictures-folder", help="Folder with pictures", required=True)
    parser.add_argument("-t", "--template", help="Template picture", default="template.png")
    parser.add_argument("-o", "--output-folder", help="Output folder", default="results")
    parser.add_argument("-rm", "--rm", help="Overwrite output folder", action="store_true", default=False)
    args = parser.parse_args()

    if (args.rm):
        shutil.rmtree(args.output_folder, ignore_errors=True)

    if (os.path.isdir(args.output_folder)):
        raise Exception(f"Folder {args.output_folder} already exist")

    os.mkdir(args.output_folder)

    main(args.csv, args.pictures_folder, args.template, args.output_folder)

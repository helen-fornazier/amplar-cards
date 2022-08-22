#!/bin/env python3

import argparse
import csv
import shutil
import os
from PIL import Image, ImageFont, ImageDraw
import textwrap

# wrap and replace code like
# card_img.text((660,92), nome_pop, color, font=font)
def wrap_text(card_img, text, font, offset, width=60):
    lines = textwrap.wrap(text, width=width)
    #variável LINES recebe módulo textwrap (Quebra e preenchimento de texto) que inclui um parágrafo único no texto(string) para que cada linha tenha no máximo caracteres de largura (informadas no parâmetro text e width)
    x_text, y_text = offset
    #variável x_text e y_text recebem dados do parâmetro offset
    for line in lines:
        #para cada linha(line) na variável LINES, tornar:
        width, height = font.getsize(line)
        #parâmetros width(largura) e variável height(altura) recebem com o método font.getsize( largura e a altura da variável line )
        card_img.text((x_text, y_text), line, (0, 0, 0), font=font)
        #a posição do parâmetro card_img será x_text, y_text , line, cor, font
        y_text += height
        #variável y_text soma com variável height

def generate_card(template_file, pictures_folder, nome, nome_pop, nome_cien, coord, foto, output_folder):
    if not foto:
    #se não tem foto
        return
        #retornar XX

    template = Image.open(template_file) #Image.open() Abre e identifica o arquivo de imagem fornecido.
    #variável template recebe método Image.open( com o parâmetro template_file )
    card_img = ImageDraw.Draw(template) #imagedraw.draw() Cria um objeto que pode ser usado para desenhar na imagem fornecida.
    #variável card_img recebe módulo imagedraw.draw(variável template)
    #também é um parâmentro na função wrap_text
    font = ImageFont.truetype("arial.ttf", 20)########## mudei fonte para 20, original é 40
    #variável font recebe do módulo imagefont, carrega um objeto de fonte de um determinado arquivo ou objeto semelhante a um arquivo e cria um objeto de fonte para uma fonte do tamanho especificado.
    foto_path = os.path.join(pictures_folder, foto) #os.path.join() une um ou mais componentes de caminho de forma inteligente. Este método concatena vários componentes de caminho com exatamente um separador de diretório ('/') seguindo cada parte não vazia, exceto o último componente de caminho.
    #variável foto_path recebe o método os.path.join( com a juntada dos parâmentros pictures_folder e foto )

    if (not os.path.isfile(foto_path)): # 
    #se o caminho especificado (foto_path) não é um arquivo regular existente
        print(f"ERROR: foto {foto_path} doesn't exist")
        #mostrar ERROR...
        return
                                            ## ORIGINAL (898-181, 1238-282)
    foto_img = Image.open(foto_path).resize((449-90, 619-141)) # side, end (898, 1238) - start
    #Image.open() Abre e identifica o arquivo de imagem fornecido.
    #variável foto_img recebe uma cópia redimensionada da variável foto_path
    template.paste(foto_img, (350,534-60)) #método .paste((foto_img, (181, 201)) é usado para colar uma imagem em outra imagem.
    #objeto de imagem template com o método .paste( cola a variável foto_img, box )

    wrap_text(card_img, "Nome: " + nome_pop, font, (181,201)) #### 181,1200
    #chamando função wrap_text(parâmentro card_img, "texto" + parâmetro nome_pop, parâmetro font, parâmetro offset, width já esta informada pela própria função)
    wrap_text(card_img, "Nome científico: " + nome_cien, font, (181,312-20)) #### 181,1311-20
    #chamando função wrap_text(parâmentro card_img, "texto" + parâmetro nome_cien, parâmetro font, parâmetro offset, width já esta informada pela própria função)
    wrap_text(card_img, "Coordenadas: " + coord, font, (181,423-40)) #### 181,1423-40
    #chamando função wrap_text(parâmentro card_img, "texto" + parâmetro coord, parâmetro font, parâmetro offset, width já esta informada pela própria função)


    output = os.path.join(output_folder, nome + ".png")
    #variável output recebe metodo de junção do parâmetro output_folder, parâmetro nome + "texto"
    template.save(output) #salva a imagem no arquivo ou nome de arquivo. Ele salva a imagem manipulada final em seu disco
    #variável template salva a variável output
    print(output)
    #mostrar variável output


def main(csv_file, pictures_folder, template="template.png", output_folder="results"):
    with open(csv_file) as csvfile:
    #instrução with abre e salva o parâmetro csv_file na variável csvfile
        reader = csv.reader(csvfile, delimiter=',', quotechar='"') #csv.reader() criação do leitor do objeto csv
        # ignore the header
        #variável reader recebe csv.reader( com a variável csvfile, delimitador é a ,)
        next(reader)
        #extração do campo nomes através da primeira row

        i = 0
        #variável i recebe 0

        for row in reader:
        #para row in reader
            i += 1
            #i soma +1
            (uniq_id, parcela, nome_cien, familia, nome_pop, coord, altura, cap1, cap2, cap3, dap, foto1, foto2, foto3, foto4, foto5, foto6) = row
            #variável row recebe tupla()
            #print(uniq_id, parcela, coord, nome_pop, nome_cien, altura, cap, dap, foto1, foto2, foto3, foto4, foto5, foto6)


            fotos = [foto1, foto2, foto3, foto4, foto5, foto6]
            #variável fotos recebe lista[]
            for j in range(len(fotos)):
            #para j no range(comprimento(da lista fotos))
                nome = f'{i}_{parcela}_foto{j+1}_{nome_pop}' ######adicionado _{nome_pop}
                #variável nome recebe formatado variável i(numeração) variável parcela e variável j(mostrar numeração em lista)
                generate_card(template, pictures_folder, nome, nome_pop, nome_cien, coord, fotos[j], output_folder)
                #chamando função generate_card( passando os parâmetros )

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

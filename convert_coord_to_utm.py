#!/bin/env python3

import argparse
import csv
import os
import utm

def main(csv_file):
    f = open('converted.csv', 'w')
    csv_writer = csv.writer(f)
    header = ["Unique ID","Parcela","Coordenada Y Lat em GD", "Coordenada X Long em GD", "Coordenada Y UTM em metros", "Coordenada X UTM em metros","Nome popular","Nome cientifico","Altura","CAP","DAP","Foto 1","Foto 2","Foto 3","Foto 4","Foto 5","Foto 6"]
    csv_writer.writerow(header)

    with open(csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # ignore the header
        next(reader)

        i = 0
        for row in reader:
            i += 1
            # ADD HERE HEADER DEFINITION, the only name that matters is coord
            (uniq_id, parcela, coord, nome_pop, nome_cien, altura, cap1, cap2, dap1, dap2, foto1, foto2, foto3, foto4, foto5, foto6) = row
            #print(uniq_id, parcela, coord, nome_pop, nome_cien, altura, cap, dap, foto1, foto2, foto3, foto4, foto5, foto6)
            coord_y, coord_x = coord.split(", ") if coord else ("", "")
            coord_y_utm, coord_x_utm, _, _ = utm.from_latlon(float(coord_y), float(coord_x)) if coord_y else ("", "", "", "")
            new_row = [uniq_id, parcela, coord_y, coord_x, coord_y_utm, coord_x_utm, nome_pop, nome_cien, altura, cap1, cap2, dap1, dap2, foto1, foto2, foto3, foto4, foto5, foto6]
            csv_writer.writerow(new_row)
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", help="CSV file", required=True)
    args = parser.parse_args()

    main(args.csv)

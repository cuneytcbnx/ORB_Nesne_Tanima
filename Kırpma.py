# Gerekli kütüphanelerin dahil edilmesi
import xml.etree.ElementTree as ET
from PIL import Image
import glob
import os

# Değişkenlerin tanımlanması
sayac5 = 1
sayac7_5 = 1
sayac10 = 1
sayac15 = 1
sayac20 = 1
sayac25 = 1
sayac30K = 1
sayac30B = 1
sayac50 = 1
sayac100 = 1
sayac110 = 1
sayac130 = 1


# Gerçekleştirilecek işlemler için fonksiyon oluşturma
def read_content(xml_file: str):
    global sayac5, sayac7_5, sayac10, sayac15, sayac20, sayac25, sayac30B, \
        sayac30K, sayac50, sayac100, sayac110, sayac130

    # XML dosyası okuma
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # XMl dosyası içindeki verileri kullanma
    for boxes in root.iter('object'):

        filename = root.find('filename').text
        im = Image.open(r"labeleddata/1400fusebox/" + filename)
        ymin, xmin, ymax, xmax = None, None, None, None

        for box in boxes.findall("bndbox"):
            name = boxes.find("name").text
            ymin = int(box.find("ymin").text)
            xmin = int(box.find("xmin").text)
            ymax = int(box.find("ymax").text)
            xmax = int(box.find("xmax").text)

            if name == "5AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("5\\" + str(sayac5) + '.jpg', 'JPEG')
                sayac5 += 1

            elif name == "7.5AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("7.5\\" + str(sayac7_5) + '.jpg', 'JPEG')
                sayac7_5 += 1

            elif name == "10AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("10\\" + str(sayac10) + '.jpg', 'JPEG')
                sayac10 += 1

            elif name == "15AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("15\\" + str(sayac15) + '.jpg', 'JPEG')
                sayac15 += 1

            elif name == "20AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("20\\" + str(sayac20) + '.jpg', 'JPEG')
                sayac20 += 1

            elif name == "25AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("25\\" + str(sayac25) + '.jpg', 'JPEG')
                sayac25 += 1

            elif name == "30KAMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("30K\\" + str(sayac30K) + '.jpg', 'JPEG')
                sayac30K += 1

            elif name == "30BAMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("30B\\" + str(sayac30B) + '.jpg', 'JPEG')
                sayac30B += 1

            elif name == "50AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("50\\" + str(sayac50) + '.jpg', 'JPEG')
                sayac50 += 1

            elif name == "100AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("100\\" + str(sayac100) + '.jpg', 'JPEG')
                sayac100 += 1

            elif name == "110AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("110\\" + str(sayac110) + '.jpg', 'JPEG')
                sayac110 += 1


            elif name == "130AMP":
                cropped = im.crop((xmin, ymin, xmax, ymax))
                cropped.save("130\\" + str(sayac130) + '.jpg', 'JPEG')
                sayac130 += 1

            else:
                pass


for eleman in glob.glob("labeleddata/1400fuseboxannotion/*.xml"):
    isim, uzanti = os.path.splitext(eleman)
    read_content(xml_file=isim + uzanti)



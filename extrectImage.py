import PyPDF2
import os
import sys
from PIL import Image
from io import BytesIO
import struct
import numpy as np

###
# PDF file image extractor
# Author: BJ Jang (jangbi882 at gmail.com)
# License: GPL2
# Referenced source: https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
###

TEST_FILE = r"/Temp/book1.pdf"
TEST_OUT_FOLDER = "/Temp"
TEST_PAGE = None
DEBUG_MODE = True
DEFAULT_PALETTE = b'\xff\xff\xff\xfe\xfe\xfe\xfd\xfd\xfd\xfc\xfc\xfc\xfb\xfb\xfb' \
                  b'\xfa\xfa\xfa\xf9\xf9\xf9\xf8\xf8\xf8\xf7\xf7\xf7\xf6\xf6\xf6' \
                  b'\xf5\xf5\xf5\xf4\xf4\xf4\xf3\xf3\xf3\xf2\xf2\xf2\xf1\xf1\xf1' \
                  b'\xf0\xf0\xf0\xef\xef\xef\xee\xee\xee\xed\xed\xed\xec\xec\xec' \
                  b'\xeb\xeb\xeb\xea\xea\xea\xe9\xe9\xe9\xe8\xe8\xe8\xe7\xe7\xe7' \
                  b'\xe6\xe6\xe6\xe5\xe5\xe5\xe4\xe4\xe4\xe3\xe3\xe3\xe2\xe2\xe2' \
                  b'\xe1\xe1\xe1\xe0\xe0\xe0\xdf\xdf\xdf\xde\xde\xde\xdd\xdd\xdd' \
                  b'\xdc\xdc\xdc\xdb\xdb\xdb\xda\xda\xda\xd9\xd9\xd9\xd8\xd8\xd8' \
                  b'\xd7\xd7\xd7\xd6\xd6\xd6\xd5\xd5\xd5\xd4\xd4\xd4\xd3\xd3\xd3' \
                  b'\xd2\xd2\xd2\xd1\xd1\xd1\xd0\xd0\xd0\xcf\xcf\xcf\xce\xce\xce' \
                  b'\xcd\xcd\xcd\xcc\xcc\xcc\xcb\xcb\xcb\xca\xca\xca\xc9\xc9\xc9' \
                  b'\xc8\xc8\xc8\xc7\xc7\xc7\xc6\xc6\xc6\xc5\xc5\xc5\xc4\xc4\xc4' \
                  b'\xc3\xc3\xc3\xc2\xc2\xc2\xc1\xc1\xc1\xc0\xc0\xc0\xbf\xbf\xbf' \
                  b'\xbe\xbe\xbe\xbd\xbd\xbd\xbc\xbc\xbc\xbb\xbb\xbb\xba\xba\xba' \
                  b'\xb9\xb9\xb9\xb8\xb8\xb8\xb7\xb7\xb7\xb6\xb6\xb6\xb5\xb5\xb5' \
                  b'\xb4\xb4\xb4\xb3\xb3\xb3\xb2\xb2\xb2\xb1\xb1\xb1\xb0\xb0\xb0' \
                  b'\xaf\xaf\xaf\xae\xae\xae\xad\xad\xad\xac\xac\xac\xab\xab\xab' \
                  b'\xaa\xaa\xaa\xa9\xa9\xa9\xa8\xa8\xa8\xa7\xa7\xa7\xa6\xa6\xa6' \
                  b'\xa5\xa5\xa5\xa4\xa4\xa4\xa3\xa3\xa3\xa2\xa2\xa2\xa1\xa1\xa1' \
                  b'\xa0\xa0\xa0\x9f\x9f\x9f\x9e\x9e\x9e\x9d\x9d\x9d\x9c\x9c\x9c' \
                  b'\x9b\x9b\x9b\x9a\x9a\x9a\x99\x99\x99\x98\x98\x98\x97\x97\x97' \
                  b'\x96\x96\x96\x95\x95\x95\x94\x94\x94\x93\x93\x93\x92\x92\x92' \
                  b'\x91\x91\x91\x90\x90\x90\x8f\x8f\x8f\x8e\x8e\x8e\x8d\x8d\x8d' \
                  b'\x8c\x8c\x8c\x8b\x8b\x8b\x8a\x8a\x8a\x89\x89\x89\x88\x88\x88' \
                  b'\x87\x87\x87\x86\x86\x86\x85\x85\x85\x84\x84\x84\x83\x83\x83' \
                  b'\x82\x82\x82\x81\x81\x81\x80\x80\x80\x7f\x7f\x7f~~~}}}|||{{{' \
                  b'zzzyyyxxxwwwvvvuuutttsssrrrqqqpppooonnnmmmlllkkkjjjiiihhhggg' \
                  b'fffeeedddcccbbbaaa```___^^^]]]\\\\\\[[[ZZZYYYXXXWWWVVVUUUTTT' \
                  b'SSSRRRQQQPPPOOONNNMMMLLLKKKJJJIIIHHHGGGFFFEEEDDDCCCBBBAAA@@@' \
                  b'???>>>===<<<;;;:::999888777666555444333222111000///...---,,,' \
                  b'+++***)))(((\'\'\'&&&%%%$$$###"""!!!   \x1f\x1f\x1f\x1e\x1e\x1e' \
                  b'\x1d\x1d\x1d\x1c\x1c\x1c\x1b\x1b\x1b\x1a\x1a\x1a\x19\x19\x19' \
                  b'\x18\x18\x18\x17\x17\x17\x16\x16\x16\x15\x15\x15\x14\x14\x14' \
                  b'\x13\x13\x13\x12\x12\x12\x11\x11\x11\x10\x10\x10\x0f\x0f\x0f' \
                  b'\x0e\x0e\x0e\r\r\r\x0c\x0c\x0c\x0b\x0b\x0b\n\n\n\t\t\t\x08\x08' \
                  b'\x08\x07\x07\x07\x06\x06\x06\x05\x05\x05\x04\x04\x04\x03\x03' \
                  b'\x03\x02\x02\x02\x01\x01\x01\x00\x00\x00'


def parseParam():
    sourceName = None
    outputFolder = None
    targetPage = None

    if len(sys.argv) <= 1:
        if not DEBUG_MODE:
            printHelp()
        else:
            sourceName = TEST_FILE
            outputFolder = TEST_OUT_FOLDER
            targetPage = TEST_PAGE
    else:
        sourceName = sys.argv[1]
        if len(sys.argv) >= 2:
            outputFolder = "."
        else:
            outputFolder = sys.argv[2]
        targetPage = None
        if len(sys.argv) >= 3:
            try:
                targetPage = int(sys.argv[3])
            except ValueError:
                targetPage = None
    return (sourceName, outputFolder, targetPage)


def printHelp():
    print("[USAGE] python extractImage.py <prf_file_path> [output_folder]")
    exit(0)


def main():
    sourceName, outputFolder, targetPage = parseParam()
    fileBase = os.path.splitext(os.path.basename(sourceName))[0]
    pdfObj = PyPDF2.PdfFileReader(open(sourceName, "rb"))
    for iPage in range(0, pdfObj.numPages):
        pageObj = pdfObj.getPage(iPage)

        if targetPage and (iPage+1 != targetPage):
            print("Skip page {}.".format(iPage + 1))
            continue
        print("Processing page {}...".format(iPage+1))

        try:
            xObject = pageObj['/Resources']['/XObject'].getObject()
        except KeyError:
            continue

        iImage = 0
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                iImage += 1
                title = obj[1:]
                fileName = "{2}_p{0:0>3}_{3}".format(iPage+1, iImage, fileBase, title)
                outFileName = os.path.join(outputFolder, fileName)

                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])

                colorSpace = xObject[obj]['/ColorSpace']
                if colorSpace == '/DeviceRGB':
                    mode = "RGB"
                elif colorSpace == '/DeviceCMYK':
                    mode = "CMYK"
                elif colorSpace[0] == "/Indexed":
                    mode = "P"
                    colorSpace, base, hival, lookup = [v.getObject() for v in colorSpace]
                    palette = lookup.getData()
                elif colorSpace[0] == "/ICCBased":
                    mode = "P"
                    lookup = colorSpace[1].getObject()
                    palette = lookup.getData()
                elif colorSpace[0] == "/DeviceN":
                    # UNKNOWN TYPE
                    mode = "P"
                    palette = DEFAULT_PALETTE
                else:
                    mode = "P"
                    if hasattr(colorSpace, "__len__"):
                        lookup = colorSpace[1].getObject()
                        palette = lookup.getData()
                        print("[FILE]"+fileName+" [MODE] "+colorSpace[0]+" [FILTER]"+xObject[obj]['/Filter'])
                    else:
                        palette = DEFAULT_PALETTE
                        print("[FILE]"+fileName+" [MODE]: "+colorSpace+" [FILTER]"+xObject[obj]['/Filter'])

                try:
                    if xObject[obj]['/Filter'] == '/FlateDecode':
                        data = xObject[obj].getData()
                        img = Image.frombytes(mode, size, data)
                        if mode == "P":
                            img.putpalette(palette)
                        if mode == "CMYK":
                            img = img.convert('RGB')
                        img.save(outFileName + ".png")

                    elif xObject[obj]['/Filter'] == '/DCTDecode':
                        data = xObject[obj]._data

                        jpgData = BytesIO(data)
                        img = Image.open(jpgData)
                        if mode == "CMYK":
                            # case of CMYK invert all channel

                            # imgData = list(img.tobytes())
                            # invData = [(255 - val) & 0xff for val in imgData]
                            # data = struct.pack("{}B".format(len(invData)), *invData)
                            # img = Image.frombytes(img.mode, img.size, data)

                            imgData = np.frombuffer(img.tobytes(), dtype='B')
                            invData = np.full(imgData.shape, 255, dtype='B')
                            invData -= imgData
                            img = Image.frombytes(img.mode, img.size, invData.tobytes())
                            img.save(outFileName + ".jpg")

                    elif xObject[obj]['/Filter'] == '/JPXDecode':
                        data = xObject[obj]._data
                        img = open(outFileName + ".jp2", "wb")
                        img.write(data)
                        img.close()
                except Exception as ex:
                    print("[ERROR] "+fileName)
                    print("\t" + str(ex))
    print("Completed.")


if __name__ == '__main__':
    main()

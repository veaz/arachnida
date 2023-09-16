import exifread
import sys

class bcolors:
    OK = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    RESET = "\033[0m"

def metadata(name):
    try:
        imagen = open(name, 'rb')
    except:
        print(bcolors.FAIL + "Error: image " + name + " cant be open" + bcolors.RESET)
        return
    print(bcolors.OK + "##############################################\nImage: " + name + "\n##############################################" + bcolors.RESET)
    valores_exif = exifread.process_file(imagen)
    if len(valores_exif) == 0:
        print(bcolors.WARNING + "Warning: metadata not foud" + bcolors.RESET)
    for tag in valores_exif.keys():
        if tag is not "JPEGThumbnail":
            print(bcolors.WARNING + str(tag) + bcolors.RESET + " : " + str(valores_exif[tag]))

def small_metadata(name):
    small_cases = [1 , 2, 4, 5, 9, 10, 11, 14, 15, 16, 17, 30, 31, 35, 41, 48, 55, 56]
    x = 0
    try:
        image = open(name, 'rb')
    except:
        print(bcolors.FAIL + "Error: image " + name + " cant be open" + bcolors.RESET)
        return
    print(bcolors.OK + "##############################################\nImage: " + name + "\n##############################################" + bcolors.RESET)
    valores_exif = exifread.process_file(image)
    if len(valores_exif) == 0:
        print(bcolors.WARNING + "Warning: metadata not foud" + bcolors.RESET)
    for tag in valores_exif.keys():
        x += 1
        if x in small_cases:
            print(bcolors.WARNING + str(tag) + bcolors.RESET + " : " + str(valores_exif[tag]))

if __name__ == '__main__':
    n_images = len(sys.argv) - 1
    if n_images > 0:
        images = [images for images in sys.argv[1:]]
        if images[0] == "-s":
            print(bcolors.WARNING + "Scorpion ~ Small version" + bcolors.RESET)
            images.remove("-s")
            for image in images:
                small_metadata(image)
        else:
            for image in images:
                metadata(image)
    else:
        print("Error: invalid numbers of arguments")
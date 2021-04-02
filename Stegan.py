from PIL import Image
def Encode(img, msg, lst):
    length=len(msg)
    width, height = img.size
    if length > width*height:
        print("Text too long! (don't exeed " + str(width*height) + " characters)")
        return False
    if img.mode != 'RGB':
        print("Image mode needs to be RGB")
        return False
    # Making deep copy of image to make encryption! with original image intact
    encoded_img = img.copy()
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            r = r >> 2
            r = r << 2
            g = g >> 2
            g = g << 2
            b = b >> 3
            b = b << 3
            if index < length:
                c = lst[index]
                cb = c >> 4
                b = b | cb
                cb = cb << 4
                cg = (c - cb) >> 2
                g = g | cg
                cg = cg << 2
                cr = (c - cb - cg)
                r = r | cr
            elif index == length:
                b = b | 7
                g = g | 3
                r = r | 3 
            encoded_img.putpixel((col, row), (r, g, b))
            index += 1
    return encoded_img

# Decode function of Steganography

def Decode(img):
    width, height = img.size
    lst = []
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                r, g, b, a = img.getpixel((col, row))
            cr = r & 3
            cb = b & 7
            cg = g & 3
            cb = cb << 4
            cg = cg << 2
            value = cb + cg + cr
            if (value == 127):
                return lst
            lst += [value]
    return lst

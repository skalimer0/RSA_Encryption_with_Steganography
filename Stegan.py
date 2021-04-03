from PIL import Image

def bitLenCount(int_type):
    length = 0
    count = 0
    while (int_type):
        count += (int_type & 1)
        length += 1
        int_type >>= 1
    return(length, count)

def Encode(img, msg, lst, n):
    if img.mode != 'RGB':
        print("Image mode needs to be RGB")
        return False

    length=len(msg)
    width, height = img.size
    bitLen, _ = bitLenCount(n)
    form = "{0:0" + str(bitLen) + "b}"
    print("We need %s bits to encode a value" % (bitLen))
    print("We need %s bits to encode the message" % (bitLen * length))

    if (bitLen * length) + 2 > (24 * width * height):
        print("Make your choice: Text too long or RSA too strong or image too small!")
        return False

    bitByPixel = (bitLen * length) // (width * height - 2)
    if (bitLen * length) % (width * height - 2) != 0:
        bitByPixel = bitByPixel + 1
    print("We need %s bits by pixel to write the message" % (bitByPixel))
    rbit = bitByPixel // 3
    bbit = bitByPixel // 3
    gbit = bitByPixel // 3
    if bitByPixel % 3 == 1:
        rbit = rbit + 1
    elif bitByPixel % 3 == 2:
        rbit = rbit + 1
        bbit = bbit + 1

    binaryValues = ""
    for value in lst:
        binaryValues += form.format(value)

    # Making deep copy of image to make encryption! with original image intact
    encoded_img = img.copy()
    binary_index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if col == 0 and row == 0:
                # to know how many bits by color is used
                r = r >> (rbit + 1)
                r = r << (rbit + 1)
                r = r | ((2 ** rbit) - 1)
                g = g >> (gbit + 1)
                g = g << (gbit + 1)
                g = g | ((2 ** gbit) - 1)
                b = b >> (bbit + 1)
                b = b << (bbit + 1)
                b = b | ((2 ** bbit) - 1)

            elif binary_index < len(binaryValues):                
                if rbit > 0:
                    r = r >> rbit
                    r = r << rbit
                    value =  int(binaryValues[binary_index:binary_index+rbit], 2)
                    r = r | value
                    binary_index += rbit
                if gbit > 0:
                    g = g >> gbit
                    g = g << gbit
                    value =  int(binaryValues[binary_index:binary_index+gbit], 2)
                    g = g | value
                    binary_index += gbit
                if bbit > 0:
                    b = b >> bbit
                    b = b << bbit
                    value =  int(binaryValues[binary_index:binary_index+bbit], 2)
                    b = b | value
                    binary_index += bbit

            elif binary_index == len(binaryValues):
                # to know how many bits by color is used
                r = r >> rbit
                r = r << rbit
                g = g >> gbit
                g = g << gbit
                b = b >> bbit 
                b = b << bbit

            encoded_img.putpixel((col, row), (r, g, b))
    return encoded_img

# Decode function of Steganography
def Decode(img, n):
    if img.mode != 'RGB':
        print("Image mode needs to be RGB")
        return False
    width, height = img.size
    bitLen, _ = bitLenCount(n)
    lst = []
    binary_value = ""
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if col == 0 and row == 0:
                binR = '{0:08b}'.format(r)
                rbit = 7 - binR.rfind('0')
                formr = "{0:0" + str(rbit) + "b}"
                binR = '{0:08b}'.format(g)
                gbit = 7 - binR.rfind('0')
                formg = "{0:0" + str(rbit) + "b}"
                binR = '{0:08b}'.format(b)
                bbit = 7 - binR.rfind('0')
                formb = "{0:0" + str(rbit) + "b}"
            else:
                valuer = r & ((2 ** rbit) - 1)
                valueg = g & ((2 ** gbit) - 1)
                valueb = b & ((2 ** bbit) - 1)
                temp_binary = ""
                if rbit > 0:
                    temp_binary += formr.format(valuer)
                if gbit > 0:
                    temp_binary += formg.format(valueg)
                if bbit > 0:
                    temp_binary += formb.format(valueb)
                binary_value += temp_binary
    index = 0
    index_last_value = binary_value.rfind('1')
    while index + bitLen < index_last_value + bitLen:
        lst += [int(binary_value[index:index+bitLen], 2)]
        index += bitLen
    return lst

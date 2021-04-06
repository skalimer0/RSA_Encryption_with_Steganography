from PIL import Image

def bitLenCount(int_type):
    length = 0
    count = 0
    while (int_type):
        count += (int_type & 1)
        length += 1
        int_type >>= 1
    return(length, count)

def Encode(img, length, lst, n):
    if img.mode != 'RGB':
        print("Image mode needs to be RGB")
        return False

    fileSizeNbByteEncode = 32
    width, height = img.size
    bitLen, _ = bitLenCount(n)
    form = "{0:0" + str(bitLen) + "b}"
    print("We need %s bits to write a value" % (bitLen))
    print("We need %s bits to write the message" % (bitLen * length))

    if (bitLen * length) + 1 + fileSizeNbByteEncode > 12 * width * height:
        print("Make your choice: Text too long or RSA too strong or image too small, this exceed 12 bits par pixel")
        return False

    bitByPixel = ((bitLen * length) + fileSizeNbByteEncode) // (width * height - 1)
    if ((bitLen * length) + fileSizeNbByteEncode) % (width * height - 1) != 0:
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
    # Save the file size (on 24bits > 16 Mo)
    binarySize = ("{0:0" + str(fileSizeNbByteEncode) + "b}").format(bitLen * length)
    # Making deep copy of image to make encryption! with original image intact
    encoded_img = img.copy()
    binary_index = 0
    binaryData = binarySize
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
            else:                                    
                for i in range(rbit,0,-1):
                    if binary_index < len(binaryData):
                        r = r >> i
                        r = r << i
                        fact = 2 * (i - 1)
                        value =  int(binaryData[binary_index:binary_index+1], 2)
                        if fact > 0:
                            value = value * fact
                        r = r | value
                        binary_index += 1
                    elif binarySize != "":
                        binaryData = binaryValues
                        r = r >> i
                        r = r << i
                        fact = 2 * (i - 1)
                        value =  int(binaryData[0:1], 2)
                        if fact > 0:
                            value = value * fact
                        r = r | value
                        binary_index = 1
                        binarySize = ""
                if gbit > 0:
                    for i in range(gbit,0,-1):
                        if binary_index < len(binaryData):
                            g = g >> i
                            g = g << i
                            fact = 2 * (i - 1)
                            value =  int(binaryData[binary_index:binary_index+1], 2)
                            if fact > 0:
                                value = value * fact
                            g = g | value
                            binary_index += 1
                        elif binarySize != "":
                            binaryData = binaryValues
                            g = g >> i
                            g = g << i
                            fact = 2 * (i - 1)
                            value =  int(binaryData[0:1], 2)
                            if fact > 0:
                                value = value * fact
                            g = g | value
                            binary_index = 1
                            binarySize = ""
                if bbit > 0:
                    for i in range(bbit,0,-1):
                        if binary_index < len(binaryData):
                            b = b >> i
                            b = b << i
                            fact = 2 * (i - 1)
                            value =  int(binaryData[binary_index:binary_index+1], 2)
                            if fact > 0:
                                value = value * fact
                            b = b | value
                            binary_index += 1
                        elif binarySize != "":
                            binaryData = binaryValues
                            b = b >> i
                            b = b << i
                            fact = 2 * (i - 1)
                            value =  int(binaryData[0:1], 2)
                            if fact > 0:
                                value = value * fact
                            b = b | value
                            binary_index = 1
                            binarySize = ""
            encoded_img.putpixel((col, row), (r, g, b))
    return encoded_img

# Decode function of Steganography
def Decode(img, n):
    if img.mode != 'RGB':
        print("Image mode needs to be RGB")
        return False
        
    width, height = img.size
    img_size = 24 * width * height
    lst = []
    index = 0
    binary_value = ""
    bitLen, _ = bitLenCount(n)
    messageSize = img_size
    indexData = 0
    fileSizeNbByteEncode = 32
    dataSize = fileSizeNbByteEncode
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if col == 0 and row == 0:
                binR = '{0:08b}'.format(r)
                rbit = 7 - binR.rfind('0')
                binR = '{0:08b}'.format(g)
                gbit = 7 - binR.rfind('0')
                binR = '{0:08b}'.format(b)
                bbit = 7 - binR.rfind('0')
                nbpixel = rbit + bbit + gbit
                print("%s bits by pixel used by the data" % (nbpixel))
            else:
                for i in range(rbit-1,-1,-1):
                    if indexData < messageSize:
                        if index < dataSize:                 
                            if r & (2 ** i) > 0:
                                binary_value += "1"
                            else:
                                binary_value += "0"
                            index += 1
                            indexData += 1
                        else:
                            if messageSize < img_size:
                                lst += [int(binary_value, 2)]
                            else:
                                messageSize = int(binary_value, 2)
                                dataSize = bitLen
                                indexData = 0
                                print("%s bits used by the data" % (messageSize))
                            if r & (2 ** i) > 0:
                                binary_value = "1"
                            else:
                                binary_value = "0"
                            index = 1
                            indexData += 1
                    elif indexData == messageSize:
                        lst += [int(binary_value, 2)]
                        indexData += 1
                if gbit > 0:
                    for i in range(gbit-1,-1,-1):
                        if indexData < messageSize:
                            if index < dataSize:                 
                                if g & (2 ** i) > 0:
                                    binary_value += "1"
                                else:
                                    binary_value += "0"
                                index += 1
                                indexData += 1
                            else:
                                if messageSize < img_size:
                                    lst += [int(binary_value, 2)]
                                else:
                                    messageSize = int(binary_value, 2)
                                    dataSize = bitLen
                                    indexData = 0
                                    print("%s bits used by the data" % (messageSize))
                                if g & (2 ** i) > 0:
                                    binary_value = "1"
                                else:
                                    binary_value = "0"
                                index = 1
                                indexData += 1
                        elif indexData == messageSize:
                            lst += [int(binary_value, 2)]
                            indexData += 1
                if bbit > 0:
                    for i in range(bbit-1,-1,-1):
                        if indexData < messageSize:
                            if index < dataSize:                 
                                if b & (2 ** i) > 0:
                                    binary_value += "1"
                                else:
                                    binary_value += "0"
                                index += 1
                                indexData += 1
                            else:
                                if messageSize < img_size:
                                    lst += [int(binary_value, 2)]
                                else:
                                    messageSize = int(binary_value, 2)
                                    dataSize = bitLen
                                    indexData = 0
                                    print("%s bits used by the data" % (messageSize))
                                if b & (2 ** i) > 0:
                                    binary_value = "1"
                                else:
                                    binary_value = "0"
                                index = 1
                                indexData += 1
                        elif indexData == messageSize:
                            lst += [int(binary_value, 2)]
                            indexData += 1
    return lst

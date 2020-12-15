
_fileName = "input08.txt"
_imageWidth = 25
_imageHeight = 6

infile = open(_fileName, 'r')
data = infile.read().rstrip()

def parse_input_data(width, height, data):
    layers = []

    x = 0
    y = 0

    currentLayer = [[]];

    for d in data:
        currentLayer[y].append(int(d))

        x += 1

        if x == width:
            x = 0
            y += 1
            currentLayer.append([])

        if y == height:
            y = 0
            currentLayer = currentLayer[:-1]
            layers.append(currentLayer)
            currentLayer = [[]]

    return layers


def digits_per_layer(layer, digit):

    count = 0

    for row in layer:
        for pixel in row:
            if pixel == digit:
                count += 1
    return count


layers = parse_input_data(_imageWidth, _imageHeight, data)

minZeros = _imageWidth * _imageHeight
minZerosLayer = {}

for layer in layers:
    layerZeros = digits_per_layer(layer, 0)
    if layerZeros < minZeros:
        minZeros = layerZeros
        minZerosLayer = layer

ones = digits_per_layer(minZerosLayer, 1)
twos = digits_per_layer(minZerosLayer, 2)
answer = ones * twos

print ('Answer: ', answer)
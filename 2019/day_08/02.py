
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


def render_image_from_layers(layers, width, height):

    image = {}

    for y in range(height):
        image[y] = {}
        for x in range(width):
            image[y][x] = -1
            for l in range(len(layers)):

                if image[y][x] == -1: #Not been set yet
                    image[y][x] = layers[l][y][x]

                if image[y][x] == 2: #Pixel is transparrent
                    image[y][x] = layers[l][y][x]



    return image




layers = parse_input_data(_imageWidth, _imageHeight, data)

renderedImage = render_image_from_layers(layers, _imageWidth, _imageHeight)

from PIL import Image

img = Image.new( 'RGB', (_imageWidth, _imageHeight), "black")
pixels = img.load()

for x in range(_imageWidth):
    for y in range(_imageHeight):
        pixels[x, y] = (255 * renderedImage[y][x], 255 * renderedImage[y][x], 255 * renderedImage[y][x])


img.show()

constChemDataPoints = [
{'x': 4.91, 'y': 1.14},
{'x': 4.74, 'y': 1.23},
{'x': 4.57, 'y': 1.32},
{'x': 4.40, 'y': 1.42},
{'x': 4.23, 'y': 1.52},
{'x': 4.06, 'y': 1.61},
{'x': 3.89, 'y': 1.73},
{'x': 3.72, 'y': 1.83},
{'x': 3.55, 'y': 1.94},
{'x': 3.39, 'y': 2.04},
{'x': 3.22, 'y': 2.18},
{'x': 3.05, 'y': 2.28},
{'x': 2.88, 'y': 2.42},
{'x': 2.71, 'y': 2.56},
{'x': 2.54, 'y': 2.68},
{'x': 2.37, 'y': 2.84},
{'x': 2.20, 'y': 2.98},
{'x': 2.03, 'y': 3.05},
{'x': 1.86, 'y': 3.12},
{'x': 1.69, 'y': 3.25},
{'x': 1.52, 'y': 3.39},
{'x': 1.35, 'y': 3.57},
{'x': 1.18, 'y': 3.84},
{'x': 1.12, 'y': 3.95},
{'x': 1.02, 'y': 3.98},
{'x': 0.85, 'y': 4.12},
{'x': 0.68, 'y': 4.29},
{'x': 0.51, 'y': 4.53},
{'x': 0.34, 'y': 4.85},
{'x': 0.17, 'y': 5.54}
    ]

wmwl = [
    {'x': -11, 'y': -78},
    {'x': 0.1, 'y': 10.8}
]

jezor = [
    {'x': 9, 'y': 5},
    {'x': 8, 'y': 2.5},
    {'x': 7, 'y': 1},
    {'x': 6, 'y': -1},
    {'x': 5, 'y': -2.5},
    {'x': 4, 'y': -5},
    {'x': 3, 'y': -7},
    {'x': 2, 'y': -9},
    {'x': 1.5, 'y': -10.5},
    {'x': 1, 'y': -14},
    {'x': 0.9, 'y': -16},
    {'x': 0.85, 'y': -17.5},
    {'x': 0.9, 'y': -20},
    {'x': 1.1, 'y': -22},
    {'x': 1.5, 'y': -24},
    {'x': 2, 'y': -25},
    {'x': 2.5, 'y': -25.5},
    {'x': 3, 'y': -25},
    {'x': 4, 'y': -23.5},
    {'x': 5, 'y': -21.5},
    {'x': 6, 'y': -19.5},
    {'x': 7, 'y': -17.5},
    {'x': 8, 'y': -15},
    {'x': 9, 'y': -12.5},
    {'x': 10, 'y': -10},
    {'x': 11, 'y': -7.5},
    {'x': 12, 'y': -4.5},
    {'x': 12.5, 'y': -2.5}
]

smow = {'x': 0, 'y': 0}

gorneParowanie = [
    {'x': 0.1, 'y': 2},
    {'x': 2.7, 'y': 13.5}
]

dolneParowanie = [
    {'x': 0.4, 'y': 0},
    {'x': 6, 'y': 10}
]

koncoweParowanie = [
    {'x': 12.2, 'y': 11.5},
    {'x': 12.25, 'y': 10.75},
    {'x': 12.26, 'y': 10},
    {'x': 12.19, 'y': 8.8},
    {'x': 12.11, 'y': 8},
    {'x': 12.05, 'y': 7.5},
    {'x': 11.5, 'y': 4.65},
    {'x': 11, 'y': 2.45}
]

jezor2 = [
    {'x': 5, 'y': -2.5},
    {'x': 4, 'y': -5.5},
    {'x': 3.5, 'y': -8},
    {'x': 3.4, 'y': -10},
    {'x': 3.35, 'y': -12.5},
    {'x': 3.4, 'y': -15},
    {'x': 3.6, 'y': -17.5},
    {'x': 4, 'y': -20},
    {'x': 4.5, 'y': -21},
    {'x': 5, 'y': -21.25},
    {'x': 6, 'y': -19.5}
]

def lineGenerator(a, b, pointsNumber):
    pointList = []
    xRange = b['x'] - a['x']
    yRange = b['y'] - a['y']
    xStep = xRange / float(pointsNumber)
    yStep = yRange / float(pointsNumber)
    for i in range(0, pointsNumber+1):
        pointList.append({ 'x': round(a['x'] + i*xStep, 2), 'y': round(a['y'] + i*yStep, 2) })
    return pointList

wmwl = lineGenerator(wmwl[0], wmwl[1], 100)
gorneParowanie = lineGenerator(gorneParowanie[0], gorneParowanie[1], 30)
dolneParowanie = lineGenerator(dolneParowanie[0], dolneParowanie[1], 60)
koncoweParowanie = koncoweParowanie + lineGenerator(koncoweParowanie[5], koncoweParowanie[7], 10)
jezor = jezor + lineGenerator(jezor[0], jezor[7], 30)
jezor = jezor + lineGenerator(jezor[18], jezor[26], 30)
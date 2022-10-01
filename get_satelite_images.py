"""
Stitch together Google Maps images from lat, long coordinates
Based on work by heltonbiker and BenElgar
Changes:
  * updated for Python 3
  * added Google Cloud Static Maps API key field (now required for access)
  * handle http request exceptions
"""

import requests
from io import BytesIO
from math import log, exp, tan, atan, pi, ceil
from PIL import Image
import sys
import numpy
from datetime import datetime

import road_width_detect

now = datetime.now()

EARTH_RADIUS = 6378137
EQUATOR_CIRCUMFERENCE = 2 * pi * EARTH_RADIUS
INITIAL_RESOLUTION = EQUATOR_CIRCUMFERENCE / 256.0
ORIGIN_SHIFT = EQUATOR_CIRCUMFERENCE / 2.0
GOOGLE_MAPS_API_KEY = ''
MIN_IMAGE_SIZE = 0.05   # 5 meters

ROUTE = [
    (50.853839,-1.45225),
    (50.852403,-1.452057),
    (50.859575,-1.460752),
    (50.859087,-1.461697),
]


def latlontopixels(lat, lon, zoom):
    mx = (lon * ORIGIN_SHIFT) / 180.0
    my = log(tan((90 + lat) * pi/360.0))/(pi/180.0)
    my = (my * ORIGIN_SHIFT) /180.0
    res = INITIAL_RESOLUTION / (2**zoom)
    px = (mx + ORIGIN_SHIFT) / res
    py = (my + ORIGIN_SHIFT) / res
    return px, py

def pixelstolatlon(px, py, zoom):
    res = INITIAL_RESOLUTION / (2**zoom)
    mx = px * res - ORIGIN_SHIFT
    my = py * res - ORIGIN_SHIFT
    lat = (my / ORIGIN_SHIFT) * 180.0
    lat = 180 / pi * (2*atan(exp(lat*pi/180.0)) - pi/2.0)
    lon = (mx / ORIGIN_SHIFT) * 180.0
    return lat, lon


def lower_bound(in_1, in_2):
    if abs(in_1 - in_2) < MIN_IMAGE_SIZE:
        return in_1, in_2 + MIN_IMAGE_SIZE
    return in_1, in_2


def get_maps_image(NW_lat_long, SE_lat_long, zoom=18):

  ullat, ullon = NW_lat_long
  lrlat, lrlon = SE_lat_long

  # Set some important parameters
  scale = 1
  maxsize = 640

  # convert all these coordinates to pixels
  ulx, uly = latlontopixels(ullat, ullon, zoom)
  lrx, lry = latlontopixels(lrlat, lrlon, zoom)

  # calculate total pixel dimensions of final image
  dx, dy = lrx - ulx, uly - lry

  print(dx, dy)

  # calculate rows and columns
  cols, rows = int(ceil(dx/maxsize)), int(ceil(dy/maxsize))

  # calculate pixel dimensions of each small image
  bottom = 120
  largura = int(ceil(dx/cols))  # width
  altura = int(ceil(dy/rows))   # Height
  alturaplus = altura + bottom

  # assemble the image from stitched
  final = Image.new("RGB", (int(dx), int(dy)))
  for x in range(cols):
      for y in range(rows):
          dxn = largura * (0.5 + x)
          dyn = altura * (0.5 + y)
          latn, lonn = pixelstolatlon(ulx + dxn, uly - dyn - bottom/2, zoom)
          position = ','.join((str(latn), str(lonn)))
          print(x, y, position)
          urlparams = {'center': position,
                        'zoom': str(zoom),
                        'size': '%dx%d' % (largura, alturaplus),
                        'maptype': 'satellite',
                        'sensor': 'false',
                        'scale': scale}
          if GOOGLE_MAPS_API_KEY is not None:
            urlparams['key'] = GOOGLE_MAPS_API_KEY

          url = 'http://maps.google.com/maps/api/staticmap'
          try:
            response = requests.get(url, params=urlparams)
            response.raise_for_status()
          except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

          im = Image.open(BytesIO(response.content))
          final.paste(im, (int(x*largura), int(y*altura)))

  return final


def process_route_segment(start_cord, end_cord):
    NW_lat_long = [0, 0]
    SE_lat_long = [0, 0]
    if start_cord[0] > end_cord[0]:
        NW_lat_long[0] = start_cord[0]
        SE_lat_long[0] = end_cord[0]
    else:
        NW_lat_long[0] = end_cord[0]
        SE_lat_long[0] = start_cord[0]

    if start_cord[1] < end_cord[1]:
        NW_lat_long[1] = start_cord[1]
        SE_lat_long[1] = end_cord[1]
    else:
        NW_lat_long[1] = end_cord[1]
        SE_lat_long[1] = start_cord[1]

    if abs(NW_lat_long[0] - SE_lat_long[0]) < 0.0002:
        SE_lat_long[0] -= 0.0002
        NW_lat_long[0] += 0.0002
    if abs(NW_lat_long[1] - SE_lat_long[1]) < 0.0002:
        NW_lat_long[1] -= 0.0002
        SE_lat_long[1] += 0.0002

    print(f"{NW_lat_long=} {SE_lat_long=}")
    result = get_maps_image(NW_lat_long, SE_lat_long, zoom=20)
    time = now.strftime("%H-%M-%S-%fZ")
    result.save(f"final_image_{time}.png", "PNG")
    # result.show()

    result = road_width_detect.get_road_sides(numpy.array(result))
    if result is not None:
        near, far = result
        print(near, far)
        near_m = pixelstolatlon(near, 0, 20)[1] * 111139/4 # Earth coordinates
        far_m = pixelstolatlon(far, 0, 20)[1] * 111139/4 # Earth coordinates
        print(near_m, far_m)
        print(f"road width: {near_m - far_m}")

    else:
        print("UNABLE TO FIND ROAD")

############################################

if __name__ == '__main__':
    process_route_segment(ROUTE[0], ROUTE[1])
    process_route_segment(ROUTE[2], ROUTE[3])

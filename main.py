import json
import pymssql
import matplotlib.path as mplPath
import matplotlib.pyplot as plt
import numpy as np
import time
import random
from shapely.geometry import Polygon, Point

def read_geo_json():
  with open('hexagon_grid.geojson') as f:
      data = json.load(f)

  return data

def print_geo_json(data):
  for feature in data['features']:
    print feature['geometry']['type']
    print feature['geometry']['coordinates']

  print len(data['features'])

def is_in_polygon(polygons, locations):
  freq_map = {}
  bb_path_list = []

  for feature in polygons['features']:
    bb_path = mplPath.Path(np.array(feature['geometry']['coordinates'][0]))
    bb_path_list.append(bb_path)

  for location in locations:
    polygon_id = 0

    for bb_path in bb_path_list:
      res = bb_path.contains_point((location[1], location[0])) # lon, lat

      if res == True:
        if polygon_id in freq_map:
          freq_map[polygon_id] += 1
        else:
          freq_map[polygon_id] = 1

        break

      polygon_id = polygon_id + 1

  return freq_map

def get_random_point_in_polygon(poly):
  (minx, miny, maxx, maxy) = poly.bounds
  while True:
    p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
    if poly.contains(p):
      return p

def generate_random_lat_long_points(number_of_points):
  rand_locations = []
  mypoly = Polygon([
  (40.703286, -74.017739),
  (40.735551, -74.010487),
  (40.752979, -74.007397),
  (40.815891, -73.960540),
  (40.800966, -73.929169),
  (40.783921, -73.94145),
  (40.776122, -73.941965),
  (40.739974, -73.972864),
  (40.729308, -73.971663),
  (40.711614, -73.978014),
  (40.706148, -74.00239),
  (40.702114, -74.009671),
  (40.701203, -74.015164)])

  for i in range(1,number_of_points):
    rand_point = get_random_point_in_polygon(mypoly)
    rand_locations.append((rand_point.x, rand_point.y))

  return rand_locations

def main():
  rand_locations = generate_random_lat_long_points(100000)
  polygons = read_geo_json()

  start = time.time()
  freqMap = is_in_polygon(polygons, rand_locations)
  end = time.time()
  print(end - start)

  X = np.arange(len(freqMap))
  plt.bar(X, freqMap.values(), align='center', width=0.5)
  plt.xticks(X, freqMap.keys())
  ymax = max(freqMap.values()) + 1
  plt.ylim(0, ymax)
  plt.title("Location frequency in hexagonal cells")
  plt.xlabel("Value")
  plt.ylabel("Frequency")
  plt.show()

if __name__ == "__main__":
  main()
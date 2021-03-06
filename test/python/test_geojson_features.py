import logging
import os
import unittest

logging.basicConfig(level=logging.DEBUG)

from . import utils
from jupyterlab_geojs import Scene

ny_polygons = { "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[
      [-78.878369, 42.886447],
      [-76.147424, 43.048122],
      [-75.910756, 43.974784],
      [-73.756232, 42.652579],
      [-75.917974, 42.098687],
      [-78.429927, 42.083639],
      [-78.878369, 42.886447]
    ]]
  },
  "properties": {
    "author": "Kitware",
    "cities": ["Buffalo", "Syracuse", "Watertown", "Albany", "Binghamton", "Olean"]
  }
}

class TestGeoJSONFeatures(unittest.TestCase):

    def test_geojson_features(self):
        '''Test creating geojson features'''
        scene = Scene()
        scene.center = {'x': -76.5, 'y': 43.0};
        scene.zoom = 7;
        scene.create_layer('osm', renderer='canvas');
        feature_layer = scene.create_layer('feature', features=['point', 'line', 'polygon'])
        feature_layer.create_feature('geojson', data=ny_polygons)

        display_model = scene._build_display_model()
        #print(data)

        # Validate display model against schema
        utils.validate_model(display_model)

        # Optionally write result to model file
        utils.write_model(display_model, 'geojson_model.json')

    def test_shpfile_features(self):
        '''Test creating geojson feature from shp file'''
        scene = Scene()
        osm_layer = scene.create_layer('osm');
        feature_layer = scene.create_layer('feature', features=['polygon'])

        filename = os.path.join(utils.data_folder, 'polygons.shp')
        feature = feature_layer.create_feature('polygon', filename)
        display_model = scene._build_display_model()
        utils.validate_model(display_model)
        utils.write_model(display_model, 'shpfile_model.json')

if __name__ == '__main__':
    unittest.main()

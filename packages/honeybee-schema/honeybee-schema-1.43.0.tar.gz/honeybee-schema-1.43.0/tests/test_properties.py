from honeybee_schema.radiance.properties import FaceRadiancePropertiesAbridged, \
    RoomRadiancePropertiesAbridged, ModelRadianceProperties
from honeybee_schema.energy.properties import ModelEnergyProperties

import os
import json

# target folder where all of the samples live
root = os.path.dirname(os.path.dirname(__file__))
target_folder = os.path.join(root, 'samples', 'model')
target_folder_prop = os.path.join(root, 'samples', 'properties')


file_path = os.path.join(target_folder, 'model_complete_office_floor.hbjson')
with open(file_path) as json_file:
    office_model = json.load(json_file)


def test_model_radiance_properties():
    model_rad_props = office_model['properties']['radiance']
    ModelRadianceProperties.parse_obj(model_rad_props)


def test_room_radiance_properties():
    room_prop_abridged = office_model['rooms'][0]['properties']['radiance']
    RoomRadiancePropertiesAbridged.parse_obj(room_prop_abridged)


def test_face_radiance_properties():
    face_prop_abridged = office_model['rooms'][0]['faces'][0]['properties']['radiance']
    FaceRadiancePropertiesAbridged.parse_obj(face_prop_abridged)


def test_model_energy_properties_office():
    file_path = os.path.join(target_folder_prop, 'model_energy_properties_office.json')
    ModelEnergyProperties.parse_file(file_path)

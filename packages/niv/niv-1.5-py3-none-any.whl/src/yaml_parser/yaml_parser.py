"""
Parses given .yaml file
"""
import errno
import os
from sys import platform
import yaml


def get_yaml(path):
    """
    Reads in a .yaml file from a given path

    :param path: path to the .yaml file
    :return: yaml object or Exception
    """
    with open(path, "r") as stream:
        try:
            yaml_parsed = yaml.safe_load(stream)
            return yaml_parsed
        except yaml.YAMLError as exc:
            raise Exception from exc


def create_config_file(path):
    """
    Creates yaml_defaults.yaml at given path

    :param path: path where the .yaml file will be created
    :return: yaml object from get_yaml()
    """
    file_name = path.rsplit('/', 1)[1]
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if file_name == 'config.yaml':
        with open(path, 'w') as file:
            file.write(get_config_preset())
    else:
        with open(path, 'w') as file:
            file.write(get_yaml_default_preset())

    print(f"No {file_name} found. Creating file in " + path + ".\n")
    return get_yaml(path)


def get_yaml_default_preset():
    """
    Contains preset of yaml_default necessary for creating a new yaml_defaults.yaml

    :return: data for yaml_default.yaml
    """
    data = """\
diagram:
    backgroundColor: # Background color of the diagram (default: transparent; type: string; list of all available colors: https://graphviz.org/doc/info/colors.html#svg)
    padding: # Padding around the graph (default: 0.5; type: double)
    layout: # Name of the layout algorithm to use (default: fdp; type: string; options: fdp, dot, neato(only way to use coordinates))
    connectionStyle: # Style of connections between nodes (default: spline; type: string; options: spline, curved, ortho)
    direction: # Sets direction of graph layout (default: LR; type: string; options: LR, RL, TB, BT)
title:
    text: # Title under the Diagram (default: Diagram; type: string)
    subText: # Text underneath the title (default: ""; type: string)
    fontSize: # Font size (default: 15; type: int)
    author: # Name of author (default: ""; type: string)
    company: # Name of company (default: ""; type: string)
    date: # Date (default: current date; type: string)
    version: # Version of the diagram (default: 1.0; type: double)
    fontColor: # Color of the title text (default: black, type: string) 
nodes:
    name: # Icon name (default: "Node"; type: string)
    x: # X-Coordinate of icon (default: 0; type: int)
    y: # Y-Coordinate of icon (default: 0; type: int)
    ip: # IP-Address of device/icon (default: ""; type: string)
    tooltip: # Text shown at the bottom of the tooltip (default: ""; type: string)
    mac: # MAC-Address shown in the tooltip (default: ""; type: string)
    modelnr: # model number shown in the tooltip (default: ""; type: string)
    manufacturer: # Manufacturer shown in the tooltip (default: ""; type: string)
    storage: # Storage information shown in the tooltip (default: ""; type: string)
    switch-view: # Turn on switch view to see ports (default: False; type: bool)
    ports: # Amount of ports shown when switch-view is True (default: 24; type: int)   
groups:
    name: # Name of group (default: Group; type: string)
    tooltip: # Text shown at the bottom of the tooltip (default: ""; type: string)
    layout: # Specific layout for this group (default: ""; type: string)
    rack: # Turn on rack view to sort the subgroup vertically (default: False; type: bool)
connections:
    text: # Connection description (default: ""; type: string)
    color: # Color of connection-stroke (default: #7B8894; type: string)
    width: # Width of connection-stroke (default: 1; type: int)
    showports: # Visibility of ports next to connection (default: false; type: bool)
    tooltip: # Text shown at the bottom of the tooltip (default: ""; type: string)
"""
    return data


def get_config_preset():
    """
    Contains preset of config.yaml necessary for creating a new config.yaml

    :return: data for config.yaml
    """
    data = """\
default:            
    std_type: ".svg" # Default output type            
    std_details: 2 # Default level of Detail // 0 = all detail levels, 1 = least detail, 2 = most detail            
    open_on_creation: True # Open in browser after the diagram is built, True or False
"""
    return data


def get_path_to_config():
    """
    Returns path to config directory for current platform

    :return: path to config directory
    """
    # Check if platform is linux or mac
    if platform in ('linux', 'darwin'):
        return os.getenv('HOME') + '/.config/niv'
    # Windows
    return os.getenv('APPDATA') + '/niv'

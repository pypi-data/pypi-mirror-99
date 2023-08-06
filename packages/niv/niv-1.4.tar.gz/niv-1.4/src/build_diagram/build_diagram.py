# pylint: disable=unused-wildcard-import, method-hidden
# pylint: disable=unused-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-statements
# pylint: disable=too-many-nested-blocks
"""
build_diagram.py
Dynamically creates the diagram
"""
import ipaddress
from datetime import datetime

from src.diagrams.icons.VRT_dark_png import *
from src.diagrams.icons.VRT_light_png import *
from src.diagrams.icons.VRT_dark_svg import *
from src.diagrams.icons.VRT_light_svg import *
from src.niv_logger import niv_logger
from src.diagrams import *
from src.diagrams.icons.ciscoPng import *
from src.diagrams.icons.osa import *
from src.diagrams.icons.cisco import *
from src.diagrams.icons.osaPng import *
from src.yaml_parser import yaml_parser


class BuildDiagram:
    """
    Handles creation of diagram
    """
    path_to_project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = yaml_parser.get_yaml(path_to_project + '/config.yaml')

    # logging.basicConfig(filename='logs/arg_parser.log', level=logging.DEBUG)
    logger = niv_logger.NivLogger

    # Read yaml_defaults.yaml if it exists, otherwise create the file and assign empty default to yaml_defaults
    yaml_defaults = yaml_parser.get_yaml(path_to_project + '/yaml_defaults.yaml') if os.path.isfile(
        path_to_project + '/yaml_defaults.yaml') else yaml_parser.create_yaml_defaults(
        path_to_project + '/yaml_defaults.yaml')

    counter = 1

    def __init__(self, load_path, save_path, detail_level, verbose):
        # Initialize variables for dynamically getting the values from the .yaml file

        # get verbosity level (True/False)
        self.verbose = verbose

        # Load the .yaml from the given path
        self.yaml = yaml_parser.get_yaml(load_path)
        self.save_path = save_path[0] if save_path is not None \
            else f"./Diagram{self.config.get('default').get('std_type') or '.svg'}"
        self.load_path = load_path
        self.detail_level = detail_level
        self.output_format = self.save_path.split('.')[-1]
        self.filename = os.path.splitext(self.save_path)[0]

        # Load diagram properties
        self.graph_bg_color = self.set_variables("diagram", "backgroundColor",
                                                 self.yaml_defaults.get('diagram').get(
                                                     'backgroundColor') or 'transparent')
        self.graph_padding = self.set_variables("diagram", "padding", self.yaml_defaults.get('diagram').get(
            'padding') or 0.5)
        self.graph_layout = self.set_variables("diagram", "layout", self.yaml_defaults.get('diagram').get(
            'layout') or "fdp")
        self.graph_splines = self.set_variables("diagram", "connectionStyle", self.yaml_defaults.get('diagram').get(
            'connectionStyle') or "spline")
        self.graph_direction = self.set_variables("diagram", "direction", self.yaml_defaults.get('diagram').get(
            'direction') or "LR")

        # Load title properties (others are in set_diagram_title())
        self.title_font_size = self.set_variables("title", "fontSize", self.yaml_defaults.get('title').get(
            'fontSize') or 15)

        self.title_font_color = self.set_variables("title", "fontColor", self.yaml_defaults.get('title').get(
            'fontColor') or "black")

        # Get icon of each node
        self.nodes_icon = self.fill_dictionary("nodes", "icon", "")

        # Get text of each node
        self.nodes_name = self.fill_dictionary("nodes", "name", self.yaml_defaults.get('nodes').get(
            'name') or "Node")

        # Get Ports-number of each switch default = 24
        self.switch_ports = self.fill_dictionary("nodes", "ports", self.yaml_defaults.get('nodes').get(
            'ports') or 24)

        # Get if type switch of each nodes
        self.switch_type = self.fill_dictionary("nodes", "switch-view", self.yaml_defaults.get('nodes').get(
            'switch-view') or False)

        # Get ip of each node
        self.nodes_ip = self.fill_dictionary("nodes", "ip", self.yaml_defaults.get('nodes').get(
            'ip') or "")

        # Get port of each node
        self.nodes_port = self.fill_dictionary("nodes", "port", self.yaml_defaults.get('nodes').get(
            'port') or "")

        # Get the URL of each node, clear empty URLs
        self.nodes_url = self.fill_dictionary("nodes", "url", self.yaml_defaults.get('nodes').get(
            'url') or "")

        # Get the tooltip of each node
        self.nodes_tooltip = self.fill_dictionary("nodes", "tooltip", self.yaml_defaults.get('nodes').get(
            'tooltip') or "")

        # Get mac addresses of each node
        self.nodes_mac = self.fill_dictionary("nodes", "mac", self.yaml_defaults.get('nodes').get(
            'mac') or "")

        # Get model number of each node
        self.nodes_modelnr = self.fill_dictionary("nodes", "modelnr", self.yaml_defaults.get('nodes').get(
            'modelnr') or "")

        # Get manufacturer of each node
        self.nodes_manufactuer = self.fill_dictionary("nodes", "manufacturer", self.yaml_defaults.get('nodes').get(
            'manufacturer') or "")

        # Get storage information of each node
        self.nodes_storage = self.fill_dictionary("nodes", "storage", self.yaml_defaults.get('nodes').get(
            'storage') or "")

        # Get X coordinate of each node
        self.nodes_x = self.fill_dictionary("nodes", "x", self.yaml_defaults.get('nodes').get(
            'x') or 0)

        # Get Y coordinate of each node
        self.nodes_y = self.fill_dictionary("nodes", "y", self.yaml_defaults.get('nodes').get(
            'y') or 0)

        # Get name of each group
        self.group_name = self.fill_dictionary("groups", "name", self.yaml_defaults.get('groups').get(
            'name') or "Group")

        # Get members of each group
        self.group_members = self.fill_dictionary("groups", "members", "")

        # Get the URL of each group, clear empty URLs
        self.group_url = self.fill_dictionary("groups", "url", self.yaml_defaults.get('groups').get(
            'url') or "")

        # Get the tooltip of each group
        self.group_tooltip = self.fill_dictionary("groups", "tooltip", "")

        # Save each endpoint of a connection as a list
        self.connections_endpoints = []
        for i in range(0, len(self.yaml.get("connections"))):
            self.connections_endpoints.append(self.yaml.get("connections")[i].get("endpoints"))

        # Get each port of a connection as a list
        self.connections_ports = []
        for i in range(0, len(self.yaml.get("connections"))):
            if self.yaml.get("connections")[i].get("ports") is not None:
                self.connections_ports.append(self.yaml.get("connections")[i].get("ports"))
            else:
                self.connections_ports.append(["", ""])

        # Get color of connections
        self.connections_color = self.fill_connection_dictionary("connections", "color",
                                                                 self.yaml_defaults.get('connections').get(
                                                                     'color') or "#7B8894")

        # Get text of connections
        self.connections_text = self.fill_connection_dictionary("connections", "text",
                                                                self.yaml_defaults.get('connections').get(
                                                                    'text') or "")

        # Get width of connections
        self.connections_width = self.fill_connection_dictionary("connections", "width", "")

        # Get the tooltip of each connection
        self.connections_tooltip = self.fill_connection_dictionary("connections", "tooltip", "")

        # Get the visibility of port of each connection
        self.connections_visibility = self.fill_connection_dictionary("connections", "showports",
                                                                      self.yaml_defaults.get('connections').get(
                                                                          'showports') or False)

        self.instances_keys = []
        self.instances = []
        self.members = []
        self.nodes_not_in_groups = []
        self.n_url = []

    def create_nodes(self):
        """
        Create nodes outside and inside of clusters
        """
        file_name = os.path.split(self.save_path)[-1]
        file_name = file_name.split('.')[0]
        # Fill "members" list with all the group members
        for group_name in self.group_members:
            for member in list(self.group_members.get(group_name)):
                self.members.append(member)

        # If a node is not a member of a group, create it outside of a cluster
        for node in self.nodes_name:
            if node not in self.members:
                self.create_single_node(node, self.graph_layout, True)
                self.nodes_not_in_groups.append(node)

        # Dynamically create the amount of groups with the corresponding group name
        # If no tooltip is given within the group, set the current name of the group as the tooltip
        for name in self.group_members:
            # Create tooltip for each group
            tooltip = self.create_tooltip(element="group", group=name)

            clustr_attr = {
                "fontname": "helvetica-bold",
                "margin": "20",
                # "URL": f"{self.group_url[name]}"
                # Connect the main diagram with the created under-diagrams with a URL-link
                "URL": f"{file_name}-subdiagrams/{file_name}_{name}.{self.output_format}",
                "tooltip": f"{tooltip}",
                "fontcolor": "black"
            }
            with Cluster(self.group_name[name], graph_attr=clustr_attr):
                # Create a node for each member in every group
                for member in list(self.group_members.get(name)):
                    self.create_single_node(member, self.graph_layout, True)

    def create_connections(self, error: bool):
        """
        Create connections between nodes
        """
        # Check if any endpoints are not given in 'nodes', if not print an error
        for connection in self.connections_endpoints:
            for endpoint in connection:
                if endpoint not in self.nodes_name and error:
                    # Avoid printing the same error message multiple times, just because we call the same function
                    # various times while creating more than 1 diagram
                    log_message = f"KeyError in {self.load_path}: '{endpoint}' is not given in 'nodes', that's why it" \
                                  f" does not show in the diagram. Add it to 'nodes' or remove it as an endpoint."
                    self.logger.verbose_warning(log_message, self.verbose)
                    print(log_message)

        # Create connections
        for i, endpoints in enumerate(self.connections_endpoints):
            first = endpoints[0]
            second = endpoints[1]

            # Only create the connection if both endpoints are instanced as nodes
            if first in self.instances_keys and second in self.instances_keys:
                try:
                    # Create tooltip for each connection
                    tooltip = self.create_tooltip(element="connection", connection=i)

                    # Get index of first and second value to get the corresponding instances
                    first_index = self.instances_keys.index(first)
                    second_index = self.instances_keys.index(second)

                    # If the "showports" parameter is set to true show ports next to connection
                    if self.connections_visibility[i]:
                        _ = self.instances[first_index] - \
                            Edge(color=f"{self.connections_color[i]}",
                                 label=f"{self.connections_text[i]}",
                                 labeltooltip=f"{self.connections_text[i]}",
                                 penwidth=f"{self.connections_width[i]}",
                                 edgetooltip=tooltip) - \
                            self.instances[second_index]
                    else:
                        _ = self.instances[first_index] - \
                            Edge(color=f"{self.connections_color[i]}",
                                 label=f"{self.connections_text[i]}",
                                 labeltooltip=f"{self.connections_text[i]}",
                                 penwidth=f"{self.connections_width[i]}",
                                 edgetooltip=tooltip,
                                 headlabel=f"{self.connections_ports[i][0]}",
                                 labeldistance="3.5",
                                 labelangle="30",
                                 taillabel=f"{self.connections_ports[i][1]}"
                                 ) - \
                            self.instances[second_index]
                except (ValueError, KeyError):
                    pass

        # Clear both lists to have empty lists for every diagram creation to fix not seeing connections
        # when multiple diagrams are created
        self.instances_keys.clear()
        self.instances = []

    def run(self):
        """
        Checks detail level and call create_diagram()
        """
        if self.detail_level == 0:
            for i in range(2):
                self.create_diagram(suffix=str(i))
                self.counter += 1
        else:
            self.create_diagram()

    def create_diagram(self, suffix=""):
        """
        Creates the diagram with the right amount of nodes, clusters and connections
        """
        path, file_name = os.path.split(self.save_path)
        file_name = file_name.split('.')[0]
        path_for_sub_diagrams = f"{path}/{file_name}-subdiagrams/{file_name}" if path != "" \
            else f"{file_name}-subdiagrams/{file_name}"

        graph_attr = {
            "bgcolor": f"{self.graph_bg_color}",
            "pad": f"{self.graph_padding}",
            "layout": f"{self.graph_layout}",
            "fontsize": f"{self.title_font_size}",
            "fontname": "helvetica-bold",
            "nodesep": "1.0",
            "ranksep": "2.0",
            "splines": f"{self.graph_splines}",
            "rankdir": f"{self.graph_direction}",
            "fontcolor": f"{self.title_font_color}"
        }
        with Diagram(self.set_diagram_title(),
                     filename=self.filename + suffix,
                     outformat=self.output_format,
                     show=self.config.get('default').get('open_in_browser'), graph_attr=graph_attr):
            # Create nodes and clusters
            self.create_nodes()
            # Create connections
            self.create_connections(True)
        # Create a separated diagram for each group in the main diagram and save it in group_diagrams/
        for i in self.group_members:
            # if rack in yaml is on True then the direction of the sub-group icons will be Left to Right
            if str(self.yaml.get("groups").get(f"{i}").get("rack")) == "True":
                direction = "LR"
            else:
                direction = "TB"
            # if the sub-group has no layout then the main layout of the diagram will be used instead
            if self.yaml.get("groups").get(f"{i}").get("layout") is None:
                layout = str(self.graph_layout)
            else:
                layout = str(self.yaml.get("groups").get(f"{i}").get("layout"))
            # modify the subgroup with attributes
            subgraph_attr = {
                "bgcolor": f"{self.graph_bg_color}",
                "pad": f"{self.graph_padding}",
                "layout": layout,
                "fontsize": f"{self.title_font_size}",
                "fontname": "helvetica-bold",
                "nodesep": "1.0",
                "ranksep": "2.0",
                "splines": f"{self.yaml.get}",
                "rankdir": direction,
            }
            with Diagram(self.set_diagram_title(),
                         filename=f"{path_for_sub_diagrams}_{i}",
                         outformat=self.output_format,
                         show=False, graph_attr=subgraph_attr):
                # Create tooltip for each group
                tooltip = self.create_tooltip(element="group", group=i)
                clustr_attr = {
                    "fontname": "helvetica-bold",
                    "margin": "20",
                    "tooltip": f"{tooltip}"
                }
                with Cluster(self.yaml.get("groups").get(i).get("name"), graph_attr=clustr_attr):
                    switches_nodes = {}
                    intent_con_ports = {}
                    in_ether_port = {}
                    out_ether_port = {}
                    switches_in_group = []

                    for member in list(self.group_members.get(i)):
                        intent_con_ports[member] = 0
                        in_ether_port[member] = 0
                        out_ether_port[member] = 0

                    self.calculate_connections_in_groups(intent_con_ports, in_ether_port, i)

                    self.create_list_with_switchviews(switches_in_group, out_ether_port, in_ether_port,
                                                      intent_con_ports, layout, switches_nodes, i)

                    self.create_connections_for_switches(switches_nodes, switches_in_group, i)

                    self.create_connections(False)
                    self.instances.clear()

        print("Diagram successfully created")
        self.logger.log("Diagram successfully created")

    def create_connections_for_switches(self, switches_nodes: dict, switches_in_group: list, i: int):
        """
        Create the connection inside the group and between switches

        :param switches_nodes: a dic for all ports for each switch
        :param switches_in_group: a list of all switches in the group with switch-view = True
        :param i: a single group
        """
        counter_for_eth_in_switch = {}
        for switch in switches_in_group:
            counter_for_eth_in_switch[switch] = 0
        # check if instaces != null
        if self.instances:
            # iterate through group_members
            for membr in self.group_members.get(i):
                # iterate through endpoints
                for endpoint in range(len(self.connections_endpoints)):
                    # check if group_member is in endpoints at [0]
                    if membr == self.connections_endpoints[endpoint][0]:
                        # iterate through switches
                        for end_eth in switches_in_group:
                            # check if the other endpoint is a switch
                            if self.connections_endpoints[endpoint][1] == end_eth:
                                eths = switches_nodes.get(end_eth)
                                if membr in switches_in_group:
                                    ets = switches_nodes.get(membr)
                                    _ = ets[counter_for_eth_in_switch[membr]] - eths[
                                        counter_for_eth_in_switch[end_eth]]
                                    counter_for_eth_in_switch[end_eth] += 1
                                    counter_for_eth_in_switch[membr] += 1
                                else:
                                    _ = eths[counter_for_eth_in_switch[end_eth]] - self.instances[
                                        counter_for_eth_in_switch[end_eth]]
                                    counter_for_eth_in_switch[end_eth] += 1

    def create_list_with_switchviews(self, switches_in_group: list, out_ether_port: dict, in_ether_port: dict,
                                     intent_con_ports: dict, layout: str, switches_nodes: dict, i: int):
        """
        Create a list of switches with switch-view for each group

        :param switches_in_group: a list of all switches with switch-view = True in the group
        :param out_ether_port: a list of port, those are connected with a port outside the group
        :param in_ether_port: a list pf ports from the switch those are connected with devices in the same group
        :param intent_con_ports: a list of ports for the switch, those are connected with switch with switch-view = True
        :param layout: a layout for the subgroup
        :param switches_nodes: a dic pf all switches and their ports
        :param i: a single group
        """
        for member in list(self.group_members.get(i)):
            groups_diagrams = []
            if self.switch_type[member]:
                switches_in_group.append(member)
                switch_nodes = []
                # How many ethernet ports are going outside the group ?
                for switch in switches_in_group:
                    out_ether = 0
                    for j in range(len(self.connections_endpoints)):
                        if switch in self.connections_endpoints[j]:
                            if self.connections_endpoints[j][0] not in self.group_members.get(i):
                                out_ether += 1
                            if self.connections_endpoints[j][1] not in self.group_members.get(i):
                                out_ether += 1

                out_ether_port[member] = out_ether

                self.calculate_connections_between_groups(member, groups_diagrams)

                # create the ports with the colored icons for every single switch
                self.create_switch(self.switch_ports[member], self.nodes_name[member], switch_nodes,
                                   in_ether_port[member] + intent_con_ports[member], out_ether_port[member],
                                   groups_diagrams)
                switches_nodes[member] = switch_nodes
            else:
                # Create other devices except switches
                self.create_single_node(member, layout, False)

    def calculate_connections_between_groups(self, member: str, groups_diagrams: list):
        """
        Read url for each port and save it in a list

        :param member: a member of group
        :param groups_diagrams: a list of all subgroup
        """
        for k in range(len(self.connections_endpoints)):
            # check if member in endpoints
            if member in self.connections_endpoints[k]:
                for node in self.nodes_not_in_groups:
                    if node in self.connections_endpoints[k]:
                        self.n_url.append(node)
                # iterate through yaml groups
                for group in self.group_members:
                    # iterate through group members from group
                    for group_member in self.group_members.get(group):
                        # check if group member is in endpoints and if member is in group members
                        # and add it to the list
                        if group_member in self.connections_endpoints[k]:
                            if member not in self.group_members.get(group):
                                groups_diagrams.append(group)
                                groups_diagrams.append(group_member)

    def calculate_connections_in_groups(self, intent_con_ports: dict, in_ether_port: dict, i: int):
        """
        Calculate how many connections are between the switches from the same group and between switches and nodes, with
        switch-view set to False

        switches with switch-view= False for each group :param in_ether_port:a dic of ports, those are connected with
        non switches with switch-view= True for each group :param i:
        """
        for member in list(self.group_members.get(i)):
            in_ethernet = 0
            eth_between_switches = 0
            for membr in self.group_members.get(i):
                for endpoint in range(0, len(self.connections_endpoints)):
                    if (membr == self.connections_endpoints[endpoint][0] and member ==
                            self.connections_endpoints[endpoint][1]):
                        if self.switch_type[membr]:
                            eth_between_switches = eth_between_switches + 1
                            intent_con_ports[membr] = intent_con_ports[membr] + 1
                        in_ethernet = in_ethernet + 1
            in_ether_port[member] = in_ethernet

    def set_diagram_title(self):
        """
        Build title for diagram from title section in .yaml

        :return: Title of diagram
        """
        _dict = {"Title": self.set_variables("title", "text", self.yaml_defaults.get('title').get(
            'text') or "Diagram"),
                 "Description": self.set_variables("title", "subText", self.yaml_defaults.get('title').get(
                     'subText') or ""),
                 "Author": self.set_variables("title", "author", self.yaml_defaults.get('title').get(
                     'author') or ""),
                 "Date": self.set_variables("title", "date", datetime.today().strftime('%d.%m.%Y')),
                 "Company": self.set_variables("title", "company", self.yaml_defaults.get('title').get(
                     'company') or ""),
                 "Version": self.set_variables("title", "version", self.yaml_defaults.get('title').get(
                     'version') or 1.0)}
        title = ""
        for item in _dict:
            if _dict[item] != "":
                title += item + ": " + str(_dict[item]) + "\n"
        return title

    def create_single_node(self, node, layout, error):
        """
        Create an instance of a given node class, if not valid print name of not valid node
        """
        try:
            # Set text label for each node
            node_text = self.set_node_text(node)
            # Remove double newlines for the case when port is given but no url
            node_text = node_text.replace("\n\n", "\n")

            url = self.nodes_url[node]

            # Create tooltip for each node
            tooltip = self.create_tooltip(element="node", node=node)

            try:
                # Only pass coordinates to node creation if layout == neato
                if layout == "neato":
                    pos = f"{self.nodes_x[node]}, {self.nodes_y[node]}!"
                    # If output format is other than svg, create diagram with png icons, else with svg icons
                    if self.output_format != "svg":
                        self.instances.append(
                            globals()[self.nodes_icon[node] + "Png"](node_text,
                                                                     URL=url,
                                                                     pos=pos,
                                                                     tooltip=tooltip,
                                                                     style="rounded",
                                                                     color="red",
                                                                     imagepos="tc",
                                                                     fixedsize="box",
                                                                     width="1",
                                                                     height="2.5",
                                                                     imagescale="true"))
                    else:
                        self.instances.append(
                            globals()[self.nodes_icon[node]](node_text,
                                                             URL=url,
                                                             pos=pos,
                                                             tooltip=tooltip,
                                                             style="rounded",
                                                             color="red",
                                                             imagepos="tc",
                                                             fixedsize="box",
                                                             width="1",
                                                             height="2.5",
                                                             imagescale="true"))
                else:
                    if self.output_format != "svg":
                        self.instances.append(
                            globals()[self.nodes_icon[node] + "Png"](node_text,
                                                                     URL=url,
                                                                     tooltip=tooltip,
                                                                     style="rounded",
                                                                     color="red",
                                                                     imagepos="tc",
                                                                     fixedsize="box",
                                                                     width="1",
                                                                     height="2.5",
                                                                     imagescale="true"
                                                                     ))
                    else:
                        self.instances.append(
                            globals()[self.nodes_icon[node]](node_text,
                                                             URL=url,
                                                             tooltip=tooltip,
                                                             style="rounded",
                                                             color="red",
                                                             imagepos="tc",
                                                             fixedsize="box",
                                                             width="1",
                                                             height="2.5",
                                                             imagescale="true",
                                                             # labelloc="t"
                                                             ))
                self.instances_keys.append(node)
            except KeyError:
                # Avoid printing the same error message multiple times
                if error:
                    log_message = f"KeyError in {self.load_path}: '{self.nodes_icon[node]}' is not a valid icon, " \
                                  f"that's why it does not show in the diagram " \
                                  f"Please take a look at the icon catalog in resources or remove the node."
                    self.logger.verbose_warning(log_message, self.verbose)
                    print(log_message)

        except KeyError:
            # Avoid printing the same error message multiple times
            if error:
                log_message = f"KeyError in {self.load_path}: '{node}' is not given in 'nodes', that's why it does " \
                              f"not show in the diagram. Add it to 'nodes' or remove it as a member."
                self.logger.verbose_warning(log_message, self.verbose)
                print(log_message)

    def set_node_text(self, node) -> str:
        """
        Set text (label) of a given node

        :param node: the node to set the text for
        :return: text of the node
        """
        # For detail level 0 check counter to create corresponding text nodes
        # Counter checks how many diagrams have been created thus far
        if self.detail_level == 0:
            if self.counter == 1:
                node_text = f"\n{self.nodes_name[node]}\n"
            else:
                node_text = f"\n{self.nodes_name[node]}\n" \
                            f" {self.nodes_ip[node]}\n"
        # Detail level 1 shows text and IP's
        elif self.detail_level == 1:
            node_text = f"\n{self.nodes_name[node]}\n"
        # Detail level 2 shows text, IP's and Ports
        else:
            node_text = f"\n{self.nodes_name[node]}\n" \
                        f" {self.nodes_ip[node]}\n"

        # Remove double newlines for the case when port is given but no url
        node_text = node_text.replace("\n\n", "\n")
        return node_text

    def fill_connection_dictionary(self, _object: str, _subobject: str, _default: any) -> dict:
        """
        Fills a given dictionary with color or text of connection from a .yaml

        :param _object: object in the .yaml
        :param _subobject: sub-object in the .yaml
        :param _default: default value for the variable
        :return: filled dictionary
        """
        _dict = {}
        for i, connection in enumerate(self.yaml.get(_object)):
            if connection.get(_subobject) is not None:
                _dict[i] = connection.get(_subobject)
            else:
                _dict[i] = _default
        return _dict

    def fill_dictionary(self, _object: str, _subobject: str, _default: any) -> dict:
        """
        Fills a given dictionary with information from a .yaml

        :param _object: object in the .yaml
        :param _subobject: sub-object in the .yaml
        :param _default: default value for the variable
        :return: filled dictionary
        """
        _dict = {}
        try:

            for i in self.yaml.get(_object):
                _dict[i] = self.yaml.get(_object).get(i).get(_subobject)
                if self.yaml.get(_object)[i].get(_subobject) is None:
                    if _object == "groups" and _subobject == "members":
                        log_message = f"{i}: No members given, group won\'t be shown. Add members to group or remove " \
                                      f"group! :) "
                        self.logger.verbose_warning(log_message, self.verbose)
                        print(log_message)
                    _dict[i] = _default
                elif _subobject == "ip":
                    if not self.validate_ip(_dict[i]):
                        log_message = f"'{_dict[i]}' does not seem to be a valid IPv4 or IPv6 address"
                        self.logger.verbose_warning(log_message, self.verbose)
                        print(log_message)
            return _dict
        except TypeError as e:
            log_message = f"Didn't use Groups or Nodes in Yaml"
            self.logger.log_error(e)
            print(log_message)

        return _dict

    def set_variables(self, _object: str, _subobject: str, _default: any):
        """
        Set a given variable

        :param _object: object in the .yaml
        :param _subobject: sub-object in the .yaml
        :param _default: default value for the variable
        """
        _var = None
        if self.yaml.get(_object).get(_subobject) is not None:
            _var = self.yaml.get(_object).get(_subobject)
        else:
            _var = _default
        return _var

    @staticmethod
    def validate_ip(ip_string: str) -> bool:
        """
        Check if an ip is a valid IPv4/6 address

        :param ip_string: IP to check
        :return: True if IP is valid, otherwise false
        """
        try:
            ipaddress.ip_address(ip_string)
            return True

        except ValueError as error:
            logger = niv_logger.NivLogger()
            logger.log_error(error)
            return False

    def create_tooltip(self, element, node="", group="", connection=None):
        """
        Create a tooltip for a given element

        :param element: type of element you want to create a tooltip for (e.g. node, group, connection)
        :param node: the node you want to create the tooltip for
        :param group: the group you want to create the tooltip for
        :param connection: the connection you want to create the tooltip for
        :return: tooltip text
        """
        tooltip = ""

        if element == "node":
            tooltip = f"Name: {self.nodes_name[node]}\n" \
                      f"MAC-Address: {self.nodes_mac[node]}\n" \
                      f"Modelnr: {self.nodes_modelnr[node]}\n" \
                      f"Manufacturer: {self.nodes_manufactuer[node]}\n" \
                      f"Storage: {self.nodes_storage[node]}\n" \
                      f"Tooltip: {self.nodes_tooltip[node]}\n" \
 \
                # Remove double and triple newlines and "names: " for the case when not all values are given
            tooltip = tooltip.replace("\n\n\n", "\n") \
                .replace("\n\n", "\n") \
                .replace("Name: \n", "") \
                .replace("MAC-Address: \n", "") \
                .replace("Modelnr: \n", "") \
                .replace("Manufacturer: \n", "") \
                .replace("Storage: \n", "") \
                .replace("Tooltip: \n", "")

        elif element == "group":
            # If no tooltip is given within the group, set the current name of the group as the tooltip
            tooltip = self.group_tooltip[group]
            if self.group_tooltip[group] == "":
                tooltip = self.group_name[group]

        elif element == "connection":
            first_endpoint = self.connections_endpoints[connection][0]
            second_endpoint = self.connections_endpoints[connection][1]

            try:
                first_port = self.connections_ports[connection][0]
                second_port = self.connections_ports[connection][1]
                tooltip_without_port = f"{self.nodes_name[second_endpoint]} " \
                                       f"<---> " \
                                       f"{self.nodes_name[first_endpoint]}"

                tooltip_with_port = f"{self.nodes_name[second_endpoint]} (Port: {second_port}) " \
                                    f"<---> " \
                                    f"{self.nodes_name[first_endpoint]} (Port: {first_port})"

                # If a tooltip is given within the connections, set it as the tooltip
                if self.connections_tooltip[connection] != "":
                    tooltip_with_port = f"{tooltip_with_port}\n{self.connections_tooltip[connection]}"
                    tooltip_without_port = f"{tooltip_without_port}\n{self.connections_tooltip[connection]}"
                # If no tooltip is given within the connection, set both endpoints as the tooltip
                # if self.connections_tooltip[connection] == "":
                # If no ports are given for a connection only print endpoints
                if self.connections_ports[connection][1] == "" or self.connections_ports[connection][0] == "":
                    tooltip = tooltip_without_port
                else:
                    # Detail level 0 creates both diagrams for detail level 1 and 2
                    if self.detail_level == 0:
                        if self.counter == 1:
                            tooltip = tooltip_without_port
                        else:
                            tooltip = tooltip_with_port

                    # Detail level 1 shows no ports in tooltip
                    elif self.detail_level == 1:
                        tooltip = tooltip_without_port

                    # Detail level 2 shows ports aswell
                    else:
                        tooltip = tooltip_with_port
            except IndexError:
                log_message = f"For endpoints {self.connections_endpoints[connection]} only 1 port " \
                              f"{self.connections_ports[connection]} is given. " \
                              f"Add another one or remove them completely."
                self.logger.verbose_warning(log_message, self.verbose)
                print(log_message)
                tooltip = f"{self.nodes_name[second_endpoint]} " \
                          f"<---> " \
                          f"{self.nodes_name[first_endpoint]}"

        return tooltip

    def create_switch(self, ports, name, nodes, busy, out, url):

        """
        function create switches as busy or free

        :param url: a list of all subdiagrams
        :param out: how many ports are connected to ports outside the group
        :param ports: how many ports to create
        :param name: the name of the switch
        :param nodes: empty list to fill with the created switches
        :param busy: how many busy nodes to create
        """
        path, file_name = os.path.split(self.save_path)
        file_name = file_name.split('.')[0]
        if busy + out > ports:
            ports = busy + out

        with Cluster(name):
            if ports % 2:
                raw = (ports - 1) / 2
                raw = int(raw)
            else:
                raw = ports / 2
                raw = int(raw)
            # create busy ports
            for k in range(0, busy):
                if self.output_format == "svg":
                    nodes.append(OsaEthernetBusy(f"eth{k + 1}"))
                else:
                    nodes.append(OsaEthernetBusyPng(f"eth{k + 1}"))

            # create Free ports
            for k in range(busy, out + busy):
                if not url:
                    name = self.n_url.pop()
                    file = self.save_path.split('/')[-1]
                    if self.output_format == "svg":
                        nodes.append(OsaEthernetCable(f"\n\neth{k + 1} \nto\n{self.nodes_name[name]}\nin\n{file}",
                                                      URL=f"../{file_name}.{self.output_format}"))
                    else:
                        nodes.append(OsaEthernetCablePng(f"\n\neth{k + 1} \nto\n{self.nodes_name[name]}\nin\n{file}",
                                                         URL=f"../{file_name}.{self.output_format}"))

                else:
                    switch = url.pop()
                    group = url.pop()
                    if self.output_format == "svg":
                        nodes.append(OsaEthernetCable(
                            f"\n\neth {k + 1}\nto\n{self.nodes_name[switch]}\nin\n{self.group_name[group]}",
                            URL=f"{file_name}_{group}.{self.output_format}"))
                    else:
                        nodes.append(OsaEthernetCablePng(
                            f"\n\neth {k + 1}\nto\n{self.nodes_name[switch]}\nin\n{self.group_name[group]}",
                            URL=f"{file_name}_{group}.{self.output_format}"))

            # make the connections between ports transparent
            for k in range(out + busy, ports):
                if self.output_format == "svg":
                    nodes.append(OsaEthernetFree(f"eth{k + 1}"))
                else:
                    nodes.append(OsaEthernetFreePng(f"eth{k + 1}"))

            for k in range(0, raw):
                if k + raw <= ports:
                    _ = nodes[k] - Edge(color="transparent") - nodes[k + raw]

    def get_connections(self, member_name: str) -> list:
        """
        Function to get the Partner connections from a given node

        :param member_name: name of the node you want the partner from
        :return partners: a list of all connections that are connected with given node
        """
        partners = []

        # iterate through connections
        for connection in self.connections_endpoints:
            # try to get 2 elements from connections, len(connection) should always be 2, otherwise give log message
            try:
                # get connection values
                node1 = connection[0]
                node2 = connection[1]

                # append partners with the other node if the member_name node is in the connection
                if node1 == member_name:
                    partners.append(node2)
                if node2 == member_name:
                    partners.append(node1)

            except IndexError:
                self.logger.log("A connection in your yaml doesnt contain only 2 objects")

        return partners

    def are_connected(self, node1: str, node2: str) -> int:
        """
        Function to look if 2 given nodes are connected

        :param node1: one node name to look for
        :param node2: second node name to look for
        :return: index in connections_endpoints where they are connected
        """
        if node1 == node2:
            return -1
        # iterate through connections
        for connection in self.connections_endpoints:
            # look if nodes are in connection
            node1_given = node1 in connection
            node2_given = node2 in connection

            if node1_given and node2_given:
                # print(f"node1: {node1}, node2: {node2}, index: {self.connections_endpoints.index(connection)}")
                return self.connections_endpoints.index(connection)
        return -1

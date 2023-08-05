import numpy as np
import pandas as pd
import cv2
from sgdot.tools.grid_visualizer import GridVisualizer
from sgdot.tools.io import make_folder
import copy
from configparser import ConfigParser
import os


class Grid:
    """
    Defines a basic grid containing all the information about the topology
    of the network. The grid contains a network representation composed of
    a set of nodes and a set of links.

    Attributes
    ----------
    id : str
        Identifier

    nodes : :class:`pandas.core.frame.DataFrame`
        Dataframe containing all information related to the nodes composing
        the grid. Each node possesses:
            - a label
            - x and y pixel coordinates
            - a node_type (either 'household', 'meterhub' or 'powerhub') which
              can be fixed using the type_fixed parameter
            - a segment denoting which cluster the node belongs to
            - an allocation capacity, denoting how many households can be
              connected to the node.

    links : :class:`pandas.core.frame.DataFrame`
        Table containing all information related to the links
        between the nodes. The links are by definition undirected,
        'from' and 'to' denote the labels of the two nodes that are connected
        by the given link. Each link has a type: 'distribution' for links
        between households and hubs (meterhubs or powerhubs) and 'interhub'
        for links between two hubs.

    image: :class `numpy.ndarray`
        Satellite picture of the grid village in 'numpy.ndarray' type

    image_path: str
        Path to the jpeg or png image file of the grid (satellite picture
        of the village).

    meter_per_pixel_ratio: float
        Ratio describing distance in meters corresponding to one pixel of the
        image.

    price_meterhub: float
        Price associated with each meterhub.

    price_household: float
        Price associtated with each household

    price_interhub_cable_per_meter: float
        Price per unit lenght [1/m] associated with interhub cables.

    price_distribution_cable_per_meter: float
        Price per unit lenght [1/m] associated with distribution cables.

    default_hub_capacity: int
        Default value for the maximal number of households that can be
        connected to one hub.

    max_current: float
        Value of the maximal current expected to flow into the cables [A].

    voltage: float
        Value of the nominal voltage delivered to each node in [V].

    interhub_cable_section: float
        Section of the interhub cables in [mm²].

    interhub_cable_resistivity: float
        Electrical resistivity of the interhub cables in [Ohm*mm²/m].

    distribution_cable_section: float
        Section of the distribution cables in [mm²].

    distribution_cable_resistivity: float
        Electrical resistivity of the distribution cables in [Ohm*mm²/m].
    """
    # -------------------------- CONSTRUCTOR --------------------------#

    def __init__(self,
                 grid_id="unnamed_grid",
                 nodes=pd.DataFrame(
                     {
                         'label': pd.Series([], dtype=str),
                         'pixel_x_axis': pd.Series([], dtype=np.dtype(int)),
                         'pixel_y_axis': pd.Series([], dtype=np.dtype(int)),
                         'node_type': pd.Series([], dtype=str),
                         'type_fixed': pd.Series([], dtype=bool),
                         'segment': pd.Series([], dtype=np.dtype(str)),
                         'allocation_capacity': pd.Series([],
                                                          dtype=np.dtype(int))
                     }
                 ).set_index('label'),
                 links=pd.DataFrame({'label': pd.Series([], dtype=str),
                                     'from': pd.Series([], dtype=str),
                                     'to': pd.Series([], dtype=str),
                                     'type': pd.Series([], dtype=str),
                                     'distance': pd.Series([], dtype=int)
                                     }).set_index('label'),
                 image_path=None,
                 meter_per_pixel_ratio=1,
                 price_meterhub=600,
                 price_household=50,
                 price_interhub_cable_per_meter=5,
                 price_distribution_cable_per_meter=2,
                 default_hub_capacity=0,
                 max_current=10,  # [A]
                 voltage=230,  # [V]
                 interhub_cable_section=4,  # [mm²]
                 interhub_cable_resistivity=0.0171,  # [Ohm*mm²/m]
                 distribution_cable_section=2.5,  # [mm²]
                 distribution_cable_resistivity=0.0171  # [Ohm*mm²/m]
                 ):
        self.__id = grid_id
        self.__nodes = nodes
        self.__links = links
        self.__meter_per_pixel_ratio = meter_per_pixel_ratio
        self.__price_meterhub = price_meterhub
        self.__price_household = price_household
        self.__price_interhub_cable_per_meter = price_interhub_cable_per_meter
        self.__price_distribution_cable_per_meter = (
            price_distribution_cable_per_meter
        )
        self.__voltage = voltage
        self.__interhub_cable_section = interhub_cable_section
        self.__interhub_cable_resistivity = interhub_cable_resistivity
        self.__distribution_cable_section = distribution_cable_section
        self.__distribution_cable_resistivity = distribution_cable_resistivity
        self.__default_hub_capacity = default_hub_capacity
        self.__max_current = max_current

        # If no path given, the grid background image is black
        self.__initial_image = cv2.imread(image_path)
        if image_path is None:
            visu = GridVisualizer()
            self.__initial_image = np.ones((1024, 1024, 3), np.uint8) * 255
            self.__image = visu.add_upper_margin(np.zeros((1024, 1024, 3),
                                                          np.uint8),
                                                 int(0.15 * 1024))
        else:
            self.__image = cv2.imread(image_path)

    # -------------------------- GET METHODS ------------------------- #

    def get_nodes(self):
        """
        Returns a copy of the _nodes Dataframe (_nodes) attribute of the grid.

        Returns
        ------
        class:`pandas.core.frame.DataFrame`
            DataFrame containing all node informations from the grid.
        """
        return self.__nodes.copy()

    def get_hubs(self):
        """
        Returns the filtered _nodes DataFrame with only nodes of
        'meterhub' and 'powerhub' house type.

        Returns
        ------
        class:`pandas.core.frame.DataFrame`
            Filtered DataFrame containing all 'powerhub' and 'meterhub' nodes
            from the grid

        """
        return self.__nodes[(self.__nodes['node_type'] == 'meterhub')
                            | (self.__nodes['node_type'] == 'powerhub')].copy()

    def get_households(self):
        """
        Returns the filtered _nodes DataFrame with only 'household' nodes.

        Returns
        ------
        class:`pandas.core.frame.DataFrame`
            Filtered DataFrame containing all 'household' nodes
            from the grid
        """
        return self.__nodes[self.__nodes['node_type'] == 'household'].copy()

    def get_non_fixed_nodes(self):
        """
        Returns filtered _nodes DataFrame with only nodes with
        type_fixed value being 'False'.

        Returns
        ------
        class:`pandas.core.frame.DataFrame`
            Filtered DataFrame containing all nodes with 'type_fixed' == True

        """
        return self.__nodes[
            self.__nodes['type_fixed'] == False].copy()  # noqa: E712

    def get_links(self):
        """
        Returns _link Dataframe of the grid.

        Returns
        ------
        class:`pandas.core.frame.DataFrame`
            Dataframe containing all the links composing the grid
        """
        return self.__links.copy()

    def get_image(self):
        """
        Returns the image (_image) attribute of the grid.

        Returns
        ------
        class:numpy.ndarray
            Image of the grid (cv2 image format)
        """
        return self.__image

    def get_meter_per_pixel_ratio(self):
        """
        Returns the __meter_per_piexel attribute of the grid.

        Returns
        ------
        class: float
        """
        return self.__meter_per_pixel_ratio

    def get_segment_hub_capacity(self, segment):
        """
        Returns the total capacity of all the hubs in the segment.

        Parameters
        ----------
        segment:
            Label of the segment
        """

        return self.get_hubs()[
            self.get_hubs()['segment']
            == segment]['allocation_capacity'].sum()

    def get_total_hub_capacity(self):
        """
        Returns the total capacity of all the hubs in the grid.

        """
        return self.get_hubs()['allocation_capacity'].sum()

    def get_initial_image(self):
        """
        Returns initial image (_initial_image) attribute of the grid.

        Returns
        ------
        class:numpy.ndarray
            Initial image of the grid (cv2 image format)
        """
        return self.__initial_image

    def get_id(self):
        """
        Returns __id attribute of the grid.

        Returns
        ------
        str
            __id parameter of the grid
        """
        return self.__id

    def get_default_hub_capacity(self):
        """
        Returns __default_hub_capacity attribute of the grid.

        Returns
        ------
        int
            __default_hub_capacity parameter of the grid
        """
        return self.__default_hub_capacity

    def get_distribution_cable_price(self):
        """
        Returns __distribution_cable_price attribute of the grid.

        Returns
        ------
        int
            __distribution_cable_price parameter of the grid
        """
        return self.__price_distribution_cable_per_meter

    def get_interhub_cable_price(self):
        """
        Returns __interhub_cable_price attribute of the grid.

        Returns
        ------
        int
            __interhub_cable_price parameter of the grid
        """
        return self.__price_interhub_cable_per_meter

    def get_price_meterhub(self):
        """
        Returns __price_meterhub attribute of the grid.

        Returns
        ------
        int
            __price_meterhub parameter of the grid
        """
        return self.__price_meterhub

    def get_price_household(self):
        """
        Returns __price_household attribute of the grid.

        Returns
        ------
        int
            __price_household parameter of the grid
        """
        return self.__price_household

    # ------------------ FEATURE METHODS ------------------ #

    def does_link_exist(self, label_node1, label_node2):
        """
        This method returns True if there is a link bewteen the two node
        indices given as input, otherwise returns False.

        Parameters
        ----------
        label_node1: str
            Label of the first node
        label_node2: str
            Label of the second node

        Returns
        -------
        If there exists a link between the two nodes given as input, 'True' is
        returned, otherwise False is returned
        """

        if self.get_links()[
                (self.get_links()['from'] == label_node1) &
                (self.get_links()['to'] == label_node2)].shape[0] > 0:
            return True
        elif self.get_links()[
                (self.get_links()['from'] == label_node2) &
                (self.get_links()['to'] == label_node1)].shape[0] > 0:
            return True
        else:
            return False

    def is_hub_capacity_constraint_too_strong(self):
        """
        This methods returns wheter or not hub capacity constraint prevents
        from connecting all households to hubs.

        Returns
        ------
            If number of households is greater than the sum of the respective
            segment's hubs capacity, True is returned. Otherwise, False is
            returned.
        Note
        ----
            If all hubs in the grid have a an allocation_capacity equals
            to 0, the allocation capacity is by default unrestricted and an
            arbitrary number of nodes can be assigned to each hub.
        """
        # If the sum of the allocation_capacity of the hubs is 0, capacity is
        # by default unrestricted
        if self.get_hubs()['allocation_capacity'].sum() == 0:
            return False

        is_capacity_constraint_too_strong = False
        for segment in self.get_nodes()['segment'].unique():
            if self.get_households()[
                self.get_households()['segment'] == segment].shape[0] >\
                    self.get_hubs()[
                    self.get_hubs()['segment']
                    == segment]['allocation_capacity'].sum():
                is_capacity_constraint_too_strong = True

        return is_capacity_constraint_too_strong

    def is_segment_spanning_tree(self, segment):
        """
        This methods checks wheter or not the given nodes from the segment
        is spanning (i.e. buiding a connected graph).

        Parameters:
            str
                Segment index

        Returns:
            bool
                If the segment is spanning, True is returned.
                Otherwise False is returned
        """

        node_0 = self.get_nodes()[
            self.get_nodes()['segment'] == segment].index[0]

        nodes_in_spanning_tree = [node_0]
        loop_in_graph = False

        # find all neighbors of node_0
        neighbors_of_node_0 = []
        for index_neighbour in self.get_links()[(self.get_links()['from']
                                                 == node_0)]['to']:
            neighbors_of_node_0.append(index_neighbour)
        for index_neighbour in self.get_links()[(self.get_links()['to']
                                                 == node_0)]['from']:
            neighbors_of_node_0.append(index_neighbour)

        for neighbor in neighbors_of_node_0:
            if not loop_in_graph:
                self.loop_detection_iteration(segment,
                                              nodes_in_spanning_tree,
                                              loop_in_graph,
                                              node_0,
                                              neighbor)
        segment_size = self.get_nodes()[
            self.get_nodes()['segment'] == segment].shape[0]
        return len(nodes_in_spanning_tree) == segment_size

    def loop_detection_iteration(self,
                                 segment,
                                 nodes_in_spanning_tree,
                                 loop_in_graph,
                                 previous_node,
                                 current_node):
        """
        This method is a helping method used in the function
        is_segment_spanning_tree to explore graph and discover wheter or not
        the segment is a connected tree.

        Parameters
        ----------
        segment: str
            Segment index
        nodes_in_spanning_tree: list
            List of the indices of the nodes that have been explored already
            and are in the spanning tree.
        loop_in_graph: bool
            Indicates whether or not a loop has been found in the graph
            This parameter is then passed to the calling function until it
            reaches the is_segment_spanning_tree function.
        previous_node: str
            Index of the node that came before in the iteration. This
            parameter is used to ensure that the exploration of the graph goes
            forward (except if there is a loop).
        current_node: str
            Index of the next node in the iteration.
        """

        if current_node in nodes_in_spanning_tree:
            loop_in_graph = True

        else:
            nodes_in_spanning_tree.append(current_node)
            neighbors_of_current_nodes = []
            for index_neighbour in self.get_links()[(self.get_links()['from']
                                                     == current_node)]['to']:
                if index_neighbour != previous_node:
                    neighbors_of_current_nodes.append(index_neighbour)
            for index_neighbour in self.get_links()[(self.get_links()['to']
                                                     == current_node)]['from']:
                if index_neighbour != previous_node:
                    neighbors_of_current_nodes.append(index_neighbour)

            for next_node in neighbors_of_current_nodes:
                self.loop_detection_iteration(segment,
                                              nodes_in_spanning_tree,
                                              loop_in_graph,
                                              current_node,
                                              next_node)

    def get_interhub_cable_length(self):
        """
        This method returns the sum of the interhub cables length.

        Returns
        ------
        type: float
        Total distance of interhub cable in the grid.
        """
        return self.get_links()[
            self.get_links()['type']
            == 'interhub']['distance'].sum()

    def get_distribution_cable_length(self):
        """
        This method returns the sum of the distribution cables length.

        Returns
        ------
        type: float
        Total distance of distribution cable in the grid.
        """
        return self.get_links()[
            self.get_links()['type']
            == 'distribution']['distance'].sum()

    # ------------------- SET METHODS --------------------- #

    def set_nodes(self, nodes):
        """
        Set grid's _nodes attibute to nodes parameter.

        Parameters
        ----------
        nodes : :class:`pandas.core.frame.DataFrame`
            node DataFrame (pandas) to set as Grid._nodes attribute.
        """
        self.__nodes = nodes.copy()

    def set_links(self, links):
        """
        Set grid's _links attibute to links parameter.

        Parameters
        ----------
        links : :class:`pandas.core.frame.DataFrame`
            node DataFrame (pandas) to set as Grid._links attribute.
        """
        self.__links = links.copy()

    def set_image(self, image):
        """
        Set grid's image attibute to image parameter.

        Parameters
        ----------
        image: : :class `numpy.ndarray`
            image to set as Grid._image attribute
        """
        self.__image = image

    def set_initial_image(self, image):
        """
        Set grid's initial_image attibute to image parameter.

        Parameters
        ----------
        image: : :class `numpy.ndarray`
            image to set as Grid._initial_image attribute.
        """
        self.__initial_image = image

    # -------------- MANIPULATE NODES --------------- #

    def add_node(self, label, pixel_x_axis, pixel_y_axis,
                 node_type, type_fixed=False, segment='0',
                 allocation_capacity=0):
        """Adds a node to the grid's _nodes Dataframe.

        Parameters
        ----------
        label: str
            node label.
        pixel_x_axis: int
            x coordinate of node in pixels.
        pixel_y_axis: int
            y coordinate of node in pixels.
        node_type: str
            node_type of the node (either 'household', 'meterhub'
            or 'powerhub').
        type_fixed: bool
            Paramter specifing if node_type can be changed or not.
            If type_fixed is True, then the node_type is fix and cannot
            be changed.
        segment: str
            Label of the segment the node should be part of.
        allocation_capacity: int
            Only relevant for hubs, define maximum number of households
            that can be connected to each hub.
        """

        if allocation_capacity == 0 and 'hub' in node_type:
            allocation_capacity = self.__default_hub_capacity
        self.__nodes.loc[str(label)] = [int(pixel_x_axis),
                                        int(pixel_y_axis),
                                        node_type,
                                        type_fixed,
                                        segment,
                                        allocation_capacity]

    def remove_node(self, node_label):
        """
        This method removes the node corresponding to the node_label
        parameter from the grid's _nodes.

        Parameter
        ---------
        node_label: str
            node to be removed from the grid

        Notes
        -----
        If the node_label parameter doesn't correspond to any node of the
        grid, the method raises a Warning.
        """
        node_label = str(node_label)
        if node_label in self.get_nodes().index:
            self.__nodes = self.__nodes.drop(node_label, axis=0)
        else:
            raise Warning(f"The node label given as input ('{node_label}') "
                          + "doesn't correspond to any node in the grid")

    def clear_nodes_and_links(self):
        """ Removes all the nodes and links from the grid.
        """
        self.clear_links()
        self.__nodes = self.__nodes.drop(
            [label for label in self.__nodes.index],
            axis=0)

    def remove_outlier_nodes(self):
        """ Removes all nodes that are outside of the image (whose
        coordinates does not lie within the image boundaries).
        """
        self.__nodes = self.__nodes.drop(
            [label for label
             in self.__nodes[
                 self.__nodes['pixel_y_axis'] > self.__image.shape[0]].index],
            axis=0)
        self.__nodes = self.__nodes.drop(
            [label for label
             in self.__nodes[
                 self.__nodes['pixel_y_axis'] < (
                     self.__image.shape[0]
                     - self.__initial_image.shape[0])
             ].index],
            axis=0)
        self.__nodes = self.__nodes.drop(
            [label for label
             in self.__nodes[
                 self.__nodes['pixel_x_axis'] > self.__image.shape[1]].index],
            axis=0)
        self.__nodes = self.__nodes.drop(
            [label for label
             in self.__nodes[
                 self.__nodes['pixel_x_axis'] < 0].index],
            axis=0)

    def flip_node(self, node_label):
        """
        Switch the node_type of a node i.e. if node_type is 'meterhub',
        change it to 'household', if node_type is 'household', change
        it to 'meterhub'.

        Parameters
        ----------
        node_label: str
            label of the node.
        """

        if not self.__nodes['type_fixed'][node_label]:
            if self.__nodes['node_type'][node_label] == 'meterhub':
                self.set_node_type(node_label=node_label,
                                   node_type='household')
                self.set_hub_capacity(str(node_label), 0)
            elif self.__nodes['node_type'][node_label] == 'household':
                self.set_node_type(node_label=node_label,
                                   node_type='meterhub')
                self.set_hub_capacity(str(node_label),
                                      self.__default_hub_capacity)

    def flip_random_node(self):
        """
        This function picks a node uniformly at random and flips its
        'node_type' (i.e. if node_type is meterhub, change it to
        household, if node_type is household, change it to meterhub).
        """
        # First be sure that the node dataframe is not empty
        if self.get_non_fixed_nodes().shape[0] > 0:  # noqa: E712
            randomly_selected_node_label =\
                self.get_non_fixed_nodes()[
                    self.get_non_fixed_nodes()['node_type']
                    != 'powerhub'].sample(n=1).index[0]
            self.flip_node(randomly_selected_node_label)

    def swap_random(self,
                    swap_option='random'):
        """
        This method picks a meterhub uniformly at random and, swap it
        house state with a household selected according to the
        swap_option parameter (ie. the 'node_type' of the picked
        meterhub is changed to 'household' and the 'node_type' of the
        selected household is set to 'meterhub).

        Parameters
        ----------
        swap_option: :class:`bool`
            If parameter is 'nearest_neighbour', the household that is picked
            is necessarily the one that is the clostest to the picked
            meterhub. If parameter is 'random', the household to be swaped
            with the meterhub is selected uniformly at random.
        """

        # Make sure that the grid contains at least one meterhub and household
        if self.get_non_fixed_nodes()[self.get_non_fixed_nodes()['node_type']
                                      == 'meterhub'].shape[0] > 0\
                and self.get_non_fixed_nodes()[
                    self.get_non_fixed_nodes()['node_type']
                    == 'household'].shape[0] > 0:

            # Pick a meterhub uniformly at random among the ones not fixed
            randomly_selected_meterhub_label =\
                self.get_non_fixed_nodes()[
                    self.get_non_fixed_nodes()['node_type']
                    == 'meterhub'].sample(n=1).index[0]

            # If swap_option is 'nearest_neighbour', find nearest household
            # and flip its node_type
            if swap_option == 'nearest_neighbour':
                # Define first household of the nodes Dataframe before looping
                # to finde the nearest to the picked meterhub and save
                # distance
                selected_household_label\
                    = self.get_non_fixed_nodes()[
                        self.get_non_fixed_nodes()['node_type']
                        == 'household'].index[0]

                dist_to_selected_household = self.distance_between_nodes(
                    randomly_selected_meterhub_label,
                    selected_household_label)
                # Loop over all households to find the one that is the nearest
                # to the meterhub
                for household_label in \
                        self.get_non_fixed_nodes()[
                            self.get_non_fixed_nodes()['node_type']
                            == 'household'].index:
                    if self.distance_between_nodes(
                            randomly_selected_meterhub_label, household_label)\
                            < dist_to_selected_household:
                        selected_household_label = household_label
                        dist_to_selected_household =\
                            self.distance_between_nodes(
                                randomly_selected_meterhub_label,
                                selected_household_label)
            else:
                selected_household_label =\
                    self.get_non_fixed_nodes()[
                        self.get_non_fixed_nodes()['node_type']
                        == 'household'].sample(n=1).index[0]

            self.flip_node(randomly_selected_meterhub_label)
            self.flip_node(selected_household_label)

    def set_all_node_type_to_households(self):
        """"
        This method sets the node_type to 'household' for all nodes with
        type_fixed == False.
        """

        for label in self.get_non_fixed_nodes()[(self.__nodes['node_type']
                                                 != 'powerhub')].index:
            self.set_node_type(label, 'household')

    def set_all_node_type_to_meterhubs(self):
        """"
        This method sets the node_type to 'meterhub' for all nodes with
        type_fixed == False.
        """

        for label in self.__nodes[self.__nodes['node_type']
                                  != 'powerhub'].index:
            if not self.get_nodes()['type_fixed'][label]:
                self.set_node_type(label, 'meterhub')

    def set_node_type(self, node_label, node_type):
        """
        This method set the node type of a given node to the value
        given as parameter.

        Parameter
        ---------
            node_label: str
                Label of the node contained in grid.
            node_type: str
                value the 'node_type' of the given node is set to.
        """
        if not self.get_nodes()['type_fixed'][node_label]:
            self.__nodes.at[node_label, 'node_type'] = node_type
            if node_type == 'meterhub' or node_type == 'powerhub':
                self.__nodes.at[node_label, 'allocation_capacity'] =\
                    self.__default_hub_capacity
            elif node_type == 'household':
                self.__nodes.at[node_label, 'allocation_capacity'] = 0

    def set_node_type_randomly(self, probability_for_meterhub):
        """"
        This method sets the node_type of each node to meterhub with a
        probability probability_for_meterhub, the rest are being set to
        households.

        Parameters
        ----------
            probability_for_meterhub: float
                Probabilty to assign each node to node_type value 'meterhub'.
        """

        for label in self.__nodes.index:
            if np.random.rand() < probability_for_meterhub:
                self.set_node_type(node_label=label, node_type='meterhub')
            else:
                self.set_node_type(node_label=label, node_type='household')

    def set_segment(self, node_label, segment):
        """ This method assigns the segment attribute of the node corresponding
        to node_label to the value of segment.

        Parameters
        ----------
        node_label: str
            Label of the node
        segment: str
            Label of the segment the node should be assigned to.
        Notes
        -----
            If the node label doesn't correspond to any node in the grid,
            method does nothing.
        """
        if node_label in self.__nodes.index:
            segment = str(segment)
            self.__nodes.at[str(node_label), 'segment'] = segment

    def set_type_fixed(self, node_label, type_to_set):
        """
        Set the type_fixed of the selected node to the value of type_to_set.

        Parameters
        ----------
        node_label: str
            label of the node.
        type_to_set: :class:`bool`
            value of the type_fixed of the node should be set to.
        Note
        ----
        The node_type of the nodes with type_fixed is True shouldn't not be
        changed.
        """
        if self.__nodes.shape[0] > 0:
            self.__nodes.at[str(node_label), 'type_fixed'] = type_to_set

    def set_hub_capacity(self, hub_label, allocation_capacity):
        """
        This method sets the allocation capacity of a hub to the value given
        by the allocation_capacity parameter. If the node is not a hub, the
        method doesn't do anything.

        Parameters
        ----------
        hub_label: str
            Label of the hub.
        allocation_capacity: int
            Value the allocation_capacity of the hub is assigned to.
        """
        if hub_label in self.get_hubs().index\
                and type(allocation_capacity) == int:
            self.__nodes.at[str(hub_label),
                            'allocation_capacity'] = allocation_capacity

    def shift_node(self,
                   node,
                   delta_x: float,
                   delta_y: float,
                   allow_shifting_node_outside_boundary: bool = True):
        """
        This method increment the 'pixel_x_axis' value by delta_x and the
        'pixel_y_axis' value by delta_y for the node given as parameter.

        Parameters
        ----------
            node: str
                Index of the node that should be shift.
            delta_x: int
                Integer representing the number in pixel that should be added
                to 'pixel_x_axis' of the given node.
            delta_y: int
                Integer representing the number in pixel that should be added
                to 'pixel_y_axis' of the given node.
            allow_shifting_node_outside_boundary: bool
                When True, nodes can be shifted to a coordinate that
                is not within the image boundary.
        """

        # Detect if shifting the node would make it leave image boundary
        new_coord_within_boundary = (
            self.get_nodes()['pixel_x_axis'][node] +
            delta_x <= self.get_image().shape[0]
            and self.get_nodes()['pixel_x_axis'][node] + delta_x >= 0
            and self.get_nodes()[
                'pixel_y_axis'][node] + delta_y <= self.get_image().shape[1]
            and self.get_nodes()[
                'pixel_y_axis'][node] + delta_y >= 0)
        if new_coord_within_boundary or allow_shifting_node_outside_boundary:
            # shift node
            self.__nodes.at[node, 'pixel_x_axis'] =\
                self.__nodes['pixel_x_axis'][node] + delta_x
            self.__nodes.at[node, 'pixel_y_axis'] =\
                self.__nodes['pixel_y_axis'][node] + delta_y
        else:
            raise Warning(f'Impossible to shift node {node} from ({delta_x},'
                          + f' {delta_y}) since it would leave image '
                          + 'boundaries')

    # ----------------------- MANIPULATE LINKS ------------------------ #

    def add_link(self, label_node_from, label_node_to):
        """
        This method adds a link between two nodes from self.__nodes
        to the grid and determines the distance of the link.

        Parameters
        ----------
        label_node_from: str
            Label of the first node
        label_node_to: str
            Label of the second node

        Notes
        -----
        The method first makes sure that the two labels correspond to
        nodes in the grid. If it's not the case, no link is added.
        """
        # Make sure that the link is not already part of the _links DataFrame

        if self.__links[(self.__links['from'] == label_node_from)
                        & (self.__links['to'] == label_node_to)].shape[0] >= 1\
                or self.__links[(self.__links['from'] == label_node_from)
                                & (self.__links['to']
                                   == label_node_to)].shape[0] >= 1:
            raise Warning(
                'link (' + label_node_from + ', '
                + label_node_to + ') has not been added to the _links since '
                + 'it is already in the DataFrame')

        # Make sure that the nodes are in the node dataframe and define
        # link type
        if label_node_from in self.__nodes.index\
                and label_node_to in self.__nodes.index:
            if (self.__nodes['node_type'][label_node_from] == 'meterhub'
                or self.__nodes['node_type'][label_node_from] == 'powerhub')\
               and (self.__nodes['node_type'][label_node_to] == 'meterhub'
                    or (self.__nodes['node_type'][label_node_to]
                        == 'powerhub')):
                link_type = 'interhub'
            else:
                link_type = 'distribution'
            distance = self.distance_between_nodes(label_node_from,
                                                   label_node_to)
            # since links are undirected, the convention is that
            # label_node_from is first label when sorted in alphabetical order
            (label_node_from, label_node_to) = sorted([label_node_from,
                                                       label_node_to])

            label = f'({label_node_from}, {label_node_to})'
            self.__links.loc[str(label)] = [label_node_from,
                                            label_node_to,
                                            link_type,
                                            distance]
        # If at least one of the nodes are not part of the list, return error
        else:
            raise Exception('label' + str(label_node_from) + ' or '
                            + str(label_node_to)
                            + ' is not part of the node dataframe')

    def remove_link(self, node1, node2):
        """
        This method removes, if it exists, the link between the two nodes
        given as parameter.

        Parameters
        ----------
        node1: str
            Label of one of the nodes connected by the link.
        node2: str
            Label of the other node connected by the link.
        """
        (label_node_from, label_node_to) = sorted([node1,
                                                   node2])
        link_label = f'({label_node_from}, {label_node_to})'
        if link_label in self.get_links().index:
            self.__links = self.__links.drop(link_label, axis=0)
        else:
            raise Warning(f"The link between {node1} and {node2} cannot be  "
                          + "removed since the two nodes are not connected")

    def clear_links(self):
        """Removes all the links from the grid.
        """
        self.__links = self.get_links().drop(
            [label for label in self.get_links().index],
            axis=0)

    def clear_interhub_links(self):
        """Removes all the interhub links from the grid$.
        """
        self.__links = self.__links[self.__links['type'] != 'interhub']

    def clear_distribution_links(self):
        """Removes all the interhub links from the grid.
        """
        self.__links = self.__links[self.__links['type'] != 'distribution']

    # ----------------------- PRICE FUNCTION ------------------------ #

    def price(self):
        """
        This method computes the price of the grid.

        Returns
        -------
        Returns the price of the grid computed taking into account the number
        of nodes, their types and the length of the cables as well as
        the cable types.
        """

        # If there are no meterhubs in the grid, the price function
        # returns a very large value
        if self.get_hubs().shape[0] == 0:
            return 999999999999999.1

        # Compute total interhub cable length in meter
        interhub_cable_lentgh_meter =\
            self.get_interhub_cable_length()
        # Compute total distribution cable length in meter
        distribution_cable_length_meter =\
            self.get_distribution_cable_length()
        # Compute the number of meterhubs
        number_of_meterhubs =\
            self.__nodes[self.__nodes['node_type'] == 'meterhub'].shape[0]

        # Compute the number of households
        number_of_households =\
            self.__nodes[self.__nodes['node_type'] == 'household'].shape[0]

        grid_price = ((number_of_meterhubs * self.__price_meterhub)
                      + (number_of_households * self.__price_household)
                      + (distribution_cable_length_meter
                         * self.__price_distribution_cable_per_meter)
                      + (interhub_cable_lentgh_meter
                         * self.__price_interhub_cable_per_meter))

        return np.around(grid_price, decimals=2)

    # ----------------------- MANIPULATE IMAGE ------------------------ #

    def clear_image(self):
        """
        Reset the grid image to initial image (i.e, clears all nodes and links
        and empty margin).
        """
        visu = GridVisualizer()
        self.__image = copy.deepcopy(self.__initial_image)
        self.__image = visu.add_upper_margin(
            self.get_image(),
            int(0.15 * self.get_image().shape[0]))

    # ----------------- COMPUTE DISTANCE BETWEEN NODES -----------------#

    def distance_between_nodes(self, label_node_1, label_node_2):
        """
        Returns the distance between two nodes of the grid.

        Parameters
        ----------
        label_node_1: str
            Label of the first node.
        label_node_2: str
            Label of the second node.

        Returns
        -------
            Distance between the two nodes in meter.
        """
        # ------------------------ Import config parameters --------------#

        if label_node_1 in self.__nodes.index\
                and label_node_2 in self.__nodes.index:
            return self.get_meter_per_pixel_ratio()\
                * np.sqrt((self.__nodes["pixel_x_axis"][label_node_1]
                           - (self.__nodes["pixel_x_axis"][label_node_2])
                           ) ** 2
                          + (self.__nodes["pixel_y_axis"][label_node_1]
                             - self.__nodes["pixel_y_axis"][label_node_2]
                             ) ** 2
                          )
        else:
            return np.infty

    def get_cable_distance_from_households_to_powerhub(self):
        """
        This method computes the cable distance separating each node
        from its powerhub. It recursively uses the method
        measure_distance_for_next_node() to explore the tree starting from
        the powerhub and following each tree branch until all nodes are
        reached.

        Returns
        ------
        class:`pandas.core.frame.DataFrame`
            This method returns a pandas DataFrame containing all the
            nodes in the grid and the total length of interhub and
            distribution cable separating it from its respective powerhub.
         """

        # Create dataframe with interhub and distribution cable length
        distance_df = pd.DataFrame({'label': [],
                                    'interhub cable [m]': [],
                                    'distribution cable [m]': [],
                                    'powerhub label': []})
        distance_df = distance_df.set_index('label')
        # For every powerhub, compute cable length to nodes from the segment
        for index_powerhub in self.get_nodes()[
                self.get_nodes()['node_type'] == 'powerhub'].index:

            distance_df.loc[index_powerhub] = [0, 0, index_powerhub]

            # this list gathers the index of all nodes that are directly
            # connected with a link to the powerhub
            node_next_neighbours = []
            # add all nodes connected to the meterhub to the list
            for next_node in self.get_links()[
                    (self.get_links()['from'] == index_powerhub)]['to']:
                if next_node not in node_next_neighbours\
                        and next_node not in distance_df.index:
                    node_next_neighbours.append(next_node)
            for next_node in self.get_links()[
                    (self.get_links()['to'] == index_powerhub)]['from']:
                if next_node not in node_next_neighbours\
                        and next_node not in distance_df.index:
                    node_next_neighbours.append(next_node)
            # Call measure_distance_for_next_node for all branches
            for node in node_next_neighbours:
                self.measure_distance_for_next_node(index_powerhub,
                                                    node,
                                                    distance_df,
                                                    index_powerhub)
        return distance_df

    def measure_distance_for_next_node(self,
                                       node_n_minus_1,
                                       node_n,
                                       distance_df,
                                       index_powerhub):
        """
        This method is used to measure the cable distance between each nodes
        and the powerhub. It is designed to be recursively called to explore
        all the branches of the tree taking the powerhub as the starting point
        and exploring every branch and sub-branches until the distance to every
        node has been computed. It takes advantage that the network is a tree,
        it is thus possible to explore the branches without considering each
        node more than once.
        Parameters
        ----------
        node_n_minus_1: str
            index corresponding to the node at the base of the branch leading
            to the "node_n" (which is the node whose distance to powerhub
            has to be computed).
        node_n: str
            index corresponding to the node whose distance to powerhub has to
            be computed.
        distance_df: :class:`pandas.core.frame.DataFrame`
            dictionnary containing the distance to the powerhub of all nodes
            that where already computed using the function.
         """

        # find out what the link index of the link between nodes node_n_minus_1
        # and node_n is. Since nodes are undirected, we need to look for the
        # link from node_n_minus_1 to node_n and from node_n and node_n_minus_1
        if self.get_links()[
                (self.get_links()['from'] == node_n_minus_1)
                & (self.get_links()['to'] == str(node_n))].shape[0] == 1:
            index_link_between_nodes = self.get_links()[
                (self.get_links()['from'] == node_n_minus_1)
                & (self.get_links()['to'] == str(node_n))].index[0]

        elif self.get_links()[
                (self.get_links()['from'] == node_n)
                & (self.get_links()['to'] == node_n_minus_1)].shape[0] == 1:
            index_link_between_nodes = self.get_links()[
                (self.get_links()['from'] == node_n)
                & (self.get_links()['to'] == node_n_minus_1)].index[0]

        # check what type the link is to know distiguish of the cable types
        # in the datafram
        if self.get_links()['type'][index_link_between_nodes] == 'interhub':
            distance_df.loc[node_n] = [
                distance_df['interhub cable [m]'][node_n_minus_1]
                + self.distance_between_nodes(node_n_minus_1, node_n),
                0,
                index_powerhub]
        elif self.get_links()['type'][
                index_link_between_nodes] == 'distribution':
            distance_df.loc[node_n] = [
                distance_df['interhub cable [m]'][node_n_minus_1],
                self.distance_between_nodes(node_n_minus_1, node_n),
                index_powerhub]

        # Call function for all the nodes that were not measured yet
        node_next_neighbours = []
        for node_next_neighbour in self.get_links()[(self.get_links()['from']
                                                     == node_n)]['to']:
            if node_next_neighbour not in node_next_neighbours\
                    and node_next_neighbour not in distance_df.index:
                node_next_neighbours.append(node_next_neighbour)
        for node_next_neighbour in self.get_links()[
                (self.get_links()['to'] == node_n)]['from']:
            if node_next_neighbour not in node_next_neighbours\
                    and node_next_neighbour not in distance_df.index:
                node_next_neighbours.append(node_next_neighbour)
        for next_neighbour in node_next_neighbours:
            self.measure_distance_for_next_node(node_n,
                                                next_neighbour,
                                                distance_df,
                                                index_powerhub)

    # -------------------- GRID PERFORMANCE ---------------------- #

    def get_voltage_drop_at_nodes(self):
        """
        This method computes the voltage drop at each node using the
        parameters defined in config_grid.cfg under [power flow].

        Returns
        ------
        class:`pandas.core.frame.DataFrame`
            pandas DataFrame containing the cable distance for the different
            types of cables as well as the cable resistance between the node
            and the corresponding powerhub. The DataFrame also contains an
            estimation of the voltage drop and the voltage drop fraction.

        Notes
        -----
            The cable resistance R_i is computed as follow
            R_i =  rho_i * 2* d_i / (i_cable_section)
            where i represent the cable type, rho the cable electric
            resistivity (self.__interhub_cable_resistivity),
            d the cable distance and i_cable_section the section of the cable.
            The voltage drop is computed using Ohm's law
            U = R * I where U is the tension (here corresponding to the
            voltage drop), R the resistance and I the current.
        """
        voltage_drop_df =\
            self.get_cable_distance_from_households_to_powerhub()

        voltage_drop_df['interhub cable resistance [Ω]'] = (
            self.__interhub_cable_resistivity
            * 2 * voltage_drop_df['interhub cable [m]']
            / self.__interhub_cable_section
        )

        voltage_drop_df['distribution cable resistance [Ω]'] = (
            self.__distribution_cable_resistivity * 2 *
            voltage_drop_df['distribution cable [m]']
            / self.__distribution_cable_section
        )

        voltage_drop_df['voltage drop [V]'] = (
            (voltage_drop_df['interhub cable resistance [Ω]']
             * self.__max_current)
            + (voltage_drop_df['distribution cable resistance [Ω]'] *
               self.__max_current)
        )

        voltage_drop_df['voltage drop fraction [%]'] = (
            100 * voltage_drop_df['voltage drop [V]'] / self.__voltage
        )

        return voltage_drop_df

    def export(self,
               backup_name=None,
               folder=None,
               allow_saving_in_existing_backup_folder=False,
               empty_background=False,
               save_image=True):
        """
        Method calling the export_grid function to save a backup of the grid.

        """
        export_grid(self,
                    backup_name=backup_name,
                    folder=folder,
                    allow_saving_in_existing_backup_folder=(
                        allow_saving_in_existing_backup_folder),
                    empty_background=empty_background,
                    save_image=save_image
                    )

# - FUNCTIONS RELATED TO EXPORTING AND IMPORTING GRIDS FROM EXTERNAL FILE --#


def export_grid(grid,
                backup_name=None,
                folder=None,
                allow_saving_in_existing_backup_folder=False,
                empty_background=False,
                save_image=True):
    """
    Export grid in folder as separated files:
        - nodes.csv
            contains the __nodes attribute data.
        - links.csv
            contains the __links attribute data.
        - initial_image(.jpeg or .png)
            contains initial image.
        - grid_attributes.cfg
            contains the value of the Grid's attributes.

    Parameters
    ----------
    grid: :class:`~sgdot.grids.Grid`
            Grid object.
    folder: str
        Path of the folder the grid should be saved in
    backup_name: str
        Name of the grid backup.

    allow_saving_in_existing_backup_folder: bool
        When True and a folder with the same name as the parameter
        backup_name, no new folder is created and the grid is exported in
        the folder of the backup_name.
        When False and a folder with the same name as the parameter
        backup_name exists, a new folder is created with a extension _i
        (where i is an integer).

     empty_background: bool
        When True, an image of the grid network is saved on a transparent
        background.

    save_image: bool
        Determines whether or not the images (grid image and initial image)
        are saved in the backup folder.

    Notes
    -----
        If no folder is given, the default path to folder is
        f'data/backup/{grid._id}/'.

        If no folder name is given, the grid will be saved in a folder called
        f'backup_{grid._id}_{counter}', where counter is a index added
        to distiguish backups of the same grid.
    ----------
    """

    if folder is None:
        folder = 'data/backup/' + grid.get_id()
        make_folder('data')
        make_folder('data/backup')
        make_folder(folder)
    else:
        if not os.path.exists(folder):
            parent_folders = folder.split('/')
            for i in range(1, len(parent_folders) + 1):
                path = ''
                for x in parent_folders[0:i]:
                    path += x + '/'
                make_folder(path[0:-1])

    if backup_name is None:
        backup_name = f'backup_{grid.get_id()}'

    if not allow_saving_in_existing_backup_folder:
        if os.path.exists(f'{folder}/{backup_name}'):
            counter = 1
            while os.path.exists(
                    f'{folder}/{backup_name}_{counter}'):
                counter += 1
            backup_name = f'{backup_name}_{counter}'
    full_path = f'{folder}/{backup_name}'

    make_folder(full_path)

    # Export nodes dataframe into csv file
    grid.get_nodes().to_csv(full_path + '/nodes.csv')

    # Export links dataframe into csv file
    grid.get_links().to_csv(full_path + '/links.csv')

    # Create config files containing Grid's attributes
    config = ConfigParser()

    config["attributes"] = {
        key: (value, type(value)) for key, value in
        grid.__dict__.items() if key not in [
            "_Grid__nodes",
            "_Grid__links",
            "_Grid__initial_image",
            "_Grid__image"]}

    with open(f"{full_path}/grid_attributes.cfg", 'w') as f:
        config.write(f)

    # Save initial and grid images
    if save_image:
        import sgdot.tools.grid_visualizer as grid_visualizer
        visu = grid_visualizer.GridVisualizer()
        visu.draw_grid(grid)
        cv2.imwrite(full_path + '/initial_image.png', grid.get_initial_image())
        cv2.imwrite(full_path + '/Grid_' + str(grid.get_id())
                    + '.png', grid.get_image())
        if empty_background is True:
            cv2.imwrite(full_path + '/Grid_empty_background.png',
                        visu.transparent_grid_image(grid))

    print(f'Grid saved in \n{full_path}\n\n')


def import_grid(folder):
    """
    Import a grid that was previously exported using the export_grid
    function.

    Parameters
    ----------
    folder: str
        Path to the folder where the backup files (nodes.csv, links.csv
        initial_image(.jpeg or .png) and attributes.cfg)
        of the given grid have been saved in.
    Returns
    -------
        Copy of the exported Grid located in the folder defined by the path.
    """

    # Import grid id from grid_attributes.cfg file
    config_attributes = ConfigParser()

    config_attributes.read(folder + '/grid_attributes.cfg')
    attributes = {}

    # Load all attributes names, values and type and fill attributes dict
    for section in config_attributes.sections():
        for (key, val) in config_attributes.items(section):
            value, str_type = config_attributes.get(section, key).replace(
                "'", "").replace("(", "").replace(">)", "").replace(
                    " ", "").replace("<class", "").split(",")
            if str_type == "int":
                value = int(value)
            if str_type == "float":
                value = float(value)
            # Format class name from _grid__ to _Grid__
            key_in_list = [letter for letter in key]
            key_in_list[1] = key_in_list[1].upper()
            key_formated = "".join(key_in_list)
            attributes[key_formated] = value

    # Import data from csv files to nodes and links DataFrames
    nodes = pd.read_csv(folder + '/nodes.csv',
                        converters={
                            'label': str,
                            'pixel_x_axis': int,
                            'pixel_y_axis': int,
                            'node_type': str,
                            'type_fixed':
                                lambda x: True if x == 'True' else False,
                            'segment': str,
                            'allocation_capacity': int})
    nodes = nodes.set_index('label')

    links = pd.read_csv(folder + '/links.csv',
                        converters={'from': str,
                                    'to': str,
                                    'type': str,
                                    'distance': float,
                                    },
                        index_col=[0])
    # Create new Grid containing nodes and links
    grid = Grid(nodes=nodes,
                links=links,
                image_path=folder + "initial_image.png")
    # Set grid attributes using dict created from grid_config.cfg
    for key, value in attributes.items():
        setattr(grid, key, value)

    return grid

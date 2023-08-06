""" Module defining the Base Classes for Sensors.

This module implements the base class Sensor, that all sensors inherit from.
It also implements a base class RayCollisionSensor.
RayCollisionSensor use pymunk collisions with lines to create different
families of sensors and allow very fast computation.

Apart if specified, all sensors are attached to an anchor.
They compute sensor-values from the point of view of this anchor.
"""

from abc import abstractmethod, ABC
import math
from operator import attrgetter

import pymunk
import numpy as np

from simple_playgrounds.utils.definitions import SensorTypes
from simple_playgrounds.entity import Entity
from simple_playgrounds.utils.parser import parse_configuration


class Sensor(ABC):
    """ Base class Sensor, used as an Interface for all sensors.

    Attributes:
        anchor: body Part to which the sensor is attached.
            Sensor is attached to the center of the Anchor.
        sensor_values: current values of the sensor.
        name: Name of the sensor.

    Class Attributes:
        sensor_type: string that represents the type of sensor (e.g. 'rgb' or 'lidar').

    Note:
        The anchor is always invisible to the sensor.

    """

    _index_sensor = 0
    sensor_type = SensorTypes.SENSOR
    sensor_modality = SensorTypes.SENSOR

    def __init__(self, anchor, fov, resolution, max_range,
                 invisible_elements, normalize, noise_params, name=None, **_kwargs):
        """
        Sensors are attached to an anchor. They detect every visible Agent Part or Scene Element.
        If the entity is in invisible elements, it is not detected.

        Args:
            anchor: Body Part or Scene Element on which the sensor will be attached.
            fov: Field of view of the sensor (in degrees).
            resolution: Resolution of the sensor (in pixels, or number of rays).
            max_range: maximum range of the sensor (in the same units as the playground distances).
            invisible_elements: list of elements invisible to the sensor.
            normalize: boolean. If True, sensor values are scaled between 0 and 1.
            noise_params: Dictionary of noise parameters.
                Noise is applied to the raw sensor, before normalization.
            name: name of the sensor. If not provided, a name will be chosen by default.

        Noise Parameters:
            type: 'gaussian', 'salt_pepper'
            mean: mean of gaussian noise (default 0)
            scale: scale / std of gaussian noise (default 1)
            salt_pepper_probability: probability for a pixel to be turned off or max

        Notes:
             As only 32 invisible groups can be set in pymunk, this limits the number of sensors
             with invisible_elements to around 30.
        """

        # Sensor name
        # Internal counter to assign number and name to each sensor
        if name is not None:
            self.name = name
        else:
            self.name = self.sensor_type.name.lower() + '_' + str(Sensor._index_sensor)
            Sensor._index_sensor += 1

        self.anchor = anchor
        self.sensor_values = None

        if invisible_elements is None:
            self.invisible_elements = None
        else:
            if isinstance(invisible_elements, Entity):
                invisible_elements = [invisible_elements]

            self.invisible_elements = invisible_elements

        self.invisible_filter = pymunk.ShapeFilter()

        self._normalize = normalize

        self._noise = False
        if noise_params is not None:
            self._noise = True
            self._noise_type = noise_params.get('type', 'gaussian')

            if self._noise_type == 'gaussian':
                self._noise_mean = noise_params.get('mean', 0)
                self._noise_scale = noise_params.get('scale', 1)

            elif self._noise_type == 'salt_pepper':
                self._noise_probability = noise_params.get('probability', 0.1)

            else:
                raise ValueError('Noise type not implemented')

        self._range = max_range
        self._fov = fov * math.pi / 180
        self._resolution = resolution

        if not self._resolution > 0:
            raise ValueError('resolution must be more than 1')
        if not self._fov > 0:
            raise ValueError('field of view must be more than 1')
        if not self._range > 0:
            raise ValueError('range must be more than 1')

        # Sensor max value is used for noise and normalization calculation
        self._sensor_max_value = 0

    def apply_shape_filter(self, sensor_collision_index):

        for elem in self.invisible_elements:
            elem.update_mask_shape_filter(sensor_collision_index)

        self.invisible_filter = pymunk.ShapeFilter(categories=2 ** sensor_collision_index)

    def update(self, **kwargs):
        """
        Updates the attribute sensor_values.
        Applies normalization and noise if necessary.

        Args:
            **kwargs: either playground, or playground

        Returns:

        """
        self._compute_raw_sensor(**kwargs)

        if self._noise:
            self._apply_noise()

        if self._normalize:
            self._apply_normalization()

    @abstractmethod
    def _compute_raw_sensor(self, playground, sensor_surface):
        pass

    @abstractmethod
    def _apply_normalization(self):
        pass

    @abstractmethod
    def _apply_noise(self):
        pass

    @property
    def shape(self):
        """ Returns the shape of the numpy array, if applicable."""
        return None

    @abstractmethod
    def draw(self, width, height):
        """
        Function that creates an image for visualizing a sensor.

        Keyword Args:
            width: width of the returned image
            height: when applicable (in the case of 1D sensors), the height of the image.

        Returns:
            Numpy array containing the visualization of the sensor values.

        """
        return None


class RayCollisionSensor(Sensor, ABC):
    """
    Base class for Ray Collision sensors.
    Ray collisions are computed using pymunk segment queries.
    They detect intersection with obstacles.
    Robotic sensors and Semantic sensors inherit from this class.

    """
    sensor_modality = SensorTypes.ROBOTIC

    def __init__(self, remove_duplicates, **sensor_params):
        """
        Args:
            remove_duplicates: If True, removes detections of the same objects on multiple rays.
                Keeps the closest detection.
            **sensor_params: Additional sensor params.
        """

        default_config = parse_configuration('agent_sensors', self.sensor_type)
        sensor_params = {**default_config, **sensor_params}

        super().__init__(**sensor_params)

        self._remove_duplicates = remove_duplicates

        # Field of View of the Sensor
        if self._resolution == 1:
            self._ray_angles = [0]
        else:
            self._ray_angles = [n * self._fov / (self._resolution - 1) - self._fov / 2
                                for n in range(self._resolution)]

    @staticmethod
    def _remove_duplicate_collisions(collisions_by_angle):

        all_shapes = list(set(col.shape
                              for angle, col in collisions_by_angle.items()
                              if col))

        all_collisions = []
        for angle, col in collisions_by_angle.items():
            if col: all_collisions.append(col)

        all_min_collisions = []
        for shape in all_shapes:
            min_col = min([col for col in all_collisions if col.shape is shape],
                          key=attrgetter('alpha'))
            all_min_collisions.append(min_col)

        # Filter out noon-min collisions
        for angle, col in collisions_by_angle.items():
            if col and col not in all_min_collisions:
                collisions_by_angle[angle] = None

        return collisions_by_angle

    def _compute_collision(self, playground, sensor_angle):

        position = self.anchor.pm_body.position
        angle = self.anchor.pm_body.angle + sensor_angle

        position_end = position + pymunk.Vec2d(self._range, 0).rotated(angle)

        collision = playground.space.segment_query_first(position, position_end, 1, self.invisible_filter)

        return collision

    def _compute_points(self, playground):

        points = {}

        for sensor_angle in self._ray_angles:

            collision = self._compute_collision(playground, sensor_angle)
            points[sensor_angle] = collision

        if self._remove_duplicates:
            points = self._remove_duplicate_collisions(points)

        return points

    def _apply_noise(self):

        if self._noise_type == 'gaussian':

            additive_noise = np.random.normal(self._noise_mean, self._noise_scale, size=self.shape)

        elif self._noise_type == 'salt_pepper':

            prob = [self._noise_probability/2, 1-self._noise_probability, self._noise_probability/2]
            additive_noise = np.random.choice([-self._sensor_max_value, 0, self._sensor_max_value],
                                              p=prob,
                                              size=self.shape)

        else:
            raise ValueError

        self.sensor_values += additive_noise

        self.sensor_values[self.sensor_values < 0] = 0
        self.sensor_values[self.sensor_values > self._sensor_max_value] = self._sensor_max_value

""" Contains Engine class.

Engine class manages the interactions between agents and playground during an episode.
Engine can be inherited in order to create wrappers.
Engine allows to visualize the playground, as well as the agent sensors.

Typical Usage:
    engine = Engine(time_limit=10000, playground=my_playground, screen=True)

    while engine.game_on:
        actions = engine.get_actions()
        engine.step(actions)
        engine.update_observations()

    engine.terminate()
"""

import numpy as np

import pygame
import pygame.locals
import pygame.color

from pymunk import pygame_util
# import gym

from skimage.transform import rescale

from simple_playgrounds.utils.definitions import SensorTypes, SIMULATION_STEPS, ActionTypes

_BORDER_IMAGE = 5
_PYGAME_WAIT_DISPLAY = 30


class Engine:

    """
    An Engine manages the interactions between agents and a playground.

    Attributes:
        playground: Playground
        agents: list of all agents in the Playground.
        game_on: if True, the playground didn't reached termination.
    """

    # pylint: disable=too-many-function-args
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=line-too-long

    def __init__(self, playground, time_limit=None, screen=False, debug=False):
        """
        Args:
            playground (:obj: 'Playground'): Playground where the agents will be placed.
            time_limit (:obj: 'int'): Number of time steps that the playground will be run.
                                      Can also be defined in playground.
            screen: If True, a pygame screen is created for display.
                Default: False
            debug: If True, scene is displayed using debug colors instead of textures.

        Notes:
            A pygame screen is created by default if one agent is controlled by Keyboard.
            You can terminate an engine using the Q key.
            Screen is intended for debugging or playing by a human (using Keyboard).

            If time limit is defined in playground and engine, engine prevails.
            If time limit is False, environment never terminates.

        """

        self.playground = playground
        self.agents = self.playground.agents

        if time_limit is not None:
            self._time_limit = time_limit

        elif self.playground.time_limit is not None:
            self._time_limit = self.playground.time_limit

        self._debug = debug

        # Display screen
        self._screen = None
        if screen:
            # Screen for Pygame
            self._screen = pygame.display.set_mode((self.playground.width, self.playground.length))
            self._screen.set_alpha(None)
            self._quit_key_ready = True

        # Pygame Surfaces to display the environment
        self._surface_background = pygame.Surface((self.playground.width, self.playground.length))
        self._surface_background.fill(pygame.Color(0, 0, 0, 0))

        self._surface_buffer = pygame.Surface((self.playground.width, self.playground.length))

        self.game_on = True
        self.elapsed_time = 0

    # STEP

    def multiple_steps(self, actions, n_steps=1):
        """
        Runs multiple steps of the game, with the same actions for the agents.
        The physical actions are performed for n_steps.
        The interactive action (eat and activate) are only performed at the last timestep.

        Args:
            actions: Dictionary containing the actions for each agent.
            n_steps: Number of consecutive steps where the same actions will be applied

        """
        hold_actions = {}
        last_action = {}

        terminate = False

        for agent_name, agent_actions in actions.items():
            hold_actions[agent_name] = {}
            last_action[agent_name] = {}

            for actuator, value in agent_actions.items():

                last_action[agent_name][actuator] = value
                hold_actions[agent_name][actuator] = value

                if actuator.action_type in [ActionTypes.ACTIVATE, ActionTypes.EAT]:
                    hold_actions[agent_name][actuator] = 0

        cumulated_rewards = {}
        for agent in actions:
            cumulated_rewards[agent] = 0

        step = 0

        while step < n_steps and not terminate:

            if step < n_steps-1:
                action = hold_actions
            else:
                action = last_action

            self._engine_step(action)

            for agent in self.agents:
                cumulated_rewards[agent] += agent.reward

            step += 1

            terminate = self._has_terminated()

        for agent in self.agents:
            agent.reward = cumulated_rewards[agent]

        if self._reached_time_limit() and self.playground.time_limit_reached_reward is not None:
            for agent in self.agents:
                agent.reward += self.playground.time_limit_reached_reward

    def step(self, actions):
        """
        Runs a single step of the game, with the same actions for the agents.

        Args:
            actions: Dictionary containing the actions for each agent. keys are agents,
                     values are dictionary of actions.

        """

        self._engine_step(actions)
        self._has_terminated()

        if self._reached_time_limit() and self.playground.time_limit_reached_reward is not None:
            for agent in self.agents:
                agent.reward += self.playground.time_limit_reached_reward

    def _engine_step(self, actions):

        for agent in actions:
            agent.apply_actions_to_body_parts(actions[agent])

        self.playground.update(SIMULATION_STEPS)

        self.elapsed_time += 1

    # TERMINATION CONDITIONS

    def _has_terminated(self):

        playground_terminated = self.playground.done
        reached_time_limit = self._reached_time_limit()
        keyboard_quit = self._check_keyboard()

        if keyboard_quit or playground_terminated or reached_time_limit:
            self.game_on = False
            return True

        return False

    def _reached_time_limit(self):

        if not self._time_limit:
            return False

        if self.elapsed_time >= self._time_limit-1:
            return True

        return False

    def _check_keyboard(self):
        """
        Tests whether the game came to an end, because of time limit or termination of playground.

        Returns:
            True if the game is terminated
            False if the game continues
        """
        terminate_game = False

        if self._screen is not None:

            pygame.event.get()

            # pylint: disable=no-member

            # Press Q to terminate
            if not pygame.key.get_pressed()[pygame.locals.K_q] and not self._quit_key_ready:
                self._quit_key_ready = True

            elif pygame.key.get_pressed()[pygame.locals.K_q] and self._quit_key_ready:
                self._quit_key_ready = False
                terminate_game = True

        return terminate_game

    # PYGAME SURFACE UPDATE

    def _update_surface_background(self):
        # Check that some background elements maybe need to be drawn
        for element in self.playground.scene_elements:
            if element.background and not element.drawn:
                element.draw(self._surface_background, )

    def _generate_surface_environment(self, with_interactions=False):
        """
        Draw all agents and entities on the surface environment.
        Additionally, draws the interaction areas.

        """
        self._update_surface_background()
        self._surface_buffer.blit(self._surface_background, (0, 0))

        for agent in self.agents:
            agent.draw(self._surface_buffer)

        for entity in self.playground.scene_elements:

            if entity.background and not entity.drawn:
                entity.draw(self._surface_buffer, draw_interaction=with_interactions)

            if not entity.background or entity.graspable or entity.interactive:
                entity.draw(self._surface_buffer, draw_interaction=with_interactions)



    def update_screen(self):
        """
        If the screen is set, updates the screen and displays the environment.
        """

        if self._screen is not None:

            if self._debug:
                self._screen.fill((0, 0, 0))
                options = pygame_util.DrawOptions(self._screen)
                self.playground.space.debug_draw(options)

            else:
                self._generate_surface_environment(with_interactions=True)
                self._screen.blit(self._surface_buffer, (0, 0), None)

            pygame.display.flip()

        else:
            raise ValueError('No screen to update')

    def generate_playground_image(self, max_size=None, plt_mode=False):
        """
        Updates the Environment Surface and convert it into an array.
        Color code follows OpenCV.

        For displaying with matplotlib, use plt_mode = True

        Returns: image of he playground

        """

        self._generate_surface_environment(with_interactions=True)

        np_image = pygame.surfarray.pixels3d(self._surface_buffer.copy()) / 255.
        np_image = np.rot90(np_image, -1, (1, 0))
        np_image = np_image[::-1, :, ::-1]

        if max_size is not None:

            scaling_factor = max_size/max(np_image.shape[0], np_image.shape[1])
            np_image = rescale(np_image, scaling_factor, multichannel=True)

        if plt_mode:
            np_image = np_image[:, :, ::-1]

        return np_image

    # AGENTS

    def get_actions(self):
        actions = {}
        for agent in self.agents:
            actions[agent] = agent.controller.generate_actions()
        return actions

    def update_observations(self):
        """
        Updates observations of each agent

        """

        for agent in self.agents:

            for sensor in agent.sensors:

                if sensor.sensor_modality is SensorTypes.VISUAL:

                    self._update_surface_background()
                    self._surface_buffer.blit(self._surface_background, (0, 0))
                    sensor.update(playground=self.playground, sensor_surface=self._surface_buffer)

                elif sensor.sensor_modality is SensorTypes.ROBOTIC \
                        or sensor.sensor_modality is SensorTypes.SEMANTIC:
                    sensor.update(playground=self.playground)

                else:
                    raise ValueError("Sensor Modality not recognized")

    def generate_agent_image(self, agent,
                             with_pg=True,
                             max_size_pg=200,
                             rotate_pg=False,
                             with_actions=True,
                             width_action=200,
                             height_action=20,
                             with_sensors=True,
                             width_sensors=150,
                             height_sensor=20,
                             plt_mode=False,
                             layout=('playground', ('sensors', 'actions'))):
        """
        Method to generate an image for displaying the playground, agent sensors and actions.

        Args:
            agent (Agent): Instance of agent.
            with_pg (bool): Display the playground.
            max_size_pg (int): Maximum size of the playground image ( either width or depth, depending on shape).
            rotate_pg (bool): Rotate the playground. Useful when the playground is a rectangle.
            with_actions (bool): Display actions.
            width_action (int): Width of the action bars.
            height_action (int): Height of the action bars.
            with_sensors (bool): Display sensors.
            width_sensors (int): Width of the sensors.
            height_sensor (int): Height of the sensors (when applicable).
            plt_mode (bool): Set to True to return a matplotlib compatible image.
            layout (tuple): See notes

        Note:
            Layout is a tuple representing the layout of the agent image:

            - ('playground', ('sensors', 'actions') ) will put playground on the left, then split sensors and actions
            horizontally on the right.
            - (('playground', 'sensors'), 'actions') ) will split playground and sensor on the left,
            then display sensors on the right.

        Returns:
            if plt_mode is False: returns a cv2 compatible image / array, scaled between 0 and 1.
            if plt_mode is True: returns a matplotlib compatible image / array, scaled between 0 and 1.


        """

        # pylint: disable=too-many-locals

        images = {}

        if with_pg:
            pg_image = self.generate_playground_image(max_size=max_size_pg)

            if rotate_pg:
                pg_image = np.rot90(pg_image)
            images['playground'] = pg_image

        if with_actions:
            action_image = agent.generate_actions_image(width_action=width_action, height_action=height_action)
            images['actions'] = action_image

        if with_sensors:
            sensor_image = agent.generate_sensor_image(width_sensor=width_sensors, height_sensor=height_sensor)
            images['sensors'] = sensor_image

        full_width = _BORDER_IMAGE
        full_height = 0

        for column in layout:

            if isinstance(column, str):
                full_width += images[column].shape[1] + _BORDER_IMAGE
                full_height = max(full_height, images[column].shape[0] + 2*_BORDER_IMAGE)

            elif isinstance(column, tuple):
                full_width += max([images[col].shape[1] for col in column]) + _BORDER_IMAGE
                full_height = max(full_height, _BORDER_IMAGE
                                  + sum(images[col].shape[0] + _BORDER_IMAGE for col in column))

        full_img = np.ones((full_height, full_width, 3))

        current_width = _BORDER_IMAGE

        for column in layout:

            if isinstance(column, str):
                full_img[_BORDER_IMAGE: _BORDER_IMAGE + images[column].shape[0],
                         current_width:current_width + images[column].shape[1], :] \
                         = images[column][:, :, :]

                current_width += images[column].shape[1] + _BORDER_IMAGE

            elif isinstance(column, tuple):

                current_height = _BORDER_IMAGE

                for col in column:

                    # center
                    delta_width = max([images[col].shape[1] for col in column]) - images[col].shape[1]
                    delta_width = int(delta_width/2)

                    full_img[current_height: current_height + images[col].shape[0],
                             current_width + delta_width:current_width + delta_width + images[col].shape[1], :] \
                        = images[col][:, :, :]

                    current_height += images[col].shape[0] + _BORDER_IMAGE

                current_width += max([images[col].shape[1] for col in column]) + _BORDER_IMAGE

        if plt_mode:
            full_img = full_img[:, :, ::-1]

        return full_img

    def reset(self):
        """
        Resets the game to its initial state.

        """
        self.playground.reset()
        self.elapsed_time = 0
        self.game_on = True

        # Redraw everything
        self._surface_background.fill(pygame.Color(0, 0, 0, 0))

        for elem in self.playground.scene_elements:
            if elem.background:
                elem.draw(self._surface_background)

    def run(self, steps=None, update_screen=False, print_rewards=False):
        """ Run the engine for the full duration of the game or a certain number of steps"""

        if self._screen is False and update_screen:
            raise ValueError("Can't update non-existing screen")

        continue_for_n_steps = True

        while self.game_on and continue_for_n_steps:

            actions = {}
            for agent in self.agents:
                actions[agent] = agent.controller.generate_actions()

            self.step(actions)
            self.update_observations()

            if update_screen and self.game_on:
                self.update_screen()
                pygame.time.wait(_PYGAME_WAIT_DISPLAY)

            if print_rewards:
                for agent in self.agents:
                    if agent.reward != 0:
                        print(agent.name, ' got reward ', agent.reward)

            if steps is not None:
                steps -= 1
                if steps == 0:
                    continue_for_n_steps = False

    @staticmethod
    def terminate():
        """
        Terminate the engine. Quits all pygame instances.

        """
        pygame.quit()  # pylint: disable=no-member


# class RLibSingleAgentWrapper(gym.Env):
#
#     def __init__(self, playground, time_limit, **kwargs):
#
#         if len(playground.agents) != 1:
#             raise ValueError('Only single agent')
#
#         self.agent = playground.agents[0]
#         self.multisteps = kwargs.get('multisteps', 1)
#         self.engine = Engine(playground, time_limit=time_limit)
#
#         self._set_action_space()
#         self._set_observation_space()
#
#     def _set_action_space(self):
#
#         pass
#
#     def _set_observation_space(self):
#
#         self.observation_space = gym.spaces.Dict({"position": gym.spaces.Discrete(2), "velocity": gym.spaces.Discrete(3)})
#
#
#     def reset(self):
#         self.engine.reset()
#
#     def step(self, action):


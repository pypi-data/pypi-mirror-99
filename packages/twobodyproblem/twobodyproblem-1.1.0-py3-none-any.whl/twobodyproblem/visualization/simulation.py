import os
import signal
import sys

import vpython as vp

from twobodyproblem.visualization import body


class Simulation:
    """class used for the visualization of the simulation"""

    def __init__(self, values: dict, options: dict):
        """args:
            values: dictionary of required values for the simulation
            option: dictionary of additional options for the simulation
        """
        self._values = values
        self._options = options

    @property
    def values(self):
        return self._values

    @property
    def options(self):
        return self._options

    def pause(self, button: vp.button):
        """pause and un-pause the simulation

        args:
            button: pause button itself
        """
        if button.text == "Pause":
            button.text = "Play"
        else:
            button.text = "Pause"

    def restart(self):
        """restart the program"""
        # does not work perfectly, especially on command line
        os.execl(sys.executable, sys.executable, *sys.argv)
        # os.execv(sys.executable, ["python"] + sys.argv)

    def adjust_radius(self, slider: vp.slider, sphere: body.Body):
        """adjust the visual size of the body according to the slider value

        args:
            slider: slider which was changed
            sphere: body associated with the slider
        """
        sphere.radius = self.values[sphere.name + "_radius"] * slider.value

    def reset_slider(self, slider: vp.slider):
        """reset the slider to the default value

        args:
            slider: slider to be reset
        """
        slider.value = 1
        slider.bind()

    def start(self):
        """open the vpython window and start the simulation"""
        # set up important boolean values from options
        testing = bool(self.options["do_testing"])
        central_centered = bool(self.options["do_central_centered"])
        show_pointers = bool(self.options["show_pointers"])

        # set up canvas, bodies and pointers
        scene = vp.canvas(
            title="Simulation zum Zweikörperproblem",
            height=self.options["canvas"]["height"],
            width=self.options["canvas"]["width"]
        )
        central = body.Body(
            sim=self, name="central", mass=self.values["central_mass"],
            velocity=vp.vector(
                self.values["central_v0"]["x"],
                self.values["central_v0"]["y"],
                self.values["central_v0"]["z"]
            ),
            radius=self.values["central_radius"], make_trail=True,
            color=vp.vector(
                self.options["color"]["objects"]["r"] / 255,
                self.options["color"]["objects"]["g"] / 255,
                self.options["color"]["objects"]["b"] / 255
            )
        )
        sat = body.Body(
            sim=self, name="sat", mass=self.values["sat_mass"],
            velocity=vp.vector(
                self.values["sat_v0"]["x"],
                self.values["sat_v0"]["y"],
                self.values["sat_v0"]["z"]
            ),
            pos=vp.vector(
                self.values["distance"] + self.values["central_radius"]
                + self.values["sat_radius"],
                0, 0),
            radius=self.values["sat_radius"], make_trail=True,
            color=vp.vector(
                self.options["color"]["objects"]["r"] / 255,
                self.options["color"]["objects"]["g"] / 255,
                self.options["color"]["objects"]["b"] / 255
            )
        )
        # TODO: three (or more?) bodies
        central_ptr = vp.arrow()
        sat_ptr = vp.arrow()
        if show_pointers:
            central_ptr = vp.arrow(
                axis=vp.vector(
                    0,
                    -((self.values["distance"] + central.radius +
                       sat.radius) / 2),
                    0
                ),
                color=vp.vector(
                    self.options["color"]["pointer"]["r"],
                    self.options["color"]["pointer"]["g"],
                    self.options["color"]["pointer"]["b"]
                )
            )
            central_ptr.pos = (central.pos - central_ptr.axis) + vp.vector(
                0, self.values["central_radius"], 0)
            sat_ptr = vp.arrow(
                axis=vp.vector(
                    0,
                    -((self.values["distance"] + central.radius +
                       sat.radius) / 2),
                    0
                ),
                color=vp.vector(
                    self.options["color"]["pointer"]["r"],
                    self.options["color"]["pointer"]["g"],
                    self.options["color"]["pointer"]["b"]
                )
            )
            sat_ptr.pos = sat.pos - sat_ptr.axis + vp.vector(
                0, self.values["sat_radius"], 0)

        # set up buttons
        pause_sim = vp.button(text="Pause", bind=self.pause)
        vp.button(text="Stop",
                  bind=lambda: os.kill(os.getpid(), signal.SIGINT))
        vp.button(text="Restart", bind=self.restart)
        scene.append_to_caption("\n")

        # set up sliders for changing the radius of the two bodies
        central_radius_slider: vp.slider = vp.slider(
            max=(self.values["distance"] + self.values["central_radius"])
            / self.values["central_radius"],
            min=1, value=1, top=12, bottom=12,
            bind=lambda: self.adjust_radius(
                slider=central_radius_slider, sphere=central)
        )
        vp.button(text="Reset", bind=lambda: self.reset_slider(
            central_radius_slider))
        scene.append_to_caption("\n")
        sat_radius_slider: vp.slider = vp.slider(
            max=(self.values["distance"] + self.values["sat_radius"])
            / self.values["sat_radius"],
            min=1, value=1, top=12, bottom=12,
            bind=lambda: self.adjust_radius(
                slider=sat_radius_slider, sphere=sat)
        )
        vp.button(text="Reset",
                  bind=lambda: self.reset_slider(sat_radius_slider))
        # TODO: sliders for "update_rate" and "t_factor"

        # set up time variables
        t = 0
        t_max = self.options["update_rate"] * self.options["max_seconds"]
        # TODO: optional endless simulation
        # main simulation loop
        if central_centered:
            scene.camera.follow(central)
        while t < t_max:
            # weird behaviour of those two
            vp.rate(self.options["update_rate"])
            # vp.sleep(1/self.options["update_rate"])
            if pause_sim.text == "Pause":
                central.calculate(sat, self.options["t_factor"])
                if show_pointers:
                    # move pointers
                    central_ptr.pos = central.pos - central_ptr.axis + \
                                      vp.vector(0, central.radius, 0)
                    sat_ptr.pos = sat.pos - sat_ptr.axis + vp.vector(
                        0, sat.radius, 0)
                t += 1
        if bool(self.options["do_restart"]):
            self.restart()

import vpython as vp


class Body(vp.sphere):
    """class used for displaying vpython spheres with additional attributes

    inherits from: vpython.sphere
    """

    # TODO: collision detection

    def __init__(self, sim, name: str, mass=1.0, velocity=vp.vector(0, 0, 0),
                 **kwargs):
        """constructor extends vpython.sphere constructor

        args:
            sim: simulation where the bodies are created in
            name: the name of the body
            mass: the mass of the body (default 1.0)
            velocity: the initial velocity of the body (as vpython.vector)
        """
        super(Body, self).__init__(**kwargs)
        self.parent = sim
        self._name = name
        self._velocity = velocity
        self._mass = mass
        self._force = vp.vector(0, 0, 0)
        self._acceleration = vp.vector(0, 0, 0)

    @property
    def name(self):
        return self._name

    @property
    def mass(self):
        return self._mass

    @property
    def force(self):
        return self._force

    @force.setter
    def force(self, value):
        if not isinstance(value, vp.vector):
            raise TypeError("force must be a vector")
        self._force = value

    @property
    def acceleration(self):
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        if not isinstance(value, vp.vector):
            raise TypeError("acceleration must be a vector")
        self._acceleration = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if not isinstance(value, vp.vector):
            raise TypeError("velocity must be a vector")
        self._velocity = value

    def calculate(self, other, delta_t=1):
        """calculate force, acceleration, velocity and position of both bodies

        args:
            other: the other body that should be calculated with
            delta_t: Δt value (number of seconds in one calculation)
        """
        # vector for distance
        r = other.pos - self.pos
        # scalar value of the gravitational force
        force_value = (6.67430e-11 * self.mass * other.mass) / (vp.mag(r) ** 2)
        # TODO: visualize force, acceleration and velocity with arrows
        # TODO: relativistic formulae
        # calculation for self
        self.force = force_value * vp.norm(r)
        self.acceleration = self.force / self.mass
        self.velocity = self.acceleration * delta_t + self.velocity
        self.pos = self.velocity * delta_t + self.pos
        # calculation for other
        other.force = force_value * vp.norm(-r)
        other.acceleration = other.force / other.mass
        other.velocity = other.acceleration * delta_t + other.velocity
        other.pos = other.velocity * delta_t + other.pos

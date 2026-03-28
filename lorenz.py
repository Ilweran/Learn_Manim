from manim import *
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

def lorenz_system(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho -z) -y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
    function,
    t_span=(0, time),
    y0=state0,
    t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

class LorenzAttractor(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range = (-50, 50, 5),
            y_range = (-50, 50, 5),
            z_range = (-50, 50, 5),
        )
        axes.center()

        self.add(axes)

        #state0 = [10, 10, 10]
        epsilon = 0.001
        evolution_time = 300
        states = [
            [10, 10, 10 + n * epsilon]
                for n in range(2)
        ]

        colors = [BLUE, RED]
        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            # Convert to Manim coordinates
            path_points = [axes.c2p(x, y, z) for x, y, z in points]

            # --- Draw thin attractor curve ---
            curve = VMobject()
            curve.set_points_smoothly(path_points)
            curve.set_stroke(color, width=0.5)
            curve.set_color(color, 2)
            curves.add(curve)

        # Camera angle
        self.set_camera_orientation(phi=85 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Draw curve first
        self.play(*(Create(curve, run_time=120, rate_func=linear) for curve in curves))

        """
        # Moving particle
        dot = Dot3D(point=path_points[0], radius=0.05, color=RED)

        # Animation parameter
        tracker = ValueTracker(0)

        # --- Trail ---
        trail = VMobject(color=BLUE)

        def update_trail(mob):
            i = int(tracker.get_value())
            i = min(i, len(path_points) - 1)
            mob.move_to(path_points[i])
        
        dot.add_updater(update_trail)

        # --- Dot updater ---
        def update_dot(mob):
            i = int(tracker.get_value())
            i = min(i, len(path_points) - 1)
            mob.move_to(path_points[i])

        dot.add_updater(update_dot)

        self.add(trail, dot)

        # Camera angle
        self.set_camera_orientation(phi=45 * DEGREES, theta=75 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Animate movement
        self.play(
            tracker.animate.set_value(len(path_points) - 1),
            run_time=10,
            rate_func=linear
        )

        dot.remove_updater(update_dot)
        trail.remove_updater(update_trail)
        """
        self.wait()

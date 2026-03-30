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

        epsilon = 0.001
        evolution_time = 150
        states = [
            [10, 10, 10 + n * epsilon]
                for n in range(2)
        ]

        colors = color_gradient([BLUE, YELLOW], len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            # Convert to Manim coordinates
            path_points = [axes.c2p(x, y, z) for x, y, z in points]

            # --- Draw thin attractor curve ---
            curve = VMobject()
            curve.set_points_smoothly(path_points)
            curve.set_stroke(color, width=0.2)
            curve.set_color(color, 2)
            curves.add(curve)
        
        def create_3d_glow(dot, color=color, layers=8, radius_multiplier=2.5):
            glow = Group()
            for i in range(1, layers + 1):
                # Calculate radius and opacity for each layer
                layer_radius = dot.radius * (1 + (i / layers) * radius_multiplier)
                opacity = 0.15 * (1 - i / layers)

                layer = Dot3D(
                    point=dot.get_center(),
                    radius=layer_radius,
                    color=color,
                    resolution=dot.resolution # Match resolution for consistency
                ).set_opacity(opacity)

                glow.add(layer)
            return glow

        def CreateGlowDot(color):
            
            dot = Dot3D(radius=0.02, color=color)
            glow = create_3d_glow(dot, color=color)
            glowing_dot = Group(glow, dot)
            return glowing_dot

        dots_list = [CreateGlowDot(color) for color in colors]
        dots = Group(*dots_list)


        for dot, curve in zip(dots, curves):
            dot.add_updater(lambda d, c=curve: d.move_to(c.get_end()))

        # Camera angle
        self.set_camera_orientation(phi=85 * DEGREES, theta=15 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Draw curve
        run_time = 200
        self.add(dots)
        self.play(*(Create(curve, run_time=run_time, rate_func=linear) for curve in curves))

        self.wait()

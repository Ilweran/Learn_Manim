from manim import *
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

def vanderpol(t, state, mu=3.2, omega0=5.8):
    x, y = state
    dxdt = y
    dydt = mu*(1 - x**2)*y - omega0**2*x
    return [dxdt, dydt]

def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
    function,
    t_span=(0, time),
    y0=state0,
    t_eval=np.arange(0, time, dt)
    )
    return solution.y.T
    
class VanDerPol(ThreeDScene):
    def construct(self):
        axes = Axes(
            x_range = (-10, 10, 2),
            y_range = (-20, 20, 2),
        )
        axes.center()

        self.add(axes)

        # Add Van der Pol equations
        equations = Tex(R"""
            \[
            x_1 = x, \quad x_2 = \frac{dx}{dt}
            \]

            \[
            \begin{cases}
            \dot{x}_1 = x_2 \\
            \dot{x}_2 = \mu (1 - x_1^2)\,x_2 - \omega_0^2 x_1
            \end{cases}
            \]

            """,
            tex_to_color_map={
                "x": GREEN,
                "y": YELLOW,
            },
            font_size=30
        )
        equations.to_corner(UL)
        self.play(Write(equations))


        #epsilon = 0.001
        evolution_time = 30
        states = [[2.3, 0.1]]

        colors = color_gradient([BLUE_A, BLUE_E], len(states))

        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(vanderpol, state, evolution_time)
            # Convert to Manim coordinates
            path_points = [axes.c2p(x, y) for x, y in points]

            # --- Draw thin attractor curve ---
            curve = VMobject()
            curve.set_points_smoothly(path_points)
            curve.set_stroke(color, width=0.7)
            curve.set_color(color, 2)
            curves.add(curve)

        def create_3d_glow(dot, color=color, layers=10, radius_multiplier=2.5):
            glow = Group()
            for i in range(1, layers + 1):
                # Calculate radius and opacity for each layer
                layer_radius = dot.radius * (1 + (i / layers) * radius_multiplier)
                opacity = 0.1 * (1 - i / layers)

                layer = Dot3D(
                    point=dot.get_center(),
                    radius=layer_radius,
                    color=color,
                    resolution=dot.resolution # Match resolution for consistency
                ).set_opacity(opacity)

                glow.add(layer)
            return glow

        def CreateGlowDot(color):

            dot = Dot3D(radius=0.05, color=color)
            glow = create_3d_glow(dot, color=color)
            glowing_dot = Group(glow, dot)
            return glowing_dot

        dots_list = [CreateGlowDot(color) for color in colors]
        dots = Group(*dots_list)


        for dot, curve in zip(dots, curves):
            dot.add_updater(lambda d, c=curve: d.move_to(c.get_end()))


        # Draw curve
        run_time = 60
        self.add(dots)
        self.play(*(Create(curve, run_time=run_time, rate_func=linear) for curve in curves))

        self.wait()

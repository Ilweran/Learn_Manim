from manim import *
import numpy as np
from scipy.integrate import odeint

class ChuaSimulation(ThreeDScene):
    def construct(self):
        # 1. Define Parameters
        alpha = 15.6
        beta = 28.58
        m0 = -1.143
        m1 = -0.714

        def chua_system(state, t):
            x, y, z = state
            # The nonlinear function f(x)
            fx = m1 * x + 0.5 * (m0 - m1) * (abs(x + 1) - abs(x - 1))
            dxdt = alpha * (y - x - fx)
            dydt = x - y + z
            dzdt = -beta * y
            return [dxdt, dydt, dzdt]

        # 2. Solve the ODE
        initial_state = [0.1, 0.1, 0.1]
        t = np.arange(0, 100, 0.01)
        states = odeint(chua_system, initial_state, t)
        
        # Scale to fit
        max_val = np.max(np.abs(states))
        scale_factor = 3.5 / max_val
        scaled_data = states * scale_factor

        points = [np.array([s[0], s[1], s[2]]) for s in scaled_data]

        # 3. Setup Scene
        curve = VMobject().set_points_smoothly(points)
        curve.set_stroke(color=YELLOW, width=1.5, opacity=0.8)

        def create_3d_glow(dot_center, color=YELLOW, layers=15):
            glow = Group()
            for i in range(1, layers + 1):
                # Larger radius and lower opacity for outer layers
                opacity = 0.12 * (1 - i / layers)
                layer = Dot3D(
                    point=dot_center,
                    radius=0.03 + (i * 0.02), 
                    color=color
                ).set_opacity(opacity)
                glow.add(layer)
            return glow

        # Create the leading head of the line
        glow_dot = create_3d_glow(curve.get_start())

        # Updater to make glow follow the growing end of the curve
        glow_dot.add_updater(lambda m: m.move_to(curve.get_end()))

        # Convert points to Manim vectors
        # points = [np.array([x, y, z]) for x, y, z in states]
        path = VMobject().set_points_as_corners(points)
        path.set_stroke(color=YELLOW, width=0.5, opacity=0.8)

        # Add Chua equations
        tex_args = {"substrings_to_isolate": ["x", "y", "z"]}

        eq1 = MathTex(r"\frac{dx}{dt} = \alpha ( y - x - f(x) )", **tex_args)
        eq2 = MathTex(r"\frac{dy}{dt} = x - y + z", **tex_args)
        eq3 = MathTex(r"\frac{dz}{dt} = -\beta y", **tex_args)
        eq4 = MathTex(r"f(x) = m_1 x + \frac{1}{2}(m_0 - m_1)(|x + 1| - |x - 1|)", **tex_args)
        
        equations = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        equations.scale(0.6).to_corner(UL, buff=0.5)

        # Apply colors
        for eq in equations:
            eq.set_color_by_tex("x", RED)
            eq.set_color_by_tex("y", GREEN)
            eq.set_color_by_tex("z", BLUE)

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add_fixed_in_frame_mobjects(equations)


        # 4. Animation
        self.play(Write(equations))
        self.add(glow_dot)
        self.begin_ambient_camera_rotation(rate=0.2, about="theta")
        self.play(Create(curve), run_time=40, rate_func=linear)
        self.wait(3)

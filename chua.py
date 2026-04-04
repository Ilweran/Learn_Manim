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
        points = [np.array([x, y, z]) for x, y, z in states]

        # 3. Setup Scene
        curve = VMobject().set_points_smoothly(points)
        curve.set_stroke(color=YELLOW, width=0.5, opacity=0.8)

        def create_3d_glow(dot_center, color=YELLOW, layers=15):
            glow = Group()
            for i in range(1, layers + 1):
                # Larger radius and lower opacity for outer layers
                opacity = 0.15 * (1 - i / layers)
                layer = Dot3D(
                    point=dot_center,
                    radius=0.05 + (i * 0.04), 
                    color=color
                ).set_opacity(opacity)
                glow.add(layer)
            return glow

        # Create the leading head of the line
        glow_dot = create_3d_glow(curve.get_start())

        # Updater to make glow follow the growing end of the curve
        glow_dot.add_updater(lambda m: m.move_to(curve.get_end()))

        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=10 * DEGREES)
        
        # Convert points to Manim vectors
        points = [np.array([x, y, z]) for x, y, z in states]
        path = VMobject().set_points_as_corners(points)
        path.set_stroke(color=YELLOW, width=0.5, opacity=0.8)

        # Add Chua equations
        equations = Tex(R"""
            \[
            \begin{aligned}
            \frac{dx}{dt} &= \alpha \left( y - x - f(x) \right) \\
            \frac{dy}{dt} &= x - y + z \\
            \frac{dz}{dt} &= -\beta y
            \end{aligned}
            f(x) = m_1 x + \frac{1}{2}(m_0 - m_1)\left(|x + 1| - |x - 1|\right)
            \]
            """,
            tex_to_color_map={
                "x": RED,
                "y": GREEN,
                "z": BLUE,
            },
            font_size=25
        )
        self.add_fixed_in_frame_mobjects(equations)
        equations.to_corner(UL)
        self.play(Write(equations))


        # 4. Animation
        self.add(ThreeDAxes(), glow_dot)
        self.begin_ambient_camera_rotation(rate=0.1) # Add some cinematic spin
        self.play(Create(curve), run_time=30, rate_func=linear)
        self.wait(2)

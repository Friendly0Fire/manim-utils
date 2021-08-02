from manim import *


class ShrinkToPoint(Transform):
    def __init__(
        self,
        mobject: "Mobject",
        point: np.ndarray,
        point_color: str = None,
        remover: bool = True,
        **kwargs
    ) -> None:
        self.point = point
        self.point_color = point_color
        super().__init__(mobject, remover=remover, **kwargs)

    def create_target(self) -> "Mobject":
        end = self.mobject.copy()
        end.scale(0)
        end.move_to(self.point)
        if self.point_color:
            end.set_color(self.point_color)
        return end

    def clean_up_from_scene(self, scene: "Scene" = None) -> None:
        super().clean_up_from_scene(scene)
        self.interpolate(0)


class ShrinkArrow(ShrinkToPoint):
    def __init__(self, arrow: "Arrow", remover: bool = True, **kwargs) -> None:
        point = arrow.get_end()
        super().__init__(arrow, point, remover=remover, **kwargs)

    def create_target(self) -> "Mobject":
        end_arrow = self.mobject.copy()
        end_arrow.scale(0, scale_tips=True, about_point=self.point)
        if self.point_color:
            end_arrow.set_color(self.point_color)
        return end_arrow

    def clean_up_from_scene(self, scene: "Scene" = None) -> None:
        super().clean_up_from_scene(scene)
        self.interpolate(0)


def turn_animation_into_updater2(animation, cycle=False, delay=0.0, **kwargs):
    """
    Add an updater to the animation's mobject which applies
    the interpolation and update functions of the animation
    If cycle is True, this repeats over and over.  Otherwise,
    the updater will be popped upon completion
    """
    mobject = animation.mobject
    animation.suspend_mobject_updating = False
    animation.begin()
    animation.total_time = 0
    animation.do_cycle = cycle
    animation.delay = delay

    def update(m, dt):
        run_time = animation.get_run_time()
        time_ratio = max(0, (animation.total_time - animation.delay) / run_time)
        if animation.do_cycle:
            alpha = time_ratio % 1
        else:
            alpha = np.clip(time_ratio, 0, 1)
            if alpha >= 1:
                animation.finish()
                m.remove_updater(update)
                return
        animation.interpolate(alpha)
        animation.update_mobjects(dt)
        animation.total_time += dt

    if cycle:

        def stop_cycle():
            animation.do_cycle = False
            animation.total_time = (
                max(0, animation.total_time - animation.delay)
                % animation.get_run_time()
                + animation.delay
            )

        animation.stop_cycle = stop_cycle

    mobject.add_updater(update)
    return mobject
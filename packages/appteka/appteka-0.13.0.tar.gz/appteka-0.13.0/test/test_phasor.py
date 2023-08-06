import unittest
from PyQt5 import QtCore
from appteka.pyqt import testing
from appteka.pyqtgraph import phasor


class TestPhasorDiagram(unittest.TestCase):
    def test_add_phasor(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1)
        app(d, ["White phasor in first quadrant"])

    def test_update_phasor(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1)
        d.update_phasor('ph-1', 80, 2)
        app(d, ["Phasor in second quadrant"])

    def test_phasor_color(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1, (255, 0, 0))
        app(d, ["Red phasor in first quadrant"])

    def test_three_phasors(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram(end='arrow')
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))

        app(d, [
            "3 phasors: red, green and blue",
            "About 120 degrees between phasors",
        ])

    def test_three_phasors_rotated(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))
        d.update_phasor('ph-1', 80, 1)
        d.update_phasor('ph-2', 80, 1 + 2 * 3.1415 / 3)
        d.update_phasor('ph-3', 80, 1 - 2 * 3.1415 / 3)

        app(d, [
            "3 phasors: red, green and blue",
            "About 120 degrees between phasors",
            "Red phasor has angle about 1 radian",
        ])

    def test_width_of_phasors(self):
        app = testing.TestApp(self)

        # Given phasor diagram
        d = phasor.PhasorDiagram()

        # When add two phasors
        # And widths of phasors are set to be significantly differ
        d.add_phasor('ph-1', color=(255, 255, 255), width=1)
        d.add_phasor('ph-2', color=(255, 255, 255), width=4)
        d.update_phasor('ph-1', 100, 1)
        d.update_phasor('ph-2', 100, 2)
        d.set_range(100)

        # Then widths of phasors are differ
        app(d, ["Widths of phasors are differ"])


class TestPhasorDiagram_Range(unittest.TestCase):
    def test_range_is_two(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(2)
        app(d, ["Range is 2"])

    def test_change_range(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.set_range(2)
        d.set_range(4)
        app(d, ["Range is 4"])

    def test_range_to_phasor(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.add_phasor('ph-1', color=(255, 255, 0))
        d.update_phasor('ph-1', 1, 1)
        d.update_phasor('ph-1', 100, 1)
        d.set_range(100)
        app(d, ["Grid corresponds to phasor"])


class TestPhasorDiagram_Animation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    def test_three_phasors_animation(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram(end='arrow')
        d.add_phasor('ph-1', color=(255, 0, 0))
        d.add_phasor('ph-2', color=(0, 255, 0))
        d.add_phasor('ph-3', color=(0, 0, 255))
        d.show_legend()

        def rotate():
            a = 2 * 3.1415 / 3
            sh = self.counter / 200
            ash = self.counter / 10
            d.update_phasor('ph-1', ash + 10, sh)
            d.update_phasor('ph-2', 10, sh + a)
            d.update_phasor('ph-3', 10, sh - a)
            d.set_range(ash + 10)
            self.counter = self.counter + 1

        timer = QtCore.QTimer()
        timer.setInterval(10)
        timer.timeout.connect(rotate)
        self.counter = 0
        timer.start()

        app(d, [
            "Phasors smoothly rotating",
            "Amplitude of red phasor grows",
        ])


class TestPhasorDiagram_Legend(unittest.TestCase):
    def test_legend(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.add_phasor('ph-1', 80, 0, (255, 0, 0), width=3)
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))
        d.show_legend()
        d.set_range(80)

        app(d, [
            "Legend OK",
            "Lines in legend have different widths",
        ])

    def test_legend_prefer_names(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.add_phasor(0, amp=80, phi=0, color=(255, 0, 0), name="Ua")
        d.add_phasor(1, amp=80, phi=2*3.14/3, color=(0, 255, 0), name="Ub")
        d.add_phasor(2, amp=80, phi=-2*3.14/3, color=(0, 0, 255), name="Uc")
        d.show_legend()
        d.set_range(80)

        app(d, ["Legend: Ua, Ub, Uc"])

    def test_show_legend_twice(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.set_range(1)
        d.add_phasor(0, 1, 0)
        d.show_legend()
        d.show_legend()

        app(d, ["Legend OK"])


class TestPhasorDiagram_Clearing(unittest.TestCase):
    def test_clear_empty(self):
        app = testing.TestApp(self)
        d = phasor.PhasorDiagram()
        d.remove_phasors()
        app(d, ["Grid OK"])

    def test_clear_and_show_legend(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()

        d.set_range(80)
        d.add_phasor(0, amp=80, phi=0, color=(255, 0, 0), name="Ua")
        d.add_phasor(1, amp=80, phi=0, color=(0, 255, 0), name="Ub")
        d.show_legend()
        d.remove_phasors()

        d.add_phasor(0, amp=80, phi=0, name="Ua")
        d.show_legend()

        app(d, ["Legend OK"])


class TestPhasorDiagram_Visibility(unittest.TestCase):
    def test_set_invisible(self):
        app = testing.TestApp(self)

        d = phasor.PhasorDiagram()
        d.set_range(2)
        d.add_phasor(0, 1, 0, color=(255, 0, 0))
        d.add_phasor(1, 2, 1, color=(0, 255, 0))
        d.add_phasor(2, 2, 1, color=(0, 0, 255))
        d.show_legend()

        d.set_phasor_visible(1, False)
        d.set_phasor_visible(2, False)
        d.set_phasor_visible(2, True)
        d.set_phasor_visible(3, False)

        app(d, [
            "2 phasors in diagram",
            "3 items in legend",
        ])


class TestPhasorDiagram_Deprecation(unittest.TestCase):
    def test_size_arg(self):
        testing.TestApp(self)
        with self.assertWarns(FutureWarning):
            phasor.PhasorDiagram(size=100)

    def test_end_arg(self):
        testing.TestApp(self)
        with self.assertWarns(FutureWarning):
            phasor.PhasorDiagram(end='arrow')

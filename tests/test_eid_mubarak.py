"""Tests for the Eid Mubarak terminal greeting tool."""

import unittest
from unittest.mock import patch

from terminal_fun.tools.eid_mubarak import (
    THEMES,
    _build_frame,
    get_figlet_text,
    run,
)


class TestThemes(unittest.TestCase):
    """Test that all themes are valid and loadable."""

    def test_all_themes_exist(self):
        self.assertIn("classic", THEMES)
        self.assertIn("royal", THEMES)
        self.assertIn("minimal", THEMES)

    def test_theme_structure(self):
        for name, theme in THEMES.items():
            self.assertIn("primary", theme, f"{name} missing 'primary'")
            self.assertIn("secondary", theme, f"{name} missing 'secondary'")
            self.assertIn("accent", theme, f"{name} missing 'accent'")
            for key, rgb in theme.items():
                self.assertEqual(len(rgb), 3, f"{name}.{key} should be RGB tuple")
                for val in rgb:
                    self.assertGreaterEqual(val, 0)
                    self.assertLessEqual(val, 255)

    def test_invalid_theme_raises(self):
        with self.assertRaises(SystemExit):
            run(static=True, theme="nonexistent")


class TestFigletText(unittest.TestCase):
    """Test pyfiglet font fallback chain."""

    def test_returns_lines(self):
        lines = get_figlet_text("Eid Mubarak", 120)
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)

    def test_fits_within_width(self):
        width = 80
        lines = get_figlet_text("Eid Mubarak", width)
        for line in lines:
            self.assertLessEqual(len(line), width)

    def test_fallback_on_narrow_width(self):
        # Very narrow width should still return something
        lines = get_figlet_text("Eid Mubarak", 15)
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 0)


class TestBuildFrame(unittest.TestCase):
    """Test static frame composition."""

    def test_frame_has_border(self):
        frame = _build_frame(100, 30, "classic")
        self.assertTrue(frame[0].startswith("╔"))
        self.assertTrue(frame[0].endswith("╗"))
        self.assertTrue(frame[-1].startswith("╚"))
        self.assertTrue(frame[-1].endswith("╝"))

    def test_frame_consistent_width(self):
        frame = _build_frame(100, 30, "classic")
        expected_width = 100  # cols
        for i, line in enumerate(frame):
            self.assertEqual(len(line), expected_width, f"Line {i} width mismatch")

    def test_frame_contains_subtitle(self):
        frame = _build_frame(100, 30, "classic")
        combined = "\n".join(frame)
        self.assertIn("blessed Eid", combined)


class TestStaticMode(unittest.TestCase):
    """Test that static rendering works without errors."""

    @patch("terminal_fun.tools.eid_mubarak.shutil.get_terminal_size")
    def test_static_runs_without_error(self, mock_size):
        mock_size.return_value = (100, 30)
        # Should not raise
        run(static=True, theme="classic")

    @patch("terminal_fun.tools.eid_mubarak.shutil.get_terminal_size")
    def test_static_all_themes(self, mock_size):
        mock_size.return_value = (100, 30)
        for theme_name in THEMES:
            run(static=True, theme=theme_name)


class TestTerminalSizeFallback(unittest.TestCase):
    """Test terminal size detection with fallback."""

    @patch("terminal_fun.tools.eid_mubarak.shutil.get_terminal_size")
    def test_fallback_size(self, mock_size):
        mock_size.return_value = (100, 30)
        lines = get_figlet_text("Eid Mubarak", 96)
        self.assertIsInstance(lines, list)


if __name__ == "__main__":
    unittest.main()

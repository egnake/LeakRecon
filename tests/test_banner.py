"""Tests for core.banner module – random banner selection and utilities."""
import pytest
from unittest.mock import patch
from core.banner import (
    BANNERS,
    TAGLINE,
    get_random_banner,
    is_global_command,
    MENUS,
)


class TestRandomBanner:
    """Tests for the random ASCII art banner system."""

    def test_banners_list_not_empty(self):
        """Verify that the BANNERS collection contains at least one banner."""
        assert len(BANNERS) >= 1, "BANNERS list must not be empty"

    def test_banners_count(self):
        """Verify that there are exactly 6 unique banners."""
        assert len(BANNERS) == 6

    def test_each_banner_is_string(self):
        """Verify every banner in the collection is a string."""
        for i, banner in enumerate(BANNERS):
            assert isinstance(banner, str), f"Banner {i} is not a string"

    def test_each_banner_has_content(self):
        """Verify that no banner is blank or whitespace-only."""
        for i, banner in enumerate(BANNERS):
            assert banner.strip(), f"Banner {i} is empty or blank"

    def test_get_random_banner_returns_string(self):
        """Verify that get_random_banner() always returns a string."""
        result = get_random_banner()
        assert isinstance(result, str)

    def test_get_random_banner_includes_tagline(self):
        """Verify that the tagline is always appended to the selected banner."""
        result = get_random_banner()
        assert TAGLINE in result

    def test_get_random_banner_includes_one_banner(self):
        """Verify that the result contains at least one known banner art."""
        result = get_random_banner()
        found = any(banner in result for banner in BANNERS)
        assert found, "get_random_banner() did not include any known banner art"

    def test_randomness_produces_variation(self):
        """
        Run get_random_banner() many times and verify that at least 2 different
        banners are selected (statistical test – failure is extremely unlikely
        with 6 banners and 100 draws).
        """
        results = set()
        for _ in range(100):
            banner = get_random_banner()
            results.add(banner)
        assert len(results) >= 2, "Expected at least 2 different banners in 100 draws"

    def test_specific_banner_selection(self):
        """Verify that fixing random.choice returns the expected banner."""
        for idx, expected_banner in enumerate(BANNERS):
            with patch("core.banner.random.choice", return_value=expected_banner):
                result = get_random_banner()
                assert expected_banner in result
                assert TAGLINE in result


class TestGlobalCommands:
    """Tests for global command parsing."""

    def test_help_commands(self):
        for cmd in ("help", "h", "?"):
            assert is_global_command(cmd) == "help"

    def test_back_commands(self):
        for cmd in ("back", "b", "geri", "0"):
            assert is_global_command(cmd) == "back"

    def test_home_commands(self):
        for cmd in ("home", "ana"):
            assert is_global_command(cmd) == "home"

    def test_clear_commands(self):
        for cmd in ("clear", "cls", "temizle"):
            assert is_global_command(cmd) == "clear"

    def test_exit_commands(self):
        for cmd in ("exit", "quit", "q"):
            assert is_global_command(cmd) == "exit"

    def test_status_commands(self):
        for cmd in ("status", "durum"):
            assert is_global_command(cmd) == "status"

    def test_unknown_command(self):
        assert is_global_command("foobar") is None
        assert is_global_command("123") is None


class TestMenus:
    """Tests for menu structure integrity."""

    def test_all_expected_menus_exist(self):
        expected = {"main", "darkweb", "identity", "network", "onion", "credential", "crypto", "tools"}
        assert set(MENUS.keys()) == expected

    def test_each_menu_has_required_keys(self):
        for key, menu in MENUS.items():
            assert "title" in menu, f"Menu '{key}' missing 'title'"
            assert "icon" in menu, f"Menu '{key}' missing 'icon'"
            assert "items" in menu, f"Menu '{key}' missing 'items'"

    def test_each_menu_has_items(self):
        for key, menu in MENUS.items():
            assert len(menu["items"]) > 0, f"Menu '{key}' has no items"

    def test_menu_items_are_tuples_of_three(self):
        for key, menu in MENUS.items():
            for item in menu["items"]:
                assert len(item) == 3, f"Menu '{key}' item {item} should be a 3-tuple"

    def test_main_menu_has_7_items(self):
        assert len(MENUS["main"]["items"]) == 7

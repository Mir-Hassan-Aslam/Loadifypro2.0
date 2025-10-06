"""
Advanced UI Manager for LoadifyPro
Handles advanced UI customizations like theme and appearance management,
decoupling visual style logic from the main application.
"""
import customtkinter as ctk
import logging

logger = logging.getLogger(__name__)

class ThemeManager:
    """Manages the application's visual theme and appearance."""

    def __init__(self, settings_manager):
        """
        Initializes the ThemeManager.

        Args:
            settings_manager: An instance of the SettingsManager used to retrieve
                              the current theme and appearance settings.
        """
        self.settings_manager = settings_manager

    def apply_theme(self):
        """
        Applies the appearance mode and color theme globally using customtkinter settings.
        This function should be called at startup and whenever settings are changed.
        """
        try:
            appearance_mode = self.settings_manager.settings.get('appearance_mode', 'Dark')
            color_theme = self.settings_manager.settings.get('color_theme', 'blue')
            
            ctk.set_appearance_mode(appearance_mode)
            ctk.set_default_color_theme(color_theme)
            
            logger.info(f"Theme applied: Appearance='{appearance_mode}', Color='{color_theme}'")
        except Exception as e:
            logger.error(f"Failed to apply theme: {e}. Falling back to default.")
            ctk.set_appearance_mode("Dark")
            ctk.set_default_color_theme("blue")

    def get_theme_options(self) -> dict:
        """
        Provides a static dictionary of available theme options,
        used to populate dropdowns in the settings UI.
        
        Returns:
            A dictionary containing lists of available modes and themes.
        """
        return {
            "appearance_modes": ["Light", "Dark", "System"],
            "color_themes": ["blue", "green", "dark-blue"]
        }
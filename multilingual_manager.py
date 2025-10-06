"""
Multilingual Manager for LoadifyPro
Handles all string translations for the application's user interface.
This module is responsible for loading and providing localized text.
"""
from typing import Dict, List

class LocaleManager:
    """
    Manages loading and retrieving translated strings for the UI.
    This class acts as a central repository for all user-facing text,
    allowing for dynamic language switching.
    """

    def __init__(self, language: str = "en"):
        """
        Initializes the LocaleManager.

        Args:
            language (str): The initial language code to use (e.g., "en", "es").
        """
        self.translations: Dict[str, Dict[str, str]] = {}
        self._load_translations()
        self.current_language = language if language in self.translations else "en"

    def _load_translations(self):
        """
        Loads all language strings from an embedded dictionary.
        """
        self.translations = {
            "en": {
                "app_title": "LoadifyPro - Professional Download Manager",
                "settings_title": "Settings",
                "active_downloads": "ACTIVE",
                "completed_downloads": "COMPLETED",
                "total_speed": "SPEED",
                "url_placeholder": "Enter or Drag & Drop URL here...",
                "destination": "Destination",
                "browse": "Browse",
                "start_download": "Start Download",
                "active_tab": "Active",
                "completed_tab": "Completed",
                "scan_status": "Scan",
                "eta": "ETA",
                "status_queued": "QUEUED",
                "status_downloading": "DOWNLOADING",
                "status_completed": "COMPLETED",
                "status_error": "ERROR",
                "status_cancelled": "CANCELLED",
                "status_scanning": "SCANNING",
                "status_infected": "INFECTED",
                "status_quarantined": "QUARANTINED",
                "settings_ui_customization": "UI Customization",
                "settings_appearance_mode": "Appearance Mode:",
                "settings_color_theme": "Color Theme:",
                "settings_language": "Language:",
                "settings_save": "Save Settings",
                "restart_required": "Some changes may require a restart to take full effect.",
                "error_title": "Error",
                "success_title": "Success",
                "url_dest_required": "URL and destination are required.",
                "settings_saved": "Settings saved successfully!",
                "settings_antivirus": "Antivirus Settings",
                "settings_active_engine": "Active Engine:",
                "settings_auto_scan": "Auto-scan after download",
                "settings_vt_api_key": "VirusTotal API Key:",
            },
            "es": {
                "app_title": "LoadifyPro - Gestor de Descargas Profesional",
                "settings_title": "Configuración",
                "active_downloads": "ACTIVOS",
                "completed_downloads": "COMPLETADOS",
                "total_speed": "VELOCIDAD",
                "url_placeholder": "Ingrese o Arrastre y Suelte la URL aquí...",
                "destination": "Destino",
                "browse": "Navegar",
                "start_download": "Iniciar Descarga",
                "active_tab": "Activas",
                "completed_tab": "Completadas",
                "scan_status": "Análisis",
                "eta": "ETA",
                "status_queued": "EN COLA",
                "status_downloading": "DESCARGANDO",
                "status_completed": "COMPLETADO",
                "status_error": "ERROR",
                "status_cancelled": "CANCELADO",
                "status_scanning": "ANALIZANDO",
                "status_infected": "INFECTADO",
                "status_quarantined": "EN CUARENTENA",
                "settings_ui_customization": "Personalización de Interfaz",
                "settings_appearance_mode": "Modo de Apariencia:",
                "settings_color_theme": "Tema de Color:",
                "settings_language": "Idioma:",
                "settings_save": "Guardar Cambios",
                "restart_required": "Algunos cambios pueden requerir un reinicio para aplicarse completamente.",
                "error_title": "Error",
                "success_title": "Éxito",
                "url_dest_required": "La URL y el destino son obligatorios.",
                "settings_saved": "¡Configuración guardada con éxito!",
                "settings_antivirus": "Configuración de Antivirus",
                "settings_active_engine": "Motor Activo:",
                "settings_auto_scan": "Analizar tras descargar",
                "settings_vt_api_key": "Clave API de VirusTotal:",
            }
        }

    def get(self, key: str, fallback: str = None) -> str:
        """Gets a translated string for the current language."""
        return self.translations.get(self.current_language, self.translations["en"]).get(key, fallback or key)

    def set_language(self, language_code: str):
        """Sets the current language for translations, with a fallback to English."""
        self.current_language = language_code if language_code in self.translations else "en"

    def get_available_languages(self) -> List[str]:
        """Returns a list of all available language codes (e.g., ["en", "es"])."""
        return list(self.translations.keys())
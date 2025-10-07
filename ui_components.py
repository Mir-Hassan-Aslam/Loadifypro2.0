"""
UI Components for LoadifyPro
Contains all custom widget classes like DownloadCard and SettingsWindow.
These components are designed to be self-contained and reusable.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from download_core import DownloadState
from antivirus_manager import ScanStatus

# --- Constants ---
SPEED_COLOR = '#ff0080'
SUCCESS_COLOR = '#00ff88'
ERROR_COLOR = '#ff4444'
WARNING_COLOR = '#ffaa00'

class DownloadCard(ctk.CTkFrame):
    """A self-contained UI card for displaying the progress of a single download item."""
    def __init__(self, master, item, app_callbacks):
        super().__init__(master, border_width=1)
        self.item = item
        self.callbacks = app_callbacks
        self.translator = self.callbacks['get_translator']()
        self._create_widgets()
        self.update_ui(self.item)

    def _create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        icon_text = "📹" if self.item.is_youtube else "📁"
        ctk.CTkLabel(self, text=icon_text, font=ctk.CTkFont(size=24)).grid(row=0, column=0, rowspan=4, padx=15, pady=15, sticky="ns")
        
        self.filename_label = ctk.CTkLabel(self, text=self.item.filename, font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        self.filename_label.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 0))
        
        # Quality label
        quality_text = getattr(self.item, 'quality', 'best')
        quality_display = {'best': '🎬 Best', '2160p': '📺 4K', '1080p': '📺 1080p', '720p': '📺 720p', '480p': '📺 480p', '360p': '📺 360p', 'audio': '🎵 MP3', 'audio_m4a': '🎵 M4A'}.get(quality_text, f'📺 {quality_text}')
        self.quality_label = ctk.CTkLabel(self, text=quality_display, font=ctk.CTkFont(size=10), text_color='#666')
        self.quality_label.grid(row=0, column=1, sticky="e", padx=10, pady=(10, 0))

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=(0, 5))
        self.percentage_label = ctk.CTkLabel(stats_frame, text="0.0%", font=ctk.CTkFont(size=10)); self.percentage_label.pack(side="left", padx=(0, 15))
        self.size_label = ctk.CTkLabel(stats_frame, text="0 MB / 0 MB", font=ctk.CTkFont(size=10)); self.size_label.pack(side="left", padx=(0, 15))
        self.speed_label = ctk.CTkLabel(stats_frame, text="0.00 MB/s", font=ctk.CTkFont(size=10), text_color=SPEED_COLOR); self.speed_label.pack(side="left", padx=(0, 15))
        
        self.eta_label_prefix = self.translator.get('eta')
        self.eta_label = ctk.CTkLabel(stats_frame, text=f"{self.eta_label_prefix}: --", font=ctk.CTkFont(size=10)); self.eta_label.pack(side="left")

        self.scan_status_label_prefix = self.translator.get('scan_status')
        self.scan_status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=10, weight="bold")); self.scan_status_label.grid(row=3, column=1, sticky="w", padx=10, pady=(0, 10))

        self.status_label = ctk.CTkLabel(self, text=self.translator.get('status_queued'), width=100, font=ctk.CTkFont(size=10, weight="bold")); self.status_label.grid(row=0, column=2, padx=15)
        
        # Control buttons frame
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.grid(row=1, column=2, padx=15, pady=5)
        
        self.pause_button = ctk.CTkButton(self.control_frame, text="⏸️", width=30, height=30, fg_color="transparent", hover_color="#FFA500", command=self._on_pause)
        self.pause_button.grid(row=0, column=0, padx=2)
        
        self.resume_button = ctk.CTkButton(self.control_frame, text="▶️", width=30, height=30, fg_color="transparent", hover_color="#4CAF50", command=self._on_resume)
        self.resume_button.grid(row=0, column=1, padx=2)
        
        self.cancel_button = ctk.CTkButton(self.control_frame, text="❌", width=30, height=30, fg_color="transparent", hover_color=ERROR_COLOR, command=self._on_cancel)
        self.cancel_button.grid(row=0, column=2, padx=2)
        
        # Bind right-click context menu to all widgets
        self._bind_context_menu_recursive(self)

    def _bind_context_menu_recursive(self, widget):
        """Recursively bind right-click context menu to widget and all its children."""
        widget.bind("<Button-3>", self._show_context_menu)  # Right-click
        for child in widget.winfo_children():
            self._bind_context_menu_recursive(child)

    def _show_context_menu(self, event):
        """Show right-click context menu for download options."""
        try:
            import tkinter as tk
            context_menu = tk.Menu(self, tearoff=0)
            
            # Add refresh option for failed downloads
            if self.item.state == DownloadState.ERROR:
                context_menu.add_command(label="🔄 Refresh Download Link", command=self._on_refresh_link)
            
            # Add pause/resume options based on state
            if self.item.state == DownloadState.DOWNLOADING:
                context_menu.add_command(label="⏸️ Pause Download", command=self._on_pause)
            elif self.item.state == DownloadState.PAUSED:
                context_menu.add_command(label="▶️ Resume Download", command=self._on_resume)
            elif self.item.state == DownloadState.ERROR:
                context_menu.add_command(label="▶️ Resume Download", command=self._on_resume)
            
            # Add cancel option for active downloads
            if self.item.state in [DownloadState.DOWNLOADING, DownloadState.PAUSED, DownloadState.QUEUED]:
                context_menu.add_command(label="❌ Cancel Download", command=self._on_cancel)
            
            # Add separator and info
            context_menu.add_separator()
            context_menu.add_command(label=f"📁 Open Folder", command=self._open_download_folder)
            context_menu.add_command(label=f"🔗 Copy URL", command=self._copy_url)
            
            # Show context menu
            context_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error showing context menu: {e}")

    def _on_refresh_link(self):
        """Refresh the download link."""
        if self.callbacks.get('refresh_download_link'):
            self.callbacks['refresh_download_link'](self.item.id)

    def _open_download_folder(self):
        """Open the download folder in file explorer."""
        try:
            import os
            import subprocess
            import platform
            
            folder_path = os.path.dirname(self.item.filepath)
            if os.path.exists(folder_path):
                if platform.system() == "Windows":
                    subprocess.run(["explorer", folder_path])
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", folder_path])
                else:  # Linux
                    subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            print(f"Error opening folder: {e}")

    def _copy_url(self):
        """Copy the download URL to clipboard."""
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide the window
            root.clipboard_clear()
            root.clipboard_append(self.item.url)
            root.update()  # Update clipboard
            root.destroy()
        except Exception as e:
            print(f"Error copying URL: {e}")

    def update_ui(self, new_item_data):
        self.item = new_item_data
        self.filename_label.configure(text=self.item.filename)
        
        # Update quality display
        quality_text = getattr(self.item, 'quality', 'best')
        quality_display = {'best': '🎬 Best', '2160p': '📺 4K', '1080p': '📺 1080p', '720p': '📺 720p', '480p': '📺 480p', '360p': '📺 360p', 'audio': '🎵 MP3', 'audio_m4a': '🎵 M4A'}.get(quality_text, f'📺 {quality_text}')
        self.quality_label.configure(text=quality_display)
        
        self.progress_bar.set(self.item.progress / 100)
        self.percentage_label.configure(text=f"{self.item.progress:.1f}%")
        self.size_label.configure(text=f"{self._format_size(self.item.downloaded_size)} / {self._format_size(self.item.total_size)}")
        self.speed_label.configure(text=f"{self.item.speed:.2f} MB/s")
        self.eta_label.configure(text=f"{self.eta_label_prefix}: {self.item.time_remaining}")
        
        translated_state = self.translator.get(f'status_{self.item.state.lower()}')
        self.status_label.configure(text=translated_state, text_color=self._get_status_color(self.item.state))

        if self.item.scan_status:
            scan_color = self._get_scan_status_color(self.item.scan_status)
            translated_scan_status = self.translator.get(f'status_{self.item.scan_status.lower()}', self.item.scan_status)
            self.scan_status_label.configure(text=f"{self.scan_status_label_prefix}: {translated_scan_status}", text_color=scan_color)
            if self.item.scan_status in [ScanStatus.INFECTED.value, ScanStatus.QUARANTINED.value]:
                self.configure(border_color=ERROR_COLOR)
        
        # Update button visibility based on download state
        self._update_control_buttons()
        
        if self.item.state in [DownloadState.COMPLETED, DownloadState.CANCELLED, DownloadState.ERROR]:
            if self.item.state == DownloadState.COMPLETED and not (self.item.scan_status and self.item.scan_status != ScanStatus.CLEAN.value):
                 self.configure(border_color=SUCCESS_COLOR)
            elif self.item.state == DownloadState.ERROR: self.configure(border_color=ERROR_COLOR)
            if self.cancel_button.winfo_exists(): self.cancel_button.destroy()

    def _on_pause(self):
        """Pause the download."""
        if self.callbacks.get('pause_download'):
            self.callbacks['pause_download'](self.item.id)

    def _on_resume(self):
        """Resume the download."""
        if self.callbacks.get('resume_download'):
            self.callbacks['resume_download'](self.item.id)
    
    def _update_control_buttons(self):
        """Update the visibility and state of control buttons based on download state."""
        if self.item.state == DownloadState.DOWNLOADING:
            self.pause_button.grid()
            self.resume_button.grid_remove()
        elif self.item.state == DownloadState.PAUSED:
            self.pause_button.grid_remove()
            self.resume_button.grid()
        elif self.item.state == DownloadState.QUEUED:
            self.pause_button.grid_remove()
            self.resume_button.grid_remove()
        elif self.item.state == DownloadState.ERROR:
            # Show resume button for failed downloads
            self.pause_button.grid_remove()
            self.resume_button.grid()
        else:  # COMPLETED, CANCELLED
            self.pause_button.grid_remove()
            self.resume_button.grid_remove()

    def _on_cancel(self):
        if self.callbacks.get('cancel_download'):
            self.callbacks['cancel_download'](self.item.id)

    def _format_size(self, b): return f"{b/1024**2:.2f} MB" if isinstance(b, (int, float)) and b > 0 else "0 MB"

    def _get_status_color(self, s):
        theme = ctk.get_appearance_mode()
        return {'QUEUED': 'gray', 'DOWNLOADING': ('#00BFFF', '#1E90FF')[theme == "Dark"], 'PAUSED': '#FFA500', 'COMPLETED': SUCCESS_COLOR, 'ERROR': ERROR_COLOR, 'CANCELLED': 'gray'}.get(s, None)
    
    def _get_scan_status_color(self, s):
        return {ScanStatus.SCANNING.value: WARNING_COLOR, ScanStatus.CLEAN.value: SUCCESS_COLOR, ScanStatus.INFECTED.value: ERROR_COLOR, ScanStatus.QUARANTINED.value: ERROR_COLOR, ScanStatus.ERROR.value: ERROR_COLOR}.get(s, 'gray')


class SettingsWindow(ctk.CTkToplevel):
    """The settings window, decoupled from main app logic."""
    def __init__(self, master):
        super().__init__(master)
        self.app = master
        self.translator = self.app.translator
        self.title(self.translator.get('settings_title')); self.geometry("600x650"); self.transient(master)
        self.grid_columnconfigure(1, weight=1)
        self._create_widgets()
        self._load_current_settings()

    def _create_widgets(self):
        from advanced_ui_manager import ThemeManager
        theme_opts = ThemeManager(None).get_theme_options()

        ctk.CTkLabel(self, text=self.translator.get('settings_ui_customization'), font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        ctk.CTkLabel(self, text=self.translator.get('settings_appearance_mode')).grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.appearance_menu = ctk.CTkOptionMenu(self, values=theme_opts['appearance_modes']); self.appearance_menu.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=self.translator.get('settings_color_theme')).grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.theme_menu = ctk.CTkOptionMenu(self, values=theme_opts['color_themes']); self.theme_menu.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=self.translator.get('settings_language')).grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.lang_menu = ctk.CTkOptionMenu(self, values=self.translator.get_available_languages()); self.lang_menu.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(self, text=self.translator.get('settings_antivirus'), font=ctk.CTkFont(size=16, weight="bold")).grid(row=4, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="w")
        ctk.CTkLabel(self, text=self.translator.get('settings_active_engine')).grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.engine_menu = ctk.CTkOptionMenu(self, values=list(self.app.av_manager.configs.keys())); self.engine_menu.grid(row=5, column=1, padx=20, pady=5, sticky="ew")
        
        self.auto_scan_var = tk.BooleanVar()
        ctk.CTkCheckBox(self, text=self.translator.get('settings_auto_scan'), variable=self.auto_scan_var).grid(row=6, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        
        ctk.CTkLabel(self, text=self.translator.get('settings_vt_api_key')).grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.vt_api_key_entry = ctk.CTkEntry(self, placeholder_text="Enter your VirusTotal API key"); self.vt_api_key_entry.grid(row=7, column=1, padx=20, pady=5, sticky="ew")

        ctk.CTkButton(self, text=self.translator.get('settings_save'), command=self._on_save).grid(row=11, column=1, padx=20, pady=20, sticky="e")

    def _load_current_settings(self):
        s = self.app.settings
        av_configs = s.get('av_configs', {})
        av_active = s.get('av_active_config')
        
        self.appearance_menu.set(s.get('appearance_mode', 'Dark'))
        self.theme_menu.set(s.get('color_theme', 'blue'))
        self.lang_menu.set(s.get('language', 'en'))
        
        if av_active: self.engine_menu.set(av_active)
        if av_active and av_active in av_configs:
            self.auto_scan_var.set(av_configs[av_active].get('auto_scan', True))
        if "VirusTotal" in av_configs:
            self.vt_api_key_entry.insert(0, av_configs["VirusTotal"].get('api_key', ''))

    def _on_save(self):
        try:
            new_settings = {
                'appearance_mode': self.appearance_menu.get(),
                'color_theme': self.theme_menu.get(),
                'language': self.lang_menu.get(),
                'av_active_config': self.engine_menu.get(),
                'av_configs': self.app.av_manager.configs,
            }
            # Update specific AV configs from UI
            active_av = new_settings['av_active_config']
            if active_av in new_settings['av_configs']:
                new_settings['av_configs'][active_av]['auto_scan'] = self.auto_scan_var.get()
            if "VirusTotal" in new_settings['av_configs']:
                new_settings['av_configs']['VirusTotal']['api_key'] = self.vt_api_key_entry.get().strip()

            self.app.save_and_apply_settings(new_settings)
            messagebox.showinfo(self.translator.get('success_title'), f"{self.translator.get('settings_saved')}")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save settings: {e}")
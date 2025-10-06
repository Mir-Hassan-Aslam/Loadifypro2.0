"""
LoadifyPro - Main Application Entry Point
Initializes all managers, the main user interface, and connects all components.
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import queue
import threading
import logging

from tkinterdnd2 import DND_FILES, TkinterDnD

# Import all project modules
from multilingual_manager import LocaleManager
from antivirus_manager import AntivirusManager
from settings_manager import SettingsManager
from advanced_ui_manager import ThemeManager
from proxy_manager import ProxyManager
from scheduler import Scheduler
from speed_limiter import SpeedLimiter
from auth_manager import AuthManager
from download_core import DownloadItem, DownloadState, download_youtube_task, download_direct_file_task
from ui_components import DownloadCard, SettingsWindow
from drag_drop_manager import DragDropManager
from http_integration import HTTPIntegration

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='loadifypro.log', filemode='w')

class ModernDownloadManager(TkinterDnD.Tk):
    """The main application class for LoadifyPro."""
    def __init__(self):
        super().__init__()
        
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.settings
        
        self.theme_manager = ThemeManager(self.settings_manager)
        self.translator = LocaleManager(self.settings['language'])
        
        self.title(self.translator.get('app_title'))
        self.geometry("1100x750")

        self.downloads: dict[str, DownloadItem] = {}
        self.download_cards: dict[str, DownloadCard] = {}
        self.download_queue, self.ui_update_queue = queue.Queue(), queue.Queue()
        self.active_download_threads, self.max_concurrent_downloads = [], 3
        
        # HTTP integration for browser
        self.http_integration = HTTPIntegration(self._add_download_from_browser)
        
        self.proxy_manager = ProxyManager()
        self.scheduler = Scheduler()
        self.speed_limiter = SpeedLimiter()
        self.auth_manager = AuthManager()
        self.av_manager = AntivirusManager(update_callback=self._queue_ui_update)
        
        self._apply_all_settings()
        self._create_ui()
        
        self.drag_drop_manager = DragDropManager(self, self.url_entry)
        self.drag_drop_manager.enable_drag_drop()
        
        # Start HTTP integration
        self.http_integration.start()
        
        self.scheduler.start()
        self.after(200, self._process_ui_updates)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _apply_all_settings(self):
        s = self.settings_manager.settings
        self.theme_manager.apply_theme()
        self.proxy_manager.configure(s.get('proxy_enabled', False), s.get('proxy_http', ''), s.get('proxy_https', ''))
        self.speed_limiter.configure(s.get('speed_limit_enabled', False), s.get('speed_limit_kb', 1024))
        self.auth_manager.configure(s.get('auth_enabled', False), s.get('auth_user', ''), s.get('auth_pass', ''))
        self.av_manager.configs = s.get('av_configs', {})
        self.av_manager.active_config_name = s.get('av_active_config')


    def save_and_apply_settings(self, new_settings: dict):
        self.settings_manager.settings.update(new_settings)
        self.settings_manager.save_settings()
        self.translator.set_language(new_settings['language'])
        self._apply_all_settings()
        self._rebuild_ui()

    def _process_queue(self):
        self.active_download_threads = [t for t in self.active_download_threads if t.is_alive()]
        while not self.download_queue.empty() and len(self.active_download_threads) < self.max_concurrent_downloads:
            item_id = self.download_queue.get()
            item = self.downloads[item_id]
            self._queue_ui_update(item_id, {'state': DownloadState.DOWNLOADING})
            
            target = download_youtube_task if item.is_youtube else download_direct_file_task
            args = (item, self._queue_ui_update, self._download_finished, {
                'proxy': self.proxy_manager,
                'auth': self.auth_manager,
                'speed_limiter': self.speed_limiter
            })

            thread = threading.Thread(target=target, args=args, daemon=True)
            self.active_download_threads.append(thread); thread.start()

    def _on_closing(self):
        self.scheduler.stop()
        self.http_integration.stop()
        self.destroy()

    def _create_ui(self):
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(3, weight=1)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkLabel(header, text="LOADIFYPRO", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")
        self.settings_button = ctk.CTkButton(header, text=f"⚙️ {self.translator.get('settings_title')}", command=self._open_settings)
        self.settings_button.pack(side="right")

        stats_panel = ctk.CTkFrame(self, fg_color="transparent")
        stats_panel.grid(row=1, column=0, padx=20, pady=0, sticky="ew")
        self.active_label_prefix = self.translator.get('active_downloads')
        self.active_label=ctk.CTkLabel(stats_panel,text=f"{self.active_label_prefix}: 0");self.active_label.pack(side="left",padx=10)
        self.completed_label_prefix = self.translator.get('completed_downloads')
        self.completed_label=ctk.CTkLabel(stats_panel,text=f"{self.completed_label_prefix}: 0");self.completed_label.pack(side="left",padx=10)
        self.speed_label_prefix = self.translator.get('total_speed')
        self.speed_label=ctk.CTkLabel(stats_panel,text=f"{self.speed_label_prefix}: 0 MB/s",text_color='#ff0080');self.speed_label.pack(side="left",padx=10)

        new_dl_frame = ctk.CTkFrame(self); new_dl_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        new_dl_frame.grid_columnconfigure(1, weight=1)
        self.url_entry = ctk.CTkEntry(new_dl_frame, placeholder_text=self.translator.get('url_placeholder')); self.url_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.dest_label = ctk.CTkLabel(new_dl_frame, text=self.translator.get('destination')); self.dest_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.dest_entry = ctk.CTkEntry(new_dl_frame); self.dest_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads")); self.dest_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.browse_button = ctk.CTkButton(new_dl_frame, text=self.translator.get('browse'), width=80, command=self._browse); self.browse_button.grid(row=1, column=2, padx=10, pady=5)
        self.start_button = ctk.CTkButton(new_dl_frame, text=self.translator.get('start_download'), command=self._add_download); self.start_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.tabview = ctk.CTkTabview(self); self.tabview.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.active_tab = self.tabview.add(self.translator.get('active_tab'))
        self.completed_tab = self.tabview.add(self.translator.get('completed_tab'))
        self.active_frame = ctk.CTkScrollableFrame(self.active_tab, fg_color="transparent"); self.active_frame.pack(fill="both", expand=True)
        self.completed_frame = ctk.CTkScrollableFrame(self.completed_tab, fg_color="transparent"); self.completed_frame.pack(fill="both", expand=True)

    def _add_download(self):
        url, dest = self.url_entry.get().strip(), self.dest_entry.get().strip()
        if not (url and dest): return messagebox.showerror(self.translator.get('error_title'), self.translator.get('url_dest_required'))
        item = DownloadItem(url, dest)
        self.downloads[item.id] = item
        callbacks = {
            'cancel_download': self.cancel_download, 
            'pause_download': self.pause_download,
            'resume_download': self.resume_download,
            'get_translator': lambda: self.translator
        }
        card = DownloadCard(self.active_frame, item, callbacks)
        card.pack(fill="x", padx=5, pady=5); self.download_cards[item.id] = card
        self.download_queue.put(item.id); self.url_entry.delete(0, ctk.END); self._process_queue()

    def _process_ui_updates(self):
        try:
            while not self.ui_update_queue.empty():
                item_id, update_data = self.ui_update_queue.get_nowait()
                if (item := self.downloads.get(item_id)) and (card := self.download_cards.get(item_id)):
                    for key, value in update_data.items(): setattr(item, key, value)
                    card.update_ui(item)
            self._update_global_stats()
        except queue.Empty: pass
        finally: self.after(200, self._process_ui_updates)

    def _add_download_from_browser(self, url, quality='best'):
        """Add download from browser extension via HTTP."""
        if url and url.strip():
            # Check if it's a YouTube video or a file download
            if 'youtube.com' in url or 'youtu.be' in url:
                # YouTube video - use quality selection
                self.url_entry.delete(0, ctk.END)
                self.url_entry.insert(0, url.strip())
                self._add_download_with_quality(quality)
                logging.info(f"Added video download from browser: {url} with quality: {quality}")
            else:
                # File download - no quality selection needed
                self.url_entry.delete(0, ctk.END)
                self.url_entry.insert(0, url.strip())
                self._add_download()
                logging.info(f"Added file download from browser: {url}")
    
    def _add_download_with_quality(self, quality='best'):
        """Add download with specific quality setting."""
        url, dest = self.url_entry.get().strip(), self.dest_entry.get().strip()
        if not (url and dest): 
            return messagebox.showerror(self.translator.get('error_title'), self.translator.get('url_dest_required'))
        
        item = DownloadItem(url, dest)
        item.quality = quality  # Store quality preference
        self.downloads[item.id] = item
        callbacks = {
            'cancel_download': self.cancel_download, 
            'pause_download': self.pause_download,
            'resume_download': self.resume_download,
            'get_translator': lambda: self.translator
        }
        card = DownloadCard(self.active_frame, item, callbacks)
        card.pack(fill="x", padx=5, pady=5); self.download_cards[item.id] = card
        self.download_queue.put(item.id); self.url_entry.delete(0, ctk.END); self._process_queue()
    
    def _add_download_from_browser_file(self, url):
        """Add file download from browser extension (no quality selection needed)."""
        if url and url.strip():
            # Add the URL to the URL entry field and trigger download
            self.url_entry.delete(0, ctk.END)
            self.url_entry.insert(0, url.strip())
            # Automatically start the download (files don't have quality options)
            self._add_download()
            logging.info(f"Added file download from browser: {url}")

    def _update_global_stats(self):
        active = [item for item in self.downloads.values() if item.state == DownloadState.DOWNLOADING]
        completed = [item for item in self.downloads.values() if item.state in [DownloadState.COMPLETED, DownloadState.ERROR, DownloadState.CANCELLED]]
        total_speed = sum(item.speed for item in active)
        self.active_label.configure(text=f"{self.active_label_prefix}: {len(active)}")
        self.completed_label.configure(text=f"{self.completed_label_prefix}: {len(completed)}")
        self.speed_label.configure(text=f"{self.speed_label_prefix}: {total_speed:.2f} MB/s")

    def _queue_ui_update(self, item_id: str, update_dict: dict):
        self.ui_update_queue.put((item_id, update_dict))

    def _download_finished(self, item_id):
        item = self.downloads.get(item_id)
        if item and item.state == DownloadState.COMPLETED: self.av_manager.scan_file_async(item.filepath, item.id)
        if item and (card := self.download_cards.get(item_id)) and card.master == self.active_frame:
            card.pack_forget()
            callbacks = {
            'cancel_download': self.cancel_download, 
            'pause_download': self.pause_download,
            'resume_download': self.resume_download,
            'get_translator': lambda: self.translator
        }
            completed_card = DownloadCard(self.completed_frame, item, callbacks); completed_card.pack(fill="x", padx=5, pady=5)
            self.download_cards[item_id] = completed_card
        self._process_queue()
    
    def _browse(self):
        if folder := filedialog.askdirectory(): self.dest_entry.delete(0, ctk.END); self.dest_entry.insert(0, folder)
    
    def pause_download(self, item_id):
        """Pause a download."""
        if item := self.downloads.get(item_id):
            item.pause()
            if item_id in self.download_cards:
                self.download_cards[item_id].update_ui(item)
            logging.info(f"Download {item_id} paused by user")

    def resume_download(self, item_id):
        """Resume a download."""
        if item := self.downloads.get(item_id):
            item.resume()
            if item_id in self.download_cards:
                self.download_cards[item_id].update_ui(item)
            # Re-queue the download for processing
            self.download_queue.put(item_id)
            logging.info(f"Download {item_id} resumed by user")

    def cancel_download(self, item_id):
        if item := self.downloads.get(item_id): item.cancel_event.set()

    def _open_settings(self):
        SettingsWindow(self)

    def _rebuild_ui(self):
        for widget in self.winfo_children(): widget.destroy()
        self._create_ui()
        for item_id, item in self.downloads.items():
            frame = self.completed_frame if item.state in [DownloadState.COMPLETED, DownloadState.ERROR, DownloadState.CANCELLED] else self.active_frame
            callbacks = {
            'cancel_download': self.cancel_download, 
            'pause_download': self.pause_download,
            'resume_download': self.resume_download,
            'get_translator': lambda: self.translator
        }
            card = DownloadCard(frame, item, callbacks)
            card.pack(fill="x", padx=5, pady=5)
            self.download_cards[item_id] = card

if __name__ == "__main__":
    app = ModernDownloadManager()
    app.mainloop()


import os
import json
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox


def load_config() -> dict:
    """Loads the json file for configuration"""
    config_path = os.path.dirname(__file__)
    config_path = os.path.join(config_path, 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def save_config(config: dict) -> None:
    """Saves the json file for configuration"""
    config_path = os.path.dirname(__file__)
    config_path = os.path.join(config_path, 'config.json')
    with open(config_path, 'r') as f:
        json.dump(config, f, indent=4)


class StatusBar(ttk.Frame):
    def __init__(self, master: ttk.Frame, **kwargs):
        super().__init__(master, **kwargs)

        # PROPERTIES
        self.base_string = 'Ready to continue...'
        self.text = ttk.StringVar()
        self.text_label = ttk.Label(self, textvariable=self.text)
        self.text_label.pack(anchor='w', padx=10)
        self.reset()
    
    def raise_notification(self, text: str, type_: str) -> None:
        """Raises a notificacion, is a template"""
        style = 'danger' if type_ == 'error' else type_
        self.config(bootstyle=style)
        self.text_label.config(bootstyle=f'{style}-inverse')
        self.text.set(text)
        notification = getattr(Messagebox, f'show_{type_}')
        notification(text, title=type_.title(), parent=self.master)
        self.reset()

    def warning(self, text: str) -> None:
        """Changes the bar and raises a warning notification"""
        self.raise_notification(text, 'warning')
    
    def error(self, text: str) -> None:
        """Changes the bar and raises a warning notification"""
        self.raise_notification(text, 'error')
    
    def info(self, text: str) -> None:
        """Changes the bar and raises a warning notification"""
        self.raise_notification(text, 'info')
    
    def reset(self):
        """Restores the status bar"""
        self.text.set(self.base_string)
        self.config(bootstyle='secondary')
        self.text_label.config(bootstyle='secondary-inverse')
    
    def set(self, text: str) -> None:
        """Changes the status bar text"""
        self.text.set(text)
        self.base_string = text
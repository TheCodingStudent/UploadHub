import os
import json
import time
import argparse
import subprocess
import ttkbootstrap as ttk
from tkinter.filedialog import askdirectory
from ttkbootstrap.dialogs import Messagebox

# TERMINAL ARGUMENTS
parser = argparse.ArgumentParser(prog='UploadHub', description='Manages package uploads')
parser.add_argument('mode')
args = parser.parse_args()
mode = args.mode


def load_config() -> dict:
    config_path = os.path.dirname(__file__)
    config_path = os.path.join(config_path, 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


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


# INTERFACES
class NewPackage(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # CONFIG
        self.config = load_config()

        # VARIABLES
        options = ['No', 'Yes']
        modes = ['Public', 'Private']

        info_frame = ttk.LabelFrame(self, text='Package Info')
        info_frame.pack(expand=True, fill='x', padx=10, pady=10)
        ttk.Label(info_frame, text='Package name ').grid(row=0, column=0, sticky='w', padx=10, pady=(5, 0))
        self.package_name = ttk.Entry(info_frame, width=70)
        self.package_name.grid(row=0, column=1, sticky='w', padx=10, pady=(5, 0))
        ttk.Label(info_frame, text='Package directory ').grid(row=1, column=0, sticky='w', padx=10, pady=(5, 0))
        self.package_dir = ttk.Entry(info_frame, width=70, state='readonly')
        self.package_dir.grid(row=1, column=1, sticky='w', padx=10, pady=(5, 0))
        ttk.Button(
            info_frame, text='Select Folder...', bootstyle='info',
            command=self.add_package_dir
        ).grid(row=1, column=2, sticky='w', padx=(0, 10), pady=(5, 0))
        ttk.Label(info_frame, text='Package version').grid(row=2, column=0, sticky='w', padx=10, pady=(5, 0))
        self.version = ttk.Entry(info_frame, width=70)
        self.version.grid(row=2, column=1, sticky='w', padx=10, pady=(5, 0))
        self.version.insert(0, self.config['version'])
        ttk.Label(info_frame, text='Package description').grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.description = ttk.Entry(info_frame, width=70)
        self.description.grid(row=3, column=1, sticky='w', padx=10, pady=5)

        user_frame = ttk.LabelFrame(self, text='User Info')
        user_frame.pack(expand=True, fill='x', padx=10, pady=10)
        ttk.Label(user_frame, text='Package author').grid(row=0, column=0, sticky='w', padx=10, pady=(5, 0))
        self.author = ttk.Entry(user_frame, width=70)
        self.author.grid(row=0, column=1, sticky='w', padx=10, pady=(5, 0))
        self.author.insert(0, self.config['author'])
        ttk.Label(user_frame, text='Package mail').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.mail = ttk.Entry(user_frame, width=70)
        self.mail.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        self.mail.insert(0, self.config['mail'])

        git_frame = ttk.LabelFrame(self, text='Git Info')
        git_frame.pack(expand=True, fill='x', padx=10, pady=10)
        ttk.Label(git_frame, text='Git username').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.user_git = ttk.Entry(git_frame, width=70)
        self.user_git.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        self.user_git.insert(0, self.config['gituser'])
        ttk.Label(git_frame, text='Create Git repository ').grid(row=1, column=0, sticky='w', padx=10, pady=(5, 0))
        self.add_git = ttk.Combobox(git_frame, width=10, values=options, state='readonly')
        self.add_git.grid(row=1, column=1, sticky='w', padx=10, pady=(5, 0))
        self.add_git.current(0)
        ttk.Label(git_frame, text='Push Git repository ').grid(row=2, column=0, sticky='w', padx=10, pady=(5, 0))
        self.push_git = ttk.Combobox(git_frame, width=10, values=options, state='readonly')
        self.push_git.grid(row=2, column=1, sticky='w', padx=10, pady=(5, 0))
        self.push_git.current(0)
        ttk.Label(git_frame, text='Git repository mode').grid(row=3, column=0, sticky='w', padx=10, pady=(5, 0))
        self.mode_git = ttk.Combobox(git_frame, width=10, values=modes, state='readonly')
        self.mode_git.grid(row=3, column=1, sticky='w', padx=10, pady=(5, 0))
        self.mode_git.current(0)
        ttk.Label(git_frame, text='Git first commit ').grid(row=4, column=0, sticky='w', padx=10, pady=5)
        self.commit_git = ttk.Entry(git_frame, width=70)
        self.commit_git.grid(row=4, column=1, sticky='w', padx=10, pady=5)
        self.commit_git.insert(0, self.config['commit'])

        create_button = ttk.Button(self, text='Create new package...', bootstyle='success', command=self.create_package)
        create_button.pack(expand=True, fill='x', padx=10, pady=10)

        self.status_bar = StatusBar(self)
        self.status_bar.pack(expand=True, fill='x')

        # PROPERTIES
        self.entries = [self.package_name, self.package_dir, self.version, self.author, self.description, self.mail]

        # BINDS
        for entry in self.entries:
            entry.bind('<KeyRelease>', lambda event, _entry=entry: self.update_entry(_entry))
            entry.bind('<Return>', self.create_package)
    
    def update_entry(self, entry: ttk.Entry) -> None:
        entry.config(bootstyle='default')

    def create_setup(self, path: str, name: str, version: str, author: str, description: str, mail: str) -> None:
        self.status_bar.set('Creating setup.py...')
        setup_path = os.path.dirname(__file__)
        setup_path = f'{setup_path}/setup.py'
        with open(setup_path, 'r') as f:
            setup = f.read()

        setup = setup.replace('"VERSION"', f'"{version}"')
        setup = setup.replace('"NAME"', f'"{name}"')
        setup = setup.replace('"AUTHOR"', f'"{author}"')
        setup = setup.replace('"DESCRIPTION"', f'"{description}"')
        setup = setup.replace('"MAIL"', f'"{mail}"')
        with open(f'{path}/setup.py', 'w') as f: f.write(setup)
        self.status_bar.set('Setup.py created successfully...')

    def create_license(self, path: str) -> None:
        self.status_bar.set('Creating LICENSE...')
        license_path = os.path.dirname(__file__)
        license_path = f'{license_path}/license.py'
        with open(license_path, 'r') as f: license_text = f.read()
        with open(f'{path}/LICENSE', 'w') as f: f.write(license_text)
        self.status_bar.set('LICENSE created successfully...')
    
    def create_readme(self, path: str) -> None:
        self.status_bar.set('Creating README.md...')
        open(f'{path}/README.md', 'w').close()
        self.status_bar.set('README.md created successfully...')

    # @thread_it
    def create_package(self, *_) -> None:

        # PACKAGE INFO
        if not (package_name := self.check_entry(self.package_name)): return
        if not (package_dir := self.check_entry(self.package_dir)): return
        if not (version := self.check_entry(self.version)): return

        # USER INFO
        if not (author := self.check_entry(self.author)): return
        if not (description := self.check_entry(self.description)): return
        if not (mail := self.check_entry(self.mail)): return

        # GIT INFO
        add_git = self.add_git.get()
        push_git = self.push_git.get()
        mode_git = self.mode_git.get().lower()
        user_git = self.user_git.get()

        # CREATE STRUCTURE
        package_folder = f'{package_dir}/{package_name}'
        if not os.path.isdir(package_folder): os.mkdir(package_folder)
        self.create_license(package_folder)
        self.create_readme(package_folder)
        self.create_setup(package_folder, package_name, version, author, description, mail)
        inner_folder = f'{package_folder}/{package_name}'
        if not os.path.isdir(inner_folder): os.mkdir(inner_folder)
        open(f'{inner_folder}/__init__.py', 'w').close()
        open(f'{inner_folder}/__main__.py', 'w').close()
        # time.sleep(5)

        # CREATE GIT REPOSITORY
        if add_git != 'Yes': return self.status_bar.info('Package successfully created...')
        if not (commit_git := self.check_entry(self.commit_git)): return
        self.status_bar.set('Creating repository...')
        self.run('git init', package_folder)
        self.run('git add .', package_folder)
        subprocess.run(['git', 'commit', '-m', f'"{commit_git}"'], cwd=package_folder)
        self.run('git branch -M main', package_folder)
        self.run('git branch', package_folder)
        if push_git != 'Yes': return self.status_bar.info('Repository successfully created...')
        self.status_bar.set('Uploadind repository...')
        self.run(f'gh repo create {package_name} --{mode_git}', package_folder)
        self.run(f'git remote add origin https://github.com/{user_git}/{package_name}.git', package_folder)
        self.run('git push -u origin main', package_folder)
        self.status_bar.info('Repository successfully uploaded...')
    
    def run(self, command: str, cwd: str) -> None:
        subprocess.run(command.split(' '), cwd=cwd)

    def check_entry(self, entry: ttk.Entry) -> str|None:
        if not (value := entry.get()):
            entry.config(bootstyle='danger')
            entry.focus()
            return self.status_bar.error('Must provide argument...')
        return value

    def add_package_dir(self) -> None:
        if not (directory := askdirectory()): return
        self.package_dir.config(state='normal')
        self.package_dir.delete(0, 'end')
        self.package_dir.insert(0, directory)
        self.package_dir.config(state='readonly')


class UploadPackage(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if mode.lower().startswith('n'): window = NewPackage
elif mode.lower().startswith('u'): window = UploadPackage

window = window(
    themename='darkly',
    title='UploadHub By Armando Chaparro 18/07/23',
    resizable=(None, None)
)

window.attributes('-topmost', True)
window.place_window_center()
window.mainloop()
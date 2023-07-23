import os
import subprocess
import ttkbootstrap as ttk
from .utils import StatusBar
from tkinter.filedialog import askdirectory


class UploadPackage(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # VARIABLES
        options = ['No', 'Yes']

        # USER INTERFACE
        package_frame = ttk.LabelFrame(self, text='package Info')
        package_frame.pack(expand=True, fill='x', padx=10, pady=10)
        ttk.Label(package_frame, text='Package directory ').grid(row=0, column=0, sticky='w', padx=10, pady=(5, 0))
        self.package_dir = ttk.Entry(package_frame, width=70, state='readonly')
        self.package_dir.grid(row=0, column=1, sticky='w', padx=10, pady=(5, 0))
        ttk.Button(
            package_frame, text='Select Folder...', bootstyle='info',
            command=self.add_package_dir
        ).grid(row=0, column=2, sticky='w', padx=(0, 10), pady=(5, 0))
        ttk.Label(package_frame, text='Package version').grid(row=1, column=0, sticky='w', padx=10, pady=(5, 0))
        self.version = ttk.Entry(package_frame, width=70)
        self.version.grid(row=1, column=1, sticky='w', padx=10, pady=(5, 0))
        ttk.Label(package_frame, text='Package description').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.description = ttk.Entry(package_frame, width=70)
        self.description.grid(row=2, column=1, sticky='w', padx=10, pady=5)

        git_frame = ttk.LabelFrame(self, text='Git Info')
        git_frame.pack(expand=True, fill='x', padx=10, pady=10)
        ttk.Label(git_frame, text='Push Git repository ').grid(row=0, column=0, sticky='w', padx=10, pady=(5, 0))
        self.push_git = ttk.Combobox(git_frame, width=10, values=options, state='readonly')
        self.push_git.grid(row=0, column=1, sticky='w', padx=10, pady=(5, 0))
        self.push_git.current(0)
        ttk.Label(git_frame, text='Git commit message').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.commit_git = ttk.Entry(git_frame, width=70)
        self.commit_git.grid(row=1, column=1, sticky='w', padx=10, pady=5)

        files_frame = ttk.LabelFrame(self, text='File Info')
        files_frame.pack(expand=True, fill='x', padx=10, pady=10)
        ttk.Label(files_frame, text='Delete past version').grid(row=0, column=0, sticky='w', padx=10, pady=(5, 0))
        self.delete_past = ttk.Combobox(files_frame, width=10, values=options, state='readonly')
        self.delete_past.grid(row=0, column=1, sticky='w', padx=10, pady=(5, 0))
        self.delete_past.current(1)
        ttk.Label(files_frame, text='Update version').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.update_version = ttk.Combobox(files_frame, width=10, values=options, state='readonly')
        self.update_version.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        self.update_version.current(1)

        pypi_frame = ttk.LabelFrame(self, text='Pypi Info')
        pypi_frame.pack(expand=True, fill='x', padx=10, pady=10)
        ttk.Label(pypi_frame, text='Upload to Pypi ').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.upload_pypi = ttk.Combobox(pypi_frame, width=10, values=options, state='readonly')
        self.upload_pypi.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        self.upload_pypi.current(0)

        create_button = ttk.Button(self, text='Upload package...', bootstyle='success', command=self.upload_package)
        create_button.pack(expand=True, fill='x', padx=10, pady=10)

        self.status_bar = StatusBar(self)
        self.status_bar.pack(expand=True, fill='x')

        # PROPERTIES
        self.entries = [self.version]

        # BINDS
        for entry in self.entries:
            entry.bind('<KeyRelease>', lambda event, _entry=entry: self.update_entry(_entry))
            entry.bind('<Return>', self.upload_package)

    def update_entry(self, entry: ttk.Entry) -> None:
        """Changes the state of the entry to default"""
        entry.config(bootstyle='default')

    def parse_setup(self, package_dir: str) -> str:
        """Gets info from the setup file"""
        setup_path = os.path.join(package_dir, 'setup.py')
        self.config = dict()
        if not os.path.isfile(setup_path): return
        with open(setup_path, 'r') as f:
            lines = f.read().strip().split('\n')
        for line in lines:
            if line.startswith('VERSION'): self.config['version'] = line.split('=')[-1].strip()[1:-1]
            if line.startswith('DESCRIPTION'): self.config['description'] = line.split('=')[-1].strip()[1:-1]
        
        self.version.delete(0, 'end')
        self.version.insert(0, self.config['version'])
        self.description.delete(0, 'end')
        self.description.insert(0, self.config['description'])
    
    def update_new_version(self, package_dir: str, version: str) -> None:
        setup_path = os.path.join(package_dir, 'setup.py')
        if not os.path.isfile(setup_path): return
        with open(setup_path, 'r') as f:
            lines = f.read().strip().split('\n')
        
        result = list()
        for line in lines:
            if line.startswith('VERSION'): result.append(f'VERSION = "{version}"')
            else: result.append(line)
        
        with open(setup_path, 'w') as f:
            f.write('\n'.join(result))
        
        self.version.delete(0, 'end')
        self.version.insert(0, version)

    def run(self, command: str, cwd: str) -> None:
        """Runs a command with subprocess"""
        subprocess.run(command.split(' '), cwd=cwd)

    def check_entry(self, entry: ttk.Entry) -> str|None:
        """Checks if the entry is not empty"""
        if not (value := entry.get()):
            entry.config(bootstyle='danger')
            entry.focus()
            return self.status_bar.error('Must provide argument...')
        return value

    def add_package_dir(self) -> None:
        """Manages the folder input"""
        if not (directory := askdirectory()): return
        self.package_dir.config(state='normal')
        self.package_dir.delete(0, 'end')
        self.package_dir.insert(0, directory)
        self.package_dir.config(state='readonly')
        self.parse_setup(directory)

    def check_git(self, package_folder: str) -> bool:
        """Checks if the package folder is a git repository"""
        return subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            cwd=package_folder,
            check=False, capture_output=True
        ) is True

    def upload_package(self) -> None:

        # PACKAGE INFO
        if not (package_dir := self.check_entry(self.package_dir)): return
        if not (version := self.check_entry(self.version)): return
        
        # GIT INFO
        push_git = self.push_git.get()
        delete_past = self.delete_past.get()
        update_version = self.update_version.get()
        upload_pypi = self.upload_pypi.get()
        dist_folder = os.path.join(package_dir, 'dist')

        # UPDATE GIT REPOSITORY IF NEEDED
        if push_git == 'Yes':
            if not (commit_git := self.check_entry(self.commit_git)): return
            self.run('git add .', package_dir)
            subprocess.run(['git', 'commit', '-m', f'"{commit_git}"'], cwd=package_dir)
            self.run('git push', package_dir)

        # DELETE PREVIOUS VERSIONS IF NEEDED
        if delete_past == 'Yes' and os.path.isdir(dist_folder):
            for file in os.listdir(dist_folder):
                os.remove(os.path.join(dist_folder, file))

        # UPDATE VERSION IF NEEDED
        if update_version == 'Yes':
            a, b, c = version.split('.')
            c = int(c) + 1
            version = '.'.join([a, b, str(c)])
            self.update_new_version(package_dir, version)

        # UPLOAD TO PYPI
        if upload_pypi == 'Yes':
            self.run('python setup.py sdist bdist_wheel', package_dir)
            self.run('twine upload dist/*', package_dir)
        
        self.status_bar.info('Package successfully uploaded...')

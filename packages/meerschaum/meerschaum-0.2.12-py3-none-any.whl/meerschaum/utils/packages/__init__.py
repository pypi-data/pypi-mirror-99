#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Functions for managing packages and virtual environments reside here.
"""

from __future__ import annotations
from meerschaum.utils.typing import Any, List, SuccessTuple, Optional, Union

import importlib, importlib.util

_import_module = importlib.import_module
from meerschaum.utils.packages._packages import packages, all_packages
import os, pathlib, sys, platform
from meerschaum.utils.warnings import warn, error

_import_hook_venv = None
active_venvs = set()
def need_update(
        package : 'ModuleType',
        split : bool = True,
        color : bool = True,
        debug : bool = False,
    ) -> bool:
    """
    Check if a Meerschaum dependency needs an update.
    """
    if debug: from meerschaum.utils.debug import dprint
    import re
    root_name = package.__name__.split('.')[0] if split else package.__version__
    install_name = all_packages.get(root_name, root_name)

    _install_no_version = re.split('[=<>,! ]', install_name)[0]
    if debug: dprint(f"_install_no_version: {_install_no_version}", color=color)
    required_version = install_name.replace(_install_no_version, '')
    if debug: dprint(f"required_version: {required_version}", color=color)
    update_checker = attempt_import('update_checker', lazy=False, check_update=False)
    checker = update_checker.UpdateChecker()
    try:
        version = package.__version__
    except:
        return False

    result = checker.check(_install_no_version, version)
    if result is None:
        return False
    if required_version:
        semver = attempt_import('semver')
        if debug:
            dprint(f"Available version: {result.available_version}", color=color)
            dprint(f"Required version: {required_version}", color=color)
        return semver.match(result.available_version, required_version)

    packaging_version = attempt_import('packaging.version')
    return (
        packaging_version.parse(result.available_version) > 
        packaging_version.parse(version)
    )

def is_venv_active(
        venv: str = 'mrsm',
        color : bool = True,
        debug: bool = False
    ) -> bool:
    """
    Check if a virtual environment is active
    """
    if venv is None: return False
    if debug:
        from meerschaum.utils.debug import dprint
        dprint(f"Checking if virtual environment '{venv}' is active.", color=color)
    return venv in active_venvs

def deactivate_venv(
        venv: str = 'mrsm',
        color : bool = True,
        debug: bool = False
    ) -> bool:
    """
    Remove a virtual environment from sys.path (if it's been activated)
    """
    global active_venvs
    if venv is None: return True
    if debug:
        from meerschaum.utils.debug import dprint
        dprint(f"Deactivating virtual environment '{venv}'...", color=color)
    if venv in active_venvs: active_venvs.remove(venv)
    #  indices, new_path = [], []
    if sys.path is None: return False
    target = venv_target_path(venv, debug=debug)
    if str(target) in sys.path:
        sys.path.remove(str(target))
    #  for i, p in enumerate(sys.path):
        #  if f'venvs/{venv}/lib' not in str(p):
            #  new_path.append(p)
    #  sys.path = new_path

    ### clear the import virtual environment override
    #  uninstall_import_hook(venv, debug=debug)

    if debug: dprint(f'sys.path: {sys.path}', color=color)
    return True


def activate_venv(
        venv: str = 'mrsm',
        color : bool = True,
        debug: bool = False
    ) -> bool:
    """
    Create a virtual environment (if it doesn't exist) and add it to sys.path if necessary
    """
    global active_venvs
    if venv in active_venvs: return True
    if venv is None: return True
    if debug: from meerschaum.utils.debug import dprint
    import sys, os, platform
    from meerschaum.config._paths import VIRTENV_RESOURCES_PATH
    _venv = None
    virtualenv = attempt_import('virtualenv', venv=None, lazy=False, install=True, warn=False, debug=debug)
    if virtualenv is None:
        try:
            import ensurepip
            import venv as _venv
            virtualenv = None
        except ImportError:
            _venv = None
    if virtualenv is None and _venv is None:
        print(f"Failed to import virtualenv! Please install virtualenv via pip then restart Meerschaum.")
        sys.exit(1)
    venv_path = pathlib.Path(os.path.join(VIRTENV_RESOURCES_PATH, venv))
    bin_path = pathlib.Path(
        venv_path,
        ('bin' if platform.system() != 'Windows' else "Scripts")
    )
    if not venv_path.exists():
        if _venv is not None:
            _venv.create(
                venv_path,
                system_site_packages = False,
                with_pip = True,
                symlinks = (platform.system() != 'Windows'),
            )
        else:
            virtualenv.cli_run([str(venv_path), '--download', '--system-site-packages'])

    old_cwd = pathlib.Path(os.getcwd())
    os.chdir(VIRTENV_RESOURCES_PATH)
    if debug: dprint(f"Activating virtual environment '{venv}'...", color=color)
    #  try:
        #  exec(open(activate_this_path).read(), {'__file__': activate_this_path})
    #  except Exception as e:
        #  warn(str(e))
        #  return False
    active_venvs.add(venv)
    os.chdir(old_cwd)

    ### override built-in import with attempt_import
    #  install_import_hook(venv, debug=debug)
    target = venv_target_path(venv, debug=debug)
    if str(target) not in sys.path:
        sys.path.insert(0, str(target))
    if debug: dprint(f'sys.path: {sys.path}', color=color)
    return True

def venv_exec(code: str, venv: str = 'mrsm', debug: bool = False) -> bool:
    """
    Execute Python code in a subprocess via a virtual environment's interpeter.

    Return True if the code successfully executes, False on failure.
    """
    import subprocess, sys
    from meerschaum.config._paths import VIRTENV_RESOURCES_PATH
    executable = (
        sys.executable if venv is None
        else os.path.join(
            VIRTENV_RESOURCES_PATH, venv, (
                'bin' if platform.system() != 'Windows' else 'Scripts'
            ), 'python'
        )
    )
    return subprocess.call([executable, '-c', code]) == 0

def get_pip(debug : bool = False) -> bool:
    """
    Download and run the get-pip.py script.
    """
    import sys, subprocess
    from meerschaum.utils.misc import wget
    from meerschaum.config._paths import CACHE_RESOURCES_PATH
    from meerschaum.config.static import _static_config
    url = _static_config()['system']['urls']['get-pip.py']
    dest = CACHE_RESOURCES_PATH / 'get-pip.py'
    try:
        wget(url, dest, color=False, debug=debug)
    except Exception as e:
        print(f"Failed to fetch pip from '{url}'. Please install pip and restart Meerschaum.") 
        sys.exit(1)
    cmd_list = [sys.executable, str(dest)] 
    return subprocess.call(cmd_list) == 0

def pip_install(
        *packages: List[str],
        args: List[str] = ['--upgrade'],
        venv: str = 'mrsm',
        deactivate: bool = True,
        split : bool = True,
        check_update : bool = True,
        check_wheel : bool = True,
        color : bool = True,
        debug: bool = False
    ) -> bool:
    """
    Install pip packages
    """
    from meerschaum.config.static import _static_config
    try:
        from meerschaum.utils.formatting import ANSI, UNICODE
    except ImportError:
        ANSI, UNICODE = False, False
    if check_wheel:
        try:
            import wheel
            have_wheel = True
        except:
            have_wheel = False
    _args = list(args)
    try:
        if venv is not None:
            activate_venv(venv=venv, color=color, debug=debug)
        import pip
        have_pip = True
        if venv is not None and deactivate: deactivate_venv(venv=venv, debug=debug, color=color)
    except ImportError:
        have_pip = False
    if not have_pip:
        try:
            import ensurepip
        except ImportError:
            ensurepip = None
        if ensurepip is None:
            if not get_pip(debug=debug):
                import sys
                print(
                    "Failed to import pip and ensurepip. Please install pip and restart Meerschaum.\n\n" +
                    "You can find instructions on installing pip here: https://pip.pypa.io/en/stable/installing/"
                )
                sys.exit(1)
        else:
            ensurepip.bootstrap(upgrade=True, )
        import pip
    if venv is not None:
        activate_venv(venv=venv, debug=debug, color=color)
        if '--ignore-installed' not in args and '-I' not in _args:
            _args += ['--ignore-installed']

    ### NOTE: Added pip to be checked on each install. Too much?
    if check_update and need_update(pip, debug=debug):
        _args.append('pip')
    _args = ['install'] + _args

    if check_wheel:
        if not have_wheel:
            _args.append('wheel')

    if not ANSI and '--no-color' not in _args:
        _args.append('--no-color')

    if '--no-warn-conflicts' not in _args:
        _args.append('--no-warn-conflicts')

    if '--disable-pip-version-check' not in _args:
        _args.append('--disable-pip-version-check')

    #  if venv is not None and '--user' not in _args:
        #  _args.append('--user')
    if venv is not None and '--target' not in _args and '-t' not in _args:
        _args += ['--target', venv_target_path(venv, debug=debug)]
    elif (
        '--target' not in _args
            and '-t' not in _args
            and os.environ.get(
                _static_config()['environment']['runtime'], None
            ) != 'docker'
            and not inside_venv()
    ):
        _args += ['--user']
    if '--progress-bar' in _args:
        _args.remove('--progress-bar')
    if UNICODE:
        _args += ['--progress-bar', 'pretty']
    else:
        _args += ['--progress-bar', 'ascii']
    if debug:
        if '-v' not in _args or '-vv' not in _args or '-vvv' not in _args:
            pass
            #  _args.append('-v')
    else:
        if '-q' not in _args or '-qq' not in _args or '-qqq' not in _args:
            pass
            #  _args.append('-q')


    _packages = []
    for p in packages:
        root_name = p.split('.')[0] if split else p
        install_name = all_packages.get(root_name, root_name)
        _packages.append(install_name)

    msg = f"Installing packages:"
    for p in _packages:
        msg += f'\n  - {p}'
    print(msg)

    #  _imap_args = []
    #  for p in _packages:
        #  _imap_args.append(('pip', _args + [p], venv, debug))
    #  print(_imap_args)

    #  from meerschaum.utils.pool import get_pool

    #  from multiprocessing import cpu_count
    #  pool = get_pool('ThreadPool', max(len(_imap_args), cpu_count()))
    #  help(pool)
    #  results = pool.starmap(run_python_package, _imap_args)
    #  pool.join()
    #  pool.close()
    #  success = sum(results) == 0


    success = run_python_package('pip', _args + _packages, venv=venv, debug=debug, color=color) == 0
    if venv is not None and deactivate:
        deactivate_venv(venv=venv, debug=debug, color=color)
    msg = "Successfully installed packages." if success else "Failed to install packages."
    print(msg)
    if debug: print('pip install returned:', success)
    return success

def run_python_package(
        package_name : str,
        args : list = [],
        venv : Optional[str] = None,
        cwd : Optional[str] = None,
        color : bool = False,
        debug : bool = False
    ) -> int:
    """
    Runs an installed python package.
    E.g. Translates to `/usr/bin/python -m [package]`
    """
    import sys, os
    from subprocess import call
    from meerschaum.config._paths import VIRTENV_RESOURCES_PATH
    old_cwd = os.getcwd()
    if cwd is not None:
        os.chdir(cwd)
    executable = (
        sys.executable if venv is None
        else os.path.join(
            VIRTENV_RESOURCES_PATH, venv, (
                'bin' if platform.system() != 'Windows' else 'Scripts'
            ), ('python' + ('.exe' if platform.system() == 'Windows' else ''))
        )
    )
    command = [executable, '-m', str(package_name)] + [str(a) for a in args]
    if debug:
        print(command, file=sys.stderr)
    try:
        rc = call(command)
    except KeyboardInterrupt:
        rc = 1
    os.chdir(old_cwd)
    return rc

def attempt_import(
        *names: List[str],
        lazy: bool = True,
        warn: bool = True,
        install: bool = True,
        venv: str = 'mrsm',
        precheck: bool = True,
        split: bool = True,
        check_update : bool = False,
        deactivate : bool = True,
        color : bool = True,
        debug: bool = False
    ) -> Union['ModuleType', Tuple['ModuleType']]:
    """
    Raise a warning if packages are not installed; otherwise import and return modules.
    If lazy = True, return lazy-imported modules.

    Returns tuple of modules if multiple names are provided, else returns one module.

    Examples:

        ```
        >>> pandas, sqlalchemy = attempt_import('pandas', 'sqlalchemy')
        >>> pandas = attempt_import('pandas')

        ```

    :param names:
        The packages to be imported.

    :param lazy:
        If True, lazily load packages.
        Defaults to False.

    :param warn:
        If True, raise a warning if a package cannot be imported.
        Defaults to True.

    :param install:
        If True, attempt to install a missing package into the designated virtual environment.
        If `check_update` is True, install updates if available.
        Defaults to True.

    :param venv:
        The virtual environment in which to search for packages and to install packages into.
        Defaults to 'mrsm'.

    :param precheck:
        If True, attempt to find module before importing (necessary for checking if modules exist
        and retaining lazy imports), otherwise assume lazy is False.
        Defaults to True.        

    :param split:
        If True, split packages' names on '.'.
        Defaults to True.

    :param check_update:
        If True, check PyPI for the most recent version.
        If `install` is True, install updates if available.
        Defaults to False.

    """

    ### to prevent recursion, check if parent Meerschaum package is being imported
    if names == ('meerschaum',):
        return _import_module('meerschaum')

    if venv == 'mrsm' and _import_hook_venv is not None:
        if debug: f"Import hook for virtual environmnt '{_import_hook_venv}' is active."
        venv = _import_hook_venv

    if venv is not None: activate_venv(venv=venv, color=color, debug=debug)
    _warnings = _import_module('meerschaum.utils.warnings')
    warn_function = _warnings.warn

    def do_import(_name: str, **kw):
        #  is_venv_active(venv, debug=debug)
        if venv is not None: activate_venv(venv=venv, debug=debug)
        ### determine the import method (lazy vs normal)
        from meerschaum.utils.misc import filter_keywords
        import_method = _import_module if not lazy else lazy_import
        try:
            mod = import_method(_name, **(filter_keywords(import_method, **kw)))
        except Exception as e:
            if warn:
                warn_function(
                    f"Failed to import module '{_name}'.\nException:\n{e}",
                    ImportWarning,
                    stacklevel = (5 if lazy else 4),
                    color = False,
                )
            mod = None
        if venv is not None: deactivate_venv(venv=venv, color=color, debug=debug)
        return mod

    modules = []
    for name in names:
        ### Enforce virtual environment (something is deactivating in the loop so check each pass).
        if venv is not None: activate_venv(debug=debug)
        ### Check if package is a declared dependency.
        root_name = name.split('.')[0] if split else name
        install_name = all_packages.get(root_name, None)
        if install_name is None:
            install_name = root_name
            if warn:
                warn_function(
                    f"Package '{root_name}' is not declared in meerschaum.utils.packages.",
                    ImportWarning,
                    stacklevel = 3,
                    color = color
                )

        ### Determine if the package exists.
        if precheck is False:
            found_module = do_import(name, debug=debug, warn=False, venv=venv, color=color) is not None
        else:
            try:
                found_module = (importlib.util.find_spec(name) is not None)
            except ModuleNotFoundError as e:
                found_module = False

        if not found_module:
            if install:
                ### NOTE: pip_install deactivates venv, so deactivate must be False.
                if not pip_install(
                    root_name,
                    venv = venv,
                    deactivate = False,
                    split = False,
                    #  split = split,
                    check_update = check_update,
                    color = color,
                    debug = debug
                ) and warn:
                    warn_function(
                        f"Failed to install '{install_name}'.",
                        ImportWarning,
                        stacklevel = 3,
                        color = color
                    )
            elif warn:
                ### Raise a warning if we can't find the package and install = False.
                warn_function(
                    (f"\n\nMissing package '{name}'; features will not work correctly. "
                     f"\n\nSet install=True when calling attempt_import.\n"),
                    ImportWarning,
                    stacklevel = 3,
                    color = color
                )

        ### Do the import. Will be lazy if lazy=True.
        m = do_import(name, debug=debug, warn=warn, venv=venv, color=color)
        modules.append(m)

        ### Check for updates (skip this by default)
        if check_update:
            if need_update(m, split=split, debug=debug):
                if install:
                    if not pip_install(
                        root_name,
                        venv = venv,
                        split = False,
                        #  split = split,
                        deactivate = False,
                        check_update = check_update,
                        color = color,
                        debug = debug
                    ) and warn:
                        warn_function(
                            f"There's an update available for '{install_name}', " +
                            "but it failed to install. " +
                            "Try install via Meershaum with `install packages '{install_name}'`.",
                            ImportWarning,
                            stacklevel = 3,
                            color = color
                        )
                elif warn:
                    warn_function(
                        f"There's an update available for '{m.__name__}'.",
                        stack = False,
                        color = color
                    )
    if venv is not None and deactivate:
        deactivate_venv(venv=venv, debug=debug, color=color)

    modules = tuple(modules)
    if len(modules) == 1: return modules[0]
    return modules

def lazy_import(
        name: str,
        local_name: str = None,
        venv : Optional[str] = None,
        warn : bool = True, 
        deactivate : bool = True,
        debug : bool = False
    ) -> meerschaum.utils.packages.lazy_loader.LazyLoader:
    """
    Lazily import a package
    Uses the tensorflow LazyLoader implementation (Apache 2.0 License)
    """
    from meerschaum.utils.packages.lazy_loader import LazyLoader
    if local_name is None:
        local_name = name
    return LazyLoader(
        local_name,
        globals(),
        name,
        venv = venv,
        warn = warn,
        deactivate = deactivate,
        debug = debug
    )

def import_pandas() -> 'ModuleType':
    """
    Quality-of-life function to attempt to import the configured version of pandas
    """
    from meerschaum.config import get_config
    pandas_module_name = get_config('system', 'connectors', 'all', 'pandas', patch=True)
    ### NOTE: modin does NOT currently work!
    if pandas_module_name == 'modin':
        pandas_module_name = 'modin.pandas'
    return attempt_import(pandas_module_name)

def import_rich(lazy: bool = True, **kw) -> 'ModuleType':
    """
    Quality of life function for importing rich.
    """
    from meerschaum.utils.formatting import ANSI, UNICODE
    if not ANSI and not UNICODE:
        return None

    ## need typing_extensions for `from rich import box`
    typing_extensions = attempt_import('typing_extensions', lazy=False)
    pygments = attempt_import('pygments', lazy=False)
    return attempt_import('rich', lazy=lazy, **kw)

def get_modules_from_package(
        package: 'package',
        names: bool = False,
        recursive: bool = False,
        lazy: bool = False,
        modules_venvs: bool = False,
        debug: bool = False
    ):
    """
    Find and import all modules in a package.

    Returns: either list of modules or tuple of lists

    names = False (default) : modules
    names = True            : (__all__, modules)
    """
    from os.path import dirname, join, isfile, isdir, basename
    import glob

    pattern = '*' if recursive else '*.py'
    module_names = glob.glob(join(dirname(package.__file__), pattern), recursive=recursive)
    _all = [
        basename(f)[:-3] if isfile(f) else basename(f)
        for f in module_names
        if ((isfile(f) and f.endswith('.py')) or isdir(f))
           and not f.endswith('__init__.py')
           and not f.endswith('__pycache__')
    ]

    if debug:
        from meerschaum.utils.debug import dprint
        dprint(str(_all))
    modules = []
    for module_name in [package.__name__ + "." + mod_name for mod_name in _all]:
        ### there's probably a better way than a try: catch but it'll do for now
        try:
            ### if specified, activate the module's virtual environment before importing.
            ### NOTE: this only considers the filename, so two modules from different packages
            ### may end up sharing virtual environments.
            if modules_venvs:
                activate_venv(module_name.split('.')[-1], debug=debug)
            m = lazy_import(module_name, debug=debug) if lazy else _import_module(module_name)
            modules.append(m)
        except Exception as e:
            if debug: dprint(e)
            pass
        finally:
            if modules_venvs:
                deactivate_venv(module_name.split('.')[-1], debug=debug)
    if names:
        return _all, modules

    return modules


def import_children(
        package: Optional['ModuleType'] = None,
        package_name: Optional[str] = None,
        types: List[str] = ['method', 'builtin', 'function', 'class', 'module'],
        lazy: bool = True,
        recursive: bool = False,
        debug: bool = False
    ) -> List['ModuleType']:
    """
    Import all functions in a package to its __init__.
    Returns of list of modules.

    :param package:
        Package to import its functions into.
        If None (default), use parent.

    :param package_name:
        Name of package to import its functions into
        If None (default), use parent.

    :param types:
        Types of members to return.
        Default : ['method', 'builtin', 'class', 'function', 'package', 'module']

    """
    import sys, inspect

    ### if package_name and package are None, use parent
    if package is None and package_name is None:
        package_name = inspect.stack()[1][0].f_globals['__name__']

    ### populate package or package_name from other other
    if package is None:
        package = sys.modules[package_name]
    elif package_name is None:
        package_name = package.__name__

    ### Set attributes in sys module version of package.
    ### Kinda like setting a dictionary
    ###   functions[name] = func
    modules = get_modules_from_package(package, recursive=recursive, lazy=lazy, debug=debug)
    _all, members = [], []
    objects = []
    for module in modules:
        _objects = []
        for ob in inspect.getmembers(module):
            for t in types:
                ### ob is a tuple of (name, object)
                if getattr(inspect, 'is' + t)(ob[1]):
                    _objects.append(ob)

        if 'module' in types:
            _objects.append((module.__name__.split('.')[0], module))
        objects += _objects
    for ob in objects:
        setattr(sys.modules[package_name], ob[0], ob[1])
        _all.append(ob[0])
        members.append(ob[1])

    if debug:
        from meerschaum.utils.debug import dprint
        dprint(str(_all))
    ### set __all__ for import *
    setattr(sys.modules[package_name], '__all__', _all)
    return members


def reload_package(
        package: str,
        lazy: bool = False,
        debug: bool = False,
        **kw: Any
    ) -> 'ModuleType':
    """
    Recursively load a package's subpackages, even if they were not previously loaded
    """
    import pydoc
    if isinstance(package, str):
        package_name = package
    else:
        try:
            package_name = package.__name__
        except:
            package_name = str(package)
    return pydoc.safeimport(package_name, forceload=1)
    #  import os, types, importlib, sys
    #  assert (hasattr(package, "__package__"))
    #  fn = package.__file__
    #  fn_dir = os.path.dirname(fn) + os.sep
    #  module_visit = {fn}
    #  del fn

    #  def reload_recursive_ex(module):
        #  import os, types, importlib
        #  from meerschaum.utils.debug import dprint
        #  ### forces import of lazily-imported modules
        #  del sys.modules[module.__name__]
        #  module = __import__(module.__name__)
        #  module = _import_module(module.__name__)
        #  _module = importlib.reload(module)
        #  sys.modules[module.__name__] = _module

        #  for module_child in get_modules_from_package(module, recursive=True, lazy=lazy):
            #  if isinstance(module_child, types.ModuleType) and hasattr(module_child, '__name__'):
                #  fn_child = getattr(module_child, "__file__", None)
                #  if (fn_child is not None) and fn_child.startswith(fn_dir):
                    #  if fn_child not in module_visit:
                        #  if debug: dprint(f"reloading: {fn_child} from {module}")
                        #  module_visit.add(fn_child)
                        #  reload_recursive_ex(module_child)

    #  return reload_recursive_ex(package)


def is_installed(
        name: str,
        venv : Optional[str] = None,
    ) -> bool:
    """
    Check whether a package is installed.
    name : str
        Name of the package in question
    """
    import importlib.util
    if venv is not None: activate_venv(venv=venv)
    found = importlib.util.find_spec(name) is not None
    if venv is None:
        return found
    mod = attempt_import(name, venv=venv)
    found = (venv == package_venv(mod))
    deactivate_venv(venv=venv)
    return found

def venv_contains_package(name : str, venv : str = None) -> bool:
    """
    Search the contents of a virtual environment for a package.
    """
    import os
    if venv is None:
        return is_installed(name, venv=venv)
    vtp = venv_target_path(venv)
    if not vtp.exists(): return False
    return name in os.listdir(venv_target_path(venv))

### NOTE: this is at the bottom to avoid import problems
#  from meerschaum.utils.packages._ImportHook import install

from meerschaum.utils.warnings import warn
from importlib.machinery import PathFinder


class ImportHook(PathFinder):
    def __init__(self, venv: str = None, debug: bool = False):
        self.venv = venv
        self.debug = debug

    #  def __del__(self):
    #  deactivate_venv(self.venv, debug=self.debug)

    def create_module(self, spec):
        print(spec)

    def exec_module(self, module):
        print(module)

    def find_spec(self, fullname, path=None, target=None):
        if self.venv is not None and self.venv not in active_venvs:
            activate_venv(self.venv, debug=False)
        result = super(ImportHook, self).find_spec(fullname, path, target)
        #  try:
        #  __import__(fullname)
        #  except Exception as e:
        #  print(str(e))
        if result is None and path is None and target is None:
            if not fullname in sys.builtin_module_names:
                warn(fullname, stacklevel=3)
                pip_install(fullname, venv=self.venv, debug=self.debug)
            #  pass
            #  #  attempt_import(fullname, debug=True, venv=self.venv, precheck=False)
        #  if self.venv is not None:
        #  deactivate_venv(self.venv, debug=False)
        return result


def install_import_hook(venv: str = 'mrsm', debug: bool = False) -> bool:
    global _import_hook_venv
    if debug:
        from meerschaum.utils.debug import dprint
    from meerschaum.utils.warnings import warn
    if _import_hook_venv is not None and _import_hook_venv != venv:
        if venv != 'mrsm':
            warn(
                f"Virtual environment '{_import_hook_venv}' was set as the import hook " +
                f"but is being overwritten by '{venv}'.", stacklevel=4
            )
        else:
            if debug:
                dprint(f"_import_hook_venv is '{_import_hook_venv}', " +
                       "attempted to install venv '{venv}'. " +
                       "Uninstall import hook before installing '{venv}'."
                       )
            return False
    if debug: dprint(f"Installing import hook for virtual environment '{venv}'...")
    importlib.import_module = attempt_import
    _import_hook_venv = venv
    found_hook = False
    for finder in sys.meta_path:
        if isinstance(finder, ImportHook) and finder.venv == venv:
            found_hook = True
            break
    if not found_hook:
        sys.meta_path.insert(0, ImportHook(venv, debug=True))

    return True


def uninstall_import_hook(venv: str = 'mrsm', all_hooks: bool = False, debug: bool = False) -> bool:
    global _import_hook_venv
    if debug:
        from meerschaum.utils.debug import dprint
        dprint(f"Uninstalling import hook (was set to {_import_hook_venv})...")
    importlib.import_module = _import_module
    _import_hook_venv = None
    return True
    new_meta_path, to_delete = [], []
    for finder in sys.meta_path:
        if (
                not isinstance(finder, ImportHook) or (
                isinstance(finder, ImportHook) and not all_hooks and finder.venv != venv
        )
        ):
            new_meta_path.append(finder)
        else:
            to_delete.append(finder)
    sys.meta_path = new_meta_path
    del to_delete[:]

    return True

def venv_target_path(venv : str, debug : bool = False) -> pathlib.Path:
    """
    Return a virtual environment's site-package path.
    """
    import os, sys, platform, pathlib
    from meerschaum.config._paths import VIRTENV_RESOURCES_PATH

    venv_root_path = str(os.path.join(VIRTENV_RESOURCES_PATH, venv))
    target_path = venv_root_path

    ### Ensure 'lib' or 'Lib' exists.
    lib = 'lib' if platform.system() != 'Windows' else 'Lib'
    if lib not in os.listdir(venv_root_path):
        print(f"Failed to find lib directory for virtual environment '{venv}'.")
        sys.exit(1)
    target_path = os.path.join(target_path, lib)

    ### Check if a 'python3.x' folder exists.
    python_folder = 'python' + str(sys.version_info.major) + '.' + str(sys.version_info.minor)
    if python_folder in os.listdir(target_path): ### Linux
        target_path = os.path.join(target_path, python_folder)

    ### Ensure 'site-packages' exists.
    if 'site-packages' in os.listdir(target_path): ### Windows
        target_path = os.path.join(target_path, 'site-packages')
    else:
        from meerschaum.config._paths import set_root
        import traceback
        traceback.print_stack()
        print(f"Failed to find site-packages directory for virtual environment '{venv}'.")
        sys.exit(1)

    if debug:
        print(f"Target path for virtual environment '{venv}':\n" + str(target_path))
    return pathlib.Path(target_path)

def package_venv(package : 'ModuleType') -> Optional[str]:
    """
    Inspect a package and return the virtual environment in which it presides.
    """
    import os
    from meerschaum.config._paths import VIRTENV_RESOURCES_PATH
    if str(VIRTENV_RESOURCES_PATH) not in package.__file__:
        return None
    return package.__file__.split(str(VIRTENV_RESOURCES_PATH))[1].split(os.path.sep)[1]

def inside_venv() -> bool:
    """
    Determine whether current Python interpreter is running inside a virtual environment.
    """
    import sys
    return (
        hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix')
                and sys.base_prefix != sys.prefix
        )
    )

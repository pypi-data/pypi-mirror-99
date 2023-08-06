# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
This module is the entry point for the interactive shell
"""

from __future__ import annotations
from meerschaum.utils.typing import Union, SuccessTuple, Any, Callable, Optional, List

import sys, inspect
from meerschaum.utils.packages import attempt_import
from meerschaum.config import __doc__, __version__ as version, get_config
cmd = attempt_import(get_config('shell', 'cmd', patch=True), warn=False, lazy=False)
if cmd is None or isinstance(cmd, dict):
    cmd = attempt_import('cmd', lazy=False, warn=False)
prompt_toolkit = attempt_import('prompt_toolkit', lazy=False, warn=False, install=True)
from meerschaum.actions.shell.ValidAutoSuggest import ValidAutoSuggest
from meerschaum.actions.shell.ShellCompleter import ShellCompleter
_clear_screen = get_config('shell', 'clear_screen', patch=True)
from meerschaum.connectors.parse import parse_instance_keys
from meerschaum.utils.misc import string_width
### readline is Unix-like only. Disable readline features for Windows
try:
    import readline
except ImportError:
    readline = None

patch = True
### remove default cmd2 commands
commands_to_remove = {
    'alias',
    'macro',
    'run_pyscript',
    'run_script',
    'shell',
    'pyscript',
    #  'set',
    'py',
    'shortcuts',
    'history',
    'load',
}
### cmd2 only: hide commands
hidden_commands = {
    #  'macro',
    #  'alias',
    'sh',
    'pass',
    'exit',
    'quit',
    'eof',
    'exit',
    '_relative_run_script',
    'ipy',
}
reserved_completers = {
    'instance', 'repo'
}

def _insert_shell_actions(
        shell : Optional['Shell'] = None,
        actions : Optional[Dict[str, Callable[[Any], SuccessTuple]]] = None,
        keep_self = False,
    ) -> None:
    """
    Update the Shell with Meerschaum actions.
    """
    from meerschaum.utils.misc import add_method_to_class
    import meerschaum.actions.shell as shell_pkg
    from meerschaum.actions import get_completer
    if actions is None:
        from meerschaum.actions import actions

    _shell = shell if shell is not None else shell_pkg.Shell

    for a, f in actions.items():
        add_method_to_class(
            func = f,
            class_def = _shell,
            method_name = 'do_' + a,
        )
        if a not in reserved_completers:
            _completer = get_completer(a)
            if _completer is None:
                _completer = shell_pkg.default_action_completer
            completer = _completer_wrapper(_completer)
            setattr(_shell, 'complete_' + a, completer)

def _completer_wrapper(
        target : Callable[[Any], List[str]]
    ) -> Callable['meerschaum.actions.shell.Shell', str, str, int, int]:
    """
    Wrapper for `complete_` functions so they can instead use Meerschaum arguments.
    """
    from functools import wraps

    ### I have no idea why I had to remove `self`.
    ### Maybe it has to do with adding to an object instead of a class.
    @wraps(target)
    def wrapper(text, line, begin_index, end_index):
        _check_keys = _check_complete_keys(line)
        if _check_keys is not None:
            return _check_keys

        from meerschaum.actions.arguments._parse_arguments import parse_line
        args = parse_line(line)
        if target.__name__ != 'default_action_completer':
            if len(args['action']) > 0:
                del args['action'][0]
        args['text'] = text
        args['line'] = line
        args['begin_index'] = begin_index
        args['end_index'] = end_index
        return target(**args)

    return wrapper

def default_action_completer(
        text : Optional[str] = None,
        line : Optional[str] = None,
        begin_index : Optional[int] = None,
        end_index : Optional[int] = None,
        action : List[str] = [],
        **kw : Any
    ) -> List[str]:
    """
    Search for subactions by default. This may be overridden by each action.
    """
    from meerschaum.actions import get_subactions
    subactions = get_subactions(action[0]) if len(action) > 0 else {}
    sub = action[1] if len(action) > 1 else ''
    possibilities = []
    for sa in subactions:
        if sa.startswith(sub) and sa != sub:
            possibilities.append(sa)
    return sorted(possibilities)

def _check_complete_keys(
        line : str
    ) -> Optional[List[str]]:
    from meerschaum.actions.arguments._parser import parser, get_arguments_triggers
    from meerschaum.actions.arguments._parse_arguments import parse_line

    ### TODO Add all triggers
    trigger_args = {
        '-c' : 'connector_keys',
        '--connector-keys' : 'connector_keys',
        '-r' : 'repository',
        '--repository' : 'repository',
        '-i' : 'mrsm_instance',
        '--instance' : 'mrsm_instance',
        '--mrsm-instance' : 'mrsm_instance',
    }


    ### TODO Find out arg possibilities
    possibilities = []
    #  last_word = line.split(' ')[-1]
    last_word = line.rstrip(' ').split(' ')[-1]

    if last_word.startswith('-'):
        for _arg, _triggers in get_arguments_triggers().items():
            for _trigger in _triggers:
                if _trigger.startswith(last_word):
                    #  and _trigger != last_word
                    if _trigger != last_word or not line.endswith(' '):
                        possibilities.append(_trigger)
        if not line.endswith(' '):
            return possibilities

    #  print()
    #  print(last_word)
    #  print(len(line.split(' ')[-1]))
    #  print()

    if last_word.startswith('-') and not last_word.endswith('-'):
        if line.endswith(' ') and last_word in trigger_args:
            is_trigger = True
        elif line.endswith(' '):
            ### return empty list so we don't try to parse an incomplete line.
            #  print('ABORT')
            return []

    from meerschaum.utils.misc import get_connector_labels

    if last_word.rstrip(' ') in trigger_args:
        return get_connector_labels()

    for trigger, var in trigger_args.items():
        if trigger in line:
            ### check if any text has been entered for the key
            if line.rstrip(' ').endswith(trigger):
                return get_connector_labels()

            #  args = parse_line(line.rstrip(' '))
            #  search_term = args[var] if var != 'connector_keys' else args[var][0]
            return get_connector_labels(search_term=last_word.rstrip(' '))

    return None

class Shell(cmd.Cmd):
    def __init__(self, actions : dict = {}, sysargs : list = []):
        """
        Customize the CLI from configuration
        """
        _insert_shell_actions(shell=self, keep_self=True)
        try:
            delattr(cmd.Cmd, '_alias_create')
            delattr(cmd.Cmd, '_alias_delete')
            delattr(cmd.Cmd, '_alias_list')
            delattr(cmd.Cmd, '_macro_create')
            delattr(cmd.Cmd, '_macro_delete')
            delattr(cmd.Cmd, '_macro_list')
        except AttributeError:
            pass

        from meerschaum.config._paths import SHELL_HISTORY_PATH
        self.session = prompt_toolkit.shortcuts.PromptSession(
            history = prompt_toolkit.history.FileHistory(str(SHELL_HISTORY_PATH)),
            auto_suggest = ValidAutoSuggest(),
            completer = ShellCompleter(),
            complete_while_typing = True,
        )

        try: ### try cmd2 arguments first
            super().__init__(
                allow_cli_args = False,
                auto_load_commands = False,
                persistent_history_length = 1000,
                persistent_history_file = None,
            )
            _init = True
        except: ### fall back to default init (cmd)
            _init = False
        
        if not _init:
            #  try:
            super().__init__()
            #  except Exception as e:
                #  print(e)
                #  sys.exit(1)

        ### remove default commands from the Cmd class
        for command in commands_to_remove:
            try:
                delattr(cmd.Cmd, f'do_{command}')
                #  self.disable_command(command)
            except:
                pass

        ### NOTE: custom actions must be added to the self._actions dictionary
        self._actions = actions
        self._sysargs = sysargs
        self._actions['instance'] = self.do_instance
        self._actions['repo'] = self.do_repo
        self._actions['debug'] = self.do_debug
        self.debug = False
        self.load_config()
        self.hidden_commands = []
        ### update hidden commands list (cmd2 only)
        try:
            for c in hidden_commands:
                self.hidden_commands.append(c)
        except Exception as e:
            pass

    def load_config(self, instance : str = None):
        """
        Set attributes from the shell configuration.
        """
        from meerschaum.utils.misc import remove_ansi
        from meerschaum.utils.formatting import CHARSET, ANSI, UNICODE, colored
        
        if self.__dict__.get('intro', None) != '':
            self.intro = get_config('shell', CHARSET, 'intro', patch=patch)
            self.intro += '\n' + ''.join(
                [' '
                    for i in range(
                        string_width(self.intro) - len('v' + version)
                    )
                ]
            ) + 'v' + version
        else:
            self.intro = ""
        self._prompt = get_config('shell', CHARSET, 'prompt', patch=patch)
        self.prompt = self._prompt
        self.ruler = get_config('shell', CHARSET, 'ruler', patch=patch)
        self.close_message = get_config('shell', CHARSET, 'close_message', patch=patch)
        self.doc_header = get_config('shell', CHARSET, 'doc_header', patch=patch)
        self.undoc_header = get_config('shell', CHARSET, 'undoc_header', patch=patch)

        if instance is None and self.__dict__.get('instance_keys', None) is None:
            ### create default instance and repository connectors
            self.instance_keys = remove_ansi(get_config('meerschaum', 'instance', patch=patch))
            ### self.instance is a stylized version of self.instance_keys
            self.instance = str(self.instance_keys)
        else:
            self.instance = instance
            self.instance_keys = remove_ansi(str(instance))
        if self.__dict__.get('repo_keys', None) is None:
            self.repo_keys = get_config('meerschaum', 'default_repository', patch=patch)
        ### this will be updated later in update_prompt ONLY IF {username} is in the prompt
        self.username = ''

        if ANSI:
            def apply_colors(attr, key):
                return colored(
                    attr,
                    *get_config('shell', 'ansi', key, 'color', patch=patch)
                )

            for attr_key in get_config('shell', 'ansi', patch=patch):
                self.__dict__[attr_key] = apply_colors(self.__dict__[attr_key], attr_key)

        ### refresh actions
        _insert_shell_actions(shell=self, keep_self=True)

        ### replace {instance} in prompt with stylized instance string
        self.update_prompt()

    def insert_actions(self):
        from meerschaum.actions import actions

    def update_prompt(self, instance=None, username=None):
        from meerschaum.config import get_config
        from meerschaum.utils.formatting import ANSI, colored
        prompt = self._prompt
        mask = prompt
        if '{instance}' in self._prompt:
            if instance is None: instance = self.instance_keys
            self.instance = instance
            if ANSI: self.instance = colored(self.instance, *get_config('shell', 'ansi', 'instance', 'color', patch=True))
            prompt = prompt.replace('{instance}', self.instance)
            mask = mask.replace('{instance}', ''.join(['\0' for c in '{instance}']))

        if '{username}' in self._prompt:
            if username is None:
                from meerschaum.utils.misc import remove_ansi
                try:
                    username = parse_instance_keys(remove_ansi(self.instance_keys), construct=False)['username']
                except KeyError:
                    username = '(no username)'
                except Exception as e:
                    username = str(e)
            self.username = (
                username if not ANSI else
                colored(username, *get_config('shell', 'ansi', 'username', 'color', patch=True))
            )
            prompt = prompt.replace('{username}', self.username)
            mask = mask.replace('{username}', ''.join(['\0' for c in '{username}']))

        remainder_prompt = list(self._prompt)
        for i, c in enumerate(mask):
            if c != '\0':
                _c = c
                if ANSI: _c = colored(_c, *get_config('shell', 'ansi', 'prompt', 'color', patch=True))
                remainder_prompt[i] = _c
        self.prompt = ''.join(remainder_prompt).replace('{username}', self.username).replace('{instance}', self.instance)
        ### flush stdout
        print("", end="", flush=True)

    def precmd(self, line):
        """
        Pass line string to parent actions.
        Pass parsed arguments to custom actions

        Overrides `default`: if action does not exist,
            assume the action is `shell`
        """
        ### make a backup of line for later
        import copy
        original_line = copy.deepcopy(line)

        ### cmd2 support: check if command exists
        try:
            command = line.command
            line = str(command) + (' ' + str(line) if len(str(line)) > 0 else '')
        except Exception:
            ### we're probably running the original cmd, not cmd2
            command = None
            line = str(line)

        ### if the user specifies, clear the screen before executing any commands
        if _clear_screen:
            from meerschaum.utils.formatting._shell import clear_screen
            clear_screen(debug=self.debug)

        ### return blank commands (spaces break argparse)
        if original_line is None or len(str(line).strip()) == 0:
            return original_line

        if line in {
            'exit',
            'quit',
            'EOF',
        }:
            return "exit"
        ### help shortcut
        help_token = '?'
        if line.startswith(help_token):
            return "help " + line[len(help_token):]

        ### first things first: save history BEFORE execution
        #  from meerschaum.config._paths import SHELL_HISTORY_PATH
        #  if readline:
            #  readline.set_history_length(get_config('shell', 'max_history', patch=patch))
            #  readline.write_history_file(SHELL_HISTORY_PATH)

        ### TODO Migrate to using entry for everything instead of replicating entry inside precmd.
        #  from meerschaum.actions._entry import entry
        #  from meerschaum.actions.arguments._parser import get_arguments_triggers
        #  import shlex
        #  _sysargs = shlex.split(line)
        #  _avail_args = get_arguments_triggers()
        #  for a, _triggers in _avail_args.items():
            #  if a == 'help'


        from meerschaum.actions.arguments import parse_line
        args = parse_line(line)
        if args['help']:
            from meerschaum.actions.arguments._parser import parse_help
            parse_help(args)
            return ""

        ### NOTE: pass `shell` flag in case actions need to distinguish between
        ###       being run on the command line and being run in the shell
        args['shell'] = True

        ### if debug is not set on the command line,
        ### default to shell setting
        if not args['debug']: args['debug'] = self.debug

        action = args['action'][0]

        ### if no instance is provided, use current shell default,
        ### but not for the 'api' command (to avoid recursion)
        if 'mrsm_instance' not in args and action != 'api':
            args['mrsm_instance'] = str(self.instance_keys)

        if 'repository' not in args and action != 'api':
            args['repository'] = str(self.repo_keys)

        ### parse out empty strings
        if action.strip("\"'") == '':
            self.emptyline()
            return ""

        try:
            func = getattr(self, 'do_' + action)
            #  func_param_kinds = inspect.signature(func).parameters.items()
        except AttributeError as ae:
            ### if function is not found, default to `shell`
            action = "sh"
            args['action'].insert(0, "sh")
            func = getattr(self, 'do_sh')
            #  func_param_kinds = inspect.signature(func).parameters.items()

        ### delete the first action
        ### e.g. 'show actions' -> ['actions']
        del args['action'][0]

        positional_only = (action not in self._actions)
        if positional_only:
            return original_line

        from meerschaum.utils.packages import activate_venv, deactivate_venv
        plugin_name = (
            self._actions[action].__module__.split('.')[-1] if self._actions[action].__module__.startswith('plugins.')
            else None
        )

        ### execute the meerschaum action
        ### and print the response message in case of failure
        from meerschaum.utils.formatting import print_tuple
        activate_venv(venv=plugin_name, debug=self.debug)
        try:
            response = func(**args)
        except Exception as e:
            if self.debug or args.get('debug', False):
                import traceback
                traceback.print_exception(type(e), e, e.__traceback__)
            response = False, f"Failed to execute '{func.__name__}' with exception:\n\n'{e}'.\n\nRun again with '--debug' to see a full stacktrace."
        deactivate_venv(venv=plugin_name, debug=self.debug)
        if isinstance(response, tuple):
            if not response[0] or self.debug:
                print()
                print_tuple(response, skip_common=self.debug)
                print()

        self.postcmd(False, "")

        return ""

    #  def postcmd(stop : bool = False, line : str = ""):
        #  pass

    def postcmd(self, stop : bool = False, line : str = ""):
        self.load_config(self.instance)
        if stop:
            return True

    def do_pass(self, line):
        """
        Do nothing.
        """
        pass

    #  def do_alias(self, line):
        #  pass

    #  def do_macro(self, line):
        #  pass

    def do_debug(self, action=[''], **kw):
        """
        Toggle the shell's debug mode.
        If debug = on, append `--debug` to all commands.

        Command: `debug {on/true | off/false}`
        Ommitting on / off will toggle the existing value.
        """
        from meerschaum.utils.warnings import info
        on_commands = {'on', 'true'}
        off_commands = {'off', 'false'}
        try:
            state = action[0]
        except IndexError:
            state = ''
        if state == '':
            self.debug = not self.debug
        elif state.lower() in on_commands: self.debug = True
        elif state.lower() in off_commands: self.debug = False
        else: info(f"Unknown state '{state}'. Ignoring...")

        info(f"Debug mode is {'on' if self.debug else 'off'}.")

    def do_instance(
            self,
            action : list = [''],
            debug : bool = False,
            **kw : Any
        ) -> SuccessTuple:
        """
        Temporarily set a default Meerschaum instance for the duration of the shell.
        The default instance is loaded from the Meerschaum configuraton file
          (at keys 'meerschaum:instance').

        You can change the default instance with `edit config`.

        Usage:
            instance {instance keys}

        Examples:
            ```
            ### reset to default instance
            instance

            ### set the instance to 'api:main'
            instance api

            ### set the instance to a non-default connector
            instance api:myremoteinstance
            ```

        Note that instances must be configured, be either API or SQL connections,
          and be accessible to this machine over the network.
        """
        from meerschaum import get_connector
        from meerschaum.config import get_config
        from meerschaum.connectors.parse import parse_instance_keys
        from meerschaum.utils.warnings import warn, info
        from meerschaum.utils.misc import remove_ansi

        try:
            instance_keys = action[0]
        except:
            instance_keys = ''
        if instance_keys == '':
            instance_keys = get_config('meerschaum', 'instance', patch=True)

        conn = parse_instance_keys(instance_keys, debug=debug)
        if conn is None or not conn:
            conn = get_connector(debug=debug)

        self.instance_keys = remove_ansi(str(conn))

        self.update_prompt(instance=str(conn))
        info(f"Default instance for the current shell: {conn}")
        return True, "Success"

    def complete_instance(self, text, line, begin_index, end_index):
        from meerschaum.utils.misc import get_connector_labels
        from meerschaum.actions.arguments._parse_arguments import parse_line
        args = parse_line(line)
        _text = args['action'][1] if len(args['action']) > 1 else ""
        return get_connector_labels('api', 'sql', search_term=_text, ignore_exact_match=True)

    def do_repo(
            self,
            action : list = [''],
            debug : bool = False,
            **kw : Any
        ) -> SuccessTuple:
        """
        Temporarily set a default Meerschaum repository for the duration of the shell.
        The default repository (mrsm.io) is loaded from the Meerschaum configuraton file
          (at keys 'meerschaum:default_repository').

        You can change the default repository with `edit config`.

        Usage:
            repo {API label}

        Examples:
            ### reset to default repository
            repo

            ### set the repo to 'api:main'
            repository api

            ### set the repository to a non-default repo
            repo myremoterepo

        Note that repositories are a subset of instances.
        """
        from meerschaum import get_connector
        from meerschaum.config import get_config
        from meerschaum.connectors.parse import parse_repo_keys
        from meerschaum.utils.warnings import warn, info

        try:
            repo_keys = action[0]
        except:
            repo_keys = ''
        if repo_keys == '': repo_keys = get_config('meerschaum', 'default_repository', patch=True)

        conn = parse_repo_keys(repo_keys, debug=debug)
        if conn is None or not conn:
            conn = get_connector('api', debug=debug)

        self.repo_keys = str(conn)

        info(f"Default repository for the current shell: {conn}")
        return True, "Success"

    def complete_repo(self, *args) -> List[str]:
        return self.complete_instance(*args)

    def do_help(self, line) -> List[str]:
        """
        Show help for Meerschaum actions.

        You can also view help for actions and subactions with `--help`.

        Examples:
        ```
        help show
        help show pipes
        show pipes --help
        show pipes -h
        ```
        """
        from meerschaum.actions import actions
        from meerschaum.actions.arguments._parser import parse_help
        from meerschaum.actions.arguments._parse_arguments import parse_line
        import textwrap
        args = parse_line(line)
        if len(args['action']) == 0:
            del args['action']
            self._actions['show'](['actions'], **args)
            return ""
        if args['action'][0] not in self._actions:
            try:
                print(textwrap.dedent(getattr(self, f"do_{args['action'][0]}").__doc__))
            except:
                print(f"No help on '{args['action'][0]}'.")
            return ""
        parse_help(args)
        return ""

    def complete_help(self, text, line, begin_index, end_index):
        """
        Autocomplete the `help` command.
        """
        import inspect
        from meerschaum.actions.arguments._parse_arguments import parse_line
        from meerschaum.actions import get_subactions
        from meerschaum.actions.shell import Shell as _Shell
        args = parse_line(line)
        if len(args['action']) > 0 and args['action'][0] == 'help':
            ### remove 'help'
            del args['action'][0]

        action = args['action'][0] if len(args['action']) > 0 else ""
        sub = args['action'][1] if len(args['action']) > 1 else ""
        possibilities = []

        ### Search for subactions
        if sub is not None:
            for sa in get_subactions(action):
                if sa.startswith(sub) and sa != sub:
                    possibilities.append(sa)
        
        ### We found subarguments. Stop looking here.
        if len(possibilities) > 0:
            return possibilities

        ### No subactions. We're looking for an action.
        for name, f in inspect.getmembers(_Shell):
            if not inspect.isfunction(f):
                continue
            #  print(name)
            if name.startswith(f'do_{action}') and name != f'do_{action}' and name.replace('do_', '') not in self.hidden_commands:
                possibilities.append(name.replace('do_', ''))
        return possibilities

    def do_exit(self, params) -> True:
        """
        Exit the Meerschaum shell.
        """
        return True

    def emptyline(self):
        """
        If the user specifies, clear the screen.
        """
        ### NOTE: The screen clearing is defined in the custom input below
        pass

    def preloop(self):
        import signal, os
        #  from meerschaum.config._paths import SHELL_HISTORY_PATH
        #  if SHELL_HISTORY_PATH.exists():
            #  if readline:
                #  readline.read_history_file(SHELL_HISTORY_PATH)
        """
        Patch builtin cmdloop with my own input (defined below)
        """
        old_input = cmd.__builtins__['input']
        cmd.__builtins__['input'] = input_with_sigint(old_input, self.session)
        #  sys.modules['readline'] = session
        #  help(cmd)

        ### if the user specifies, clear the screen before initializing the shell
        if _clear_screen:
            from meerschaum.utils.formatting._shell import clear_screen
            clear_screen(debug=self.debug)

        ### if sysargs are provided, skip printing the intro and execute instead
        if self._sysargs:
            self.intro = ""
            self.precmd(' '.join(self._sysargs))

    def postloop(self):
        #  from meerschaum.config._paths import SHELL_HISTORY_PATH
        #  if readline:
            #  readline.set_history_length(get_config('shell', 'max_history', patch=patch))
            #  readline.write_history_file(SHELL_HISTORY_PATH)
        print('\n' + self.close_message)

def input_with_sigint(_input, session):
    """
    Replace built-in `input()` with prompt_toolkit.prompt.
    """

    def _patched_input(*args):
        _args = []
        for a in args:
            try:
                _a = prompt_toolkit.formatted_text.ANSI(a)
            except:
                _a = a
            _args.append(_a)
        try:
            parsed = session.prompt(*_args)
            ### clear screen on empty input
            ### NOTE: would it be better to do nothing instead?
            if len(parsed.strip()) == 0:
                if _clear_screen:
                    from meerschaum.utils.formatting._shell import clear_screen
                    clear_screen()
        except KeyboardInterrupt:
            print("^C")
            return "pass"
        return parsed

    return _patched_input

"""Action to list notes as a tree."""
import os
from pathlib import Path
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text
from bronotes import cfg


class Tree():
    """Represent a filetree of notes."""

    def __init__(self, path, directories_only=False):
        """Construct the tree."""
        self.path = Path(path)
        self.directories_only = directories_only
        self.tree = self.__build_tree()

    def __build_tree(self):
        """Build a tree from our path."""
        tree = f"{self.path.stem}/ \n"

        tree += self.__traverse_path(self.path)

        return tree

    def __traverse_path(self, path, depth=1):
        """Traverse a path and return a tring representing it."""
        tree = ''

        with os.scandir(path) as entry:
            for i in entry:
                tree += self.__handle_direntry(i, depth)

        return tree

    def __build_prefix(self, depth):
        """Build a prefix for a direntry."""
        if depth > 1:
            prefix = ''
            for i in range(1, depth + 1):
                if i == depth:
                    prefix += '|-- '
                elif i == 1:
                    prefix += '|   '
                else:
                    prefix += '    '
        else:
            prefix = '|-- '

        return prefix

    def __handle_direntry(self, entry, depth=1):
        """Handle a direntry returned by os.scandir."""
        prefix = self.__build_prefix(depth)

        if entry.name[0] == '.':
            return ''

        if entry.is_dir():
            tree = f"{prefix}{entry.name}/ \n"
            depth += 1
            tree += f"{self.__traverse_path(entry.path, depth)}"
            return tree
        else:
            if self.directories_only:
                return ''

            if not entry.name.startswith('.'):
                return f"{prefix}{entry.name} \n"

    def __str__(self):
        """Represent the tree as a string."""
        return self.tree


class ActionList(BronoteAction):
    """Show the notes structure as a tree."""

    action = 'list'
    arguments = {
        'dir': {
            'help': 'Optional directory to list.',
            'nargs': '?'
        }
    }
    flags = {
        '--directories': {
            'short': '-d',
            'action': 'store_true',
            'help': 'Only list directories, hide files.'
        }
    }

    def init(self, args):
        """Construct the action."""
        self.set_attributes(args)
        self.path = self.__decide_dir(args.dir)

    def process(self):
        """Process this action."""
        try:
            return Tree(self.path, self.directories)
        except FileNotFoundError:
            return Text.I_NO_DIR.value

    def __decide_dir(self, dir_arg):
        """Decide what directory to list from the given arg."""
        if self.dir:
            projected_path = Path(os.path.join(
                self.cfg.notes_dir, self.dir))
        else:
            return self.cfg.notes_dir

        if projected_path.is_dir():
            return projected_path
        else:
            return self.__find_dir(dir_arg)

    def __find_dir(self, dir_arg):
        """Find a directory if the given path doesn't exist."""
        for node in os.walk(self.cfg.notes_dir):
            (basepath, dirs, files) = node

            for d in dirs:
                if str(dir_arg) in str(d):
                    return Path(f"{basepath}/{d}")

        return Path(dir_arg)

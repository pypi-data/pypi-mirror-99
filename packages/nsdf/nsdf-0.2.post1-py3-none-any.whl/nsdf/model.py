# model.py --- 
# 
# Filename: model.py
# Description: 
# Author: Subhasis Ray [email: {lastname} dot {firstname} at gmail dot com]
# Maintainer: 
# Created: Fri Apr 25 19:51:42 2014 (+0530)
# Version: 
# Last-Updated: Sun Jan 17 11:31:32 2016 (-0500)
#           By: subha
#     Update #: 5
# URL: 
# Keywords: 
# Compatibility: 
# 
# 

# Commentary: 
# 
# 
# 
# 

# Change log:
# 
# 
# 
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 
# 

# Code:
"""Classes for representing the model.

"""
from __future__ import print_function
try:
    from builtins import range
    from builtins import object
except ImportError as e:
    from __builtin__ import range
    from __builtin__ import object

__author__ = 'Subhasis Ray'
__version__ = '0.1'


class ModelComponent(object):
    """Tree node for model tree.

    Attributes:
        parent (ModelComponent): parent of this component.

        children (dict): dict of child components - name is key and
            ModelComponent is value.

        attrs (dict): attributes of the component. These become HDF5
            attributes when it is written to file.

        hdfgroup (hdf5 Group): the group that this component corresponds
            to in NSDF file.

    """
    def __init__(self, name, uid=None, parent=None, attrs=None,
                 hdfgroup=None):
        self.uid = name if uid is None else uid
        self.name = name
        self.parent = parent
        self.children = {}
        # store the order in which children were added
        # self._birth_order = {} 
        self.attrs = attrs if attrs is not None else {}
        self.hdfgroup = hdfgroup
        self._id_path_dict = None
        if parent is not None:
            parent.children[name] = self
        
    def add_child(self, child):
        """Add a child component under this model component.

        Args:
            child (ModelComponent): child component to add to this component

        Returns:
            None

        Raises:
            TypeError

        """
        if not isinstance(child, ModelComponent):
            raise TypeError('require a ModelComponent instance.')
        self.children[child.name] = child
        child.parent = self

    def add_children(self, children):
        """Add a list of children to current component.

        Args:
            children (list): list of children to be added.

        Returns:
            None

        Raises:
            TypeError

        """
        for child in children:
            if not isinstance(child, ModelComponent):
                raise TypeError('require a ModelComponent instance.')
            self.children[child.name] = child
            child.parent = self

    def get_node(self, path):
        """Get node at `path` relative to this node.

        Args: 
            path (str): path obtained by concatenating component names
                with `/` as separator.

        Returns:
            ModelComponent at the specified path

        Raises:
            KeyError if there is no element at the specified path.

        """
        node = self
        for item in path.split('/'):
            name = item.strip()
            if name == '':
                continue
            node = node.children[name]

    def visit(self, function, *args, **kwargs):
        """Visit the subtree starting with `node` recursively, applying
        function `fn` to each node.

        Args:
            node (ModelComponent): node to start with.

            fn(node, *args, **kwargs): a function to apply on each
                node.

        Returns:
            None

        """
        function(self, *args, **kwargs)
        for child in list(self.children.values()):
            child.visit(function, *args, **kwargs)
                
    def print_tree(self, indent=''):
        """Recursively print subtree rooted at this component.

        Args: 
            indent (str): indentation.

        Returns:
            None

        """
        print('{}{}({})'.format(indent, self.name, self.uid))
        for child in list(self.children.values()):
            child.print_tree(indent + '  ')

    def check_uid(self, uid_dict):
        """Check that uid are indeed unique.

        Args: 
            uid_dict (dict): an empty dict for storing the uids
            mapping to all components that have the same uid.

        Note: 
            If any uid is not set, this function as a side effect
            creates the uids in the form parentuid/name - similar to
            unix file paths.

        """
        if self.uid is None:
            if self.parent is None:
                self.uid = self.name
            else:
                self.uid = '{}/{}'.format(self.parent.uid, self.name)
        try:
            clashing = uid_dict[self.uid]
            print('Components with uid clashing with {}: \n'.format(self.name))
            print('\n'.join([comp.name for comp in clashing]))
            clashing.append(self)
        except KeyError:
            uid_dict[self.uid] = [self]
        for child in list(self.children.values()):
            child.check_uid(uid_dict)
            
    @property
    def path(self):
        """Path of this component"""
        pth = self.name
        node = self.parent
        while node is not None:
            pth = node.name + '/' + pth
            node = node.parent
        return '/' + pth

    def update_id_path_dict(self):
        """Update the id->path mapping.

        This must be called before using get_id_path_dict whenever the
        model tree is been modified

        .. seealso:: get_id_path_dict

        """
        if self._id_path_dict is None:
            self._id_path_dict = {}
        def update_dict(node, dictobj):
            """Insert the (uid, path) of `node` into `dictobj`."""
            dictobj[node.uid] = node.path
        self.visit(update_dict, self._id_path_dict)

    def get_id_path_dict(self):
        """Return a dictionary mapping the unique id of the model components
        to their path in modeltree.

        .. seealso:: update_id_path_dict

        """
        if (self._id_path_dict is None) or (len(self._id_path_dict) == 0):
            self.update_id_path_dict()
        return self._id_path_dict

def common_prefix(paths, sep='/'):
    """Find the common prefix of paths.

    Note: does not check for malformed paths right now.
    """
    tokens_list = [path.split(sep) for path in paths]
    endmatch = False
    common = ''
    iii = 0
    while not endmatch:
        name = ''
        try:
            tmp = [tokens[iii] for tokens in tokens_list]
            name = tmp[0]
            for jjj in range(1, len(tmp)):
                if tmp[jjj] != tmp[0]:
                    endmatch = True
                    break
            iii += 1
        except IndexError:
            endmatch = True
        if name and (not endmatch):
            common = common + sep + name
    return common
            
        
            

# 
# model.py ends here

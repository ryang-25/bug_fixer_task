# we need to figure out how to handle external imports (ignore)
# but this risks orphaning some classes/functions? this might work
# but who knows

from inspect import getmembers
from pathlib import Path
from tree_sitter import Language, Parser

import networkx as nx
import os
import tree_sitter_python

PY_LANGUAGE = Language(tree_sitter_python.language())

NODE_TYPE_DIRECTORY = 'directory'
NODE_TYPE_MODULE = 'module'
NODE_TYPE_CLASS = 'class'
NODE_TYPE_FUNCTION = 'function'
EDGE_TYPE_CONTAINS = 'contains'
EDGE_TYPE_INHERITS = 'inherits'
EDGE_TYPE_INVOKES = 'invokes'
EDGE_TYPE_IMPORTS = 'imports'

# A set of builtin functions and classes.
BUILTINS = set(dict(getmembers(__builtins__)).keys())

class Node:
  """A node object"""
  tree_node = None

  def add_graph(self, G):
    """
    Add this node to the multidigraph
    """
    pass

  def __str__(self):
    pass

  def __init__(self, tree_node):
    self.tree_node = tree_node

class DirectoryNode(Node):
  pass

class ModuleNode(Node):
  path = ""
  imports = []

  def add_graph(self, G):
    """
    Add the node and any edges to the graph. Contain edges will be handled somewhere else.

    @@returns a dict of module_names to import names.
    """
    query_import = PY_LANGUAGE.query("""
      (import_statement
        name: (dotted_name) @module_name)
      """)
    captures = query_import.captures(self.tree_node)
    nodes = captures.get("module_name", [])

    query_import_from = PY_LANGUAGE.query("""
      (import_from_statement
        module_name: (dotted_name) @module_name
        name: (dotted_name) @import_name)
      """)
    captures = query_import_from.captures(self.tree_node)
    # add all individual modules too
    nodes.extend(captures.get("module_name", []))
    names = [fully_qualified(node) for node in nodes]
    names.extend(fully_qualified(*nodes) for nodes in zip(*captures.values()))

    query_import_relative = PY_LANGUAGE.query("""
      (import_from_statement
        module_name: (relative_import) @import_prefix
        name: (dotted_name) @import_name)
      """)
    captures = query_import_relative.captures(self.tree_node)
    print(os.listdir())





    # print(self.tree_node)
    # print(*(node.text for node in captures["import_prefix"]))



    # print(names)
    # print(self.tree_node)

    # Graph manipulation begins here
    #
    # Creating a node for a module is a rather tricky endeavor because we need
    # to be able to resolve a pathname relative to another if it's a local
    # module

    # This works because cwd invariant should be upheld
    module_name = path_to_module(self.path)
    G.add_node(module_name, type=NODE_TYPE_MODULE, code=self.tree_node.text)
    for name in names:
      # a simple check—if first part in cwd, it's probably internal

      pass

    # names_resolved =





    # Imports edges
    # G.add_node(self.file_name, )


    # G.add_edge(self.root_node)


    print(G)


    # for name in module_names:
    #   print(name.text)



  def __init__(self, tree_node, path):
    super().__init__(tree_node)
    self.path = path

class ClassNode(Node):
  def add_graph(self, G):
    cursor = self.tree_node.walk()
    cursor.go_to_first_child()
    print(cursor.node.text)

  def __init__(self, tree_node, module_name):
    super().__init__(tree_node)
    self.module_name = module_name


class FunctionNode(Node):
  def add_graph(self, G):
    name = self.tree_node.name.text.decode()
    full_function_name = self.module_name + name

    captures = PY_LANGUAGE.query("""
      (call
        function: (identifier) @function_name)
      """).captures(self.tree_node)
    names = captures.get("function_name", [])

    # Graph manipulation
    G.add_node(full_function_name, type=NODE_TYPE_FUNCTION, code=self.tree_node.text)

    # invoke edges
    for name in names:
      name = name.text.decode()
      module = names_dict.get(name, self.module_name)
      full_name = module + name
      G.add_edge(full_function_name, )

      module + name




    # G.add_edge()

    # G.add_node()

  def __init__(self, tree_node, module_name, names_dict):
    super().__init__(tree_node)
    self.module_name = module_name
    self.names_dict = names_dict

def add_import_from(G, node):
  pass

def add_import(G, node):
  pass

def add_class(G, node):
  pass

def add_function(G, node):
  """
  Do we want to add parameter names, line numbers?
  """
  row_start = node.start_point.row
  roe_end = node.end_point.row
  text = node.text

  pass


def add_from_cst(G, node):
  pass


def fully_qualified(*nodes):
  return ".".join(node.text.decode() for node in nodes)

def path_to_module(path):
  p = Path(path)
  parts = p.parts[:-1] + (p.stem,) # remove extension
  return ".".join(parts)

def module_is_internal(module_name):
  pass


def resolve_to_module(file_name):
  pass


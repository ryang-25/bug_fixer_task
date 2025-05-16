# a python parser

from tree_sitter import Language, Parser
from graph import ModuleNode

import networkx as nx

import tree_sitter_python
import os

PY_LANGUAGE = Language(tree_sitter_python.language())
parser = Parser(PY_LANGUAGE)


def parse_file(file):
  """
  Parses a file object into a graph. Within our graph, nodes are directory,
  module, class, or function definitions. The edges are referential
  relationships between the nodes.
  """
  tree = parser.parse(file.read())
  cursor = tree.walk()
  print(cursor.node)
  print()

  cursor.goto_first_child()
  cursor.goto_first_child()
  query_call = PY_LANGUAGE.query("""
    (call
      function: (identifier) @function_name)
    """)
  c = query_call.captures(cursor.node)
  print(cursor.node, c["function_name"][0].text)

  # potential associated comments
  comments = []
  while cursor.goto_next_sibling():
    match cursor.node.type:
      case "class":
        # node = 
        pass
      case "function":
        pass
      case "comment":
        pass
      case _:
        pass



  # print(node.type)



  # node = ModuleNode(root, file.name)

  G = nx.MultiDiGraph()

  # cursor.goto_first_child()
  # while cursor.goto_next_sibling():
  #   # node


  #   print(cursor.node)


  # We can associate comments with file or class nodes.







  # node.add_graph(nx.DiGraph())

  # cursor = tree.walk()

  # print(root.range)
  # print(root)

def parse_codebase(path):
  return
  py_files = []
  for root, _, files in os.walk(path):
    pass
  for file in files:
    if not file.endswith(".py"):
      pass


#(module (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (import_from_statement module_name: (dotted_name (identifier)) name: (dotted_name (identifier))) (import_from_statement module_name: (dotted_name (identifier) (identifier) (identifier)) name: (dotted_name (identifier))) (import_from_statement module_name: (dotted_name (identifier) (identifier) (identifier)) name: (dotted_name (identifier))) (import_from_statement module_name: (dotted_name (identifier)) name: (dotted_name (identifier))) (import_statement name: (dotted_name (identifier))) (import_statement name: (dotted_name (identifier))) (expression_statement (assignment left: (identifier) right: (call function: (attribute object: (identifier) attribute: (identifier)) arguments: (argument_list (string (string_start) (string_content) (string_end)))))) (expression_statement (assignment left: (identifier) right: (string (string_start) (string_content) (string_end)))) (expression_statement (assignment left: (identifier) right: (string (string_start) (string_content) (string_end)))) (function_definition name: (identifier) parameters: (parameters) (comment) body: (block (expression_statement (assignment left: (identifier) right: (call function: (identifier) arguments: (argument_list (string (string_start) (string_content) (string_end)))))))) (function_definition name: (identifier) parameters: (parameters) body: (block (expression_statement (call function: (identifier) arguments: (argument_list (call function: (identifier) arguments: (argument_list (string (string_start) (string_content) (string_end)) (string (string_start) (string_content) (string_end))))))))) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (comment) (if_statement condition: (comparison_operator (identifier) (string (string_start) (string_content) (string_end))) consequence: (block (expression_statement (call function: (identifier) arguments: (argument_list))))))
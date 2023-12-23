import ast
import random


class Perturber:
    def __init__(self):
        """
        Initialize the Perturber class with a dictionary of mutation functions.
        """
        self.mutation_functions = {
            ast.IfExp: self.mutate_IfExp,
            ast.Lambda: self.mutate_Lambda,
            ast.Dict: self.mutate_Dict,
            ast.BoolOp: self.mutate_BoolOp,
            ast.BinOp: self.mutate_BinOp,
            ast.UnaryOp: self.mutate_UnaryOp,
            ast.AugAssign: self.mutate_AugAssign
            # Add mappings for other node types
            # ...
        }






    
    # Operator Perturbations
    def collect_expr_nodes(self, parsed_tree):
        """
        Create a list of all the expression nodes in the parsed tree generator.

        args:
            parsed_tree: generator
                The generator to search for expressions.

        return:
            output: List
                The list of all expression nodes in the generator.
        """
        
        implemented_types = self.mutation_functions.keys()

        return [node for node in parsed_tree if isinstance(node, tuple(implemented_types))]
        # Eventually, we will have implemented mutations for all expressions.
        # For now, since we only have a few implemented, it is inefficient 
        #   to try to sample from those we have not implemented yet and get a new
        #   corrupted piece of code very infrequently
        #return [node for node in parsed_tree if isinstance(node, ast.expr) or isinstance(node, ast.stmt)]


    def adjust_expr(self, tree, expr_nodes):
        """
        Adjust the expression nodes in the AST.

        args:
            tree: ast.AST
                The abstract syntax tree to be mutated.

        return:
            output: ast.AST
                The mutated abstract syntax tree.
        """
        if not expr_nodes: return tree
        node = random.choice(expr_nodes)
        self.mutate_expr(node)
        return tree


    def mutate_expr(self, node):
        """
        Mutate a given expression node.

        args:
            node: ast.expr
                The expression node to mutate.

        return:
            output: ast.expr
                The mutated expression node.
        """
        # TODO: Change to use the mutation_functions dictionary
        if isinstance(node, ast.BoolOp):
            return self.mutate_BoolOp(node)
        elif isinstance(node, ast.BinOp):
            return self.mutate_BinOp(node)
        elif isinstance(node, ast.UnaryOp):
            return self.mutate_UnaryOp(node)
        elif isinstance(node, ast.IfExp):
            return self.mutate_IfExp(node)
        elif isinstance(node, ast.Lambda):
            return self.mutate_Lambda(node)
        elif isinstance(node, ast.Dict):
            return self.mutate_Dict(node)
        elif isinstance(node, ast.AugAssign):
            return self.mutate_AugAssign(node)


    def mutate_BoolOp(self, node):
        """
        Mutate a BoolOp node by randomly changing its operator.

        args:
            node: ast.BoolOp
                The BoolOp node to mutate.

        return:
            output: ast.BoolOp
                The mutated BoolOp node.
        """
        node.op = random.choice([ast.And(), ast.Or()])
        return node


    def mutate_BinOp(self, node):
        """
        Mutate a BinOp node by randomly changing its operator.

        args:
            node: ast.BinOp
                The BinOp node to mutate.

        return:
            output: ast.BinOp
                The mutated BinOp node.
        """
        node.op = random.choice([ast.Add(), ast.Sub(), ast.Mult(), ast.Div(),
                                 ast.Mod(), ast.Pow(), ast.LShift(),
                                 ast.RShift(), ast.BitOr(), ast.BitXor(),
                                 ast.BitAnd(), ast.FloorDiv()])
        return node


    def mutate_UnaryOp(self, node):
        """
        Mutate a UnaryOp node by randomly changing its operator.

        args:
            node: ast.UnaryOp
                The UnaryOp node to mutate.

        return:
            output: ast.UnaryOp
                The mutated UnaryOp node.
        """
        node.op = random.choice([ast.Invert(), ast.Not(), ast.UAdd(),
                                 ast.USub()])
        return node


    def mutate_IfExp(self, node):
        """
        Mutate an IfExp node. Currently, this function swaps the body and orelse.

        args:
            node: ast.IfExp
                The IfExp node to mutate.

        return:
            output: ast.IfExp
                The mutated IfExp node.
        """
        if random.choice([True, False]):
            node.body, node.orelse = node.orelse, node.body
        return node


    def mutate_Lambda(self, node):
        """
        Mutate a Lambda node by replacing its body with a constant 'None'.

        args:
            node: ast.Lambda
                The Lambda node to mutate.

        return:
            output: ast.Lambda
                The mutated Lambda node.
        """
        node.body = ast.Constant(value=None)  # Replace lambda body with 'None'
        return node


    def mutate_Dict(self, node):
        """
        Mutate a Dict node by clearing all its keys and values.

        args:
            node: ast.Dict
                The Dict node to mutate.

        return:
            output: ast.Dict
                The mutated Dict node.
        """
        if random.choice([True, False]):
            node.keys = []
            node.values = []
        return node


    def mutate_AugAssign(self, node):
        """
        Mutate an AugAssign node by randomly changing its operator.

        args:
            node: ast.AugAssign
                The AugAssign node to mutate.

        return:
            output: ast.AugAssign
                The mutated AugAssign node.
        """
        node.op = random.choice([ast.Add(), ast.Sub(), ast.Mult(), ast.Div(),
                                 ast.Mod(), ast.Pow(), ast.LShift(),
                                 ast.RShift(), ast.BitOr(), ast.BitXor(),
                                 ast.BitAnd(), ast.FloorDiv()])
        return node






    def collect_var_nodes(self, parsed_tree):
        """
        Create a list of all the variable nodes in the parsed tree generator.

        args:
            parsed_tree: generator
                The generator to search for variables.

        return:
            output: List
                The list of all variable nodes in the generator.
        """
        return [node for node in parsed_tree if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)]


    def replace_variable(self, tree: ast.AST, var_nodes):
        """
        Replace one variable with another in the AST.

        args:
            tree: ast.AST
                The abstract syntax tree in which to replace variables.

        return:
            output: ast.AST
                The abstract syntax tree with replaced variables.
        """
        # Choose a node to replace and remove it from the list of potential replacements
        node_to_replace = random.choice(var_nodes)
        potential_replacements = [node for node in var_nodes if node.id != node_to_replace.id]
        # Guarantee a different choice of node for the replacement
        if len(potential_replacements) == 0: return tree
        replacement_node = random.choice(potential_replacements)
        node_to_replace.id = replacement_node.id
        return tree

    





    # High Level Helpers
    def randomly_modify_code(self, code):
        """
        Randomly modify Python code by mutating expressions or replacing variables.

        args:
            code: str
                The Python code to modify.

        return:
            output: str
                The modified Python code.
        """
        tree = ast.parse(code)
        parsed_tree = ast.walk(tree)
        

        var_nodes = self.collect_var_nodes(parsed_tree)
        expr_nodes = self.collect_expr_nodes(parsed_tree)


        if random.choice([True, False]):
            modified_tree = self.replace_variable(tree, var_nodes)
        else:
            modified_tree = self.adjust_expr(tree, expr_nodes)
        

        return ast.unparse(modified_tree)


    def randomly_modify_expression(self, code):
        """
        Randomly modify Python code by mutating an expression, if possible.

        args:
            code: str
                The Python code to modify.

        return:
            output: str
                The modified Python code.
        """
        tree = ast.parse(code)
        parsed_tree = ast.walk(tree)
        expr_nodes = self.collect_expr_nodes(parsed_tree)

        if len(expr_nodes) == 0: return code
        modified_tree = self.adjust_expr(tree, expr_nodes)
        return ast.unparse(modified_tree)
    

    def randomly_modify_variable(self, code):
        """
        Randomly modify Python code by mutating a variable, if possible.

        args:
            code: str
                The Python code to modify.

        return:
            output: str
                The modified Python code.
        """
        tree = ast.parse(code)
        parsed_tree = ast.walk(tree)
        var_nodes = self.collect_var_nodes(parsed_tree)
        if len(var_nodes) < 2: return code

        modified_tree = self.replace_variable(tree, var_nodes)
        return ast.unparse(modified_tree)


        
    def same_tree(self, a, b):
        """
        Check if two Python functions have the same Abstract Syntax Tree.

        args:
            a: str
                The first Python function in string format.
            b: str
                The second Python function in string format.

        return:
            output: bool
                True if the functions have the same tree, False otherwise.
        """
        return ast.dump(ast.parse(a)) == ast.dump(ast.parse(b))
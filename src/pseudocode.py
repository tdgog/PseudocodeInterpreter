import utils.lexer as u_lexer
import utils.parser as u_parser
import utils.interpreter as u_interpreter

def run(filename, text):
    # Generate tokens
    lexer = u_lexer.Lexer(filename, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate abstract syntax tree
    parser = u_parser.Parser(tokens)
    abstract_syntax_tree = parser.parse()
    if abstract_syntax_tree.error: return None, abstract_syntax_tree.error

    # Run program
    interpreter = u_interpreter.Interpreter()
    context = u_interpreter.Context(filename)
    result = interpreter.visit(abstract_syntax_tree.node, context)

    return result.value, result.error

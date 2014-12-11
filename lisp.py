types = ["STR", "INT"]

class Symbol(str): pass

class Value(object):
    def __init__( self, val, type ):
        self.val = val
        self.type = type

    def __repr__( self ):
        return str( self.val )

    def __nonzero__( self ):
        return self.val

class Proc(object):
    def __init__( self, params, body, env ):
        self.params = params
        self.body = body
        self.env = env

    def __call__( self, *args ):
        sub_env = Env( self.env )
        sub_env.vals.update(zip(self.params,args))
        return eval( self.body, sub_env )

def parse( s ):
    return build_ast( tokenize( s ) )

def tokenize( s ):
    tokens = []
    state = "NONE"
    current = ""
    for c in s:
        if state == "NONE":
            if c == "(" or c == ")":
                tokens.append( c )
            elif c == " " or c == "\n":
                continue
            else:
                current += c
                state = "TOKEN"
        elif state == "TOKEN":
            if c == ")":
                tokens.append( current )
                current = ""
                tokens.append( c )
                state = "NONE"
            elif c == " ":
                tokens.append( current )
                current = ""
                state = "NONE"
            else:
                current += c
    return tokens

def choose_container( token ):
    if not token[0].isdigit():
        return Symbol( token )
    else:
        return Value( int(token), "INT" )

def build_ast( tokens ):
    ast = []
    stack = [ast]
    for token in tokens:
        if token == "(":
            stack[-1].append( [] )
            stack.append( stack[-1][-1] )
        elif token == ")":
            stack.pop()
            if len( stack ) == 1:
                ast.append( [] )
                stack = [ast[1]]
        else:
            t = choose_container( token )
            stack[-1].append( t )
    return ast

def run( text ):
    return eval( parse( text ) )

class Env(object):
    def __init__( self, outer=None ):
        self.vals = {}
        self.outer = outer

    def find( self, var ):
        if var in self.vals:
            return self.vals[var]
        elif self.outer is not None:
            return self.outer.find( var )
        else:
            return None

global_env = Env()
global_env.vals.update({
    "*": lambda x, y: Value( x.val*y.val, "INT" )
})

import traceback

def eval( x, env=global_env ):
    if isinstance( x, Symbol ):
        v = env.find( x )
        if v is not None:
            return v
        else:
            return x
    elif isinstance( x, Value ):
        return x
    elif len(x) == 0:
        return None
    elif x[0] == 'if':
        if eval( x[1], env ):
            return eval( x[2], env )
        else:
            return eval( x[3], env )
    elif x[0] == 'define':
        env.vals[eval(x[1], env)] = eval( x[2], env )
        return None
    elif x[0] == 'lambda':
        return Proc( x[1:-1], x[-1], env )
    elif isinstance( x[0], list ):
        return [eval( v, env ) for v in x]
    else:
        proc = eval( x[0], env )
        args = [eval(v, env) for v in x[1:]]
        return proc( *args )

test = '''
(* 2 2)
'''

test1 = '''
(define hello (lambda x y (* x y)))
(hello 2 (* 2 2))


'''

print run( test1 )

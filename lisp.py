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
             stack[-1].append( token )
    return ast

def build_default_env():
    env = {}
    def define( x ):
        env[x[0]] = value[1:]
    env['define'] = define
    env['*'] = lambda x: int(x[0])*int(x[1])
    return env

def run_ast( ast ):
    env = build_default_env()
    for i in ast:
        print eval( i, env )

def eval( x, env ):
    if type( x ) == str or len( x ) == 1:
        if x in env:
            return env[x]
        else:
            return x
    args = []
    for i in xrange( 1, len( x )):
        args.append( eval( x[i], env ) )

    print x

    return env[x[0]]( args )

def run( text ):
    return run_ast( parse( text ) )

test = '''
(define hello x y (* x y))
(hello 2 (* 2 2))

'''

print parse( test )

print run( test )

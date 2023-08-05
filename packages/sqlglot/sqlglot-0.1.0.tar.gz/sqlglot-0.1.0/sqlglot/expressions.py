from sqlglot.tokens import TokenType


class Expression:
    token_type = None
    arg_types = {'expression': True}

    def __init__(self, **args):
        self.key = self.__class__.__name__.lower()
        self.args = args
        self.validate()

    def validate(self):
        for k, v in self.args.items():
            if k not in self.arg_types:
                raise ValueError(f"Unexpected keyword: {k} for {self.token_type}")

        for k, v in self.arg_types.items():
            if v and k not in self.args:
                raise ValueError(f"Required keyword: {k} missing for {self.token_type}")

    def __repr__(self):
        return self.to_s()

    def to_s(self, level=0):
        indent = '' if not level else "\n"
        indent += ''.join(['  '] * level)
        left = f"({self.token_type.name} "

        args = {
            k: ', '.join(
                v.to_s(level + 1)
                for v in (vs if isinstance(vs, list) else [vs])
                if v
            )
            for k, vs in self.args.items()
        }

        right = ', '.join(f"{k}: {v}" for k, v in args.items())
        right += ')'

        return indent + left + right


class Column(Expression):
    token_type = TokenType.COLUMN
    arg_types = {'this': True, 'db': False, 'table': False}


class Table(Expression):
    token_type = TokenType.TABLE
    arg_types = {'this': True, 'db': False}


class Select(Expression):
    token_type = TokenType.SELECT
    arg_types = {'expressions': True}


class Group(Expression):
    token_type = TokenType.GROUP
    arg_types = {'this': True, 'expressions': True}


class Join(Expression):
    token_type = TokenType.JOIN
    arg_types = {'this': True, 'expression': True, 'on': True, 'joiner': True}


class Order(Expression):
    token_type = TokenType.ORDER
    arg_types = {'this': True, 'expressions': True, 'desc': False}

# Binary Expressions
# (PLUS a b)
# (FROM table selects)
class Binary(Expression):
    arg_types = {'this': True, 'expression': True}


class And(Binary):
    token_type = TokenType.AND


class Minus(Binary):
    token_type = TokenType.DASH


class Dot(Binary):
    token_type = TokenType.DOT


class EQ(Binary):
    token_type = TokenType.EQ


class From(Binary):
    token_type = TokenType.FROM


class GT(Binary):
    token_type = TokenType.GT


class GTE(Binary):
    token_type = TokenType.GTE


class Having(Binary):
    token_type = TokenType.HAVING


class Is(Binary):
    token_type = TokenType.IS


class LT(Binary):
    token_type = TokenType.LT


class LTE(Binary):
    token_type = TokenType.LTE


class NEQ(Binary):
    token_type = TokenType.NEQ


class Or(Binary):
    token_type = TokenType.OR


class Plus(Binary):
    token_type = TokenType.PLUS


class Star(Binary):
    token_type = TokenType.STAR


class Slash(Binary):
    token_type = TokenType.SLASH


class Where(Binary):
    token_type = TokenType.WHERE


# Unary Expressions
# (NOT a)
class Unary(Expression):
    arg_types = {'this': True}


class Not(Unary):
    token_type = TokenType.NOT


class Paren(Unary):
    token_type = TokenType.PAREN


class Neg(Unary):
    token_type = TokenType.DASH

# Special Functions
class Alias(Expression):
    token_type = TokenType.ALIAS
    arg_types = {'this': True, 'to': True}

class Between(Expression):
    token_type = TokenType.BETWEEN
    arg_types = {'this': True, 'low': True, 'high': True}


class Case(Expression):
    token_type = TokenType.CASE
    arg_types = {'ifs': True, 'default': False}


class Cast(Expression):
    token_type = TokenType.CAST
    arg_types = {'this': True, 'to': True}


class In(Expression):
    token_type = TokenType.IN
    arg_types = {'this': True, 'expressions': True}

# Functions
class Func(Expression):
    token_type = TokenType.FUNC
    arg_types = {'this': True}


class Avg(Func):
    pass


class Coalesce(Func):
    arg_types = {'expressions': True}


class Count(Func):
    arg_types = {'this': False, 'distinct': False}


class First(Func):
    pass


class Last(Func):
    pass


class If(Func):
    arg_types = {'condition': True, 'true': True, 'false': False}


class LN(Func):
    pass


class Max(Func):
    pass


class Min(Func):
    pass


class Sum(Func):
    pass

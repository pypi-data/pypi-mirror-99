# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

Methods to annotate the Abstract Syntax Tree (AST) of an IDP-Z3 program.

"""

from copy import copy

from .Parse import (Vocabulary, Extern, ConstructedTypeDeclaration,
                    RangeDeclaration, SymbolDeclaration, Symbol,
                    Theory, Definition, Rule,
                    Structure, SymbolInterpretation, Enumeration, FunctionEnum,
                    Tuple, Display)
from .Expression import (Expression, Constructor, IfExpr, AQuantification, Quantee,
                         ARImplication, AImplication, AConjunction, ADisjunction,
                         BinaryOperator, AComparison, AUnary, AAggregate,
                         AppliedSymbol, UnappliedSymbol, Variable, Brackets,
                         FALSE, SymbolExpr, Number)

from .utils import BOOL, INT, REAL, DATE, SYMBOL, OrderedSet, IDPZ3Error


# Class Vocabulary  #######################################################

def annotate(self, idp):
    self.idp = idp

    # annotate declarations
    for s in self.declarations:
        s.block = self
        s.annotate(self)  # updates self.symbol_decls

    for constructor in self.symbol_decls[SYMBOL].domain:
        constructor.symbol = (Symbol(name=constructor.name[1:])
                                .annotate(self, {}))
    self.symbol_decls[SYMBOL].translate()  # to populate .map
Vocabulary.annotate = annotate


# Class Extern  #######################################################

def annotate(self, voc):
    other = voc.idp.vocabularies[self.name]
    #TODO merge while respecting order
    voc.symbol_decls = {**other.symbol_decls, **voc.symbol_decls}
Extern.annotate = annotate


# Class ConstructedTypeDeclaration  #######################################################

def annotate(self, voc):
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
    self.out.annotate(voc, {})
    for c in self.domain:
        c.type = self.name
        self.check(c.name not in voc.symbol_decls or self.name == SYMBOL,
                    f"duplicate constructor in vocabulary: {c.name}")
        voc.symbol_decls[c.name] = c
    self.range = self.domain  # TODO constructor functions
    if self.interpretation:
        self.interpretation.annotate(voc)
ConstructedTypeDeclaration.annotate = annotate


# Class RangeDeclaration  #######################################################

def annotate(self, voc):
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
    self.out.annotate(voc, {})
RangeDeclaration.annotate = annotate


# Class SymbolDeclaration  #######################################################

def annotate(self, voc):
    self.voc = voc
    self.check(self.name is not None, "Internal error")
    self.check(self.name not in voc.symbol_decls,
                f"duplicate declaration in vocabulary: {self.name}")
    voc.symbol_decls[self.name] = self
    for s in self.sorts:
        s.annotate(voc, {})
    self.out.annotate(voc, {})
    self.type = self.out.decl.name
    return self
SymbolDeclaration.annotate = annotate


# Class Symbol  #######################################################

def annotate(self, voc, q_vars):
    if self.name in q_vars:
        return q_vars[self.name]
    self.decl = voc.symbol_decls[self.name]
    self.type = self.decl.type
    return self
Symbol.annotate = annotate


# Class Theory  #######################################################

def annotate(self, idp):
    self.check(self.vocab_name in idp.vocabularies,
                f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]

    for i in self.interpretations.values():
        i.annotate(self)
    self.voc.add_voc_to_block(self)

    self.definitions = [e.annotate(self, self.voc, {}) for e in self.definitions]
    # squash multiple definitions of same symbol declaration
    for d in self.definitions:
        for decl, rule in d.clarks.items():
            if decl in self.clark:
                new_rule = copy(rule)  # not elegant, but rare
                new_rule.body = AConjunction.make('∧', [self.clark[decl].body, rule.body])
                new_rule.block = rule.block
                self.clark[decl] = new_rule
            else:
                self.clark[decl] = rule

    self.constraints = OrderedSet([e.annotate(self.voc, {})
                                    for e in self.constraints])
    self.constraints = OrderedSet([e.interpret(self)
                                    for e in self.constraints])
Theory.annotate = annotate


# Class Definition  #######################################################

def annotate(self, theory, voc, q_vars):
    self.rules = [r.annotate(voc, q_vars) for r in self.rules]

    # create common variables, and rename vars in rule
    self.clarks = {}
    for r in self.rules:
        decl = voc.symbol_decls[r.symbol.name]
        if decl.name not in self.def_vars:
            name = f"${decl.name}$"
            q_v = {f"${decl.name}!{str(i)}$":
                    Variable(f"${decl.name}!{str(i)}$", sort)
                    for i, sort in enumerate(decl.sorts)}
            if decl.out.name != BOOL:
                q_v[name] = Variable(name, decl.out)
            self.def_vars[decl.name] = q_v
        new_rule = r.rename_args(self.def_vars[decl.name])
        self.clarks.setdefault(decl, []).append(new_rule)

    # join the bodies of rules
    for decl, rules in self.clarks.items():
        exprs = sum(([rule.body] for rule in rules), [])
        rules[0].body = ADisjunction.make('∨', exprs)
        self.clarks[decl] = rules[0]
    return self
Definition.annotate = annotate


# Class Rule  #######################################################

def annotate(self, voc, q_vars):
    # create head variables
    for q in self.quantees:
        if q.sort:
            q.annotate(voc, q_vars)
        self.q_vars[q.var] = Variable(q.var, q.sort)
    q_v = {**q_vars, **self.q_vars}  # merge

    self.symbol = self.symbol.annotate(voc, q_v)
    self.args = [arg.annotate(voc, q_v) for arg in self.args]
    self.out = self.out.annotate(voc, q_v) if self.out else self.out
    self.body = self.body.annotate(voc, q_v)

    self.is_whole_domain = all(s.name not in [INT, REAL, DATE]
                                for s in self.symbol.decl.sorts)
    return self
Rule.annotate = annotate


# Class Structure  #######################################################

def annotate(self, idp):
    """
    Annotates the structure with the enumerations found in it.
    Every enumeration is converted into an assignment, which is added to
    `self.assignments`.

    :arg idp: a `Parse.IDP` object.
    :returns None:
    """
    if self.vocab_name not in idp.vocabularies:
        raise IDPZ3Error(f"Unknown vocabulary: {self.vocab_name}")
    self.voc = idp.vocabularies[self.vocab_name]
    for i in self.interpretations.values():
        i.annotate(self)
    self.voc.add_voc_to_block(self)
Structure.annotate = annotate


# Class SymbolInterpretation  #######################################################

def annotate(self, block):
    """
    Annotate the symbol.

    :arg block: a Structure object
    :returns None:
    """
    voc = block.voc
    self.block = block
    self.symbol = Symbol(name=self.name).annotate(voc, {})

    # create constructors if it is a type enumeration
    self.is_type_enumeration = (type(self.symbol.decl) != SymbolDeclaration)
    if self.is_type_enumeration:
        for i, c in enumerate(self.enumeration.tuples):
            self.check(len(c.args) == 1,
                        f"incorrect arity in {self.name} type enumeration")
            constr = Constructor(name=c.args[0].name)
            constr.type = self.name
            if self.name != BOOL:
                constr.py_value = i  # to allow comparisons
            self.check(constr.name not in voc.symbol_decls,
                    f"duplicate constructor in vocabulary: {constr.name}")
            voc.symbol_decls[constr.name] = constr

    self.enumeration.annotate(voc)

    # predicate enumeration have FALSE default
    if type(self.enumeration) != FunctionEnum and self.default is None:
        self.default = FALSE
    self.check(self.is_type_enumeration
                or all(s.name not in [INT, REAL]  # finite domain
                        for s in self.symbol.decl.sorts)
                or self.default is None,
        f"Can't use default value for '{self.name}' on infinite domain.")
    if self.default is not None:
        self.default = self.default.annotate(voc, {})
        self.check(self.default.as_rigid() is not None,
            f"Default value for '{self.name}' must be ground: {self.default}")
SymbolInterpretation.annotate = annotate


# Class Enumeration  #######################################################

def annotate(self, voc):
    for t in self.tuples:
        t.annotate(voc)
Enumeration.annotate = annotate


# Class Tuple  #######################################################

def annotate(self, voc):
    self.args = [arg.annotate(voc, {}) for arg in self.args]
    self.check(all(a.as_rigid() is not None for a in self.args),
                f"Tuple must be ground : ({self})")
Tuple.annotate = annotate


# Class Display  #######################################################

def annotate(self, idp):
    self.voc = idp.vocabulary

    # add display predicates

    viewType = ConstructedTypeDeclaration(name='View',
        constructors=[Constructor(name='normal'),
                        Constructor(name='expanded')])
    viewType.annotate(self.voc)

    # Check the AST for any constructors that belong to open types.
    # For now, the only open types are `unit` and `heading`.
    open_constructors = {'unit': [], 'heading': []}
    for constraint in self.constraints:
        constraint.generate_constructors(open_constructors)

    # Next, we convert the list of constructors to actual types.
    open_types = {}
    for name, constructors in open_constructors.items():
        # If no constructors were found, then the type is not used.
        if not constructors:
            open_types[name] = None
            continue

        type_name = name.capitalize()  # e.g. type Unit (not unit)
        open_type = ConstructedTypeDeclaration(name=type_name,
                                                constructors=constructors)
        open_type.annotate(self.voc)
        open_types[name] = Symbol(name=type_name)

    for name, out in [
        ('goal', Symbol(name=BOOL)),
        ('expand', Symbol(name=BOOL)),
        ('relevant', Symbol(name=BOOL)),
        ('hide', Symbol(name=BOOL)),
        ('view', Symbol(name='View')),
        ('moveSymbols', Symbol(name=BOOL)),
        ('optionalPropagation', Symbol(name=BOOL)),
        ('unit', open_types['unit']),
        ('heading', open_types['heading'])
    ]:
        symbol_decl = SymbolDeclaration(annotations='',
                                        name=Symbol(name=name),
                                        sorts=[], out=out)
        symbol_decl.annotate(self.voc)

    # annotate constraints
    for constraint in self.constraints:
        constraint.annotate(self.voc, {})
Display.annotate = annotate


# Class Expression  #######################################################

def annotate(self, voc, q_vars):
    " annotate tree after parsing "
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    return self.annotate1()
Expression.annotate = annotate


def annotate1(self):
    " annotations that are common to __init__ and make() "
    self.fresh_vars = set()
    if self.value is not None:
        pass
    if self.simpler is not None:
        self.fresh_vars = self.simpler.fresh_vars
    else:
        for e in self.sub_exprs:
            self.fresh_vars.update(e.fresh_vars)
    return self
Expression.annotate1 = annotate1


# Class IfExpr  #######################################################

def annotate1(self):
    self.type = self.sub_exprs[IfExpr.THEN].type
    return Expression.annotate1(self)
IfExpr.annotate1 = annotate1


# Class Quantee  #######################################################

def annotate(self, voc, q_vars):
    if self.sort:
        self.sort = self.sort.annotate(voc, q_vars).simplify1()
    out = Expression.annotate1(self.simplify1())
    if out.sort:
        out.fresh_vars.update(out.sort.fresh_vars)
    return out
Quantee.annotate = annotate


# Class AQuantification  #######################################################

def annotate(self, voc, q_vars):
    self.q_vars = {}
    for q in self.quantees:
        self.check(q.var not in voc.symbol_decls,
            f"the quantified variable '{q.var}' cannot have"
            f" the same name as another symbol")
        q.annotate(voc, q_vars)
        self.q_vars[q.var] = Variable(q.var, q.sort)
    q_v = {**q_vars, **self.q_vars}  # merge
    self.sub_exprs = [e.annotate(voc, q_v) for e in self.sub_exprs]
    return self.annotate1()
AQuantification.annotate = annotate

def annotate1(self):
    Expression.annotate1(self)
    # remove q_vars
    self.fresh_vars = self.fresh_vars.difference(set(self.q_vars.keys()))
    return self
AQuantification.annotate1 = annotate1


# Class BinaryOperator  #######################################################

def annotate1(self):
    self.check(not (self.operator[0] == '⇒' and 2 < len(self.sub_exprs)),
            "Implication is not associative.  Please use parenthesis.")
    if self.type is None:
        self.type = REAL if any(e.type == REAL for e in self.sub_exprs) \
                else INT if any(e.type == INT for e in self.sub_exprs) \
                else self.sub_exprs[0].type  # constructed type, without arithmetic
    return Expression.annotate1(self)
BinaryOperator.annotate1 = annotate1


# Class ARImplication  #######################################################


def annotate(self, voc, q_vars):
    # reverse the implication
    self.sub_exprs.reverse()
    out = AImplication(sub_exprs=self.sub_exprs,
                        operator=['⇒']*len(self.operator))
    if hasattr(self, "block"):
        out.block = self.block
    return out.annotate(voc, q_vars)
ARImplication.annotate = annotate


# Class AComparison  #######################################################

def annotate(self, voc, q_vars):
    out = BinaryOperator.annotate(self, voc, q_vars)
    # a≠b --> Not(a=b)
    if len(self.sub_exprs) == 2 and self.operator == ['≠']:
        out = AUnary.make('¬', AComparison.make('=', self.sub_exprs))
    return out
AComparison.annotate = annotate


# Class AUnary  #######################################################

def annotate1(self):
    if len(self.operators) % 2 == 0: # negation of negation
        return self.sub_exprs[0]
    self.type = self.sub_exprs[0].type
    return Expression.annotate1(self)
AUnary.annotate1 = annotate1


# Class AAggregate  #######################################################

def annotate(self, voc, q_vars):
    self.q_vars = {}
    for q in self.quantees:
        self.check(q.var not in voc.symbol_decls,
            f"the quantifier variable '{q.var}' cannot have the same name as another symbol.")
        q.annotate(voc, q_vars)
        self.q_vars[q.var] = Variable(q.var, q.sort)
    q_v = {**q_vars, **self.q_vars}  # merge
    self.sub_exprs = [e.annotate(voc, q_v) for e in self.sub_exprs]
    self.type = self.sub_exprs[AAggregate.OUT].type if self.out else INT

    assert not self.using_if
    self.sub_exprs = [IfExpr.make(if_f=self.sub_exprs[AAggregate.CONDITION],
            then_f=Number(number='1') if self.out is None else
                    self.sub_exprs[AAggregate.OUT],
            else_f=Number(number='0'))]
    self.using_if = True
    self = self.annotate1()
    # remove q_vars after annotate1
    self.fresh_vars = self.fresh_vars.difference(set(self.q_vars.keys()))
    return self
AAggregate.annotate = annotate


# Class AppliedSymbol  #######################################################

def annotate(self, voc, q_vars):
    self.symbol = self.symbol.annotate(voc, q_vars)
    self.sub_exprs = [e.annotate(voc, q_vars) for e in self.sub_exprs]
    if self.in_enumeration:
        self.in_enumeration.annotate(voc)

    # move the negation out
    if 'not' in self.is_enumerated:
        out = AppliedSymbol.make(self.symbol, self.sub_exprs,
                                    is_enumerated='is enumerated')
        out = AUnary.make('¬', out)
    elif 'not' in self.is_enumeration:
        out = AppliedSymbol.make(self.symbol, self.sub_exprs,
                                    is_enumeration='in',
                                    in_enumeration=self.in_enumeration)
        out = AUnary.make('¬', out)
    else:
        out = self.annotate1()
    return out
AppliedSymbol.annotate = annotate

def annotate1(self):
    out = Expression.annotate1(self)
    out.symbol = out.symbol.annotate1()
    out.fresh_vars.update(out.symbol.fresh_vars)
    return out.simplify1()
AppliedSymbol.annotate1 = annotate1


# Class SymbolExpr  #######################################################

def annotate(self, voc, q_vars):
    out = Expression.annotate(self, voc, q_vars)
    return out.simplify1()
SymbolExpr.annotate = annotate


# Class Variable  #######################################################

def annotate(self, voc, q_vars):
    self.type = self.sort.decl.name if self.sort and self.sort.decl else ''
    return self
Variable.annotate = annotate


# Class UnappliedSymbol  #######################################################

def annotate(self, voc, q_vars):
    if self.name in voc.symbol_decls:
        if type(voc.symbol_decls[self.name]) == Constructor:
            return voc.symbol_decls[self.name]
        self.check(False, f"{self} should be applied to arguments (or prefixed with a back-tick)")
    if self.name in q_vars:
        return q_vars[self.name]
    # elif self.name in voc.symbol_decls:  # in symbol_decls
    #     out = AppliedSymbol.make(self.s, self.sub_exprs)
    #     return out.annotate(voc, q_vars)
    # If this code is reached, an undefined symbol was present.
    self.check(False, f"Symbol not in vocabulary: {self}")
UnappliedSymbol.annotate = annotate


# Class Brackets  #######################################################

def annotate1(self):
    self.type = self.sub_exprs[0].type
    if self.annotations['reading']:
        self.sub_exprs[0].annotations = self.annotations
    self.fresh_vars = self.sub_exprs[0].fresh_vars
    return self
Brackets.annotate1 = annotate1


Done = True
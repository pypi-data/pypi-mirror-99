# cython: binding=True

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

Methods to interpret a theory in a data structure

* substitute a constant by its value in an expression
* replace symbols interpreted in a structure by their interpretation
* expand quantifiers

This module also includes methods to:

* substitute an node by another in an AST tree
* instantiate an expresion, i.e. replace a variable by a value

This module monkey-patches the ASTNode class and sub-classes.

( see docs/zettlr/Substitute.md )

"""

import copy
from itertools import product

from .Assignments import Status
from .Parse import(Extern, ConstructedTypeDeclaration, RangeDeclaration,
                   SymbolDeclaration, Symbol, Rule, SymbolInterpretation,
                   FunctionEnum)
from .Expression import (Constructor, SymbolExpr, Expression, AQuantification,
                    AImplication, AConjunction,  AEquivalence, AAggregate,
                    AComparison, AUnary, AppliedSymbol, Number,
                    Variable, TRUE)
from .utils import BOOL, RESERVED_SYMBOLS, SYMBOL


# class Extern  ###########################################################

def interpret(self, problem):
    pass
Extern.interpret = interpret


# class ConstructedTypeDeclaration  ###########################################################

def interpret(self, problem):
    self.translate()
ConstructedTypeDeclaration.interpret = interpret


# class RangeDeclaration  ###########################################################

def interpret(self, problem):
    pass
RangeDeclaration.interpret = interpret


# class SymbolDeclaration  ###########################################################

def interpret(self, problem):
    self.domain = list(product(*[s.decl.range for s in self.sorts])) #
    self.range = self.out.decl.range

    # create instances
    if self.name not in RESERVED_SYMBOLS:
        self.instances = {}
        for arg in self.domain:
            expr = AppliedSymbol.make(Symbol(name=self.name), arg)
            expr.annotate(self.voc, {})
            self.instances[expr.code] = expr
            if not expr.code.startswith('_'):
                problem.assignments.assert_(expr, None, Status.UNKNOWN, False)

    # add type constraints to problem.constraints
    if self.out.decl.name != BOOL and self.name not in RESERVED_SYMBOLS:
        for inst in self.instances.values():
            domain = self.out.decl.check_bounds(inst.copy())
            if domain is not None:
                domain.block = self.block
                domain.is_type_constraint_for = self.name
                domain.annotations['reading'] = "Possible values for " + str(inst)
                problem.constraints.append(domain)
SymbolDeclaration.interpret = interpret


# class Rule  ###########################################################

def interpret(self, theory):
    """ expand quantifiers and interpret """

    # compute self.whole_domain, by expanding:
    # ∀ v: f(v)=out <=> body
    # (after joining the rules of the same symbols)
    assert self.is_whole_domain
    self.cache = {}  # reset the cache
    if self.out:
        expr = AppliedSymbol.make(self.symbol, self.args[:-1])
        expr.in_head = True
        expr = AComparison.make('=', [expr, self.args[-1]])
    else:
        expr = AppliedSymbol.make(self.symbol, self.args)
        expr.in_head = True
    expr = AEquivalence.make('⇔', [expr, self.body])
    expr = AQuantification.make('∀', {**self.q_vars}, expr)
    self.whole_domain = expr.interpret(theory)
    self.whole_domain.block = self.block
    return self
Rule.interpret = interpret


# class SymbolInterpretation  ###########################################################

def interpret(self, problem):
    status = (Status.STRUCTURE if self.block.name != 'default' else
                Status.GIVEN)
    if self.is_type_enumeration:
        symbol = self.symbol
        symbol.decl.domain = [t.args[0]
                              for t in self.enumeration.tuples.values()]
        symbol.decl.range = symbol.decl.domain
    else: # update problem.assignments with data from enumeration
        for t in self.enumeration.tuples:
            if type(self.enumeration) == FunctionEnum:
                args, value = t.args[:-1], t.args[-1]
            else:
                args, value = t.args, TRUE
            expr = AppliedSymbol.make(self.symbol, args)
            self.check(expr.code not in problem.assignments
                or problem.assignments[expr.code].status == Status.UNKNOWN,
                f"Duplicate entry in structure for '{self.name}': {str(expr)}")
            problem.assignments.assert_(expr, value, status, False)
        if self.default is not None:
            for code, expr in self.symbol.decl.instances.items():
                if (code not in problem.assignments
                    or problem.assignments[code].status != status):
                    problem.assignments.assert_(expr, self.default, status,
                                                False)

SymbolInterpretation.interpret = interpret


# class Expression  ###########################################################

def interpret(self, problem) -> Expression:
    """ uses information in the problem and its vocabulary to:
    - expand quantifiers in the expression
    - simplify the expression using known assignments
    - instantiate definitions

    Args:
        problem (Problem): the Problem to apply

    Returns:
        Expression: the resulting expression
    """
    if self.is_type_constraint_for:  # do not interpret typeConstraints
        return self
    out = self.update_exprs(e.interpret(problem) for e in self.sub_exprs)
    return out
Expression.interpret = interpret


# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, todo=None):
    """ recursively substitute e0 by e1 in self (e0 is not a Variable)

    implementation for everything but AppliedSymbol, UnappliedSymbol and
    Fresh_variable
    """

    assert not isinstance(e0, Variable) or isinstance(e1, Variable)  # should use instantiate instead
    assert self.co_constraint is None  # see AppliedSymbol instead

    # similar code in AppliedSymbol !
    if self.code == e0.code:
        if self.code == e1.code:
            return self  # to avoid infinite loops
        return self._change(value=e1)  # e1 is Constructor or Number
    else:
        # will update self.simpler
        out = self.update_exprs(e.substitute(e0, e1, assignments, todo)
                                for e in self.sub_exprs)
        return out
Expression.substitute = substitute


def instantiate(self, e0, e1, problem=None):
    """
    Recursively substitute Variable e0 by e1 in a copy of self, and update fresh_vars.
    Interpret appliedSymbols immediately if grounded (and not occurring in head of definition).

    Do nothing if e0 does not occur in self.
    """
    assert type(e0) == Variable
    if self.value or e0.name not in self.fresh_vars:
        return self
    out = copy.copy(self)  # shallow copy !
    out.annotations = copy.copy(out.annotations)
    out.fresh_vars = copy.copy(out.fresh_vars)
    return out.instantiate1(e0, e1, problem)
Expression.instantiate = instantiate

def instantiate1(self, e0, e1, problem=None):
    """
    recursively substitute Variable e0 by e1 in self, and update fresh_vars.
    Interpret appliedSymbols immediately if grounded (and not occurring in head of definition).
    """

    # instantiate expressions, with simplification
    out = self.update_exprs(e.instantiate(e0, e1, problem) for e
                            in self.sub_exprs)

    if out.co_constraint is not None:
        co_constraint = out.co_constraint.instantiate(e0, e1, problem)
        out._change(co_constraint=co_constraint)

    if out.value is not None:  # replace by new value
        out = out.value
    elif e0.name in out.fresh_vars:
        out.fresh_vars.discard(e0.name)
        if type(e1) == Variable:
            out.fresh_vars.add(e1.name)
        out.code = str(out)
    out.annotations['reading'] = out.code
    return out
Expression.instantiate1 = instantiate1


# Class Constructor  ######################################################

def instantiate(self, e0, e1, problem=None):
    return self
Constructor.instantiate = instantiate


# class Symbol ###########################################################

def instantiate(self, e0, e1, problem=None):
    return self
Symbol.instantiate = instantiate


# Class AQuantification  ######################################################

def interpret(self, problem):
    """apply information in the problem and its vocabulary

    Args:
        problem (Problem): the problem to be applied

    Returns:
        Expression: the expanded quantifier expression
    """
    # This method is called by AAggregate.interpret !
    if not self.q_vars:
        return Expression.interpret(self, problem)
    inferred = self.sub_exprs[0].type_inference()
    if 1 < len(self.sub_exprs):
        inferred = {**inferred, **self.sub_exprs[1].type_inference()}
    for q in self.q_vars:
        if not self.q_vars[q].sort and q in inferred:
            new_var = Variable(q, inferred[q])
            self.sub_exprs[0].substitute(new_var, new_var, {})
            self.q_vars[q] = new_var
        elif self.q_vars[q].sort:
            self.q_vars[q].sort = self.q_vars[q].sort.interpret(problem)

    for v, s in inferred.items():
        assert (v not in self.q_vars
                or self.q_vars[v].sort.decl.is_subset_of(s.decl)), \
            f"Inconsistent types for {v} in {self}"

    forms = self.sub_exprs
    new_vars = {}
    for name, var in self.q_vars.items():
        range = None
        if var.sort:
            if var.sort.decl.range:
                range = var.sort.decl.range
                guard = lambda x,y: y
            elif var.sort.code in problem.interpretations:
                self.check(var.sort.decl.arity == 1,
                           f"Incorrect arity of {var.sort}")
                self.check(var.sort.decl.out.type == BOOL,
                           f"{var.sort} is not a predicate")
                enumeration = problem.interpretations[var.sort.code].enumeration
                range = [t.args[0] for t in enumeration.tuples.values()]
                guard = lambda x,y: y
            elif name in inferred:
                sort = inferred[name].decl
                if sort.name in problem.interpretations:
                    enumeration = problem.interpretations[sort.name].enumeration
                    range = [t.args[0] for t in enumeration.tuples.values()]
                    symbol = var.sort.as_rigid()
                    def guard(val, expr):
                        applied = AppliedSymbol.make(symbol, [val])
                        if self.q == '∀':
                            out = AImplication.make('⇒', [applied, expr])
                        else:
                            out = AConjunction.make('∧', [applied, expr])
                        return out
        if range is not None:
            out = []
            for f in forms:
                for val in range:
                    new_f = guard(val, f.instantiate(var, val, problem))
                    out.append(new_f)
            forms = out
        else: # infinite domain !
            new_vars[name] = var
    if new_vars:
        forms = [f.interpret(problem) if problem else f for f in forms]
    self.q_vars = new_vars
    return self.update_exprs(forms)
AQuantification.interpret = interpret


def instantiate1(self, e0, e1, problem=None):
    out = Expression.instantiate1(self, e0, e1, problem)  # updates fresh_vars
    for name, var in self.q_vars.items():
        if var.sort:
            self.q_vars[name].sort = var.sort.instantiate(e0, e1, problem)
    if e0.type == SYMBOL:
        out.interpret(problem)  # to perform type inference
    return out
AQuantification.instantiate1 = instantiate1


# Class AAggregate  ######################################################

def interpret(self, problem):
    assert self.using_if
    return AQuantification.interpret(self, problem)
AAggregate.interpret = interpret

AAggregate.instantiate1 = instantiate1  # from AQuantification


# Class AppliedSymbol  ##############################################

def interpret(self, problem):
    self.symbol = self.symbol.interpret(problem)
    sub_exprs = [e.interpret(problem) for e in self.sub_exprs]
    simpler, co_constraint = None, None
    if self.decl:
        if self.is_enumerated:
            assert self.decl.type != BOOL, \
                f"Can't use 'is enumerated' with predicate {self.decl.name}."
            if self.decl.name in problem.interpretations:
                interpretation = problem.interpretations[self.decl.name]
                if interpretation.default is not None:
                    simpler = TRUE
                else:
                    simpler = interpretation.enumeration.contains(sub_exprs, True)
                if 'not' in self.is_enumerated:
                    simpler = AUnary.make('¬', simpler)
                simpler.annotations = self.annotations
        elif self.in_enumeration:
            # re-create original Applied Symbol
            core = AppliedSymbol.make(self.symbol, sub_exprs).copy()
            simpler = self.in_enumeration.contains([core], False)
            if 'not' in self.is_enumeration:
                simpler = AUnary.make('¬', simpler)
            simpler.annotations = self.annotations
        elif (self.decl.name in problem.interpretations
            and any(s.decl.name == SYMBOL for s in self.decl.sorts)
            and all(a.as_rigid() is not None for a in sub_exprs)):
            # apply enumeration of predicate over symbols to allow simplification
            # do not do it otherwise, for performance reasons
            f = problem.interpretations[self.decl.name].interpret_application
            simpler = f(problem, 0, self, sub_exprs)
        if (not self.in_head and not self.fresh_vars
            and self.decl in problem.clark):  # has a definition
            clark = problem.clark[self.decl]
            co_constraint = clark.instantiate_definition(sub_exprs, problem)
    out = self._change(sub_exprs=sub_exprs, simpler=simpler,
                       co_constraint=co_constraint)
    return out
AppliedSymbol.interpret = interpret


# @log_calls  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, todo=None):
    """ recursively substitute e0 by e1 in self """

    assert not isinstance(e0, Variable) or isinstance(e1, Variable), \
        f"should use 'instantiate instead of 'substitute for {e0}->{e1}"

    new_branch = None
    if self.co_constraint is not None:
        new_branch = self.co_constraint.substitute(e0, e1, assignments, todo)
        if todo is not None:
            todo.extend(new_branch.symbolic_propagate(assignments))

    if self.code == e0.code:
        return self._change(value=e1, co_constraint=new_branch)
    elif self.simpler is not None:  # has an interpretation
        assert self.co_constraint is None
        simpler = self.simpler.substitute(e0, e1, assignments, todo)
        return self._change(simpler=simpler)
    else:
        sub_exprs = [e.substitute(e0, e1, assignments, todo)
                     for e in self.sub_exprs]  # no simplification here
        return self._change(sub_exprs=sub_exprs, co_constraint=new_branch)
AppliedSymbol .substitute = substitute

def instantiate1(self, e0, e1, problem=None):
    out = Expression.instantiate1(self, e0, e1, problem)  # update fresh_vars
    if type(out) == AppliedSymbol:  # might be a number after instantiation
        if type(out.symbol) == SymbolExpr and out.symbol.value is None:  # $(x)()
            out.symbol = out.symbol.instantiate(e0, e1, problem)
            if type(out.symbol) == Symbol:  # found $(x)
                self.check(len(out.sub_exprs) == len(out.symbol.decl.sorts),
                            f"Incorrect arity for {e1.code}")
                out = AppliedSymbol.make(out.symbol, out.sub_exprs)
        if problem and not self.fresh_vars:
            return out.interpret(problem)
    return out
AppliedSymbol .instantiate1 = instantiate1


# Class Variable  #######################################################

def interpret(self, problem):
    return self
Variable.interpret = interpret

# @log  # decorator patched in by tests/main.py
def substitute(self, e0, e1, assignments, todo=None):
    if self.sort:
        self.sort = self.sort.substitute(e0,e1, assignments, todo)
    return e1 if self.code == e0.code else self
Variable.substitute = substitute

def instantiate1(self, e0, e1, problem=None):
    if self.sort:
        self.sort = self.sort.instantiate(e0, e1, problem)
    return e1 if self.code == e0.code else self
Variable.instantiate1 = instantiate1


# Class Number  ######################################################

def instantiate(self, e0, e1, problem=None):
    return self
Number.instantiate = instantiate



Done = True

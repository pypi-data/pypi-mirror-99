# -*- coding: utf-8 -*-

"""
program_9ef5
============

Problem
-------

1. A brief informal statement of the problem

  - give examples

2. The precise correctness conditions required of a solution


Solution
--------

3. Describe the solution

  - Whenever needed, explain the "why" of the design

"""


# Imports

import logging
from inspect import signature

import networkx as nx
from toolz.functoolz import pipe

logger = logging.getLogger(__name__)


# Implementation


def compute_seq(digraph):
    roots = [u for u in digraph if digraph.in_degree(u) == 0]

    def rec(u):
        max_lvl = -1
        for v in digraph[u]:
            lvl = digraph.nodes[v]["lvl"]
            if lvl is None:
                lvl = rec(v)

            if max_lvl < lvl:
                max_lvl = lvl

        digraph.nodes[u]["lvl"] = max_lvl + 1

        return digraph.nodes[u]["lvl"]

    for root in roots:
        rec(root)

    sorted_nodes = sorted(digraph.nodes(data=True), key=lambda n: n[1]["lvl"])

    return [name for (name, xxx) in sorted_nodes]


class Program:
    def __init__(self, inst=set()):
        self._inst = inst
        self._inst_list = []

    def inst_add(inst):

        _inst = inst

        if isinstance(inst, Instruction):
            _inst = {inst}

        if not isinstance(_inst, set):
            raise AssertionError(
                f"expected: inst is an Instruction or set(Instruction). actual: {inst}"
            )

        self._inst = self._inst | _inst

        return self

    def ordered_insts(self):
        if self._inst_list:
            return self._inst_list

        digraph = nx.DiGraph()

        for inst in self._inst:
            key = inst.key()
            digraph.add_node(key, lvl=None)
            for dep in inst.deps():
                digraph.add_node(dep, lvl=None)
                digraph.add_edge(key, dep)

        ordered_keys = compute_seq(digraph)

        inst_by_key = {inst.key(): inst for inst in self._inst}

        self._inst_list = [
            inst_by_key[key] for key in ordered_keys if key in inst_by_key
        ]

        return self._inst_list

    def execute(self, context={}):
        insts = self.ordered_insts()
        return pipe(context, *insts)


class Instruction:
    _set = set()

    @classmethod
    def all(cls):
        return cls._set

    @classmethod
    def clean(cls):
        cls._set = set()
        return cls

    def __init__(self, func):
        self._func = func
        params = tuple(p for p in signature(func).parameters)
        self._deps = params[:-1]
        self._result_id = params[-1]
        self._set.add(self)

    def deps(self):
        return self._deps

    def key(self):
        return self._result_id

    def rule(self):
        return self._func.__name__

    def __call__(self, context):
        args = tuple(context[key] for key in self._deps) + (None,)
        logger.debug(self.__str__())
        context[self.key()] = self._func(*args)
        return context

    def __str__(self):
        msg = f"""{type(self).__name__} rule: {self.rule()} key: {self.key()} deps: {self.deps()}"""
        return msg

    def __doc__(self):
        return self._func.__doc__

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        return type(self) == type(other) and hash(self) == hash(other)

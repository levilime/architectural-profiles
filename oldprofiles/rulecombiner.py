from functools import reduce

from oldprofiles.rules.dummy import DummyRules


def combine_rules(declaritive_constraints_list=[]):
    return reduce(add_rule,
                  declaritive_constraints_list, DummyRules())

def add_rule(aggregated_constraints, current_constraints):
    aggregated_constraints.add_DeclarativeConstraints(current_constraints)
    return aggregated_constraints

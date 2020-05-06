from functools import reduce


class DeclarativeConstraints:

    def __init__(self, constraints=[]):
        self.constraints = constraints

    def to_string(self):
        return reduce(lambda agg, constraint: agg + "\n" + "\n" + constraint.to_string(), self.constraints,
                      "% PROFILE CONSTRAINTS:") + "\n \n % END PROFILE CONSTRAINTS \n \n"

    def add_DeclarativeConstraints(self, declarative_constraints):
        self.constraints = self.constraints + declarative_constraints.constraints


class DeclarativeConstraint:
    def __init__(self, description, rule):
        self.description = description
        self.rule = rule

    def to_string(self):
        return "% " + self.description + "\n" + self.rule

class TransativeDeclarativeConstraint(DeclarativeConstraint):

    def __init__(self, description, id, base_categories, transative_categories, required_for):

        names = reduce(lambda agg, k: dict(agg, **{k: k + id}),
                       ["basecategory", "transativecategory", "requiredforcategory"], {})

        categories_def = \
            reduce(lambda agg_outside, meta_category:
                   agg_outside +
                   reduce(lambda agg_inside, category: agg_inside + meta_category[0] + "(" + category + ").\n",
                          meta_category[1], "")
                   + "\n",
                   [(names["basecategory"], base_categories),
                    (names["transativecategory"], transative_categories),
                    (names["requiredforcategory"], required_for)
                    ], "")


        functions = reduce(lambda agg, k: dict(agg, **{k: names[k] + "(Category)"}),
                       names, {})
        result = categories_def + "\n"
        id + "(X,Y,Z) :- assign(X,Y,Z, ID), category(ID, Category), " + functions["basecategory"] + ".\n"
        id + "(X,Y,Z) :- assign(X1,Y1,Z1, ID1), category(ID1, Category), " + functions["transativecategory"] + ", \n" \
             "adjacent(X1, Y1, Z1, X2, Y2, Z2), assign(X2, Y2, Z2, ID2), " + id + "(X2, Y2, Z2)."
        ":- 1 {assign(X,Y,Z,ID): category(ID, Category), " + functions["requiredforcategory"] + "}.\n"

        super().__init__(description, result)



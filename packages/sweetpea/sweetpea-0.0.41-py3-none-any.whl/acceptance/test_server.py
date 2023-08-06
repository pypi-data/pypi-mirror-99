import operator as op
import pytest

from sweetpea.primitives import factor, derived_level, within_trial
from sweetpea.server import build_cnf, is_cnf_still_sat
from sweetpea.logic import And
from sweetpea import fully_cross_block


# Basic setup
color_list = ["red", "blue"]
color = factor("color", color_list)
text  = factor("text",  color_list)

# Congruent factor
con_level  = derived_level("con", within_trial(op.eq, [color, text]))
inc_level  = derived_level("inc", within_trial(op.ne, [color, text]))
con_factor = factor("congruent?", [con_level, inc_level])

block = fully_cross_block([color, text, con_factor], [color, text], [])


def test_is_cnf_still_sat_should_respond_correctly():

    cnf_result = build_cnf(block)

    # Build the CNF on the server.
    cnf_result = build_cnf(block)

    assert     is_cnf_still_sat(block, [And([1, 3])])

    assert not is_cnf_still_sat(block, [And([7, 8])])
    assert not is_cnf_still_sat(block, [And([1, 7, 13])])

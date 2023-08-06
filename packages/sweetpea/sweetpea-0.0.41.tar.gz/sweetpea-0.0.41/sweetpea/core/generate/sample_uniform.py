"""This module provides simple CNF generation functionality."""


from typing import List

from ..cnf import CNF
from .tools.unigen import DEFAULT_DOCKER_MODE_ON, call_unigen
from .utility import GenerationRequest, Solution, combine_and_save_cnf, temporary_cnf_file


__all__ = ['sample_uniform']


def sample_uniform(initial_cnf: CNF,
                   fresh: int,
                   support: int,
                   generation_requests: List[GenerationRequest],
                   use_docker: bool = DEFAULT_DOCKER_MODE_ON
                   ) -> List[Solution]:
    """Samples solutions to a CNF problem uniformly. The solution is computed
    by using Unigen.
    """
    with temporary_cnf_file() as cnf_file:
        combine_and_save_cnf(cnf_file, initial_cnf, fresh, support, generation_requests)
        solution_str = call_unigen(cnf_file, docker_mode=use_docker)
        # TODO: Validate that skipping the comments is the intended
        #       functionality. The Haskell code doesn't appear to need to do
        #       this, but this could be due to the Unigen upgrade or something
        #       else. Just check it.
        return [build_solution(line) for line in solution_str.strip().splitlines() if line and not line.startswith('c')]


def build_solution(line: str) -> Solution:
    """Given a Unigen solution, constructs a `Solution` object."""
    parts = line.replace('v', '').strip().split()
    assignment = [int(p) for p in parts[:-1]]
    frequency = int(parts[-1].split(':')[-1])
    return Solution(assignment, frequency)

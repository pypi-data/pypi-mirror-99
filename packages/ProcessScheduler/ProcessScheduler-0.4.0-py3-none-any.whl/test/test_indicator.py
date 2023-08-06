# Copyright (c) 2020-2021 Thomas Paviot (tpaviot@gmail.com)
#
# This file is part of ProcessScheduler.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

import unittest

import processscheduler as ps

class TestIndicator(unittest.TestCase):
    def test_indicator_flowtime(self) -> None:
        problem = ps.SchedulingProblem('IndicatorFlowTime', horizon=2)
        t_1 = ps.FixedDurationTask('t1', 2)
        t_2 = ps.FixedDurationTask('t2', 2)

        i_1 = ps.Indicator('FlowTime', t_1.end + t_2.end)

        solution = ps.SchedulingSolver(problem).solve()

        self.assertTrue(solution)
        self.assertEqual(solution.indicators[i_1.name], 4)

    def test_cost_indicator(self) -> None:
        problem = ps.SchedulingProblem('IndicatorResourceCost')
        t_1 = ps.VariableDurationTask('t1', work_amount=100)
        worker_1 = ps.Worker('Worker1', productivity=4, cost_per_period=10)
        worker_2 = ps.Worker('Worker2', productivity=7, cost_per_period=20)
        all_workers = [worker_1, worker_2]
        problem.add_objective_makespan()
        t_1.add_required_resources(all_workers)
        cost_ind = problem.add_indicator_resource_cost(all_workers)

        solution = ps.SchedulingSolver(problem).solve()

        self.assertTrue(solution)
        self.assertEqual(solution.indicators[cost_ind.name], 300)

    def test_resource_utilization_indicator_1(self) -> None:
        problem = ps.SchedulingProblem('IndicatorUtilization1', horizon = 10)
        t_1 = ps.FixedDurationTask('T1', duration=5)
        worker_1 = ps.Worker('Worker1')
        t_1.add_required_resource(worker_1)
        utilization_ind = problem.add_indicator_resource_utilization(worker_1)

        solution = ps.SchedulingSolver(problem).solve()

        self.assertTrue(solution)
        self.assertEqual(solution.indicators[utilization_ind.name], 50)

    def test_resource_utilization_indicator_2(self) -> None:
        """Two tasks, two workers."""
        problem = ps.SchedulingProblem('IndicatorUtilization2', horizon = 10)

        t_1 = ps.FixedDurationTask('T1', duration=5)
        t_2 = ps.FixedDurationTask('T2', duration=5)

        worker_1 = ps.Worker('Worker1')
        worker_2 = ps.Worker('Worker2')

        t_1.add_required_resource(worker_1)
        t_2.add_required_resource(ps.SelectWorkers([worker_1, worker_2]))

        utilization_res_1 = problem.add_indicator_resource_utilization(worker_1)
        utilization_res_2 = problem.add_indicator_resource_utilization(worker_2)

        solution = ps.SchedulingSolver(problem).solve()

        self.assertTrue(solution)
        result_res_1 = solution.indicators[utilization_res_1.name]
        result_res_2 = solution.indicators[utilization_res_2.name]

        # sum should be 100
        self.assertEqual(result_res_1 + result_res_2, 100)

    def test_resource_utilization_indicator_3(self) -> None:
        """Same as above, but both workers are selectable. Force one with resource
        utilization maximization objective."""
        problem = ps.SchedulingProblem('IndicatorUtilization3', horizon = 10)

        t_1 = ps.FixedDurationTask('T1', duration=5)
        t_2 = ps.FixedDurationTask('T2', duration=5)

        worker_1 = ps.Worker('Worker1')
        worker_2 = ps.Worker('Worker2')

        t_1.add_required_resource(ps.SelectWorkers([worker_1, worker_2]))
        t_2.add_required_resource(ps.SelectWorkers([worker_1, worker_2]))

        utilization_res_1 = problem.add_indicator_resource_utilization(worker_1)
        utilization_res_2 = problem.add_indicator_resource_utilization(worker_2)

        ps.MaximizeObjective('MaximieResource1Utilization', utilization_res_1)

        solution = ps.SchedulingSolver(problem).solve()

        self.assertTrue(solution)
        self.assertEqual(solution.indicators[utilization_res_1.name], 100)
        self.assertEqual(solution.indicators[utilization_res_2.name], 0)

    def test_resource_utilization_indicator_4(self) -> None:
        """20 optional tasks, one worker. Force resource utilization maximization objective."""
        problem = ps.SchedulingProblem('IndicatorUtilization4', horizon = 20)

        worker = ps.Worker('Worker')
        
        for i in range(20):
            t = ps.FixedDurationTask(f'T{i+1}', duration = 1, optional = True)
            t.add_required_resource(worker)

        utilization_res = problem.add_indicator_resource_utilization(worker)
        problem.maximize_indicator(utilization_res)

        solution = ps.SchedulingSolver(problem).solve()

        self.assertTrue(solution)
        self.assertEqual(solution.indicators[utilization_res.name], 100)

    def test_resource_utilization_indicator_5(self) -> None:
        """Same input data than previous tests, but we dont use
        an optimisation solver, the objective of 100% is set by an
        additionnal constraint. This should be **much faster**."""
        problem = ps.SchedulingProblem('IndicatorUtilization5', horizon = 20)

        worker = ps.Worker('Worker')

        for i in range(40):
            t = ps.FixedDurationTask(f'T{i+1}', duration = 1, optional = True)
            t.add_required_resource(worker)

        utilization_res = problem.add_indicator_resource_utilization(worker)

        problem.add_constraint(utilization_res.indicator_variable == 100)

        solution = ps.SchedulingSolver(problem).solve()

        self.assertTrue(solution)
        self.assertEqual(solution.indicators[utilization_res.name], 100)


if __name__ == "__main__":
    unittest.main()

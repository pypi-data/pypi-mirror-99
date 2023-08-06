import processscheduler as ps

pb = ps.SchedulingProblem('OptionalCondition2', horizon=9)
task_1 = ps.FixedDurationTask('task1', duration = 9)  # mandatory
task_2 = ps.FixedDurationTask('task2', duration = 4, optional=True) # optional

cond = ps.OptionalTaskConditionSchedule(task_2, pb.horizon > 10)
pb.add_constraint(cond)

solver = ps.SchedulingSolver(pb, verbosity=True)
solution = solver.solve()
print(solution)

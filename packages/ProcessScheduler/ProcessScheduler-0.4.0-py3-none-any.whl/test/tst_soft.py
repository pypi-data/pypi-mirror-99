import processscheduler as ps

"""Task can be scheduled."""
pb = ps.SchedulingProblem('OptionalTaskStartAt1', horizon=6)
task_1 = ps.FixedDurationTask('task1', duration = 3, optional=True)
pb.add_constraint(ps.TaskStartAt(task_1, 1))

# Force schedule, otherwise by default it is not scheduled
pb.add_constraint(task_1.scheduled == True)
solver = ps.SchedulingSolver(pb)
solution = solver.solve()

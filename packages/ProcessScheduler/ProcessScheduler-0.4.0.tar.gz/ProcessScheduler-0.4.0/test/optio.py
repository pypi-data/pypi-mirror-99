#Copyright 2020 Thomas Paviot (tpaviot@gmail.com)
#
#Licensed to the Apache Software Foundation (ASF) under one
#or more contributor license agreements.  See the NOTICE file
#distributed with this work for additional information
#regarding copyright ownership.  The ASF licenses this file
#to you under the Apache License, Version 2.0 (the
#"License"); you may not use this file except in compliance
#with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an
#"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#KIND, either express or implied.  See the License for the
#specific language governing permissions and limitations
#under the License.

import processscheduler as ps
pb = ps.SchedulingProblem('OptionalTaskStartAt1', horizon=6)
task_1 = ps.FixedDurationTask('task1', duration = 3, optional=True)
# # the following tasks should conflict if they are mandatory
cstr1 = ps.TaskStartAt(task_1, 1)
pb.add_constraint(cstr1)
# cstr2 = ps.TaskStartAt(task_1, 2, optional=True)
# cstr3 = ps.TaskEndAt(task_1, 3, optional=True)

# pb.add_constraints([cstr1, cstr2, cstr3])
# # force to apply exactly one constraint
# cstr4 = ps.ForceApplyNOptionalConstraints([cstr1, cstr2, cstr3], 2, kind="atmost")
# pb.add_constraints([cstr4])
solver = ps.SchedulingSolver(pb, verbosity=True)
print(solver)
solution = solver.solve()
print(solution)

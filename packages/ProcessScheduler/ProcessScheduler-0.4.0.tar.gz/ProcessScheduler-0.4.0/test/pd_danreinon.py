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
pb = ps.SchedulingProblem('PbDanReinon', horizon=65)
import random

worker = ps.Worker('Car')

class Student:
    def __init__(self, num_practices_double, num_practice_simple, availability):
        self.num_practices_double = num_practices_double
        self.num_practice_simple = num_practice_simple
        self.availability = availability

student_1 = Student(2, 70, [[1, 6] , [46, 67]])
student_2 = Student(3, 54, [[30, 34], [36, 43]])
students = [student_1, student_2]

id_stud = 0
for student in students:

    num_practices_double = student.num_practices_double
    num_practice_simple = student.num_practice_simple
    availability = student.availability

    # loop for tasks with duration 2
    for i in range(num_practices_double):
        task_duration_2 = ps.FixedDurationTask('task_duration_2_%i_stud_%i' %(i, id_stud), duration = 2, optional=True)
        task_duration_2.add_required_resource(worker)

        all_constraints = []

        for deb, fin in availability:
            ctr1 = ps.TaskStartAfterLax(task_duration_2, deb, optional=True)
            ctr2 = ps.TaskEndBeforeLax(task_duration_2, fin, optional=True)
            all_constraints.append(ctr1)
            all_constraints.append(ctr2)
            pb.add_constraint(ps.and_([ctr1, ctr2]))
            # force both ctr1 and ctr2 to be applied or not applied simultaneously
            pb.add_constraint(ctr1.applied == ctr2.applied)  # the double equal is important

        pb.add_constraint(ps.ForceApplyNOptionalConstraints(all_constraints, 2))

    id_stud += 1
# pb.add_constraints([cstr1, cstr2, cstr3])
# # force to apply exactly one constraint
# cstr4 = ps.ForceApplyNOptionalConstraints([cstr1, cstr2, cstr3], 2, kind="atmost")
# pb.add_constraints([cstr4])
# maximize resource utilization
utilization_res = pb.add_indicator_resource_utilization(worker)
pb.add_constraint(utilization_res.indicator_variable >= 10)

solver = ps.SchedulingSolver(pb, verbosity=False, logic='QF_FD')
print(solver)
solution = solver.solve()
#print(solution)
solution.render_gantt_matplotlib()

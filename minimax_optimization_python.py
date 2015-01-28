# -*- coding: utf-8 -*-
"""
#--Author:  Geoff Ryder
#--Version: 1.0
#--Date:  September 25, 2014
#--Title:  Minimax Optimization Example in Python
#--Input:  Hard-coded
#--Output:  Optimal values of two decision variables
#--Requirements:  Python 2.7 or later, module pulp
#..See:  http://code.google.com/p/pulp-or/
#
#--Notes:
Goal programming (GP) optimization of two decision variables, 
against 3 constraints, using the minimax approach.

Uses the open source PULP wrapper for the COIN-OR solver.
The solver comes bundled with the wrapper, so you don't need to download COIN-OR.
Based on the GP investment problem presented on page 317 in Ragsdale:
Spreadsheet Modeling and Decision Analysis 5e
Cliff T. Ragsdale, 2008

MIN: Q
subject to
12 x1 + 4 x2 >= 48
4 x1 + 4 x2 >= 28
10 x1 + 20 x2 >= 100

w1(40 X1 + 32 X2 - 244)/244 <= Q
w2(800 X1 + 1250 X2 - 6950)/6950 <= Q
w3(0.2 X1 + 0.45 X2 - 2)/2 <= Q
X1, X2 >= 0
w1, w2, w3 are positive constants (for now I'll let them equal 1)

#--THE TRICK is to rewrite the minimax constraints in the normal way
#--Just reduce them algebraically, let X3 = Q, e.g. the first constr becomes:
w1 .1639 x1 + w1 .1311 x2 - x3 <= w1 (244/244) = 1
w2 .1151 x1 + w1 .1799 x2 - x3 <= w2 (6950/6950)
w3 .1 x1 + 0.225 x2 - x3 <= w3 (2/2)


"""
#######################
#--Use PULP plus COIN LP
from pulp import *
pulp.pulpTestAll() #--OK!  Comes with COIN LP already

# Create a list of the decision variables
decision_variables = ['X1','X2','X3']
obj_func_coeff = {'X1':0,'X2':0,'X3':1.0}
#--Constraint coefficients in constraint matrix A
A_row_1 = {'X1':12, 'X2':4, 'X3':0}
A_row_2 = {'X1':4, 'X2':4, 'X3':0}
A_row_3 = {'X1':10, 'X2':20, 'X3':0}
#--later, these minimax constraints will be derived from prior steps...
#--let the weightings w1, w2, w3 be 1 for now
W1 = 1.0
W2 = 1.0
W3 = 1.0
A_row_4 = {'X1':W1*0.1639, 'X2':W1*0.1311, 'X3': -1.0}
A_row_5 = {'X1':W2*0.1151, 'X2':W2*0.1799, 'X3': -1.0}
A_row_6 = {'X1':W3*0.1, 'X2':W3*0.225, 'X3': -1.0}

#--Create the problem variable, to contain the problem data
prob = LpProblem("Minimax Goal Programming LP Framework",LpMinimize)

#--A dictionary for the decision variables
decision_vars_dict = LpVariable.dicts("Dec_X",decision_variables,lowBound=0,cat='Continuous')

#--The obj function is added to 'prob' first
prob += lpSum([obj_func_coeff[i]*decision_vars_dict[i] for i in decision_variables]), "Minimax objective"

#--Add the constraints
prob += lpSum([A_row_1[i]*decision_vars_dict[i] for i in decision_variables]) >= 48, "A_row_1"
prob += lpSum([A_row_2[i]*decision_vars_dict[i] for i in decision_variables]) >= 28, "A_row_2"
prob += lpSum([A_row_3[i]*decision_vars_dict[i] for i in decision_variables]) >= 100, "A_row_3"
prob += lpSum([A_row_4[i]*decision_vars_dict[i] for i in decision_variables]) <= 1.0, "A_row_4"
prob += lpSum([A_row_5[i]*decision_vars_dict[i] for i in decision_variables]) <= 1, "A_row_5"
prob += lpSum([A_row_6[i]*decision_vars_dict[i] for i in decision_variables]) <= 1, "A_row_6"

#--Write the problem to an .lp file
prob.writeLP("MinimaxModel.lp")

#--Use the COIN OR solver included
prob.solve()

#--Print status
print "Status: ",LpStatus[prob.status]

#--Print each variable, with its optimum value--defines the efficient frontier
for v in prob.variables():
    print v.name,"=",v.varValue
    
#--Print the opt result for the objective
print "Optimal value of Q:",value(prob.objective)





























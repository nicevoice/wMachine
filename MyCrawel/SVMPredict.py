from libsvm_3_17.python.svmutil import *
import os
import sys
import string

# "models/"
ARGS_MODEL = sys.argv[1]
# "testcases/"
ARGS_TCASE = sys.argv[2]
# number of cases
ARGS_DNUMS = string.atoi(sys.argv[3])

print "# %s"%ARGS_DNUMS

print "# Reading Testcase %s..." %ARGS_TCASE
y, x = svm_read_problem('testcases/' + ARGS_TCASE + '.txt')
print "# Reading Model %s..." %ARGS_MODEL
m = svm_load_model('models/' + ARGS_MODEL + '.model')

# p_label. p_acc, p_val = svm_predict(y, x, m, '-c 4')
print "# Running Prediction ..."
p_label, p_acc, p_val = svm_predict(y[:ARGS_DNUMS], x[:ARGS_DNUMS], m)
print "# Results: "
print p_label
print "# done."
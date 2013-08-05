from libsvm_3_17.python.svmutil import *
import os
import sys
import string

ARGS_CATEGORY = sys.argv[1]
# numbers of records
ARGS_TSETNUMS = string.atoi(sys.argv[2])

print "# Reading Problems %s..." %ARGS_CATEGORY
y, x = svm_read_problem('input_full/' + ARGS_CATEGORY + "_input.txt")
print "# Training..."
m = svm_train(y[:ARGS_TSETNUMS],x[:ARGS_TSETNUMS],'-c 4')
print "# Saving Model..."
svm_save_model('models/' + ARGS_CATEGORY + '.model', m)
print "# done."

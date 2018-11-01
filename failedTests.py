import filecmp
import glob
import os


def output_compare(root):
    failed = []
    for method_path in glob.iglob(root+'/*'):
        for output_path in glob.iglob(method_path+'/expected_outputs/*'):
            testname = os.path.basename(output_path)
            if (not filecmp.cmp(output_path, method_path+'/outputs/'+testname)):
                failed.append(testname)
    return failed


print(output_compare("./Tests"))

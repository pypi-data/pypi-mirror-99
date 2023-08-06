"""
Unit tests for the various LSL IPython notebooks.
"""

# Python2 compatibility
from __future__ import print_function, division, absolute_import
import sys
if sys.version_info < (3,):
    range = xrange
    
import unittest
import glob
import sys
import re
import os

currentDir = os.path.abspath(os.getcwd())
if os.path.exists(os.path.join(currentDir, '..', 'docs', 'notebooks')):
    MODULE_BUILD = os.path.join(currentDir, '..', 'docs', 'notebooks')
else:
    MODULE_BUILD = None

run_notebooks_tests = False
try:
    import jupyter_client
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    if MODULE_BUILD is not None:
        run_notebooks_tests = True
except ImportError:
    pass


__version__  = "0.1"
__author__   = "Jayce Dowell"


def run_notebook(notebook_path, kernel_name=None):
    """
    From:
        http://www.blog.pythonlibrary.org/2018/10/16/testing-jupyter-notebooks/
    """
    
    nb_name, _ = os.path.splitext(os.path.basename(notebook_path))
    dirname = os.path.dirname(notebook_path)
    
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
        
    proc = ExecutePreprocessor(timeout=600, kernel_name=kernel_name)
    proc.allow_errors = True
    
    proc.preprocess(nb, {'metadata': {'path': '/'}})
    output_path = os.path.join(dirname, '{}_all_output.ipynb'.format(nb_name))
    
    with open(output_path, mode='wt') as f:
        nbformat.write(nb, f)
    errors = []
    for cell in nb.cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                if output.output_type == 'error':
                    errors.append(output)
    return nb, errors


@unittest.skipUnless(run_notebooks_tests, "requires the 'nbformat' and 'nbconvert' modules")
class notebooks_tests(unittest.TestCase):
    """A unittest.TestCase collection of unit tests for the LSL IPython notebooks."""
    
    def setUp(self):
        self.maxDiff = 8192
        
        self._kernel = jupyter_client.KernelManager()
        self._kernel.start_kernel()
        self.kernel_name = self._kernel.kernel_name
        
    def tearDown(self):
        self._kernel.shutdown_kernel()
        self.kernel_name = None


def _test_generator(notebook):
    """
    Function to build a test method for each notebook that is provided.  
    Returns a function that is suitable as a method inside a unittest.TestCase
    class
    """
    
    def test(self):
        nb, errors = run_notebook(notebook, kernel_name=self.kernel_name)
        
        message = ''
        if len(errors) > 0:
            for error in errors:
                message += '%s: %s\n' % (error['ename'], error['evalue'])
                for line in error['traceback']:
                    message += '  %s\n' % line
        self.assertEqual(errors, [], message)
        
    return test


_NOTEBOOKS = glob.glob(os.path.join(MODULE_BUILD, '*.ipynb'))
_NOTEBOOKS.sort()
for notebook in _NOTEBOOKS:
    test = _test_generator(notebook)
    name = 'test_%s' % os.path.splitext(os.path.basename(notebook))[0].replace(' ', '_')
    doc = """Execution of the '%s' notebook.""" % os.path.basename(notebook)
    setattr(test, '__doc__', doc)
    setattr(notebooks_tests, name, test)


class notebooks_test_suite(unittest.TestSuite):
    """A unittest.TestSuite class which contains all of the LSL IPython
    notebook tests."""
    
    def __init__(self):
        unittest.TestSuite.__init__(self)
        
        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(notebooks_tests))


if __name__ == '__main__':
    unittest.main()
    

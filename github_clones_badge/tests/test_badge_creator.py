import os
import unittest
from github_clones_badge.get_github_clones  import git_clones_counter


class git_clones_counterTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def init_test(self):
        from github_clones_badge import get_github_clones as ghc
        gc=git_clones_counter(reponame, username=os.environ['GITUSR'], password=os.environ['GITPASS'])

#       self.assertTrue(sl.LTA_location==None)


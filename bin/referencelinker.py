#!/usr/bin/env python
from teimanipulate import *

__author__ = "Martin Paul Eve"
__email__ = "martin@martineve.com"

"""
A class that looks for references to link in an NLM file and joins them to the corresponding reference entry

"""

from debug import Debuggable
from nlmmanipulate import NlmManipulate
import re
import lxml


class ReferenceLinker(Debuggable):
    def __init__(self, global_variables):
        self.gv = global_variables
        self.debug = self.gv.debug
        Debuggable.__init__(self, 'Reference Linker')

    def run(self):
        manipulate = NlmManipulate(self.gv)

        tree = manipulate.load_dom_tree()

        ref_items = tree.xpath('//back/ref-list/ref')

        if len(ref_items) == 0:
            self.debug.print_debug(self, 'Found no references to link')
            return

        for p in tree.xpath('//p'):
            text = manipulate.get_stripped_text(p)

            reference_test = re.compile('\((?P<text>.+?)\)')
            matches = reference_test.finditer(text)

            for match in matches:

                for item in match.group('text').split(u';'):

                    bare_items = item.strip().replace(u',', '').split(u' ')

                    for ref in ref_items:
                        found = True

                        bare_ref = manipulate.get_stripped_text(ref)

                        for sub_item in bare_items:
                            if not sub_item in bare_ref:
                                found = False

                        if len(bare_items) > 0 and found:
                            print item
                            print bare_ref



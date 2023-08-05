# Copyright (C) 2012  Michael Hewner, Isaiah Mayerchak
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__author__ = "isaiahmayerchak"

from docutils import nodes
from docutils.parsers.rst import directives
from runestone.mchoice import Assessment
from runestone.server.componentdb import (
    addQuestionToDB,
    addHTMLToDB,
    maybeAddToAssignment,
)
from runestone.common.runestonedirective import RunestoneIdNode, add_i18n_js


def setup(app):
    app.add_directive("parsonsprob", ParsonsProblem)
    app.add_node(ParsonsNode, html=(visit_parsons_node, depart_parsons_node))
    app.add_config_value("parsons_div_class", "runestone", "html")


TEMPLATE_START = """
        <div class="%(divclass)s" style="max-width: none;"> 
        <div data-component="parsons" id="%(divid)s" class="alert alert-warning parsons" >
        <div class="parsons_question parsons-text" >
    """

TEMPLATE_END = """
        </div>
        <pre  data-question_label="%(question_label)s"  %(adaptive)s %(maxdist)s %(order)s %(noindent)s %(language)s %(numbered)s %(optional)s style="visibility: hidden;">
        %(code)s
        </pre>
        </div>
        </div>
    """


class ParsonsNode(nodes.General, nodes.Element, RunestoneIdNode):
    def __init__(self, options, **kwargs):
        super(ParsonsNode, self).__init__(**kwargs)
        self.runestone_options = options


def visit_parsons_node(self, node):
    div_id = node.runestone_options["divid"]
    components = dict(node.runestone_options)
    components.update({"divid": div_id})
    node.delimiter = "_start__{}_".format(node.runestone_options["divid"])
    self.body.append(node.delimiter)
    res = TEMPLATE_START % components
    self.body.append(res)


def depart_parsons_node(self, node):
    res = TEMPLATE_END % node.runestone_options
    self.body.append(res)
    addHTMLToDB(
        node.runestone_options["divid"],
        node.runestone_options["basecourse"],
        "".join(self.body[self.body.index(node.delimiter) + 1 :]),
    )
    self.body.remove(node.delimiter)


class ParsonsProblem(Assessment):
    """
    .. parsonsprob:: unqiue_problem_id_here
       :maxdist:
       :order:
       :language:
       :noindent:
       :adaptive:
       :numbered:

       Solve my really cool parsons problem...if you can.
       -----
       def findmax(alist):
       =====
          if len(alist) == 0:
             return None
       =====
          curmax = alist[0]
          for item in alist:
       =====
             if item &gt; curmax:
       =====
                curmax = item
       =====
          return curmax


    config values (conf.py):

    - parsons_div_class - custom CSS class of the component's outermost div
    """

    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = Assessment.option_spec.copy()
    option_spec.update(
        {
            "maxdist": directives.unchanged,
            "order": directives.unchanged,
            "language": directives.unchanged,
            "noindent": directives.flag,
            "adaptive": directives.flag,
            "numbered": directives.unchanged,
        }
    )
    has_content = True

    def run(self):
        """

           Instructions for solving the problem should be written and then a line with -----
           signals the beginning of the code.  If you want more than one line in a single
           code block, seperate your code blocks with =====.

           Both the instructions sections and code blocks are optional. If you don't include any
           =====, the code will assume you want each line to be its own code block.

        Example:

        .. parsonsprob:: unqiue_problem_id_here

           Solve my really cool parsons problem...if you can.
           -----
           def findmax(alist):
           =====
              if len(alist) == 0:
                 return None
           =====
              curmax = alist[0]
              for item in alist:
           =====
                 if item &gt; curmax:
           =====
                    curmax = item
           =====
              return curmax


        """

        super(ParsonsProblem, self).run()
        addQuestionToDB(self)

        env = self.state.document.settings.env
        self.options["instructions"] = ""
        self.options["code"] = self.content
        self.options["divclass"] = env.config.parsons_div_class

        if "numbered" in self.options:
            self.options["numbered"] = (
                ' data-numbered="' + self.options["numbered"] + '"'
            )  #' data-numbered="true"'
        else:
            self.options["numbered"] = ""

        if "maxdist" in self.options:
            self.options["maxdist"] = ' data-maxdist="' + self.options["maxdist"] + '"'
        else:
            self.options["maxdist"] = ""
        if "order" in self.options:
            self.options["order"] = ' data-order="' + self.options["order"] + '"'
        else:
            self.options["order"] = ""
        if "noindent" in self.options:
            self.options["noindent"] = ' data-noindent="true"'
        else:
            self.options["noindent"] = ""
        if "adaptive" in self.options:
            self.options["adaptive"] = ' data-adaptive="true"'
        else:
            self.options["adaptive"] = ""
        if "language" in self.options:
            self.options["language"] = (
                ' data-language="' + self.options["language"] + '"'
            )
        else:
            self.options["language"] = ""

        if "-----" in self.content:
            index = self.content.index("-----")
            self.options["instructions"] = self.content[:index]
            self.options["code"] = self.content[index + 1 :]
        else:
            self.options["instructions"] = ["Arrange the blocks"]

        if "=====" in self.options["code"]:
            self.options["code"] = "\n".join(self.options["code"])

            self.options["code"] = self.options["code"].replace("=====", "---")
        else:
            self.options["code"] = "\n".join(self.options["code"])

        self.assert_has_content()

        maybeAddToAssignment(self)
        parsons_node = ParsonsNode(self.options, rawsource=self.block_text)
        parsons_node.source, parsons_node.line = self.state_machine.get_source_and_line(
            self.lineno
        )
        self.state.nested_parse(
            self.options["instructions"], self.content_offset, parsons_node
        )
        # explain_text is a list.
        return [parsons_node]

#######################################################################
# Name: robot_peg.py
# Purpose: Simple DSL for defining robot movement (PEG version).
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2011 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#
# This example is inspired by an example from LISA tool (http://labraj.uni-mb.si/lisa/)
# presented during the lecture given by prof. Marjan Mernik (http://lpm.uni-mb.si/mernik/)
# at the University of Novi Sad in June, 2011.
#
# An example of the robot program:
#    begin
#        up
#        up
#        left
#        down
#        right
#    end
#######################################################################

from arpeggio import *
from arpeggio.export import PMDOTExporter, PTDOTExporter
from arpeggio.peg import ParserPEG

# Grammar rules
robot_grammar = '''
program <- 'begin' (command)* 'end' EndOfFile;
command <- UP/DOWN/LEFT/RIGHT;
UP <- 'up';
DOWN <- 'down';
LEFT <- 'left';
RIGHT <- 'right';
'''

# Semantic actions
from robot import Up, Down, Left, Right, Command, Program
semantic_actions = {
    'program': Program(),
    'command': Command(),
    'UP': Up(),
    'DOWN': Down(),
    'LEFT': Left(),
    'RIGHT': Right()
}


if __name__ == "__main__":
    try:

        # Program code
        input = '''
            begin
                up
                up
                left
                down
                right
            end
        '''


        # First we will make a parser - an instance of the robot parser model.
        # Parser model is given in the form of PEG specification therefore we
        # are using ParserPEG class.
        parser = ParserPEG(robot_grammar, 'program', debug=True)

        # Then we export it to a dot file in order to visualize it.
        # This step is optional but it is handy for debugging purposes.
        # We can make a png out of it using dot (part of graphviz) like this
        # dot -O -Tpng robot_peg_parser_model.dot
        PMDOTExporter().exportFile(parser.parser_model,
                        "robot_peg_parser_model.dot")

        # We create a parse tree out of textual input
        parse_tree = parser.parse(input)

        # Then we export it to a dot file in order to visualize it.
        # dot -O -Tpng robot_peg_parse_tree.dot
        PTDOTExporter().exportFile(parse_tree,
                        "robot_peg_parse_tree.dot")

        # getASG will start semantic analysis.
        # In this case semantic analysis will evaluate expression and
        # returned value will be the final position of the robot.
        print "position = ", parser.getASG(sem_actions=semantic_actions)

    except NoMatch, e:
        print "Expected %s at position %s." % (e.value, str(e.parser.pos_to_linecol(e.position)))

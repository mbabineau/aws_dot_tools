#!/usr/bin/env python
# encoding: utf-8
"""
Description:
Outputs a DOT graph of your EC2 instances by security group

Copying:
This file is part of AWS DOT Tools <http://github.com/mbabineau/aws_dot_tools>

AWS DOT Tools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AWS DOT Tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AWS DOT Tools.  If not, see <http://www.gnu.org/licenses/>.

Copyright (c) 2010 Mike Babineau <michael.babineau@gmail.com>. All rights reserved.
"""

import boto     # http://code.google.com/p/boto/
import gvgen    # http://software.inl.fr/trac/wiki/GvGen

def get_instances_by_security_group():
    """Queries EC2 and returns a dictionary of {group: [instances]} pairs"""
    c = boto.connect_ec2()
    reservations = c.get_all_instances()
    
    results = {}
    for r in reservations:
        for g in r.groups:
            group_instances = []
            for i in r.instances: group_instances.append(i.id)
            # If group already exists, combine old and new instance lists
            if results.has_key(g.id):
                results[g.id] += group_instances
            else:
                results.update({g.id: group_instances})
    
    return results
    
def main():
    graph = gvgen.GvGen()
    groups = get_instances_by_security_group()
    
    # Put graph items in a dict for easy reference
    items = {}
    for g in groups.keys():
        items.update({g: graph.newItem(g)})
        for i in groups[g]:
            # Don't duplicate instances
            if not items.has_key(i): items.update({i: graph.newItem(i)})
            graph.newLink(items[g], items[i])
    
    # Generate the dot code
    graph.dot()

if __name__ == '__main__':
    main()

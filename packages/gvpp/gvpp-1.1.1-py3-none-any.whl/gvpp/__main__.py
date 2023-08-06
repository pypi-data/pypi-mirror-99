# Copyright 2016, Sinestrea <git.sinestrea@gmail.com>
#
# This file is part of "gvpp".
#
# "gvpp" is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# "gvpp" is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# "gvpp". If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

from argparse import ArgumentParser, FileType
from sys import stdin

from gvpp import Animation, render, gif

def main():

	parser = ArgumentParser( prog = 'gvpp' )
	parser.add_argument( 'animation', nargs = '?', type = FileType( 'r' ), default = stdin, help = 'The file containing animation commands (default: stdin)' )
	parser.add_argument( '--delay', '-d', default = '100', help = 'The delay (in ticks per second, default: 100)' )
	parser.add_argument( 'basename', help = 'The basename of the generated file' )
	args = parser.parse_args()

	ga = Animation()
	ga.parse( args.animation )
	gif( render( ga.graphs(), args.basename, 'png' ), args.basename, args.delay )

if __name__ == '__main__':
	main()

#!/usr/bin/env python
"""
Copyright (c) 2010 MakerBot Industries

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
import inkex
from timsav_gcode.context import GCodeContext
from timsav_gcode.svg_parser import SvgParser


class TimSavGCodeGenerator(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.setup()
        self.context = None

    def setup(self):
        self.arg_parser.add_argument("--pen-up-speed",
                                     action="store", type=float,
                                     dest="pen_up_speed", default="1000",
                                     help="Pen Up Speed")
        self.arg_parser.add_argument("--pen-down-speed",
                                     action="store", type=float,
                                     dest="pen_down_speed", default="3000",
                                     help="Pen Down Speed")
        self.arg_parser.add_argument("--pen-up-z",
                                     action="store", type=float,
                                     dest="pen_up_z", default="10.0",
                                     help="Pen Up Z")
        self.arg_parser.add_argument("--pen-down-z",
                                     action="store", type=float,
                                     dest="pen_down_z", default="-10.0",
                                     help="Pen Down Z")
        self.arg_parser.add_argument("--pen-score-z",
                                     action="store", type=float,
                                     dest="pen_score_z", default="-5.0",
                                     help="Pen Score Z")
        self.arg_parser.add_argument("--pen-draw-z",
                                     action="store", type=float,
                                     dest="pen_mark_z", default="-2.0",
                                     help="Pen Mark Z")
        self.arg_parser.add_argument("--xy-feedrate",
                                     action="store", type=float,
                                     dest="xy_feedrate", default="2000.0",
                                     help="XY axes feedrate in mm/min")
        self.arg_parser.add_argument("--xy-travelrate",
                                     action="store", type=float,
                                     dest="xy_travelrate", default="7000.0",
                                     help="XY axes travelrate in mm/min")
        self.arg_parser.add_argument("--z-feedrate",
                                     action="store", type=float,
                                     dest="z_feedrate", default="500.0",
                                     help="Z axis feedrate in mm/min")
        self.arg_parser.add_argument("--z-height",
                                     action="store", type=float,
                                     dest="z_height", default="0.0",
                                     help="Z axis print height in mm")
        self.arg_parser.add_argument("--tab",
                                     action="store", type=str,
                                     dest="tab")

    def save_raw(self, ret):
        self.context.generate()

    def effect(self):
        self.context = GCodeContext(self.options.xy_feedrate,
                                    self.options.xy_travelrate,
                                    self.options.z_feedrate,
                                    self.options.pen_up_speed,
                                    self.options.pen_down_speed,
                                    self.options.pen_up_z,
                                    self.options.pen_down_z,
                                    self.options.pen_score_z,
                                    self.options.pen_mark_z,
                                    self.options.input_file)
        parser = SvgParser(self.document.getroot())
        parser.parse()
        for entity in parser.entities:
            entity.get_gcode(self.context)


if __name__ == '__main__':  # pragma: no cover
    generator = TimSavGCodeGenerator()
    generator.run()

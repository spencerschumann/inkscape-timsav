class GCodeContext:
    def __init__(self, xy_feedrate, xy_travelrate, z_feedrate, pen_up_speed, pen_down_speed,
                 pen_up_z, pen_down_z, pen_score_z, pen_mark_z, file):
        self.xy_feedrate = xy_feedrate
        self.xy_travelrate = xy_travelrate
        self.z_feedrate = z_feedrate
        self.pen_up_speed = pen_up_speed
        self.pen_down_speed = pen_down_speed
        self.pen_up_z = pen_up_z
        self.pen_down_z = pen_down_z
        self.pen_score_z = pen_score_z
        self.pen_mark_z = pen_mark_z
        self.x_home = 0
        self.y_home = 0
        self.z_height = 0
        self.file = file

        self.drawing = False
        self.last = None

        self.preamble = [
            "G21 (metric ftw)",
            "G90 (absolute mode)",
            "G92 X%.2f Y%.2f Z%.2f (you are here)" % (self.x_home, self.y_home, self.z_height),
            "G0 F%0.2f (Travel Feed Rate)" % self.xy_travelrate,
            "G1 F%0.2f (Cut Feed Rate)" % self.xy_feedrate,
            "G0 F%0.2f (Z Feed Rate)" % self.z_feedrate,
            "S%.2f (Pen Up Speed)" % self.pen_up_speed,
            "M3 (Start cutter)",
            "G0 Z%.2f (Pen Up)" % self.pen_up_z,
            ""
        ]

        self.postscript = [
            "",
            "(end of print job)",
            "S%.2f (pen up speed)" % self.pen_up_speed,
            "G0 Z%.2f" % self.pen_up_z,
            "M5 (Stop cutter)",
            "G0 X%0.2F Y%0.2F F%0.2F (go home)" % (self.x_home, self.y_home, self.xy_travelrate),
        ]

        self.codes = []


    def generate(self):
        code_sets = [self.preamble]
        code_sets.append(self.codes)

        for codeset in code_sets:
            for line in codeset:
                print(line)
        for line in self.postscript:
            print(line)


    def start(self, cut_type):
        if cut_type == 2:
            self.codes.append("G0 Z%.2f S%0.2f (pen down score)" % (self.pen_score_z, self.pen_down_speed))
        elif cut_type == 3:
            self.codes.append("G0 Z%.2f S%0.2f (pen down draw)" % (self.pen_mark_z, self.pen_down_speed))
        else:
            self.codes.append("G0 Z%.2f S%0.2F (pen down through)" % (self.pen_down_z, self.pen_down_speed))
        self.drawing = True


    def stop(self):
        self.codes.append("G0 Z%.2f S%.2f (Pen Up)" % (self.pen_up_z, self.pen_up_speed))
        self.drawing = False

    def go_to_point(self, x, y, stop=False):
        if self.last == (x, y):
            return
        if stop:
            return
        else:
            if self.drawing:
                self.codes.append("G0 Z%.2f S%.2f (Pen Up)" % (self.pen_up_z, self.pen_up_speed))
                self.drawing = False
            self.codes.append("G0 X%.2f Y%.2f " % (x, y))
        self.last = (x, y)

    def draw_to_point(self, x, y, stop=False):
        if self.last == (x, y):
            return
        if stop:
            return
        else:
            if not self.drawing:
                self.codes.append("G0 Z%.2f S%0.2F (pen down through)" % (self.pen_down_z, self.pen_down_speed))
                self.drawing = True
            self.codes.append("G1 X%0.2f Y%0.2f " % (x, y))
        self.last = (x, y)

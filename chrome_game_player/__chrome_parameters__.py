class FullScreenPara():
    def __init__(self):
        # ============ information
        self.DINOSAUR_POSITION = ((78, 569), (207, 706))  # ((left, top), (right, bottom))
        self.BACK_GROUND = ((140, 160), (145, 165))

        # ============ settings
        self.detect_area_size = (300, 137)
        self.detect_area = ((490, 569), (self.detect_area_size[0] + 490, self.detect_area_size[1] + 569))

    def print_para(self):
        print(self.DINOSAUR_POSITION)
        print(self.detect_area_size)
        print(self.detect_area)

def normal_mode():
    pass


if __name__ == "__main__":
    para = FullScreenPara()
    para.print_para()

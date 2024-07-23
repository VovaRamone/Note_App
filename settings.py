class Settings:
    def __init__(self):
        self.theme = "light"
        self.font_size = 12

    def change_theme(self, theme):
        self.theme = theme

    def change_font_size(self, size):
        self.font_size = size

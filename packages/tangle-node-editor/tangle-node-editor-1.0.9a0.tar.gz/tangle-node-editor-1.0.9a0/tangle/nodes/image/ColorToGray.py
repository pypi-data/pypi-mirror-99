import logging
logging.basicConfig(level=logging.DEBUG)

from ..image_node import ImageNode
from ...core import socket_types as socket_types
from ...core.Constants import Colors

from PIL import ImageQt

class ColorToGray(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(ColorToGray, self).__init__(scene, title_background_color=Colors.color_to_gray, x=x, y=y)
        self.change_title("to_gray")

        self.input_image, self.output_image = self.add_input_output(socket_types.PictureSocketType(self), "Gray")
        self.output_image.override_color(Colors.gray)



    def compute(self, force=False):
        if self.input_image.is_connected():
            self.input_image.fetch_connected_value()

            converted = self.input_image.get_value().convert("L")

            self.output_image.set_value(converted)

            pixmap = ImageQt.toqpixmap(converted)
            self.set_pixmap(pixmap)

            super().compute(force=force)
            self.set_dirty(False)


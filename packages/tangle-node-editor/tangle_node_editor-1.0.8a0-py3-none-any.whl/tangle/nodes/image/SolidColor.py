from PySide2.QtWidgets import *

from ..image_node import ImageNode
from ...core import socket_types as socket_types

from PIL import Image, ImageQt


class SolidColor(ImageNode):
    def __init__(self, scene, x=0, y=0):
        super(SolidColor, self).__init__(scene, x=x, y=y)
        self.change_title("solid_color")

        self.input_size = self.add_input(socket_types.TupleSocketType(self), "size")
        self.output_image = self.add_output(socket_types.PictureSocketType(self), "out")

        self.solid_color_image = Image.new("RGB", (100, 100))

        self.chk_rgba = self.add_checkbox("Output is RGBA image", checked=False)
        self.add_button("Pick color", self.pick_color)


    def pick_color(self):
        color_dialog = QColorDialog()
        color = color_dialog.getColor()

        size = self.input_size.get_value() or (100, 100)

        if color is not None:
            if self.chk_rgba.isChecked():
                img = Image.new("RGBA", size, (color.rgba()))
            else:
                img = Image.new("RGB", size, (color.red(), color.green(), color.blue()))

            pixmap = ImageQt.toqpixmap(img)
            self.set_pixmap(pixmap)
            self.output_image.set_value(img)

        self.scene.get_main_window().load_values_ui()

        self.set_dirty(True)
        self.compute()


    def get_size(self):
        return self.input_size.get_value() or (100, 100)

    def update_node(self):
        self.set_dirty(True)
        self.compute()

    def compute(self, force=False):
        if self.input_size.is_connected():
            if self.output_image.get_value() is not None:
                resized = self.output_image.get_value().resize(self.get_size())
                self.output_image.set_value(resized)

                pixmap = ImageQt.toqpixmap(resized)
            else:
                pixmap = ImageQt.toqpixmap(self.solid_color_image)

            self.set_pixmap(pixmap)
            super().compute(force=force)
            self.set_dirty(False)

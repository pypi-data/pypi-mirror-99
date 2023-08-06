#!/usr/bin/env python
"""
Dialog on top of a text area.

During start-up, the dialog will be displayed. Press tab, then enter to select
the OK button and quit the dialog. Then the main window will be focused.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    Float,
    FloatContainer,
    HSplit,
)
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Button, Dialog, Label, TextArea


class TextInputDialog:
    def __init__(self, title="", label_text="", completer=None):
        self.visible = True

        def accept():
            self.visible = False
            get_app().layout.focus(text_area)

        self.text_area = TextArea(
            completer=completer,
            multiline=False,
            width=D(preferred=40),
        )

        ok_button = Button(text="OK", handler=accept)

        self.dialog = Dialog(
            title=title,
            body=HSplit([Label(text=label_text), self.text_area]),
            buttons=[ok_button],
            width=D(preferred=80),
            modal=True,
        )

        self.container = ConditionalContainer(
            self.dialog,
            Condition(lambda: self.visible),
        )

    def __pt_container__(self):
        return self.container


# Global key bindings.
bindings = KeyBindings()


@bindings.add("c-c")
def _(event):
    event.app.exit()


text_area = TextArea(
    text="Hello",
    scrollbar=True,
    line_numbers=True,
)
dialog = TextInputDialog("Test dialog")

root_container = FloatContainer(
    content=text_area,
    floats=[Float(content=dialog)],
    key_bindings=bindings,
)

layout = Layout(root_container, focused_element=dialog)


application = Application(
    layout=layout,
    enable_page_navigation_bindings=True,
    mouse_support=True,
    full_screen=True,
)


def run():
    application.run()


if __name__ == "__main__":
    run()

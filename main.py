from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


Window.clearcolor = (0.055, 0.065, 0.09, 1)


class RoundedPanel(BoxLayout):
    def __init__(self, panel_color=(0.09, 0.105, 0.14, 1), radius=24, **kwargs):
        super().__init__(**kwargs)
        self.panel_color = panel_color
        self.radius = radius
        with self.canvas.before:
            self._color = Color(*self.panel_color)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(self.radius)])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size


class CalcButton(Button):
    def __init__(self, text, role="number", **kwargs):
        colors = {
            "number": (0.12, 0.14, 0.19, 1),
            "operator": (0.18, 0.23, 0.34, 1),
            "accent": (0.35, 0.48, 1.0, 1),
            "utility": (0.20, 0.23, 0.30, 1),
        }
        text_colors = {
            "number": (0.94, 0.95, 0.98, 1),
            "operator": (0.67, 0.77, 1.0, 1),
            "accent": (1, 1, 1, 1),
            "utility": (0.80, 0.85, 0.95, 1),
        }
        super().__init__(
            text=text,
            font_size="22sp",
            bold=(role == "accent"),
            color=text_colors[role],
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            **kwargs
        )
        self.role = role
        self.panel_color = colors[role]
        with self.canvas.before:
            self._bg_color = Color(*self.panel_color)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *_):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size


class DarkCalculator(MDApp):
    def build(self):
        self.title = "Nova Calculator"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.expression = ""
        self.just_evaluated = False

        root = BoxLayout(orientation="vertical", padding=[dp(18), dp(18), dp(18), dp(14)], spacing=dp(14))

        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(64), spacing=dp(2))
        header.add_widget(Label(
            text="[b]NOVA[/b]  [color=8EA6FF]CALCULATOR[/color]",
            markup=True, font_size="18sp", halign="left", valign="middle",
            color=(0.95, 0.96, 1, 1), size_hint_y=None, height=dp(30)
        ))
        header.add_widget(Label(
            text="A simple, modern calculator",
            font_size="12sp", color=(0.53, 0.58, 0.68, 1),
            halign="left", valign="middle", size_hint_y=None, height=dp(22)
        ))
        root.add_widget(header)

        display = RoundedPanel(orientation="vertical", padding=[dp(18), dp(16)], spacing=dp(8),
                               size_hint_y=None, height=dp(170), panel_color=(0.09, 0.105, 0.15, 1))
        self.history_label = Label(
            text="READY", color=(0.53, 0.60, 0.75, 1), font_size="13sp",
            halign="right", valign="middle", size_hint_y=0.35
        )
        self.display_label = Label(
            text="0", color=(0.97, 0.98, 1, 1), font_size="38sp",
            halign="right", valign="middle", size_hint_y=0.65
        )
        self.history_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        self.display_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
        display.add_widget(self.history_label)
        display.add_widget(self.display_label)
        root.add_widget(display)

        keys = [
            [("AC", "utility"), ("±", "utility"), ("%", "utility"), ("÷", "operator")],
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("−", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
            [("⌫", "utility"), ("0", "number"), (".", "number"), ("=", "accent")],
        ]
        grid = GridLayout(cols=4, spacing=dp(10), size_hint_y=1)
        for row in keys:
            for caption, role in row:
                btn = CalcButton(caption, role=role)
                btn.bind(on_release=self.on_key)
                grid.add_widget(btn)
        root.add_widget(grid)

        root.add_widget(Label(
            text="Designed for Android  •  NOVA",
            font_size="11sp", color=(0.40, 0.45, 0.55, 1),
            size_hint_y=None, height=dp(18)
        ))
        return root

    def on_key(self, button):
        key = button.text
        current = self.expression

        if key == "AC":
            self.expression = ""
            self.history_label.text = "CLEARED"
            self._show("0")
            return

        if key == "⌫":
            self.expression = current[:-1]
            self._show(self.expression or "0")
            return

        if key == "±":
            if not current:
                return
            try:
                value = self._evaluate(current)
                self.expression = str(-value)
                self._show(self.expression)
            except Exception:
                self._show("Invalid expression")
            return

        if key == "%":
            if not current:
                return
            try:
                value = self._evaluate(current) / 100
                self.expression = self._format(value)
                self._show(self.expression)
            except Exception:
                self._show("Invalid expression")
            return

        if key == "=":
            if not current:
                return
            try:
                value = self._evaluate(current)
                result = self._format(value)
                self.history_label.text = current.replace("*", "×").replace("/", "÷")
                self.expression = result
                self._show(result)
            except ZeroDivisionError:
                self.history_label.text = "ERROR"
                self.expression = ""
                self._show("Cannot divide by zero")
            except Exception:
                self.history_label.text = "ERROR"
                self._show("Invalid expression")
            return

        if self.just_evaluated and key in "0123456789.":
            self.expression = ""
        self.just_evaluated = False

        mapped = {"÷": "/", "×": "*", "−": "-"}
        token = mapped.get(key, key)

        if key in "+−×÷":
            if not self.expression and key != "−":
                return
            if self.expression and self.expression[-1] in "+-*/":
                self.expression = self.expression[:-1]
        if key == ".":
            # Permit only one decimal point in the current number.
            tail = self.expression.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split(" ")[-1]
            if "." in tail:
                return

        self.expression += token
        self._show(self.expression)

    def _show(self, text):
        self.display_label.text = str(text)
        self.just_evaluated = (self.history_label.text not in ("READY", "CLEARED", "ERROR") and text not in ("Invalid expression", "Cannot divide by zero"))

    @staticmethod
    def _evaluate(expression):
        # Calculator accepts only digits and arithmetic operators.
        allowed = set("0123456789.+-*/() ")
        if not expression or any(char not in allowed for char in expression):
            raise ValueError("Unsupported expression")
        return eval(expression, {"__builtins__": {}}, {})

    @staticmethod
    def _format(value):
        if int(value) == value:
            return str(int(value))
        return f"{value:.10g}"


if __name__ == "__main__":
    DarkCalculator().run()

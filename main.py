import os
import json

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

GOLD = (0.83, 0.65, 0.20, 1)
BLACK = (0.06, 0.06, 0.07, 1)
DARK = (0.12, 0.12, 0.13, 1)
WHITE = (1, 1, 1, 1)
GREY = (0.75, 0.75, 0.75, 1)


class CPMGeniusPro(App):
    def build(self):
        self.title = "CPM GENIUS PRO"
        Window.clearcolor = BLACK
        self.data_file = os.path.join(self.user_data_dir, "cpm_data.json")
        self.data = {"money": 0, "coins": 0, "cars": [], "tuning": []}
        self.load_data()

        self.root_layout = BoxLayout(
            orientation="vertical", spacing=dp(6), padding=dp(10)
        )
        self.header = Label(
            text="[b]♛ CPM GENIUS PRO[/b]", markup=True,
            font_size="23sp", color=GOLD, size_hint_y=None, height=dp(55)
        )
        self.root_layout.add_widget(self.header)
        self.content = BoxLayout(orientation="vertical")
        self.root_layout.add_widget(self.content)

        nav = GridLayout(cols=3, spacing=dp(5), size_hint_y=None, height=dp(115))
        pages = [
            ("HOME", self.home), ("MONEY", self.money_page),
            ("COINS", self.coins_page), ("CARS", self.cars_page),
            ("TUNING", self.tuning_page), ("TIPS", self.tips_page),
        ]
        for title, function in pages:
            btn = Button(
                text=title, background_normal="", background_color=GOLD,
                color=BLACK, bold=True, font_size="14sp"
            )
            btn.bind(on_release=lambda _btn, f=function: f())
            nav.add_widget(btn)
        self.root_layout.add_widget(nav)
        self.home()
        return self.root_layout

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as file:
                    saved = json.load(file)
                if isinstance(saved, dict):
                    self.data.update(saved)
        except (OSError, ValueError):
            pass

    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=2)
        except OSError:
            self.message("Could not save data.")

    def show_page(self, title):
        self.content.clear_widgets()
        page = BoxLayout(orientation="vertical", spacing=dp(12), padding=dp(10))
        heading = Label(
            text=f"[b]{title}[/b]", markup=True, color=GOLD,
            font_size="21sp", size_hint_y=None, height=dp(45)
        )
        page.add_widget(heading)
        scroll = ScrollView()
        items = BoxLayout(
            orientation="vertical", spacing=dp(10), padding=dp(5),
            size_hint_y=None
        )
        items.bind(minimum_height=items.setter("height"))
        scroll.add_widget(items)
        page.add_widget(scroll)
        self.content.add_widget(page)
        return items

    def label(self, parent, text, height=45):
        widget = Label(
            text=str(text), color=WHITE, font_size="16sp",
            size_hint_y=None, height=dp(height), halign="center",
            valign="middle"
        )
        widget.bind(size=lambda obj, size: setattr(obj, "text_size", size))
        parent.add_widget(widget)
        return widget

    def button(self, parent, text, callback):
        btn = Button(
            text=text, background_normal="", background_color=GOLD,
            color=BLACK, bold=True, font_size="16sp",
            size_hint_y=None, height=dp(48)
        )
        btn.bind(on_release=callback)
        parent.add_widget(btn)
        return btn

    def entry(self, parent, hint):
        field = TextInput(
            hint_text=hint, multiline=False, size_hint_y=None, height=dp(48),
            background_color=DARK, foreground_color=WHITE,
            cursor_color=GOLD, hint_text_color=GREY,
            padding=[dp(10), dp(12)]
        )
        parent.add_widget(field)
        return field

    def message(self, text):
        Popup(
            title="CPM GENIUS PRO",
            content=Label(text=text, color=WHITE),
            size_hint=(0.85, 0.35)
        ).open()

    def amount(self, value):
        try:
            return f"{float(value):,.2f}"
        except (ValueError, TypeError):
            return "0.00"

    def home(self):
        items = self.show_page("LUXURY DASHBOARD")
        self.label(items, "YOUR GAME. YOUR CARS. YOUR PROGRESS.", 55)
        self.label(items, "Recorded money\n" + self.amount(self.data["money"]), 65)
        self.label(items, "Recorded coins\n" + self.amount(self.data["coins"]), 65)
        self.label(items, f"Cars saved: {len(self.data['cars'])}", 45)
        self.label(items, f"Tuning setups: {len(self.data['tuning'])}", 45)
        self.button(items, "VIEW PLAYER STATISTICS", lambda _b: self.stats_page())
        self.label(items, "Companion app for Car Parking Multiplayer", 55)

    def money_page(self):
        items = self.show_page("MONEY TRACKER")
        self.label(items, "Current recorded balance: " + self.amount(self.data["money"]), 55)
        field = self.entry(items, "Enter amount")
        def update(_btn):
            try:
                value = float(field.text)
                if value < 0:
                    raise ValueError
                self.data["money"] = value
                self.save_data()
                self.money_page()
                self.message("Money record saved.")
            except ValueError:
                self.message("Enter a valid non-negative amount.")
        self.button(items, "SAVE MONEY", update)
        self.label(items, "This records your balance; it does not change your game account.", 75)

    def coins_page(self):
        items = self.show_page("COINS TRACKER")
        self.label(items, "Current recorded coins: " + self.amount(self.data["coins"]), 55)
        field = self.entry(items, "Enter coin amount")
        def update(_btn):
            try:
                value = float(field.text)
                if value < 0:
                    raise ValueError
                self.data["coins"] = value
                self.save_data()
                self.coins_page()
                self.message("Coin record saved.")
            except ValueError:
                self.message("Enter a valid non-negative amount.")
        self.button(items, "SAVE COINS", update)
        self.label(items, "Your tracker is separate from your actual game balance.", 65)

    def cars_page(self):
        items = self.show_page("MY CAR COLLECTION")
        field = self.entry(items, "Enter car name")
        def add_car(_btn):
            name = field.text.strip()
            if not name:
                self.message("Enter a car name first.")
                return
            self.data["cars"].append(name)
            self.save_data()
            self.cars_page()
        self.button(items, "ADD CAR", add_car)
        self.label(items, "YOUR SAVED CARS", 40)
        if not self.data["cars"]:
            self.label(items, "No cars saved yet.")
        else:
            for index, car in enumerate(self.data["cars"]):
                row = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))
                row.add_widget(Label(text=f"Car: {car}", color=WHITE))
                remove = Button(
                    text="REMOVE", size_hint_x=0.35, background_normal="",
                    background_color=GOLD, color=BLACK
                )
                remove.bind(on_release=lambda _btn, i=index: self.remove_car(i))
                row.add_widget(remove)
                items.add_widget(row)

    def remove_car(self, index):
        if 0 <= index < len(self.data["cars"]):
            self.data["cars"].pop(index)
            self.save_data()
            self.cars_page()

    def tuning_page(self):
        items = self.show_page("TUNING GUIDES")
        self.label(items, "Save your own tuning notes and setups.", 55)
        car_field = self.entry(items, "Car name")
        setup_field = self.entry(items, "Tuning notes or setup")
        def save_setup(_btn):
            car, setup = car_field.text.strip(), setup_field.text.strip()
            if not car or not setup:
                self.message("Enter a car name and tuning notes.")
                return
            self.data["tuning"].append({"car": car, "setup": setup})
            self.save_data()
            self.tuning_page()
        self.button(items, "SAVE TUNING SETUP", save_setup)
        for item in self.data["tuning"]:
            self.label(items, f"{item['car']}\n{item['setup']}", 75)

    def tips_page(self):
        items = self.show_page("GAME TIPS")
        tips = [
            "Practice parking in an empty area.",
            "Test tuning changes one at a time.",
            "Save notes about your favorite cars.",
            "Practice drifting in a safe open area.",
            "Keep your game updated.",
            "Never share your account password.",
            "Avoid unofficial tools claiming to generate unlimited currency."
        ]
        for number, tip in enumerate(tips, 1):
            self.label(items, f"{number}. {tip}", 65)

    def stats_page(self):
        items = self.show_page("PLAYER STATISTICS")
        self.label(items, f"Cars saved: {len(self.data['cars'])}")
        self.label(items, f"Tuning setups saved: {len(self.data['tuning'])}")
        self.label(items, f"Recorded money: {self.amount(self.data['money'])}", 55)
        self.label(items, f"Recorded coins: {self.amount(self.data['coins'])}", 55)
        self.button(items, "BACK TO HOME", lambda _b: self.home())


if __name__ == "__main__":
    CPMGeniusPro().run()

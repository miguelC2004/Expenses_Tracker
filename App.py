import mysql.connector
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex


class ExpenseApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#f0f0f0')  # Color de fondo

        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='expenses_tracker'
        )
        self.db_cursor = self.db_connection.cursor()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        header_label = Label(text='Expense Tracker', size_hint=(1, 0.1), font_size=30, color=get_color_from_hex('#333333'))

        filter_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        start_date_input = TextInput(hint_text='Start Date (YYYY-MM-DD)', size_hint=(0.4, None), height=40,
                                     background_color=get_color_from_hex('#ffffff'), foreground_color=get_color_from_hex('#333333'))
        end_date_input = TextInput(hint_text='End Date (YYYY-MM-DD)', size_hint=(0.4, None), height=40,
                                   background_color=get_color_from_hex('#ffffff'), foreground_color=get_color_from_hex('#333333'))
        filter_button = Button(text='Filter', size_hint=(0.2, None), height=40,
                               background_color=get_color_from_hex('#ffa500'), color=get_color_from_hex('#ffffff'))
        filter_button.bind(on_release=lambda _: self.filter_expenses(start_date_input.text, end_date_input.text))

        filter_layout.add_widget(start_date_input)
        filter_layout.add_widget(end_date_input)
        filter_layout.add_widget(filter_button)

        self.expense_list = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        scrollview = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        scrollview.add_widget(self.expense_list)

        description_input = TextInput(hint_text='Description', size_hint=(1, None), height=40,
                                      background_color=get_color_from_hex('#ffffff'), foreground_color=get_color_from_hex('#333333'))
        amount_input = TextInput(hint_text='Amount', size_hint=(1, None), height=40,
                                 background_color=get_color_from_hex('#ffffff'), foreground_color=get_color_from_hex('#333333'))

        save_button = Button(text='Save', size_hint=(1, None), height=40,
                             background_color=get_color_from_hex('#008000'), color=get_color_from_hex('#ffffff'))
        save_button.bind(on_release=lambda _: self.save_expense(description_input.text, amount_input.text))

        layout.add_widget(header_label)
        layout.add_widget(filter_layout)
        layout.add_widget(description_input)
        layout.add_widget(amount_input)
        layout.add_widget(save_button)
        layout.add_widget(scrollview)

        self.load_expenses()

        return layout

    def load_expenses(self):
        self.expense_list.clear_widgets()
        self.db_cursor.execute("SELECT id, description, amount FROM expenses")
        expenses = self.db_cursor.fetchall()

        for expense in expenses:
            expense_label = Label(text=f'{expense[1]} - {expense[2]}', size_hint=(1, None), height=40,
                                  color=get_color_from_hex('#333333'))
            self.expense_list.add_widget(expense_label)

    def save_expense(self, description, amount):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        query = "INSERT INTO expenses (description, amount, date) VALUES (%s, %s, %s)"
        values = (description, amount, current_date)
        self.db_cursor.execute(query, values)
        self.db_connection.commit()
        self.load_expenses()

    def filter_expenses(self, start_date, end_date):
        self.expense_list.clear_widgets()
        query = "SELECT id, description, amount FROM expenses WHERE date BETWEEN %s AND %s"
        values = (start_date, end_date)
        self.db_cursor.execute(query, values)
        expenses = self.db_cursor.fetchall()

        for expense in expenses:
            expense_label = Label(text=f'{expense[1]} - {expense[2]}', size_hint=(1, None), height=40,
                                  color=get_color_from_hex('#333333'))
            self.expense_list.add_widget(expense_label)


if __name__ == '__main__':
    ExpenseApp().run()

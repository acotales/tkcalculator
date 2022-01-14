# -*- coding: utf-8 -*-

# Built-in imports
import tkinter as tk

from functools import partial

# Imports from own package/module
from src.tkcalculator.util import Util


class Calculator(tk.Frame):
    """Graphical User Interface Calculator"""

    MAX_LENGTH_ENTRY = 16

    def __init__(self, master=None):
        # The same as tk.Frame.__init__(self, master)
        super().__init__(master)

        self.calculate = Util.Calculator

        # Load widget configurations
        self.cnf = Util.select_config()

        # Toplevel widget customization
        self.master.geometry('340x350+450+140')
        self.master.title(str(self)[2:].title())
        self.master.resizable(width=False, height=False)

        # Set calculator icon on top of window
        icon = tk.PhotoImage(data=Util.get_iconphoto())
        self.master.tk.call('wm', 'iconphoto', self.master, icon)

        # Class tk.Frame widget configurations
        self.place(relwidth=1, relheight=1)  # Frame placement to contain widgets
        self.config(cnf=self.cnf['classframe'])

        # Create an input/output display for the calculator
        display = tk.Entry(self, name='display', cnf=self.cnf['display'])
        display.place(relx=0.03, rely=0.05, relwidth=0.94, relheight=0.17)
        # Insert the initial value of 0 to show on the display
        display.insert(0, 0)
        # Make the entry a "readonly" state to make it uncompromisable
        display.config(state='readonly')

        # Create Buttons for the calculator
        button_table = [
            {"clear": "CE", "del": chr(8592), "percent": "%", "div": chr(247)},
            {"seven": 7, "eight": 8, "nine": 9, "mul": chr(215)},
            {"four": 4, "five": 5, "six": 6, "sub": "-"},
            {"one": 1, "two": 2, "three": 3, "add": "+"},
            {"blank": "", "zero": 0, "dot": ".", "equal": "="}
        ]
        # Precalculated by the author ^_^
        button_width, button_height = (0.23125, 0.136)
        button_xaxis, button_yaxis = (0.03, 0.27)
        padding = 0.005

        for row in button_table:
            for column in row:

                btn_name, btn_text = (column, row[column])

                # Map names and get the config data for each button widget
                if btn_name in ["div", "mul", "sub", "add", "equal"]:
                    cnf = self.cnf["operand"]

                elif isinstance(btn_text, int):
                    cnf = self.cnf["number"]

                else:
                    cnf = self.cnf[btn_name]

                btn = tk.Button(self, name=btn_name, text=btn_text, cnf=cnf,
                                command=partial(self._map_button_command, btn_name, btn_text)
                                )

                btn.place(relx=button_xaxis, rely=button_yaxis,
                          relwidth=button_width, relheight=button_height)

                button_xaxis = button_xaxis + button_width + padding

            button_xaxis = 0.03
            button_yaxis = button_yaxis + button_height + padding

        # Keypress bindings for the calculator
        self.master.bind("<BackSpace>", lambda i: self._delete_display_text())
        self.master.bind("<Return>", lambda i: self._calculate_equation())
        self.master.bind("<Prior>", lambda i: self._percent_operation())
        self.master.bind("<Next>", lambda i: self._percent_operation())
        self.master.bind("<Delete>", lambda i: self._clear_display_text())
        self.master.bind("/", lambda i: self._insert_on_display(chr(247)))
        self.master.bind("*", lambda i: self._insert_on_display(chr(215)))
        self.master.bind("+", lambda i: self._insert_on_display(i.char))
        self.master.bind("-", lambda i: self._insert_on_display(i.char))
        self.master.bind(".", lambda i: self._insert_on_display(i.char))
        self.master.bind("0", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("1", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("2", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("3", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("4", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("5", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("6", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("7", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("8", lambda i: self._insert_on_display(eval(i.char)))
        self.master.bind("9", lambda i: self._insert_on_display(eval(i.char)))

    def _map_button_command(self, btn_name, btn_text):
        """Map every button widget to its command function when clicked"""

        if btn_name == "clear":
            return self._clear_display_text()

        elif btn_name == "del":
            return self._delete_display_text()

        elif btn_name == "percent":
            return self._percent_operation()

        elif btn_name == "equal":
            return self._calculate_equation()

        elif btn_name == "blank":
            return self._blank_button_callback()

        else:
            return self._insert_on_display(btn_text)

    def _clear_display_text(self):
        """Clear or delete all the text on the display"""

        display = self.nametowidget("display")
        display.config(state="normal")
        display.delete(0, "end")
        display.insert(0, 0)
        display.config(state="readonly")

    def _delete_display_text(self):
        """Delete a single character on the display"""

        display = self.nametowidget("display")
        textlength = len(display.get()) - 1
        display.config(state="normal")

        if display.get() != "Error":
            display.delete(textlength)

            if textlength < 1:
                display.insert(0, 0)

        display.config(state="readonly")

    def _percent_operation(self):
        """Percent sign function operation"""

        operators = {'/': " / ", '*': " * ", '-': " - ", '+': " + "}
        result = None
        textdisplay = self.get_input_expression()
        table = textdisplay.maketrans(operators)
        partition = textdisplay.translate(table).split()

        # If input expression is a short form scientific notation
        if 'e' in textdisplay:
            calc = self.calculate(textdisplay + "/100")
            if calc.result != "Error":
                result = calc.result

        elif len(partition) < 3 and textdisplay != "Error":
            if partition[-1][-1].isnumeric():
                result = self.calculate(textdisplay + "/100").result

        # If input partition has 3 or more parts of equation
        else:
            if partition[-1].isnumeric():
                percent_num = partition.pop()
                operand = partition.pop()
                base_num = self.calculate("".join(partition)).result

                if all([
                    base_num != "Error",
                    operand in operators,
                    percent_num.isnumeric()
                ]):
                    print('Proceed:', base_num, operand, percent_num)
                    base_num, percent_num = eval(base_num), eval(percent_num)

                    if operand == '+':
                        calc = self.calculate.add_percentagee(base_num, percent_num)
                        result = self.calculate(str(calc)).result

                    elif operand == '-':
                        calc = self.calculate.sub_percentagee(base_num, percent_num)
                        result = self.calculate(str(calc)).result

                    elif operand == '*':
                        calc = self.calculate.mul_percentage(base_num, percent_num)
                        result = self.calculate(str(calc)).result

                    else:
                        calc = self.calculate.div_percentage(base_num, percent_num)
                        result = self.calculate(str(calc)).result

        # print('result:', result)
        if result:
            display = self.nametowidget("display")
            display.config(state="normal")
            display.delete(0, "end")
            display.insert(0, result[:self.MAX_LENGTH_ENTRY + 1])
            display.config(state="readonly")

    def _calculate_equation(self):
        """Equal sign function operation"""
        expression = self.get_input_expression()
        if expression != '0':
            calc = self.calculate(expression)
            display = self.nametowidget("display")
            display.config(state="normal")
            display.delete(0, "end")
            display.insert(0, calc.result[:self.MAX_LENGTH_ENTRY + 1])
            display.config(state="readonly")

    def _insert_on_display(self, char):
        """Insert the characters into the display"""

        display = self.nametowidget("display")
        display.config(state="normal")
        textdisplay = display.get()
        textlength = len(textdisplay)

        # Inserting an integer 0-9
        if isinstance(char, int):

            if textlength + 1 <= self.MAX_LENGTH_ENTRY:
                if textdisplay == '0':
                    display.delete(0, "end")
                display.insert(textlength, char)

        # Inserting a dot for decimal values
        elif char == self.children["dot"].cget("text"):

            if textdisplay[-1] != char:
                test = self.calculate(self.get_input_expression() + char)

                if test.result != "Error":
                    display.insert(textlength, char)

                else:
                    test = self.calculate(self.get_input_expression() + '0' + char)

                    if test.result != "Error":
                        display.insert(textlength, '0' + char)

        # Inserting a mathematical operator
        else:
            # Insert operator after a number or a dot
            if textdisplay[-1].isnumeric() or textdisplay.endswith('.'):
                display.insert(textlength, char)
            # Delete the prefixed operator and insert the new one
            else:
                display.delete(textlength - 1)
                display.insert(textlength, char)

        # Set readonly state to the display after insertion
        display.config(state="readonly")

    def _blank_button_callback(self):
        """Reserved for new ideas"""
        pass

    def get_input_expression(self) -> str:
        """Possibly translate the input text into an arithmetic expression"""

        translate = {
            self.children["div"].cget("text"): '/',
            self.children["mul"].cget("text"): '*',
            self.children["sub"].cget("text"): '-',
            self.children["add"].cget("text"): '+',
            self.children["dot"].cget("text"): '.'
        }

        display = self.nametowidget("display")
        table = display.get().maketrans(translate)
        final = display.get().translate(table)
        return final

    def start(self):
        # Starts the app by calling the toplevel's mainloop function
        # This can also start the app without passing any root window
        self.master.mainloop()

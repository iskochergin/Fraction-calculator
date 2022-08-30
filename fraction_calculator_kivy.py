import kivy
from fractions import Fraction

kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


class FractionCalculatorApp(App):

    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=2, spacing=2)
        self.solution = TextInput(multiline=False, readonly=True, halign='right', font_size=50, input_filter='str')
        main_layout.add_widget(self.solution)

        buttons1 = [
            ['Сократить\n    дробь', '  Выделить\nцелую часть', 'Перевести в\nдесятичную'],
            ['   Привести дроби к\nобщему знаменателю']
        ]
        for row in buttons1:
            h_layout = BoxLayout()
            for label in row:
                button = Button(text=label, pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=20)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        buttons2 = [
            ['7', '8', '9', ':'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['/', '0', '.', '+'],
            ['цел', ';', '=', 'Del', 'C']
        ]
        for row in buttons2:
            h_layout = BoxLayout()
            for label in row:
                button = Button(text=label, pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=30)
                if label == 'целых':
                    button.font_size = 25
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        return main_layout

    def on_button_press(self, instance):
        global reduction, whole_part, to_decimal, common_denominator
        if instance.text == 'C':
            self.solution.text = ''
            reduction = False
            whole_part = False
            to_decimal = False
            common_denominator = False
        elif instance.text == 'Сократить\n    дробь':
            reduction = True
            whole_part = False
            to_decimal = False
            common_denominator = False
        elif instance.text == '  Выделить\nцелую часть':
            reduction = False
            whole_part = True
            to_decimal = False
            common_denominator = False
        elif instance.text == 'Перевести в\nдесятичную':
            reduction = False
            whole_part = False
            to_decimal = True
            common_denominator = False
        elif instance.text == '   Привести дроби к\nобщему знаменателю':
            reduction = False
            whole_part = False
            to_decimal = False
            common_denominator = True
        elif instance.text in '+-*:':
            try:
                text = '______' + self.solution.text
                if not text[-1].isdigit() and text[-6:] not in ['целая ', 'целых ']:
                    self.solution.text = 'Ошибка'
                else:
                    if self.solution.text[-1] == ' ':
                        self.solution.text = self.solution.text[:-1]
                    self.solution.text += instance.text
                    reduction = False
                    whole_part = False
                    to_decimal = False
                    common_denominator = False
            except:
                self.solution.text = 'Ошибка'
        elif instance.text == 'Del':
            self.solution.text = self.solution.text[:-1]
        elif instance.text == 'цел':
            text = self.solution.text
            if '+' in text:
                text = text.split('+')
            elif '-' in text:
                text = text.split('-')
            elif '*' in text:
                text = text.split('*')
            elif ':' in text:
                text = text.split(':')
            elif ';' in text:
                text = text.split(';')
            else:
                text = [text]
                whole = float()
            try:
                whole = float(text[-1])
            except:
                self.solution.text = 'Ошибка'
            if self.solution.text != 'Ошибка':
                if whole % 10 == 1 and whole // 10 % 10 != 1:
                    self.solution.text += ' целая '
                else:
                    self.solution.text += ' целых '

        elif instance.text == '=':
            numbers = '1234567890'
            out = ''
            zero_division_error = False

            def numerator_denominator_whole_find(fraction):
                numerator = str()
                denominator = str()
                whole = str()
                whole_here = False
                fraction_here = False
                error = False
                zero_division_error = False
                for j in range(len(fraction)):
                    if fraction[j] == ' ':
                        numerator = ''
                        whole_here = True
                    elif fraction[j] == '/':
                        fraction_here = True
                        break
                    elif fraction[j] in numbers:
                        numerator += fraction[j]
                        if not whole_here:
                            whole += fraction[j]
                    else:
                        error = True
                        break
                for j in range(1, len(fraction)):
                    if fraction[-j] == '/':
                        break
                    elif fraction[-j] in numbers:
                        denominator = fraction[-j] + denominator
                    else:
                        error = True
                        break
                if error or (numerator == '' or denominator == '') or not fraction_here:
                    error = True
                    return error
                else:
                    whole = int(whole)
                    numerator = int(numerator)
                    denominator = int(denominator)
                    if denominator == 0:
                        zero_division_error = True
                    return whole, numerator, denominator, whole_here, zero_division_error

            def get_actions(actions):
                components = [[], []]
                error = False
                zero_division_error = False
                count = 0
                for component in actions:
                    if len(component.split()) == 2 and component.split()[0].isdigit() and \
                            component.split()[1] in ['целая', 'целых']:
                        components[count].append(int(component.split()[0]))
                    elif component.count('/') == 1:
                        fraction = component.replace(' целая ', ' ').replace(' целых ', ' ')
                        error = numerator_denominator_whole_find(fraction)
                        if error is True:
                            break
                        else:
                            whole, numerator, denominator, whole_here, zero_division_error \
                                = numerator_denominator_whole_find(fraction)
                            error = False
                            if whole_here:
                                numerator += whole * denominator
                            components[count].append(numerator)
                            components[count].append(denominator)
                    else:
                        try:
                            components[count].append(float(component))
                        except:
                            error = True
                    count = 1
                if error is True:
                    return error, zero_division_error
                else:
                    return components, zero_division_error

            try:
                if reduction:
                    fraction = self.solution.text
                    if fraction.split()[0].isdigit() and fraction.split()[1] in ['целая', 'целых'] and len(
                            fraction.split()) == 2:
                        out = fraction
                    else:
                        fraction = fraction.replace(' целая ', ' ').replace(' целых ', ' ')
                        error = numerator_denominator_whole_find(fraction)
                        if error is True:
                            out = 'Ошибка'
                        else:
                            whole, numerator, denominator, whole_here, zero_division_error \
                                = numerator_denominator_whole_find(fraction)
                            can_shorten_the_fraction = False
                            for i in range(2, min(numerator, denominator) + 1):
                                if numerator % i == 0 and denominator % i == 0:
                                    if whole_here:
                                        if whole % 10 == 1 and whole // 10 % 10 != 1:
                                            out = f'{whole} целая {numerator // i}/{denominator // i}'
                                        else:
                                            out = f'{whole} целых {numerator // i}/{denominator // i}'
                                    else:
                                        out = f'{numerator // i}/{denominator // i}'
                                    can_shorten_the_fraction = True
                            if not can_shorten_the_fraction:
                                out = 'Дробь несократима'

                elif whole_part:
                    fraction = self.solution.text
                    if fraction.split()[0].isdigit() and fraction.split()[1] in ['целая', 'целых'] and len(
                            fraction.split()) == 2:
                        out = fraction
                    else:
                        fraction = fraction.replace(' целая ', ' ').replace(' целых ', ' ')
                        error = numerator_denominator_whole_find(fraction)
                        if error is True:
                            out = 'Ошибка'
                        else:
                            whole, numerator, denominator, whole_here, zero_division_error \
                                = numerator_denominator_whole_find(fraction)
                            numerator2 = numerator
                            denominator2 = denominator

                            for i in range(2, min(numerator2, denominator2) + 1):
                                if numerator % i == 0 and denominator % i == 0:
                                    numerator = numerator2
                                    denominator = denominator2
                                    numerator //= i
                                    denominator //= i

                            if whole_here:
                                if numerator >= denominator:
                                    numerator += whole * denominator

                            if numerator2 < denominator2:
                                out = 'Дробь уже правильная'

                            if numerator >= denominator:
                                whole = numerator // denominator
                                if whole % 10 == 1 and whole // 10 % 10 != 1:
                                    out = f'{whole} целая '
                                else:
                                    out = f'{whole} целых '
                                if numerator % denominator != 0:
                                    out += f'{numerator2 % denominator2}/{denominator}'

                elif to_decimal:
                    fraction = self.solution.text
                    if fraction.split()[0].isdigit() and fraction.split()[1] in ['целая', 'целых'] and len(
                            fraction.split()) == 2:
                        out = str(int(fraction.split()[0]) / 1)
                    else:
                        fraction = fraction.replace(' целая ', ' ').replace(' целых ', ' ')
                        error = numerator_denominator_whole_find(fraction)
                        if error is True:
                            out = 'Ошибка'
                        else:
                            whole, numerator, denominator, whole_here, zero_division_error \
                                = numerator_denominator_whole_find(fraction)
                            numerator2 = numerator
                            denominator2 = denominator

                            if whole_here:
                                numerator += whole * denominator
                            out = str(numerator / denominator)

                            for i in range(2, min(numerator2, denominator2) + 1):
                                if numerator % i == 0 and denominator % i == 0:
                                    numerator = numerator2
                                    denominator = denominator2
                                    numerator //= i
                                    denominator //= i

                            while denominator != 1:
                                for i in range(denominator):
                                    if denominator % 5 == 0:
                                        denominator //= 5
                                    elif denominator % 2 == 0:
                                        denominator //= 2
                                    elif denominator == 1:
                                        break
                                    else:
                                        out += ' Дробь бесконечная'
                                        denominator = 1
                                        break

                elif common_denominator:
                    if ' целая ' in self.solution.text or ' целых ' in self.solution.text:
                        out = 'Нельзя использовать целые'
                    elif self.solution.text.count(';') == 0:
                        out = 'Используйте ";"'
                    else:
                        numerators1 = []
                        denominators1 = []
                        numerators2 = []
                        fractions = self.solution.text.split(';')
                        error = False

                        for fraction in fractions:
                            numerator = str()
                            denominator = str()
                            for j in range(len(fraction)):
                                if fraction[j] == '/':
                                    break
                                elif fraction[j] in numbers:
                                    numerator += fraction[j]
                                else:
                                    error = True
                                    break
                            for j in range(1, len(fraction)):
                                if fraction[-j] == '/':
                                    break
                                elif fraction[-j] in numbers:
                                    denominator = fraction[-j] + denominator
                                else:
                                    error = True
                                    break
                            if error or (numerator == '' or denominator == ''):
                                error = True
                            elif int(denominator) == 0:
                                zero_division_error = True
                                error = True
                            else:
                                numerators1.append(int(numerator))
                                denominators1.append((int(denominator)))
                            if error:
                                out = 'Ошибка'
                                break

                        if len(numerators1) == 1:
                            out = 'Введите несколько дробей'

                        if not error:
                            for i in range(len(numerators1)):
                                denominators1_copy = denominators1.copy()
                                del denominators1_copy[i]
                                new_numerator = numerators1[i]
                                for j in denominators1_copy:
                                    new_numerator *= j
                                numerators2.append(new_numerator)

                            common_denominator = denominators1[0]
                            del denominators1[0]
                            for i in denominators1:
                                common_denominator *= i

                            numerators_end = []
                            common_end_denominator = common_denominator
                            can_shorten_the_fraction = False
                            can_shorten_the_fraction_immutable = False

                            for i in range(2, min(numerators2) + 1):
                                for j in numerators2:
                                    if common_denominator % i == 0 and j % i == 0:
                                        can_shorten_the_fraction = True
                                    else:
                                        can_shorten_the_fraction = False
                                        break
                                if can_shorten_the_fraction:
                                    numerators_end.clear()
                                    common_end_denominator = common_denominator
                                    can_shorten_the_fraction_immutable = True
                                    for j in numerators2:
                                        numerators_end.append(j // i)
                                    common_end_denominator //= i

                            if not can_shorten_the_fraction_immutable:
                                numerators_end = numerators2

                            for i in numerators_end:
                                out += f'{i}/{common_end_denominator}; '
                            out = out[:-2]

                elif '+' in self.solution.text:
                    actions = self.solution.text
                    if actions.count('+') + actions.count('-') + actions.count('*') + actions.count(':') > 1:
                        out = 'Доступно только 1 действие'
                    else:
                        actions = actions.split('+')
                        error, zero_division_error = get_actions(actions)
                        if error is True:
                            out = 'Ошибка'
                        else:
                            components = error
                            c1, c2 = components[0], components[1]

                            if len(c1) == 1 and len(c2) == 1:
                                answer = str(c1[0] + c2[0])
                                if answer[-2:] == '.0':
                                    answer = answer[:-2]
                                out = answer

                            elif len(c1) == 2 and len(c2) == 1:
                                if type(c2[0]) is int or str(c2[0])[-2:] == '.0':
                                    c2 = [int(c2[0]) ** 2, int(c2[0])]
                                else:
                                    whole, numerator = str(c2[0]).split('.')
                                    denominator = 10 ** len(numerator)
                                    numerator = int(numerator)
                                    numerator += int(whole) * denominator
                                    c2 = [numerator, denominator]

                            elif len(c2) == 2 and len(c1) == 1:
                                if type(c1[0]) is int or str(c1[0])[-2:] == '.0':
                                    c1 = [int(c1[0]) ** 2, int(c1[0])]
                                else:
                                    whole, numerator = str(c1[0]).split('.')
                                    denominator = 10 ** len(numerator)
                                    numerator = int(numerator)
                                    numerator += int(whole) * denominator
                                    c1 = [numerator, denominator]

                            if len(c1) == 2 and len(c2) == 2:
                                numerator = c1[0] * c2[1] + c2[0] * c1[1]
                                denominator = c1[1] * c2[1]
                                if numerator == denominator:
                                    out = '1'
                                elif numerator > denominator and numerator % denominator == 0:
                                    out = str(numerator // denominator)
                                else:
                                    whole = 0
                                    if numerator > denominator:
                                        whole = numerator // denominator
                                        numerator %= denominator
                                    if whole > 0:
                                        out = str(whole)
                                        if int(whole) % 10 == 1 and int(whole) // 10 % 10 != 1:
                                            out += ' целая '
                                        else:
                                            out += ' целых '
                                    out += str(Fraction(numerator, denominator))

                elif '-' in self.solution.text:
                    actions = self.solution.text
                    if actions.count('+') + actions.count('-') + actions.count('*') + actions.count(':') > 1:
                        out = 'Доступно только 1 действие'
                    else:
                        actions = actions.split('-')
                        error, zero_division_error = get_actions(actions)
                        if error is True:
                            out = 'Ошибка'
                        else:
                            components = error
                            c1, c2 = components[0], components[1]

                            if len(c1) == 1 and len(c2) == 1:
                                answer = str(c1[0] - c2[0])
                                if answer[-2:] == '.0':
                                    answer = answer[:-2]
                                out = answer

                            elif len(c1) == 2 and len(c2) == 1:
                                if type(c2[0]) is int or str(c2[0])[-2:] == '.0':
                                    c2 = [int(c2[0]) ** 2, int(c2[0])]
                                else:
                                    whole, numerator = str(c2[0]).split('.')
                                    denominator = 10 ** len(numerator)
                                    numerator = int(numerator)
                                    numerator += int(whole) * denominator
                                    c2 = [numerator, denominator]

                            elif len(c2) == 2 and len(c1) == 1:
                                if type(c1[0]) is int or str(c1[0])[-2:] == '.0':
                                    c1 = [int(c1[0]) ** 2, int(c1[0])]
                                else:
                                    whole, numerator = str(c1[0]).split('.')
                                    denominator = 10 ** len(numerator)
                                    numerator = int(numerator)
                                    numerator += int(whole) * denominator
                                    c1 = [numerator, denominator]

                            if len(c1) == 2 and len(c2) == 2:
                                numerator = c1[0] * c2[1] - c2[0] * c1[1]
                                denominator = c1[1] * c2[1]
                                if -numerator == numerator and numerator != 0:
                                    out = '-'
                                    numerator = abs(numerator)
                                if numerator == denominator:
                                    out = '1'
                                elif numerator > denominator and numerator % denominator == 0:
                                    out = str(numerator // denominator)
                                else:
                                    whole = 0
                                    if numerator > denominator:
                                        whole = numerator // denominator
                                        numerator %= denominator
                                    if whole > 0:
                                        out = str(whole)
                                        if int(whole) % 10 == 1 and int(whole) // 10 % 10 != 1:
                                            out += ' целая '
                                        else:
                                            out += ' целых '
                                    out += str(Fraction(numerator, denominator))

                elif '*' in self.solution.text:
                    actions = self.solution.text
                    if actions.count('+') + actions.count('-') + actions.count('*') + actions.count(':') > 1:
                        out = 'Доступно только 1 действие'
                    else:
                        actions = actions.split('*')
                        error, zero_division_error = get_actions(actions)
                        if error is True:
                            out = 'Ошибка'
                        else:
                            components = error
                            c1, c2 = components[0], components[1]

                            if len(c1) == 1 and len(c2) == 1:
                                answer = str(c1[0] * c2[0])
                                if answer[-2:] == '.0':
                                    answer = answer[:-2]
                                out = answer

                            elif len(c1) == 2 and len(c2) == 1:
                                if type(c2[0]) is int or str(c2[0])[-2:] == '.0':
                                    c2 = [int(c2[0]) ** 2, int(c2[0])]
                                else:
                                    whole, numerator = str(c2[0]).split('.')
                                    denominator = 10 ** len(numerator)
                                    numerator = int(numerator)
                                    numerator += int(whole) * denominator
                                    c2 = [numerator, denominator]

                            elif len(c2) == 2 and len(c1) == 1:
                                if type(c1[0]) is int or str(c1[0])[-2:] == '.0':
                                    c1 = [int(c1[0]) ** 2, int(c1[0])]
                                else:
                                    whole, numerator = str(c1[0]).split('.')
                                    denominator = 10 ** len(numerator)
                                    numerator = int(numerator)
                                    numerator += int(whole) * denominator
                                    c1 = [numerator, denominator]

                            if len(c1) == 2 and len(c2) == 2:
                                numerator = c1[0] * c2[0]
                                denominator = c1[1] * c2[1]
                                if numerator == denominator:
                                    out = '1'
                                elif numerator > denominator and numerator % denominator == 0:
                                    out = str(numerator // denominator)
                                else:
                                    whole = 0
                                    if numerator > denominator:
                                        whole = numerator // denominator
                                        numerator %= denominator
                                    if whole > 0:
                                        out = str(whole)
                                        if int(whole) % 10 == 1 and int(whole) // 10 % 10 != 1:
                                            out += ' целая '
                                        else:
                                            out += ' целых '
                                    out += str(Fraction(numerator, denominator))

                elif ':' in self.solution.text:
                    actions = self.solution.text
                    if actions.count('+') + actions.count('-') + actions.count('*') + actions.count(':') > 1:
                        out = 'Доступно только 1 действие'
                    else:
                        actions = actions.split(':')
                        error, zero_division_error = get_actions(actions)
                        if error is True:
                            out = 'Ошибка'
                        else:
                            components = error
                            c1, c2 = components[0], components[1]

                            if c2[0] == 0:
                                zero_division_error = True
                            else:
                                if len(c1) == 1 and len(c2) == 1:
                                    answer = str(c1[0] / c2[0])
                                    if answer[-2:] == '.0':
                                        answer = answer[:-2]
                                    out = answer

                                elif len(c1) == 2 and len(c2) == 1:
                                    if type(c2[0]) is int or str(c2[0])[-2:] == '.0':
                                        c2 = [int(c2[0]) ** 2, int(c2[0])]
                                    else:
                                        whole, numerator = str(c2[0]).split('.')
                                        denominator = 10 ** len(numerator)
                                        numerator = int(numerator)
                                        numerator += int(whole) * denominator
                                        c2 = [numerator, denominator]

                                elif len(c2) == 2 and len(c1) == 1:
                                    if type(c1[0]) is int or str(c1[0])[-2:] == '.0':
                                        c1 = [int(c1[0]) ** 2, int(c1[0])]
                                    else:
                                        whole, numerator = str(c1[0]).split('.')
                                        denominator = 10 ** len(numerator)
                                        numerator = int(numerator)
                                        numerator += int(whole) * denominator
                                        c1 = [numerator, denominator]

                                if len(c1) == 2 and len(c2) == 2:
                                    numerator = c1[0] * c2[1]
                                    denominator = c1[1] * c2[0]
                                    if numerator == denominator:
                                        out = '1'
                                    elif numerator > denominator and numerator % denominator == 0:
                                        out = str(numerator // denominator)
                                    else:
                                        whole = 0
                                        if numerator > denominator:
                                            whole = numerator // denominator
                                            numerator %= denominator
                                        if whole > 0:
                                            out = str(whole)
                                            if int(whole) % 10 == 1 and int(whole) // 10 % 10 != 1:
                                                out += ' целая '
                                            else:
                                                out += ' целых '
                                        out += str(Fraction(numerator, denominator))

                else:
                    out = 'Выберите действие'

            except:
                out = 'Выберите действие'

            if zero_division_error:
                out = 'На 0 делить нельзя'

            self.solution.font_size = 50 - len(out) if len(out) < 35 else 53 - len(out)
            self.solution.text = out

        else:
            if self.solution.text[-5:] in ['целая', 'целых']:
                self.solution.text += ' '

            if len(self.solution.text) < 31:
                self.solution.font_size = 50 - len(self.solution.text) // 2
                self.solution.text += instance.text


if __name__ == '__main__':
    FractionCalculatorApp().run()

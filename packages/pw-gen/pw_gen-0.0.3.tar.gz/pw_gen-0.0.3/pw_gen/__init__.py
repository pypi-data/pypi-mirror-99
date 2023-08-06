import random
import secrets
import string
import urllib.request

class Simple():
    def __init__(self, length: int, characters = None):
        '''A simple password (less arguments compared to complex)'''
        self.length = length
        self.characters = characters
        self.output = []

    def generate(self, num_of_passwords: int):
        '''
        Generates a password depending on the num_of_passwords and the arugments provided in the simple class
        '''
        characters = ''
        if self.characters is None:
            characters = string.ascii_letters + string.digits
        else:
            characters = self.characters

        for i in range(num_of_passwords):
            password = ''
            for c in range(self.length):
                password += secrets.choice(characters)
            self.output.append(password)
        return self.output

    def return_result(self, index: int):
        '''
        Returns the password which is at the specified index in the output list.
        '''
        try:
            return self.output[index]
        except IndexError:
            print('Incorrect index specified. Please provide an index relevant to the number of passwords generated')

    def clear_results(self):
        '''Clears the output list if you want to make way for new passwords'''
        self.output.clear()

class Complex(Simple):
    def __init__(self, length, string_method, numbers=True, special_chars=False):
        '''
        Creates a customisable password depending on length, string_method, numbers and special_chars
        '''
        characters = ''
        self.output = []

        methods: dict = {
            "upper": string.ascii_uppercase,
            "lower": string.ascii_lowercase,
            "both": string.ascii_letters,
        }

        characters += methods[string_method]

        if numbers:
            characters += string.digits
        if special_chars:
            characters += string.punctuation

        super().__init__(length=length, characters=characters)

class Memorable(Simple):
    def __init__(self, numbers=True):
        '''A memorable password e.g HelloWorld123'''
        self.numbers = numbers
        self.output = []

    def generate(self, num_of_passwords: int):
        '''Gets some random words'''
        word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        req = urllib.request.Request(word_url, headers=headers)
        response = response = urllib.request.urlopen(req)
        long_txt = response.read().decode()
        words = long_txt.splitlines()

        '''
        Generates the password containing 2 words and numbers if self.numbers == True
        '''
        for i in range(num_of_passwords):
            password = ''
            two_words = ''
            for i in range(2):
                two_words += secrets.choice(words).title()
            password = two_words
            if self.numbers == True:
                for i in range(random.randint(3, 4)):
                    password += secrets.choice(string.digits)
            self.output.append(password)
        return self.output

class Pin(Simple):
    def __init__(self, length):
        '''Customise a pin (consisting of numbers) with specified length'''
        self.length = length
        self.output = []

    def generate(self, num_of_pins: int):
        '''Generate the specified number of pins'''
        for i in range(num_of_pins):
            pin = ''
            for c in range(self.length):
                pin += secrets.choice(string.digits)
            self.output.append(pin)
        return self.output

        super().__init__(length=length)

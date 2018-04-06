from decimal import Decimal

class BuoyInput(object):

    def convert_yes_no_boolean(self, text):
        """
        Converts input from the website of yes/no to True/False as boolean

        text (str): Text input received from the form
        """
        answer = None
        if text.lower() == 'yes':
            answer = True
        elif text.lower() == 'no':
            answer = False

        return answer

    def convert_to_coordinate(self, number_string):
        """
        This function returns the co ordinate as a double/float style value
        to replace the string that is taken from the web input

        number_string (str): String formatted as a number
        """
        number = Decimal(number_string)
        return number
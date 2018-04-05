class BuoyInput(object):

    def convert_yes_no_boolean(self, text):
        answer = None
        if text.lower() == 'yes':
            answer = True
        elif text.lower() == 'no':
            answer = False

        return answer
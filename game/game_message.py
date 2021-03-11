import textwrap
from game.color import WHITE
class Message:
    def __init__(self, text, color=WHITE):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.widht = width
        self.height = height

    def add_message(self, message):
        new_msg_lines = textwrap.wrap(message.text, self.widht)

        for line in new_msg_lines:
            if len(self.messages) == self.height:
                del self.messages[0]
            
            self.messages.append(Message(line, message.color))
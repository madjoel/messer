# -----------------------
# Message container class
# @author Matthieu Laqua
# -----------------------

# imports
import re

# message class
class Message:
    QUOTE_SUB = "{$quote$}"
    # constructor
    def __init__(self, text, recipient_ids, sender_id, sender_name):
        self.text = text.strip() # string
        self.recipient_ids = recipient_ids # list of integers
        self.sender_id = sender_id # integer
        self.sender_name = sender_name # string
    
    # construct from representation string
    @classmethod
    def fromstring(cls, string, recipient_ids):
        text = re.search("text='.*?'", string).group().replace("text='", "")
        text = text.replace("'", "").replace(Message.QUOTE_SUB, "'")
        sender_id_match = re.search("sender_id=\d+", string)
        if sender_id_match: sender_id = sender_id_match.group().replace("sender_id=", "")
        else: sender_id = "-1" # if there is a corrupted sender_id
        sender_name = re.search("sender_name='.*?'", string).group() \
            .replace("sender_name='", "")
        sender_name = sender_name.replace("'", "").replace(Message.QUOTE_SUB, "'")
        recipient_ids = recipient_ids
        return cls(text, recipient_ids, sender_id, sender_name)

    def hasRecipient(self):
        if len(self.recipient_ids) > 0:
            return True
        else:
            return False

    def nextRecipient(self):
        if len(self.recipient_ids) > 0:
            return self.recipient_ids.pop(0) # return first of the list
        else:
            return None
    
    # to string
    def __str__(self):
        return self.text
    
    # representation
    def __repr__(self):
        tmp_text = self.text.replace("'", Message.QUOTE_SUB)
        return ("[text='" + tmp_text + "', sender_id=" + str(self.sender_id)
              + ", sender_name='" + self.sender_name + "']")


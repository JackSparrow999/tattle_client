import time

class Chat:

    message = None
    epoch_time = None
    user_name = None

    def __init__(self):
        pass

    def populate(self, message, user_name):
        self.message = message
        self.epoch_time = round(time.time() * 1000)
        self.user_name = user_name

    #marker character is *
    def serialize(self):
        s = "" + self.message + "*" + str(self.epoch_time) + "*" + self.user_name
        return s

    def deserialize(self, s):
        lst = []
        id = 0
        temp = ""

        while id < len(s):
            if id+1 >= len(s):
                temp = temp + s[id]
                lst.append(temp)

            if s[id] == '*' and s[id+1] != '*':
                lst.append(temp)
                temp = ""

            else:
                temp = temp + s[id]

            id = id + 1

        self.message = lst[0]
        self.epoch_time = int(lst[1])
        self.user_name = lst[2]
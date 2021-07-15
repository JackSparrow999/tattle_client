import requests

class Command:

    cmd = None
    args = []
    host = 'http://127.0.0.1:8060'

    def init(self, s):
        lst = s.split()
        self.cmd = lst[0]
        for i in range(1, len(lst)):
            self.args.append(lst[i])

    def build_url(self, s):
        return self.host + s

    def execute(self):
        pass

    def xyz(self):
        pass


class CreateUser(Command):

    path = '/auth/user/'

    #cmd: create_user <user_name> <password>
    def execute(self):
        response = requests.post(self.build_url(self.path),
                      data={'user_name': self.args[0],
                            'password': self.args[1]})
        return 'Created user ' + response.json()['user_name']


class FetchUser(Command):

    def execute(self):
        pass


class DeleteUser(Command):

    def execute(self):
        pass


class UpdateUser(Command):

    def execute(self):
        pass

class AllUsers(Command):

    def execute(self):
        pass


class CreateRoom(Command):
    def execute(self):
        pass


class FetchRoom(Command):
    def execute(self):
        pass


class DeleteRoom(Command):
    def execute(self):
        pass


class UpdateRoom(Command):
    def execute(self):
        pass


class AllRooms(Command):
    def execute(self):
        pass


class AddUserToRoom(Command):
    def execute(self):
        pass


class AllUsersInRoom(Command):

    def execute(self):
        pass


class AllRoomsForUser(Command):

    def execute(self):
        pass


class RemoveUserFromRoom(Command):

    def execute(self):
        pass


class LoginUser(Command):

    def execute(self):
        pass



def route_command(c):

    commands_dict = {
        'create_user': CreateUser(),
        'create_room': CreateRoom,
    }

    lst = c.split(' ')
    cmd = commands_dict[lst[0]]
    cmd.init(c)

    return cmd.execute()




if __name__ == '__main__':
    cu = Command()
    cu.init('hello world')
    cu.execute()
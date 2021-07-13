
class Command:

    cmd = None
    args = []

    def init(self, s):
        lst = s.split()
        self.cmd = lst[0]
        for i in range(1, len(lst)):
            self.args.append(lst[i])

    def execute(self):
        print('parent')

    def xyz(self):
        pass


class CreateUser(Command):

    def execute(self):
        pass


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



def route_command(c):

    commands_dict = {
        'create_user': CreateUser(),
        'create_room': CreateRoom,
    }




if __name__ == '__main__':
    cu = Command()
    cu.init('hello world')
    cu.execute()
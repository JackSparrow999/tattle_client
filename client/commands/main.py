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
        return 'created user_id ' + str(response.json()['user_id'])


class FetchUser(Command):

    path = '/auth/user/'

    #cmd: get_user <user_name>
    def execute(self):
        if len(self.args) >= 1:
            user_name = self.args[0]
        else:
            user_name = None
        if user_name == None:
            response = requests.get(self.build_url(self.path))
        else:
            response = requests.get(self.build_url(self.path), params={
                'user_name': user_name
            })
        lst = response.json()['users']
        res = ''
        for x in lst:
            res = res + str(x)
            res = res + '\n'
        return res


class DeleteUser(Command):

    path = '/auth/user/'

    #del_user user_id
    def execute(self):

        if len(self.args) >= 1:
            user_id = self.args[0]
        else:
            user_id = None

        response = requests.delete(self.build_url(self.path), data={
            'user_id': user_id
        })
        return response.json()['message']


class UpdateUser(Command):

    path = '/auth/user/'

    #cmd: update_user user_id user_name password
    def execute(self):

        if len(self.args) == 3:
            user_id = self.args[0]
            user_name = self.args[1]
            user_password = self.args[2]

        response = requests.put(self.build_url(self.path), data={
            'user_id': user_id,
            'user_name': user_name,
            'user_password': user_password
        })
        return response.json()['message']


class CreateRoom(Command):

    path = '/auth/room/'

    # cmd: create_room <room_name> <private>
    def execute(self):

        response = requests.post(self.build_url(self.path),
                                 data={'room_name': self.args[0],
                                       'private': self.args[1] == 'true'})

        return 'created room_id ' + str(response.json()['room_id'])


class FetchRoom(Command):

    path = '/auth/room/'

    # cmd: get_room <room_name>
    def execute(self):
        if len(self.args) >= 1:
            room_name = self.args[0]
        else:
            room_name = None
        if room_name == None:
            response = requests.get(self.build_url(self.path))
        else:
            response = requests.get(self.build_url(self.path), params={
                'room_name': room_name
            })
        lst = response.json()['rooms']
        res = ''
        for x in lst:
            res = res + str(x)
            res = res + '\n'
        return res


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
        'get_user': FetchUser(),
        'del_user': DeleteUser(),
        'update_user': UpdateUser(),
        'create_room': CreateRoom(),
        'get_room': FetchRoom(),
    }

    lst = c.split(' ')
    cmd = commands_dict[lst[0]]
    cmd.init(c)

    return cmd.execute()




if __name__ == '__main__':
    # print(route_command('create_user ronaq password'))
    # print(route_command('get_user raja'))
    # print(route_command('del_user 11'))
    # print(route_command('update_user 7 raja password'))

    # print(route_command('create_room birthday true'))
    # print(route_command('get_room birthday'))
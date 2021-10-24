import requests

class Command:

    cmd = None
    args = []
    host = 'http://127.0.0.1:8060'

    def init(self, s):
        lst = s.split()
        self.cmd = lst[0]
        self.args = []
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

    # cmd: create_room <room_name>
    def execute(self):

        response = requests.post(self.build_url(self.path),
                                 data={'room_name': self.args[0],
                                       'private': True})

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

    path = '/auth/room/'

    # del_room room_id
    def execute(self):

        if len(self.args) >= 1:
            room_id = self.args[0]
        else:
            room_id = None

        response = requests.delete(self.build_url(self.path), data={
            'room_id': room_id
        })
        return response.json()['message']


class UpdateRoom(Command):

    path = '/auth/room/'

    # cmd: update_room room_id room_name
    def execute(self):
        if len(self.args) == 2:
            room_id = self.args[0]
            room_name = self.args[1]
            private = True

        response = requests.put(self.build_url(self.path), data={
            'room_id': room_id,
            'room_name': room_name,
            'private': private
        })
        return response.json()['message']


class AddUserToRoom(Command):

    path = '/auth/add_user/'

    #cmd: add_user room_id user_id
    def execute(self):
        response = requests.post(self.build_url(self.path), data={
            'room_id': self.args[0],
            'user_id': self.args[1],
        })
        return response.json()['message']


class AllUsersInRoom(Command):

    path = '/auth/add_user/'

    #cmd: member_users room_id
    def execute(self):
        response = requests.get(self.build_url(self.path), params={
            'room_id': self.args[0]
        })
        res = ''
        for x in response.json()['users']:
            res = res + str(x)
            res = res + '\n'

        return res


class AllRoomsForUser(Command):

    path = '/auth/add_user/'

    # cmd: member_users user_id
    def execute(self):
        response = requests.get(self.build_url(self.path), params={
            'user_id': self.args[0]
        })
        res = ''
        for x in response.json()['rooms']:
            res = res + str(x)
            res = res + '\n'

        return res


class RemoveUserFromRoom(Command):

    path = '/auth/add_user/'

    # cmd: del_user_from_room room_id user_id
    def execute(self):
        response = requests.delete(self.build_url(self.path), data={
            'room_id': self.args[0],
            'user_id': self.args[1],
        })
        return response.json()['message']


class LoginUser(Command):

    path = '/auth/login/'

    #cmd: login user_id password
    def execute(self):
        user_id = self.args[0]
        password = self.args[1]

        response = requests.post(self.build_url(self.path), data={
            'user_id': user_id,
            'password': password,
        })

        print(response.json()['logged_in'])

        if response.json()['logged_in'] == True:
            return 'true'
        else:
            return 'false'



def route_command(c):

    commands_dict = {
        'create_user': CreateUser(),
        'get_user': FetchUser(),
        'del_user': DeleteUser(),
        'update_user': UpdateUser(),
        'create_room': CreateRoom(),
        'get_room': FetchRoom(),
        'del_room': DeleteRoom(),
        'update_room': UpdateRoom(),
        'member_users': AllUsersInRoom(),
        'member_rooms': AllRoomsForUser(),
        'add_user': AddUserToRoom(),
        'del_user_from_room': RemoveUserFromRoom(),
        'login': LoginUser(),
    }

    lst = c.split(' ')
    cmd = commands_dict[lst[0]]
    cmd.init(c)

    print(c)

    return cmd.execute()




if __name__ == '__main__':
    # print(route_command('create_user ronaq password'))
    # print(route_command('get_user raja'))
    # print(route_command('del_user 11'))
    # print(route_command('update_user 7 raja password'))

    # print(route_command('create_room birthday'))
    # print(route_command('get_room piano'))
    # print(route_command('del_room 6'))
    # print(route_command('update_room 8 piano'))

    # print(route_command('member_users 1'))
    # print(route_command('member_rooms 7'))
    # print(route_command('add_user 1 7'))
    # print(route_command('del_user_from_room 1 7'))
    # print(route_command('login 2 behura'))
    # print(route_command('login 2 behra'))

    #switch room_id
    pass
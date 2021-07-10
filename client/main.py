from client.chat.message import Chat


if __name__ == '__main__':
    print("Running chat client /-")

    m = Chat()

    m.populate("Hey there!****", "ronaq")

    print(m.serialize())

    m_ = Chat()

    m_.deserialize(m.serialize())

    print(m_.message)

    print(m_.user_name)
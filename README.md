# tattle_client
A chat client that talks that supports both one-on-one and group chats. Leverages redis pub/sub to coordinate chats.

This is an active repository. I keep rolling out updates on this. Stay tuned folks!!!

Requirements:

  - Python 3.8.0
  - Pyenv(Good to have)
  - redis
  
Setup:
  
1. Install python 3.8.0

2. Install redis

3. Install packages listed in requirements.txt


Main Script for app: tattle_client/client/gui/main.py


App Commands:

1. Create user: create_user <user> <password>

2. Get user details: get_user <user_name>

3. Delete user: del_user <user_id>

4. Update user password: update_user <user_id> <user-name> <new password>

5. Create a room: create_room <room_name>

6. Get room details: get_room <room_name>

7. Delete a room: del_room <room_id>

8. Update room: update_room <room_id> <room_name>

9. List down all members of room: member_users <room_id>

10. List down all rooms in which user is a member: member_rooms <user_id>

11. Adds a user to a room: add_user <room_id> <user_id>

12. Removes a user from a room: del_user_from_room <room_id> <user_id>

13. Login a user into the app: login <user_id> <password>

14. Switches to a room in the app. Make sure you're logged into the app first: switch <room_id>

Please let me know if you guys come across any bugs.

This app works with the chat_server that is in tattle_server repo(Django).
The SpringBoot version of this server is coming soon. Stay tuned!!!

Point of entry of code: https://github.com/JackSparrow999/tattle_client/blob/master/client/gui/main.py#L233

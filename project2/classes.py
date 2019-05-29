import collections
import datetime

class Chat:

    def __init__(self, name):
        # Details about the chat
        self.name = name
        self.users = []
        self.messages = collections.deque([], maxlen=100)

    def add_user(self, user):
        self.users.append(user)
        user.chat = self.name

    def remove_user(self, user):
        self.users.remove(user)
        user.chat = ''

    def add_message(self, user, message):
        self.user = user
        self.messages.append(message)

    def print_users(self):
        print(f"Users:")
        for user in self.users:
            print(user.username)

    def print_messages(self):
        print(f"Messages:")
        for message in self.messages:
            print(message.id, message.timestamp, ":", message.user, "-", message)

    def return_messages(self):
        chat = []
        for message in self.messages:
            if message.joinchat == False:
                line = "[ " + message.timestamp.strftime("%d-%b-%Y (%H:%M:%S)") + " ] " + message.user.username + " - " + message.message
            else:
                line = "[ " + message.timestamp.strftime("%d-%b-%Y (%H:%M:%S)") + " ] " + message.message
            chat.append(line)
        return chat

    def __repr__(self):
        return self.name

class User:

    def __init__(self, username):
        self.username = username
        self.chat = ''

    def __init__(self, username, chat):
        self.username = username
        self.chat = chat

    def __repr__(self):
        return self.username

    def __eq__(self, other):
        if not isinstance(other, User):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.username == other.username and self.chat == other.chat

class Message:

    counter = 1

    def __init__(self, user, message):
        self.id = Message.counter
        Message.counter += 1
        self.message = message
        self.user = user
        self.timestamp = datetime.datetime.now()
        self.joinchat = False

    def print_message(self):
        line = "[ " + self.timestamp.strftime("%d-%b-%Y (%H:%M:%S)") + " ] " + self.user.username + " - " + self.message
        return line

    def return_all(self):
        output = [self.id, self.timestamp, self.user, self.message]
        return output

    def __repr__(self):
        return self.message

def main():

    # Test creating user objects
    print("Generate user objects...")
    alice = User(username="Alice")
    bob = User(username="Bob")
    matt = User(username="Matt")
    aaron = User(username="Aaron")
    print("[DONE]")
    print()

    # Test creating message objects
    print("Generate message objects...")
    m1 = Message(user=alice, message="Wassup.")
    m2 = Message(user=bob, message="Nothin much.")
    tada = Message(user=matt, message="Hmm...")
    print("[DONE]")
    print()

    # Test creating chat object
    print("Generate chat object...")
    c1 = Chat(name="Test Chat")
    print("[DONE]")
    print()

    # Add users to chat.
    # NOTE: Two checks should happen for add_user: 1. Check if user object exists, 2. check if user object already in the chat
    c1.add_user(alice)
    c1.add_user(bob)
    c1.add_user(matt)
    c1.add_user(aaron)

    # Create messages in the chat.
    # NOTE: Two checks need to happen before add_message: 1. Check if user object exists, 2. check if user object is in Chat.users
    c1.add_message(user=alice, message=m1)
    c1.add_message(user=bob, message=m2)
    c1.add_message(user=matt, message=tada)
    c1.add_message(user=aaron, message=Message(user=aaron, message="Does this work?"))

    # Print chat info
    print("Return chat information...")
    c1.print_users()
    print()
    c1.print_messages()
    print("[DONE]")
    print()

if __name__ == "__main__":
    main()

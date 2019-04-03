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

    def add_message(self, user, message):
        self.messages.append((user, message))

    def print_users(self):
        print(f"Users:")
        print(f"{self.users}")
        print()

    def print_chat(self):
        print(f"Messages in {self.name}:")
        for message in self.messages:
            print(message[0].name + ' - "' + message[1] + '"')
        print()

class User:

    def __init__(self, name):
        self.name = name
        self.chats = []

    def __repr__(self):
        return self.name

def main():

    # Create chat.
    c1 = Chat(name="Test Chat")

    # Create users.
    alice = User(name="Alice")
    bob = User(name="Bob")

    # Add users to chat.
    c1.add_user(alice)
    c1.add_user(bob)

    # Create messages in the chat.
    c1.add_message(alice, "Hihi")
    c1.add_message(bob, "Yoyo")

    # Print participating users.
    c1.print_users()

    # Print results
    c1.print_chat()


if __name__ == "__main__":
    main()

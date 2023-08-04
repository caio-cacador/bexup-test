from connections.message_broker import Queue, MessageBrokerConsumerConnection


def main():
    message_broken = MessageBrokerConsumerConnection()
    message_broken.start()


if __name__ == "__main__":
    main()

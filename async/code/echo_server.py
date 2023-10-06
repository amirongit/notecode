from task_scheduler import CreateTask, Scheduler, WaitRead, WaitWrite

from socket import socket, AF_INET, SOCK_STREAM


def handle(client: socket):
    while True:
        yield WaitRead(client)
        if (data := client.recv(65536)) is None:
            break
        yield WaitWrite(client)
        client.send(data)
    client.close()
    yield


def server(port: int):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(5)
    while True:
        yield WaitRead(sock)
        client, _ = sock.accept()
        yield CreateTask(handle(client))


if __name__ == '__main__':
    s = Scheduler()
    s.create(server(45000))
    s.loop()

from app.services import SynchronizerService, NotificatorService

if __name__ == '__main__':
    services = [
        SynchronizerService(),
        NotificatorService()
    ]
    for s in services:
        s.start()

    for s in services:
        s.join()

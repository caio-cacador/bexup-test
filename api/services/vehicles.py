from api.connections.vehicles import VehiclesConnection


class VehicleService():
    def __init__(self) -> None:
        self.connection = VehiclesConnection()


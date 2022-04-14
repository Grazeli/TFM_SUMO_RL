
class rewardTest:
    def __init__(self, traci) -> None:
        self._traci = traci


    def compute_reward(self):
        cars_in_simulation = self._traci.vehicle.getIDList()

        if len(cars_in_simulation) > 0:

            car_ID = cars_in_simulation[0]

            cumulative_waiting_time = self._traci.vehicle.getAccumulatedWaitingTime(car_ID)

            next_TLS = self._traci.vehicle.getNextTLS(car_ID)

            print('Car {}, CWT: {}, next TLS: {}'.format(car_ID, cumulative_waiting_time, next_TLS))

        else:
            print('No car in this time step')
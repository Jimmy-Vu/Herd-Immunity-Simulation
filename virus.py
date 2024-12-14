class Virus(object):
    # Properties and attributes of the virus used in Simulation.
    def __init__(self, name, repro_rate, mortality_rate):
        # Define the attributes of your your virus
        self.name = name
        # COMPLETED Define the other attributes of Virus
        if repro_rate < 0 or repro_rate > 1:
            print('The reproduction rate must be between 0 and 1.')
            raise ValueError("The reproduction rate must be between 0 and 1.")
        if mortality_rate < 0 or mortality_rate > 1:
            print('The mortality rate must be between 0 and 1.')
            raise ValueError("The mortality rate must be between 0 and 1.")

        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate



# Test this class
if __name__ == "__main__":
    # Test your virus class by making an instance and confirming
    # it has the attributes you defined
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3
    print('All tests passed.')

import random
import sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # COMPLETED: Create a Logger object and bind it to self.logger.
        self.logger = Logger("simulation_log.txt")

        # COMPLETED: Store the virus in an attribute
        # COMPLETED: Store pop_size in an attribute
        # COMPLETED: Store the vacc_percentage in a variable
        # COMPLETED: Store initial_infected in a variable
        # You need to store a list of people (Person instances)
        # Some of these people will be infected some will not.
        # Use the _create_population() method to create the list and
        # return it storing it in an attribute here.
        # COMPLETED: Call self._create_population() and pass in the correct parameters.
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected

        self.population = self._create_population()
        self.newly_infected = []
        self.total_dead = 0

    def _create_population(self):
        # COMPLETED: Create a list of people (Person instances). This list
        # should have a total number of people equal to the pop_size.
        # Some of these people will be uninfected and some will be infected.
        # The number of infected people should be equal to the the initial_infected
        # COMPLETED: Return the list of people
        population = []
        num_vaccinated = int(self.pop_size * self.vacc_percentage)
        num_unvaccinated = self.pop_size - num_vaccinated - self.initial_infected

        # vaccinated people
        for i in range(num_vaccinated):
            population.append(Person(i, True))

        # unvaccinated people
        for i in range(num_vaccinated, num_vaccinated + num_unvaccinated):
            population.append(Person(i, False))

        # initial infected
        for i in range(num_vaccinated + num_unvaccinated, self.pop_size):
            population.append(Person(i, False, self.virus))

        return population

    def _simulation_should_continue(self):
        # This method will return a booleanb indicating if the simulation
        # should continue.
        # The simulation should not continue if all of the people are dead,
        # or if all of the living people have been vaccinated.
        # COMPLETED: Loop over the list of people in the population. Return True
        # if the simulation should continue or False if not.
        for person in self.population:
            if person.is_alive and not person.is_vaccinated:
                return True
        return False

    def run(self):
        # This method starts the simulation. It should track the number of
        # steps the simulation has run and check if the simulation should
        # continue at the end of each step.
        self.logger.write_metadata(
            self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate
        )

        time_step_counter = 0
        should_continue = True
        while should_continue:
            # COMPLETED: Increment the time_step_counter
            # COMPLETED: for every iteration of this loop, call self.time_step()
            # Call the _simulation_should_continue method to determine if
            # the simulation should continue
            time_step_counter += 1
            self.time_step()
            should_continue = self._simulation_should_continue()
            self.logger.log_interactions(
                time_step_counter, len(
                    self.population), len(self.newly_infected)
            )

        # COMPLETED: Write meta data to the logger. This should be starting
        # statistics for the simulation. It should include the initial
        # population size and the virus.
        self.logger.log_infection_survival(
            time_step_counter, len(self.population), self.total_dead
        )
        # COMPLETED: When the simulation completes you should conclude this with
        # the logger. Send the final data to the logger.
        print(f"Simulation ended after {time_step_counter} time steps.")

    def time_step(self):
        # This method will simulate interactions between people, calulate
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other
        # people in the population
        # COMPLETED: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people
        # Run interactions by calling the interaction method below. That method
        # takes the infected person and a random person
        for person in self.population:
            if person.infection and person.is_alive:
                for _ in range(100):
                    random_person = random.choice(self.population)
                    while not random_person.is_alive:
                        random_person = random.choice(self.population)
                    self.interaction(person, random_person)

        self._infect_newly_infected()

    def interaction(self, infected_person, random_person):
        # COMPLETED: Finish this method.
        # The possible cases you'll need to cover are listed below:
        # random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        #     generate a random number between 0.0 and 1.0.  If that number is smaller
        #     than repro_rate, add that person to the newly infected array
        #     Simulation object's newly_infected array, so that their infected
        #     attribute can be changed to True at the end of the time step.
        # COMPLETED: Call logger method during this method.
        if random_person.is_vaccinated:
            return
        if random_person.infection:
            return
        if random_person.is_alive and random.random() < self.virus.repro_rate:
            self.newly_infected.append(random_person)

    def _infect_newly_infected(self):
        # COMPLETED: Call this method at the end of every time step and infect each Person.
        # COMPLETED: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.newly_infected:
            person.infection = self.virus
        self.newly_infected = []


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the simulation
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()

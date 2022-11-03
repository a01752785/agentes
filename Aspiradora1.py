# M1. Actividad
# Erika García A01745158
# David Damián A01752785

import mesa

# def compute_gini(model):
#     agent_wealths = [agent.wealth for agent in model.schedule.agents]
#     x = sorted(agent_wealths)
#     N = model.num_agents
#     B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
#     return 1 + (1 / N) - 2 * B

class DirtynessAgent(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.dirty = True
    
    def step(self):
        pass

    def clean(self):
        self.dirty = False

    def is_clean(self):
        return self.dirty


class AspiradoraAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        moved = False
        for cellmate in cellmates:
            if isinstance(cellmate, DirtynessAgent):
                if not cellmate.is_clean():
                    cellmate.clean()
                else:
                    self.move()
                    moved = True
        if not moved:
            self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    

class AspiradoraModel(mesa.Model):
    def __init__(self, width, height, num_agents, dirty_percentage):
        self.num_agents = num_agents
        self.dirty_percentage = dirty_percentage
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        for i in range(int(self.dirty_percentage * width * height)):
            agent = DirtynessAgent(self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))


        for i in range(self.num_agents):
            agent = AspiradoraAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))
        
        # self.datacollector = mesa.DataCollector(
        #     model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        # )
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    # Run the model
    model = AspiradoraModel(10, 10, 50, 0.5)
    for i in range(100):
        model.step()

    # agent_wealth = model.datacollector.get_agent_vars_dataframe()
    # agent_wealth.head()
    
    # gini = model.datacollector.get_model_vars_dataframe()
    # gini.plot()
    # plt.show()
    # end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
    # end_wealth.hist(bins=range(agent_wealth.Wealth.max() + 1))
    # plt.show()
    # one_agent_wealth = agent_wealth.xs(14, level="AgentID")
    # one_agent_wealth.Wealth.plot()
    # plt.show()

    # # save the model data (stored in the pandas gini object) to CSV
    # gini.to_csv("model_data.csv")

    # # save the agent data (stored in the pandas agent_wealth object) to CSV
    # agent_wealth.to_csv("agent_data.csv")

    # params = {"width": 10, "height": 10, "N": range(10, 500, 10)}

    # results = mesa.batch_run(
    #     MoneyModel,
    #     parameters=params,
    #     iterations=5,
    #     max_steps=100,
    #     number_processes=1,
    #     data_collection_period=1,
    #     display_progress=True,
    # )

    # import pandas as pd

    # results_df = pd.DataFrame(results)
    # print(results_df.keys())

    # results_filtered = results_df[(results_df.AgentID == 0) & (results_df.Step == 100)]
    # N_values = results_filtered.N.values
    # gini_values = results_filtered.Gini.values
    # plt.scatter(N_values, gini_values)
    # plt.show()
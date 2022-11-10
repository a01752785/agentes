# M1. Actividad
# Erika García A01745158
# David Damián A01752785

import mesa


def compute_clean_cells(model):
    cells = model.height * model.width
    dirty_cells = 0
    for agent in model.schedule.agents:
        if isinstance(agent, DirtynessAgent):
            if not agent.is_clean():
                dirty_cells += 1
    clean_ratio = (cells - dirty_cells) / cells * 100
    return clean_ratio


def compute_agent_moves(model):
    movements = 0
    for agent in model.schedule.agents:
        if isinstance(agent, AspiradoraAgent):
            movements += agent.moves
    return movements


class DirtynessAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dirty = True

    def step(self):
        pass

    def clean(self):
        self.dirty = False

    def is_clean(self):
        return not self.dirty


class AspiradoraAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0

    def step(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        turn = False
        for cellmate in cellmates:
            if isinstance(cellmate, DirtynessAgent):
                if not cellmate.is_clean():
                    cellmate.clean()
                    turn = True
                else:
                    self.move()
                    turn = True
        if not turn:
            self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.moves += 1


class AspiradoraModel(mesa.Model):
    def __init__(self, width, height, num_agents,
                 dirty_percentage):
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.dirty_percentage = dirty_percentage
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        num_dirty_cells = int(self.dirty_percentage * width * height)
        used_coordinates = set()
        for i in range(num_dirty_cells):
            agent = DirtynessAgent(i, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (x, y) in used_coordinates:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            used_coordinates.add((x, y))

        for i in range(self.num_agents):
            agent = AspiradoraAgent(i + num_dirty_cells, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        self.datacollector = mesa.DataCollector(
            model_reporters={"CleanCells": compute_clean_cells,
                             "TotalMovements": compute_agent_moves}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()


if __name__ == '__main__':
    width_param = int(input("Ingrese ancho: "))
    height_param = int(input("Ingrese alto: "))
    num_agents_param = int(input("Ingrese el numero de agentes: "))
    dirty_percentage_param = \
        float(input("Ingrese el porcentaje de casillas sucias (0 a 1): "))
    max_steps_param = int(input("Ingrese el numero de pasos maximos: "))
    iterations_param = int(input("Ingrese el numero de iteraciones: "))
    params = {"width": width_param,
              "height": height_param,
              "num_agents": num_agents_param,
              "dirty_percentage": dirty_percentage_param}

    results = mesa.batch_run(
        AspiradoraModel,
        parameters=params,
        iterations=iterations_param,
        max_steps=max_steps_param,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    import pandas as pd
    results_df = pd.DataFrame(results)
    clean_cells = []
    total_movements = []
    steps = []
    for i in range(iterations_param):
        # Obtain the row containing the general outcome of the
        # i-th run
        run_info = results_df.query(f'RunId == {i}') \
            .nlargest(1, 'TotalMovements')
        print(run_info)
        clean_cells.append(run_info.iloc[0]['CleanCells'])
        total_movements.append(run_info.iloc[0]['TotalMovements'])
    for i in range(iterations_param):
        step_info = results_df.query(f'RunId == {i} & CleanCells == 100')
        if step_info.size != 0:
            steps.append(step_info['Step'].iloc[0])
            print(step_info.iloc[0])
        else:
            steps.append(max_steps_param)

    import matplotlib.pyplot as plt
    plt.hist(clean_cells, bins=20)
    plt.title('Percentage of clean cells')
    plt.xlabel("Percentage")
    plt.ylabel("Frequency")
    plt.show()
    plt.hist(total_movements, bins=20)
    plt.title('Total movements')
    plt.xlabel("Number of steps")
    plt.ylabel("Frequency")
    plt.show()
    plt.hist(steps, bins=20)
    plt.title('Maximum time')
    plt.xlabel("Time (steps)")
    plt.ylabel("Frequency")
    plt.show()

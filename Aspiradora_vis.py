import mesa

from Aspiradora import AspiradoraModel, DirtynessAgent, AspiradoraAgent


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if type(agent) is DirtynessAgent:
        if not agent.is_clean():
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "pink"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.3
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
# chart = mesa.visualization.ChartModule(
#     [{"Label": "Gini", "Color": "#0000FF"}], data_collector_name="datacollector"
# )

model_params = {
    "num_agents": mesa.visualization.Slider(
        "Number of agents",
        1,
        1,
        50,
        1,
        description="Choose how many agents to include in the model",
    ),
    "dirty_percentage": mesa.visualization.Slider(
        "Dirty Percentage",
        0.2,
        0,
        1,
        1,
        description="Choose the percentage of dirty cells",
    ),
    "width": int(input()),
    "height": int(input()),
}

server = mesa.visualization.ModularServer(
    AspiradoraModel, [grid], "Aspiradora Model", model_params
)
server.port = 8521

if __name__ == '__main__':
    server.launch()

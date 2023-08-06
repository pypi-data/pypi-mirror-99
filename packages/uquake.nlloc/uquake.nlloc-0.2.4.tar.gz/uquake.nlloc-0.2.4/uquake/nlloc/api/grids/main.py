import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from uquake.nlloc import (ModelLayer, LayeredVelocityModel,
                          VelocityGridEnsemble)


class LayeredVelocityModelDescription(BaseModel):
    model_name: str
    project: str
    network: str
    origin: list
    dimensions: list
    spacing: list
    z: list
    vp: list
    vs: list


app = FastAPI()


@app.post('/create_layered_velocity/')
async def create_layered_velocity(data: LayeredVelocityModelDescription):
    p_layered_model = LayeredVelocityModel()
    s_layered_model = LayeredVelocityModel()
    for z, vp, vs in zip(data.z, data.vp, data.vs):
        p_layered_model.add_layer(ModelLayer(z, vp))
        s_layered_model.add_layer(ModelLayer(z, vs))

    # from ipdb import set_trace
    # set_trace()

    p_velocity_3d = p_layered_model.gen_3d_grid(data.network, data.dimensions,
                                                data.origin, data.spacing)
    s_velocity_3d = s_layered_model.gen_3d_grid(data.network, data.dimensions,
                                                data.origin, data.spacing)
    velocity_grids = VelocityGridEnsemble(p_velocity_3d, s_velocity_3d)


    return


if __name__ == '__main__':
    uvicorn.run('grid:app', reload=True)

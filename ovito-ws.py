# python script for Wigner-Seitz analysis by using ovitos
# Syntax: ovitos ws.py

from ovito.io import *
from ovito.data import *
from ovito.modifiers import *
import numpy as np

node = import_file("1pka.xyz", multiple_frames=True)

# Perform Wigner-Seitz analysis:
ws = WignerSeitzAnalysisModifier(
    per_type_occupancies = False, 
    eliminate_cell_deformation = True,
    reference_frame=2)
ws.reference.load("nvt.xyz", multiple_frames=True)
node.modifiers.append(ws)

select = SelectExpressionModifier(expression="ParticleType==3 && Occupancy==0 && (Position.X-63.5)^2+(Position.Y-63.5)^2+(Position.Z-63.5)^2>2500")
node.modifiers.append(select)

# Let OVITO do the computation and export the number of identified 
# defects as a function of simulation time to a text file:
#print('SelectExpression.num_selected')
export_file(node, "Y-vac2.txt", "txt", 
    columns = ['Timestep', 'SelectExpression.num_selected'],
    multiple_frames = True)

# Export the XYZ coordinates of just the antisites by removing all other atoms.
node.modifiers.append(InvertSelectionModifier())
node.modifiers.append(DeleteSelectedParticlesModifier())
export_file(node, "Y-vac.xyz", "xyz", 
    columns = ['Position.X', 'Position.Y', 'Position.Z'],
    multiple_frames = True)

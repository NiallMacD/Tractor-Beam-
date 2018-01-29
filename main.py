

# -------------------------Import Libaries------------------------------------

import constants; import numpy as np; from calc_pressure_field import calc_pressure_field
import transducer_placment; from vti_writer import vti_writer; import phase_algorithms;

# -------------------------Variables to set------------------------------------

#trans_to_delete = [4,5,6,13,14,15,16,17,22,23,24,25,26,31,32,33,34,35,40,41,42,43,44,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87]  # List of unwanted transducers leave blank to keep all 
#rt = transducer_placment.big_daddy()   # spcing , x nummber, y number of transducers
#rt = transducer_placment.delete_transducers(rt,trans_to_delete)
rt = transducer_placment.array_grid(0.01,2,2) 

ntrans = len (rt)   # Total number of transducers in grid

nt = transducer_placment.direction_vectors(ntrans) # nt is the direction vector of each transducer

phi_focus = phase_algorithms.phase_find(rt,0,0.02,0) # phi is the initial phase of each transducer to focus on a point
phi = phase_algorithms.add_twin_signature(rt, np.copy(phi_focus))


# ----------------------Setting up output arrays-------------------------------

p = np.zeros ((constants.npoints,constants.npoints,constants.npoints,ntrans), dtype=complex)
pcombined = np.zeros ((constants.npoints,constants.npoints,constants.npoints),dtype=complex)

px = np.zeros ((constants.npoints,constants.npoints,constants.npoints), dtype=complex)
py = np.copy(px); pz = np.copy(px)

ux = np.zeros ((constants.npoints,constants.npoints,constants.npoints), dtype=float)
uy = np.copy(ux); uz = np.copy(ux)

pabs = np.zeros ((constants.npoints,constants.npoints,constants.npoints), dtype=float) 
pxabs = np.copy(pabs); pyabs = np.copy(pabs); pzabs = np.copy(pabs)

u = np.zeros ((constants.npoints,constants.npoints,constants.npoints), dtype=float)

height = np.zeros ((constants.npoints,constants.npoints,constants.npoints), dtype=float)

# ----------------------------------------------------------------------------

p = calc_pressure_field(rt, nt, ntrans, phi) # calculate pressure field

# -----------------Loop to sum pressure of all transducers---------------------

height = np.multiply(constants.deltaxyz, np.indices([21,21,21])[1]) # 55 times faster
pcombined_numpy = np.sum(p, axis = 3) 

# -----------------Calculating derrivitive of the pressure field---------------

diff_p = np.gradient(pcombined,constants.deltaxyz)
px = np.copy(diff_p[0]); py = np.copy(diff_p[1]); pz = np.copy(diff_p[2])

# ----------------- Calculating the Gork’ov potential-------------------------

# Calculating absuloute values for the pressure field and its derrivitives
       
pabs   = np.absolute(pcombined)  
pxabs  = np.absolute(px)  
pyabs  = np.absolute(py)  
pzabs  = np.absolute(pz)  

# Calculating Gork’ov potential u (Including gravity)

u = ( np.subtract( np.subtract( np.multiply(np.multiply(2, constants.k1), np.power(pabs, 2) ), 
np.multiply( np.multiply(2, constants.k2), np.add(np.add(np.power(pxabs, 2), np.power(pyabs, 2)), np.power(pzabs, 2) ) ) ),  
np.multiply(constants.p_mass, np.multiply(constants.gravity, np.copy(height)))) ) # Gravity term

# -----------------Calculating derrivitive of Gork’ov potential ---------------

diff_u = np.gradient(u,constants.deltaxyz)
ux = np.copy(diff_u[0]); uy = np.copy(diff_u[1]); uz = np.copy(diff_u[2])

# -----------------Calculating force on particle ---------------

fx = np.copy(-ux); fy = np.copy(-uy); fz = np.copy(-uz)

# -------------------Creating output images and vtk file----------------------

vti_writer (constants.npoints, pabs, fx, fy, fz, u)

print("Calculations compleated successfuly")




"""


# ------------Main file but using the analyitical pressure equations-----------

import constants; import numpy as np; from calc_pressure_field import calc_pressure_field
import transducer_placment; from vti_writer import vti_writer; import phase_algorithms; import algorithms;


#rt = transducer_placment.big_daddy()
rt = transducer_placment.array_grid(0.01, 6, 6) 
ntrans = len (rt)
nt = transducer_placment.direction_vectors(ntrans)
phi_focus = phase_algorithms.phase_find(rt,0, 0.02, 0) # phi is the initial phase of each transducer to focus on a point
phi = phase_algorithms.add_twin_signature(rt, np.copy(phi_focus))


################# Wont work now without adding p_abs to the acoustic_potential function in algorithms(invalid index to scalar variable.)
u = np.zeros ((constants.npoints,constants.npoints,constants.npoints), dtype=float)
p_abs = np.zeros ((constants.npoints,constants.npoints,constants.npoints), dtype=float)

x = constants.x; y = constants.y; z = constants.z
gsize = constants.gsize
for xloop in range (0,constants.npoints):
    for yloop in range (0,constants.npoints):
        for zloop in range (0,constants.npoints):
            
            r = [ x  , y , z ]          # Point in space for each itteriation
            u_and_p = algorithms.acoustic_potential(r, rt, phi, nt)
            u[xloop,yloop,zloop] = u_and_p[0] - (constants.p_mass*constants.gravity*(yloop*constants.deltaxyz)) # including potential energy (mass*g*height)
            p_abs[xloop,yloop,zloop] = u_and_p[1]            
                        
            z = z + constants.deltaxyz    # Adding delta to x,y and z
        y = y + constants.deltaxyz
        z = -gsize               # Resetting the value of z to start value for next loop
    x = x + constants.deltaxyz
    y = 0                       # Resetting the value of y to start value for next loop
    z = -gsize                   # Resetting the value of z to start value for next loop
x = -gsize # Initial values of x,y and z in (m) Grid volume
y = 0.00
z = -gsize


diff_u = np.gradient(u,constants.deltaxyz)
ux = np.copy(diff_u[0]); uy = np.copy(diff_u[1]); uz = np.copy(diff_u[2])

# -----------------Calculating force on particle ---------------

fx = np.copy(-ux); fy = np.copy(-uy); fz = np.copy(-uz)

vti_writer (constants.npoints,p_abs,fx,fy,fz,u)

print("Calculations compleated successfuly")


"""













"""
This is a demonstration of my idea that any gamma ray photon which is produced inside the Sun's core due to proton-proton chain reaction during its thermonuclear fusion takes:
1. a self-avoiding walk(SAW) inside the core of the Sun
2. a simple-random walk(SRW) inside the radiative zone of the Sun
3. a non-reversing random walk(NRRW) inside the convective zone of the Sun
provided the step size is very small as compared to the radius of the zone
"""
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np 


# Defining constants and creating Sun's core, radiative zone, convective zone
r_c, r_rz, r_cz = 6, 14, 20                
sz_c, sz_rz, sz_cz = 0.25, 0.20, 0.25  
pd_c, pd_rz, pd_cz = [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]                                       
x, y = [0], [0]
t = np.linspace(0, 2*np.pi, 361)
x_c, y_c = r_c*np.cos(t), r_c*np.sin(t)
x_rz, y_rz = r_rz*np.cos(t), r_rz*np.sin(t)
x_cz, y_cz = r_cz*np.cos(t), r_cz*np.sin(t)
directions = np.array(["East", "West", "North", "South"])


# Assuming that the walk of a gamma ray photon inside the Sun's Core is self-avoiding
def SAW_Inside_Core(r_max, sz, pd):
    steps = 0
    while x[-1]**2 + y[-1]**2 < r_max**2:
        selection = np.random.choice(directions, p = pd)
        if selection == "East":
            x.append(np.round(x[-1] + sz, 2))             
            y.append(y[-1])
        elif selection == "West":
            x.append(np.round(x[-1] - sz, 2))     
            y.append(y[-1])
        elif selection == "North":
            x.append(x[-1])    
            y.append(np.round(y[-1] + sz, 2))
        else:
            x.append(x[-1])    
            y.append(np.round(y[-1] - sz, 2))
        
        while (x[-1] in x[:-1]) and (y[-1] in y[:-1]):
            del x[-1]
            del y[-1]
            selection = np.random.choice(directions, p = pd)
            if selection == "East":
                x.append(np.round(x[-1] + sz, 2))     
                y.append(y[-1])
            elif selection == "West":
                x.append(np.round(x[-1] - sz, 2))     
                y.append(y[-1])
            elif selection == "North":
                x.append(x[-1])     
                y.append(np.round(y[-1] + sz, 2))
            else:
                x.append(x[-1])     
                y.append(np.round(y[-1] - sz, 2))
        steps = steps + 1
    return steps
n_c = SAW_Inside_Core(r_c, sz_c, pd_c)
      

# Assuming that the walk of a gamma ray photon inside the Sun's Radiative Zone is simply random    
def SRW_Inside_Radiative_Zone(r_min, r_max, sz, pd):
    steps = 0
    while (x[-1]**2 + y[-1]**2 >= r_min**2) and (x[-1]**2 + y[-1]**2 < r_max**2):
        selection = np.random.choice(directions, p = pd)
        if selection == "East":
            x.append(np.round(x[-1] + sz, 2))     
            y.append(y[-1])
        elif selection == "West":
            x.append(np.round(x[-1] - sz, 2))     
            y.append(y[-1])
        elif selection == "North":
            x.append(x[-1])     
            y.append(np.round(y[-1] + sz, 2))
        else:
            x.append(x[-1])     
            y.append(np.round(y[-1] - sz, 2))
        
        if (x[-1]**2 + y[-1]**2 < r_min**2):
            del x[-1]
            del y[-1]
            continue
        
        if (x[-1]**2 + y[-1]**2 >= r_max**2):
            lsd_rz=selection
        
        steps = steps + 1
    return steps, lsd_rz
n_rz, lsd_rz = SRW_Inside_Radiative_Zone(r_c, r_rz, sz_rz, pd_rz)
    
    
# Assuming that the walk of a gamma ray photon inside the Sun's Convective Zone is non-reversing   
def NRRW_Inside_Convective_Zone(r_min, r_max, sz, pd):
    steps, z = 0, [lsd_rz]
    while (x[-1]**2 + y[-1]**2 >= r_min**2) and (x[-1]**2 + y[-1]**2 < r_max**2):
        selection = np.random.choice(directions, p = pd)
        z.append(selection)
        while (((z[-2] == "East") and (z[-1] == "West")) or ((z[-2] == "West") and (z[-1] == "East")) or ((z[-2] == "North") and (z[-1] == "South")) or ((z[-2] == "South") and (z[-1] == "North"))):
            del z[-1]
            selection = np.random.choice(directions, p = pd)
            z.append(selection)
            
        if selection == "East":
            x.append(np.round(x[-1] + sz, 2))     
            y.append(y[-1])
        elif selection == "West":
            x.append(np.round(x[-1] - sz, 2))     
            y.append(y[-1])
        elif selection == "North":
            x.append(x[-1])     
            y.append(np.round(y[-1] + sz, 2))
        else:
            x.append(x[-1])     
            y.append(np.round(y[-1] - sz, 2))
        
        if (x[-1]**2 + y[-1]**2 < r_min**2):
            del x[-1]
            del y[-1]
            del z[-1]
            continue
        steps = steps + 1
    return steps
n_cz = NRRW_Inside_Convective_Zone(r_rz, r_cz, sz_cz, pd_cz)


# Calculating total number of steps taken to reach the Sun's photosphere
n = n_c + n_rz + n_cz
X = np.array(x)
Y = np.array(y)


# It must be called in canvas = plt.axes(xlim=(-13,13), ylim=(-13,13)) to zoom the walk if you want 
def size(n):
    if n>0:
        return 1
    else:
        return -1
    

# Creating an animation for the solar photon's walk
fig = plt.figure()
canvas = plt.axes(xlim=(-21,21), ylim=(-21,21))         
photon, = canvas.plot(X[0], Y[0], marker="*", markerfacecolor="red", markersize=15, label="Gamma Ray Photon")
walk, = canvas.plot(X[0], Y[0], color="blue")


def journey(i):
    photon.set_data(X[i], Y[i])
    walk.set_data(x[:i+1], y[:i+1])
    return photon, walk,


anime = ani.FuncAnimation(fig, journey, frames = n+1, interval = 1, blit = True, repeat= False)
plt.plot(x_c, y_c, linestyle=":", color="brown")
plt.plot(x_rz, y_rz, linestyle=":", color="brown")
plt.plot(x_cz, y_cz, linestyle=":", color="brown")
plt.fill(x_cz, y_cz, color="gold")
fig.suptitle(f"Solar Photon Walk of {n} steps inside the Sun's Interior", color="fuchsia")
fig.patch.set_facecolor("black")
fig.tight_layout()
plt.annotate("Core",(-0.5,-5.5))
plt.annotate("Radiative Zone", (-1.5, -13.5))
plt.annotate("Convective Zone", (-1.75, -19.5))
plt.annotate("Courtesy of Rishikesh Jha",(16, -20), color="fuchsia")
plt.annotate(f"\n Core: {n_c} steps of length {sz_c} units", (-21,-18), color="fuchsia")
plt.annotate(f"\n Radiative Zone: {n_rz} steps of length {sz_rz} units", (-21,-19), color="fuchsia")
plt.annotate(f"\n Convective Zone: {n_cz} steps of length {sz_cz} units", (-21,-20), color="fuchsia")
plt.axis(False)
plt.legend(loc="best")
plt.show()
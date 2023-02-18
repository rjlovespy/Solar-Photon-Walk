import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np 


r_c, r_rz, r_cz = 3, 7, 10               
sz_c, sz_rz, sz_cz = 0.20, 0.25, 0.30                                     
x, y = [0], [0]
t = np.linspace(0, 2*np.pi, 361)
x_c, y_c = r_c*np.cos(t), r_c*np.sin(t)
x_rz, y_rz = r_rz*np.cos(t), r_rz*np.sin(t)
x_cz, y_cz = r_cz*np.cos(t), r_cz*np.sin(t)
directions = np.array(["East", "West", "North", "South"])

    
def SRW():
    n_c, n_rz, n_cz = 0, 0, 0
    while x[-1]**2 + y[-1]**2 < r_cz**2:
        if x[-1]**2 + y[-1]**2 < r_c**2:
            selection = np.random.choice(directions)
            if selection == "East":
                x.append(np.round(x[-1] + sz_c, 2))     
                y.append(y[-1])
            elif selection == "West":
                x.append(np.round(x[-1] - sz_c, 2))     
                y.append(y[-1])
            elif selection == "North":
                x.append(x[-1])     
                y.append(np.round(y[-1] + sz_c, 2))
            else:
                x.append(x[-1])     
                y.append(np.round(y[-1] - sz_c, 2))
            n_c = n_c + 1
        elif (x[-1]**2 + y[-1]**2 >= r_c**2) and (x[-1]**2 + y[-1]**2 < r_rz**2):
            selection = np.random.choice(directions)
            if selection == "East":
                x.append(np.round(x[-1] + sz_rz, 2))     
                y.append(y[-1])
            elif selection == "West":
                x.append(np.round(x[-1] - sz_rz, 2))     
                y.append(y[-1])
            elif selection == "North":
                x.append(x[-1])     
                y.append(np.round(y[-1] + sz_rz, 2))
            else:
                x.append(x[-1])     
                y.append(np.round(y[-1] - sz_rz, 2))
            n_rz = n_rz + 1
        else:
            selection = np.random.choice(directions)
            if selection == "East":
                x.append(np.round(x[-1] + sz_cz, 2))     
                y.append(y[-1])
            elif selection == "West":
                x.append(np.round(x[-1] - sz_cz, 2))     
                y.append(y[-1])
            elif selection == "North":
                x.append(x[-1])     
                y.append(np.round(y[-1] + sz_cz, 2))
            else:
                x.append(x[-1])     
                y.append(np.round(y[-1] - sz_cz, 2))
            n_cz = n_cz + 1
    return n_c, n_rz, n_cz
n_c, n_rz, n_cz = SRW()
    

n = n_c + n_rz + n_cz
X = np.array(x)
Y = np.array(y)


fig=plt.figure()
ax=fig.add_subplot()
GRP, = ax.plot(X[0],Y[0], marker="*", mfc="red", mec="red", ms=15, label="Gamma Ray Photon")
walk, = ax.plot(X[0],Y[0], color="blue")


def update(i):
    GRP.set_data(X[i],Y[i])
    walk.set_data(X[:i+1],Y[:i+1])
    return walk, GRP, 


anime = ani.FuncAnimation(fig, update, frames=n, interval=10, blit=True, repeat=True)
ax.plot(x_c, y_c, linestyle=":", color="brown")
ax.plot(x_rz, y_rz, linestyle=":", color="brown")
ax.plot(x_cz, y_cz, linestyle=":", color="brown")
fig.suptitle(f"Solar Photon Walk of {n} steps inside the Sun's Interior", color="fuchsia")
fig.patch.set_facecolor("black")
ax.annotate("Core",(-0.5,-r_c+0.25))
ax.annotate("Radiative Zone", (-1,-r_rz+0.25))
ax.annotate("Convective Zone", (-1.25,-r_cz+0.25))
ax.annotate("Courtesy of Rishikesh Jha",(r_cz-2.5,-r_cz), color="fuchsia")
ax.annotate(f"\n Core: {n_c} steps SAW of size {sz_c} units", (-r_cz-1,-r_cz+1), color="fuchsia")
ax.annotate(f"\n Radiative Zone: {n_rz} steps SRW of size {sz_rz} units", (-r_cz-1,-r_cz+0.5), color="fuchsia")
ax.annotate(f"\n Convective Zone: {n_cz} steps NRRW of size {sz_cz} units", (-r_cz-1,-r_cz), color="fuchsia")
ax.fill(x_cz, y_cz, color="gold")
ax.axis(False)
plt.legend(loc="best")
# anime.save("solar_photon_walk.gif")
plt.show()

# importing modules and extensions.
""" FigureCanvasTkAgg imported from matplotlib.backends, 
    tkinter and LightPipes modules used. """
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as Tk
from LightPipes import *

# creating window for output.
root=Tk.Tk()
root.wm_title("YDSE Visualization")

# initiating parameters.
""" wavelength=530nm, size=10nm, N=150, distance from screen=90cm,
    slit-radius=0.02mm, slit-distance=0.5mm, phi->0. """
wl=530*nm; 
size=10*mm;
N=150; 
N2=int(N/2)

z=90*cm
d=0.5*mm
R=0.02*mm
phi=0.0

# doublevar()-> larger float value D, Dhole set per mm, and Z set per cm.
D=DoubleVar()
Dhole=DoubleVar()
Z=DoubleVar()
PHI=DoubleVar()
D.set(d/mm)
Dhole.set(2*R/mm)
Z.set(z/cm)
PHI.set(phi)

# plotting the result.
fig=plt.figure(figsize=(8,8))
ax=fig.add_subplot(111)

# creating canvas to display on window.
canvas=FigureCanvasTkAgg(fig,master=root)
canvas._tkcanvas.pack(side=Tk.LEFT,fill=Tk.BOTH,expand=1)
v=StringVar()

# creating the function for simulation of the pattern.
""" using LightPipes modules, the Phase in started, circAperture, 
    the subphase started for F1, the circAperture for F2 is mixed,
    the intensity is distributed. """
def exp(event):
    global I
    R=Dhole.get()*mm
    d=D.get()*mm
    z=Z.get()*cm
    phi=PHI.get()
    F=Begin(size,wl,N);
    F1=CircAperture(R,-d/2,0,F);
    Phi =Phase(F);
    # looping phi over N intervals.
    for i in range(1,N):
        for j in range(1,N):
            Phi[i][j]=phi;
    F1=SubPhase(Phi,F1);
    F2=CircAperture(R,d/2,0,F);
    F=BeamMix(F1,F2);
    F=Fresnel(z,F);
    I=Intensity(1,F);
    # drawing pattern on the canvas.
    ax.clear()
    ax.contourf(I,50,cmap='jet');
    ax.axis('off');
    ax.axis('equal');
    str='Intensity Distribution for λ=530nm'
    ax.set_title(str)
    canvas.draw() 

# creating function to detect the movement and get the position of the cursor.
def move(event):
    x=event.xdata;
    y=event.ydata;
    if(x and y is not None and x>0 and x<N and y>0 and y<N):
        v.set('x=%3.2f mm, y=%3.2f mm\n I=%3.3f [a.u.]' %((-size/2+x*size/N)/mm,(-size/2+y*size/N)/mm,I[int(x)][int(y)]))
        root.configure(cursor='crosshair')
    else:
        v.set('')
        root.configure(cursor='arrow')

# creating function to stop the execution.        
def _quit():
    root.quit()

# creating scale using gui for adjusting the diameter of the slits in mm.
Scale(root,
    takefocus=1,
    orient='horizontal',
    label='diameter of the slits [mm]',
    length=200, 
    from_=0.05,
    to=0.5,
    resolution=0.001,
    variable=Dhole,
    cursor="hand2",
    bg="black",
    fg="cyan",
    command=exp).pack()

# creating scale using gui for adjusting the distance between the slits in mm.       
Scale(root,
    takefocus=1,
    orient='horizontal',
    label='distance between slits [mm]',
    length=200,
    from_=0.05, 
    to=1.5,
    resolution=0.001,
    variable=D,
    cursor="hand2",
    bg="black",
    fg="cyan",
    command=exp).pack()

# creating scale using gui for adjusting the distance of the screen from slits in cm.        
Scale(root,
    takefocus=1,
    orient='horizontal',
    label='distance from screen [cm]',
    length=200,
    from_=0.01, 
    to=200.0,
    resolution=0.01,
    variable=Z,
    cursor="hand2",
    bg="black",
    fg="cyan",
    command=exp).pack()

# creating function call simulation.        
def cb():
    exp(0)

# creating button using gui for quit function. 
Button(root,
   width=24,
   text='Quit',
   cursor="hand2",
   bg="black",
   fg="cyan",
   command=_quit).pack(pady=10)
    
# label
Label(root,textvariable=v).pack(pady=50)
# displaying the coordinates detected using move() function.
cid = fig.canvas.mpl_connect('motion_notify_event',move)

# calling the function and constantly looping the window.
exp(0)
root.mainloop()
root.destroy()
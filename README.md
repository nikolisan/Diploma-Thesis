# Diploma Thesis
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

### Summary
In this repo, I maintain all the code and the text related to my diploma thesis for my degree in Civil Engineering at University of Patras.
The main focus of this thesis is the computational modelling of the flow in a reservoir. However there are two more modules. One about the computation and a simple visualization of the Coriolis Effect on a parcel moving on a 2D plane, and the other a computation and a 3D visualization of the Lorenz system.
All code is written in Python3 and the GUI is made with QT5.

### Abstract
[**Abstract PDF**](abstract.pdf)

This dissertation is divided into three main parts.

The first chapter constitutes a presentation of the Lorenz system. Its discovery and use in the physical world is mentioned and a numerical solution is suggested. Also, a graphical environment program, developed for this dissertation, is presented which solves the system for various initial conditions set by the user and reveals an animating graphic result.

The second chapter discusses the Coriolis fictitious force and how it affects phenomena which unfold on earth. An analysis of the properties of this force is performed and the force's effect on a motion in a rotating reference system is described. Also, phenomena like inertial waves, in which Coriolis force is the main factor, are mentioned. Finally, a software is presented, which was also developed as part of this dissertation. The user can define the initial conditions and receive a graphical representation of the trajectory a parcel follows under the Coriolis force effect. The software returns some useful parameters, such as the Rossby number.

In the third and final chapter, the circulation in a bay of idealized dimensions is simulated, where the main excitation is a harmonic tidal wave. In this chapter, extensive analysis of the governing equations is carried out. During the research, the finite differences discretization is implemented in a staggered grid for the Shallow Water Equations, combined with the conservation of mass equation, integrated over depth. A stability check was performed based on the CFL condition. For the boundary cells, Neuman condition was chosen in combination with the radiation equation of the reflected waves. Finally, the various results of two separate solutions for different grid size and time lengths are presented and analyzed.

The code for all three chapters was written in Python mainly because of the flexibility and the scripting nature it provides over more robust scientific languages like Fortran.

### Table of Contents
* [**Coriolis Effect**](Coriolis)
* [**Lorenz System**](Lorenz)
* [**Flow Modelling**](CFD)

### Authors
* **Nick Andreakos** - *Initial Work* - [nikolisan](https://github.com/nikolisan)

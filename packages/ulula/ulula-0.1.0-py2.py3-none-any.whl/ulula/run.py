###################################################################################################
#
# Ulula -- run.py
#
# Runtime for the Ulula simultion code. The run function is a simple wrapper around the simulation
# object that runs a given setup and makes plots and/or movies.
#
# by Benedikt Diemer
#
###################################################################################################

import os
import subprocess
import glob
from matplotlib import pyplot as plt
import copy
import time

import ulula.simulation as ulula_sim

###################################################################################################

def run(setup, hydro_scheme = None, nx = 200, tmax = 1.0, max_steps = None, print_stride = 100, 
			movie = False, save = False, plot_every = None, plot1d = False, fn_suffix = '',
			**kwargs):
	"""
	Runtime environment for Ulula.
	
	This function takes a given problem setup and other user-defined parameters and executes the 
	hydro solver. Depending on user choices, it can also produces various outputs such as plots 
	and movies. Customizations that are implemented in the setup class are automatically matched
	to the respective plotting routines.
	
	Parameters
	-----------------------------------------------------------------------------------------------
	setup: Setup
		Setup object. See :doc:`setups` for how to create this object.
	hydro_scheme: HydroScheme
		HydroScheme object that sets the algorithm and CFL number for the simulation. If ``None``,
		the standard scheme is used. See :doc:`simulation` for details.
	nx: int
		Number of cells in the x-direction. The ratio of x and y is determined by the problem 
		setup.
	tmax: float
		Time when the simulation should be stopped (in code units).
	max_steps: int
		Maximum number of steps to take. If ``None``, no limit is imposed and the code is run to 
		a time ``tmax``. 
	print_stride: int
		Print a line to the console every ``print_stride`` timesteps.
	movie: bool
		If ``True``, a movie is created by outputting a frame at each snapshot and running the
		ffmpeg tool to combine them (this tool must be installed on the system).
	save: bool
		If ``movie == False``, plots are saved to a file if this parameter is ``True``. Otherwise,
		they are shown in an interactive matplotlib window.
	plot_every: int
		If producing a movie, only add a frame every ``plot_every`` snapshots. If not producing a
		movie, a plot is saved every ``plot_every`` snapshots. 
	plot1d: bool
		If ``True``, the 1D plotting routine is called instead of the usual 2D routine. This is 
		useful only for test setups that are intrinsically 1D such as a shocktube.
	fn_suffix: string
		String to add to all filenames.
	kwargs: kwargs
		Additional arguments that are passed to the Ulula plotting function.
	"""

	# Create simulation object and set initial conditions
	if hydro_scheme is None:
		hydro_scheme = ulula_sim.HydroScheme()
	setup_name = setup.shortName()
	sim = ulula_sim.Simulation(hydro_scheme)
	setup.initialConditions(sim, nx)

	# Plotting settings
	plot_kwargs = copy.copy(kwargs)
	if plot1d:
		plot_idir = setup.direction()
		plot_kwargs.update(dict(true_solution_func = setup.trueSolution, vminmax_func = setup.plotLimits))
	else:
		plot_kwargs.update(dict(vminmax_func = setup.plotLimits, cmap_func = setup.plotColorMaps))

	# Mini-routine for plotting
	def createPlot():
		if plot1d:
			sim.plot1D(plot_idir, **plot_kwargs)
		else:
			sim.plot2D(**plot_kwargs)
		
	# Main loop over timesteps
	t0 = time.process_time()
	step_movie = 0
	while sim.t < tmax:

		# Plotting for movie
		if movie:
			if (plot_every is None) or (sim.step % plot_every == 0):
				createPlot()
				plt.savefig('frame_%04d.png' % (step_movie), dpi = 200)
				plt.close()
				step_movie += 1
		else:
			if (plot_every is not None) and (sim.step % plot_every == 0):
				createPlot()
				plt.savefig('ulula_%s_%04d%s.png' % (setup_name, sim.step, fn_suffix))
				plt.close()
	
		# Perform timestep; by doing this after plotting, we make sure that initial conditions are
		# plotted.
		dt = sim.timestep()
		if sim.step % print_stride == 0:
			print('Timestep %5d, dt = %.2e, t = %.2e' % (sim.step, dt, sim.t))
		
		# Check for abort conditions
		if (max_steps is not None) and (sim.step >= max_steps):
			break

	ttot = time.process_time() - t0
	print('Simulation finished. Took %d steps, %.1f seconds, %.3f s/step, %.2f steps/s.' % \
		(sim.step, ttot, ttot / sim.step, sim.step / ttot))

	if movie:
		subprocess.run('ffmpeg -i frame_%04d.png -pix_fmt yuv420p -y ' + 'ulula_%s%s.mp4' \
					% (setup_name, fn_suffix), shell = True)
		for frame in glob.glob('frame*.png'):
			try:
				os.remove(frame)
			except OSError:
				pass
	elif (not plot_every):
		createPlot()
		if save:
			plt.savefig('ulula_%s%s.pdf' % (setup_name, fn_suffix))
			plt.close()
		else:
			plt.show()	

	return

###################################################################################################

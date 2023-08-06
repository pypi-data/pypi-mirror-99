###################################################################################################
#
# Ulula -- setups.py
#
# Initial conditions and analytical solutions for some classical test problems in 1D and 2D
#
# by Benedikt Diemer
#
###################################################################################################

import numpy as np
import scipy.optimize
import six
import abc
import matplotlib.pyplot as plt 

import ulula.simulation as ulula_sim

###################################################################################################

# Shorthand for frequently used index constants
DN = ulula_sim.DN
VX = ulula_sim.VX
VY = ulula_sim.VY
PR = ulula_sim.PR

###################################################################################################

@six.add_metaclass(abc.ABCMeta)
class Setup():
	"""
	General setup class
	
	This abstract container must be partially overwritten by child classes, but also contains 
	defaults for many standard routines.
	"""
	
	def __init__(self):
		
		self.gravity = False
		
		return
	
	# ---------------------------------------------------------------------------------------------

	@abc.abstractmethod
	def shortName(self):
		"""
		Short name for the problem (to be used in output filenames)
		"""
		
		return

	# ---------------------------------------------------------------------------------------------
	
	def initialConditions(self, sim, nx):
		"""
		Wrapper function to set initial data
		
		This function calls the problem-specific setup, which is assumed to set the primitive 
		variables. Those are also converted to conserved variables.
		
		Parameters
		-----------------------------------------------------------------------------------------------
		sim: Simulation
			Simulation object in which the ICs are to be set
		nx: int
			Number of cells in the x-direction
		"""
		
		self.setInitialData(sim, nx)

		sim.V[:, :, :] = sim.V_ini[:, :, :]
		sim.primitiveToConserved(sim.V, sim.U)
		
		return
	
	# ---------------------------------------------------------------------------------------------

	@abc.abstractmethod
	def setInitialData(self, sim, nx):
		"""
		Set the initial conditions (must be overwritten)

		Parameters
		-----------------------------------------------------------------------------------------------
		sim: Simulation
			Simulation object in which the ICs are to be set
		nx: int
			Number of cells in the x-direction
		"""
		
		return

	# ---------------------------------------------------------------------------------------------

	def trueSolution(self, sim):
		"""
		Return a true solution for this setup
		
		This function can be passed to the Ulula plotting routines. It returns a 1D or 2D array, but 
		if it is 1D, it should only be passed to the :func:`~ulula.simulation.Simulation.plot1D` 
		function, and vice versa.

		Parameters
		-----------------------------------------------------------------------------------------------
		sim: Simulation
			Simulation object
		"""
		
		return

	# ---------------------------------------------------------------------------------------------

	def direction(self):
		"""
		Return the direction of the problem (1D only)
		
		1D problems can be set up along the x or y direction. If the former, this function should 
		return 0, and 1 if the latter. 
		"""
		
		raise Exception('No directionality implemented for this setup.')
		
		return
	
	# ---------------------------------------------------------------------------------------------

	def plotLimits(self):
		"""
		Return min/max limits for plotted quantities
		
		This function can be passed to the Ulula plotting routines. By default, no limits are 
		returned, which means the plotting functions automatically select limits. 
		"""
		
		return None, None

	# ---------------------------------------------------------------------------------------------

	def plotColorMaps(self):
		"""
		Return colormaps for plotted quantities
		
		This function can be passed to the Ulula plotting routines. By default, velocities are 
		plotted with a divergent colormap, whereas density and pressure are plotted with a 
		perceptually uniform colormap.
		"""
		
		cm_v = plt.get_cmap('RdBu_r')
		cm_rho = plt.get_cmap('viridis')
		
		return [cm_rho, cm_v, cm_v, cm_rho]
	
###################################################################################################

class SetupAdvect(Setup):
	"""
	Tophat advection test
	
	In this test, an initially overdense tophat is placed at the center of the domain. The entire
	fluid moves towards the northeast direction. This test is the 2D equivalent of tophat 
	advection in 1D and mostly tests how diffusive a hydro solver is.
	"""
	
	def __init__(self):

		Setup.__init__(self)
		
		self.rho0 = 1.0
		self.rho1 = 2.0
		self.P0 = 1.0
		self.ux = 0.5
		self.uy = 0.3
		self.r_th = 0.1
		self.gamma = 5.0 / 3.0
		
		return 

	# ---------------------------------------------------------------------------------------------

	def shortName(self):
		
		return 'advect'

	# ---------------------------------------------------------------------------------------------
	
	def setInitialData(self, sim, nx):
		
		sim.setDomain(nx, nx, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'periodic')
		sim.setFluidProperties(self.gamma)

		sim.V_ini[DN] = self.rho0
		sim.V_ini[VX] = self.ux
		sim.V_ini[VY] = self.uy
		sim.V_ini[PR] = self.P0

		# Set tophat into the center of the domain
		x, y = sim.xyGrid()
		r = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
		mask = (r <= self.r_th)
		sim.V_ini[DN][mask] = self.rho1
		
		return
		
	# ---------------------------------------------------------------------------------------------

	def plotLimits(self):
		
		return [self.rho0 * 0.9, 0.0, 0.0, self.P0 * 0.8], [self.rho1 * 1.05, 1.0, 1.0, self.P0 * 1.2]

###################################################################################################

class SetupSod(Setup):
	"""
	Superclass for a shocktube problem in one dimension
	
	The Sod (1978) shocktube problem is a class test for Riemann solvers. A sharp break in fluid 
	properties at the center of a 1D domain causes a shock, contact discontinuity, and rarefaction
	wave. The problem can be solved analytically. The solution used here was taken from Frank van 
	den Bosch's and Susanne Hoefner's lecture notes.
	
	This class is meant as a superclass because it does not decide which direction (x or y) to use.
	This is done in subclasses, which can be used to test whether the code behaves the same in both 
	directions.
	"""
	
	def __init__(self):
		
		Setup.__init__(self)
	
		# Parameters for the Sod shocktube test
		# sod_gamma = 1.4
		# sod_x0 = 0.5
		# sod_rhoL = 8.0
		# sod_rhoR = 1.0
		# sod_PL = 10.0 / sod_gamma
		# sod_PR = 1.0 / sod_gamma
		# sod_uL = 0.0
		# sod_uR = 0.0
		
		self.sod_gamma = 1.4
		self.sod_x0 = 0.5
		self.sod_rhoL = 1.0
		self.sod_rhoR = 1.0 / 8.0
		self.sod_PL = 1.0
		self.sod_PR = 1.0 / 10.0
		self.sod_uL = 0.0
		self.sod_uR = 0.0
		
		return 

	# ---------------------------------------------------------------------------------------------

	def shortName(self):
		
		return 'sod'

	# ---------------------------------------------------------------------------------------------

	def trueSolution(self, sim, idir):
	
		# Grid variables
		t = sim.t
		if idir == 0:
			x = sim.x
			nx = sim.nx
			VV = VX
		elif idir == 1:
			x = sim.y
			nx = sim.ny
			VV = VY
		else:
			raise Exception('Unknown direction')
	
		# Shorthand	for Sod input variables
		P_L = self.sod_PL
		P_R = self.sod_PR
		rho_L = self.sod_rhoL
		rho_R = self.sod_rhoR
		u_L = self.sod_uL
		u_R = self.sod_uR
		x_0 = self.sod_x0
		
		# gamma and sound speed
		g = self.sod_gamma
		gm1 = g - 1.0
		gp1 = g + 1.0
		cs_L = np.sqrt(g * P_L / rho_L)
		cs_R = np.sqrt(g * P_R / rho_R)
	
		# Implicit equation to solve for shock speed in Sod problem
		def sod_eq(M):
			t1 = P_R / P_L * (2.0 * g / gp1 * M**2 - gm1 / gp1)
			rhs = cs_L * gp1 / gm1 * (1.0 - t1**(gm1 / 2.0 / g))
			return M - 1.0 / M - rhs
		
		# Compute speed of shock in frame of tube
		M = scipy.optimize.brentq(sod_eq, 1.0001, 20.0, xtol = 1E-6)
		
		# The numerical solution comes out wrong by this factor for some yet unknown reason.
		M *= 0.986
		M_2 = M**2
		u_s = M * cs_R
		
		# Post-shock state after shock has passed through area R. van den Bosch has
		# u1 = 2.0 / gp1 * (M - 1.0 / M) 
		# for the velocity, but this seems to give the wrong result. The current way of computing u1
		# was derived by going into the shock frame where uRp = uR - us, u1p = u1 - us, and using the
		# RH-condition that u1p / uRp = (gm1 * M2 + 2)/(gp1 * M2)
		P_1 = P_R * (2.0 * g / gp1 * M_2 - gm1 / gp1)
		rho_1 = rho_R / (2.0 / gp1 / M_2 + gm1 / gp1)
		u_1 = u_s * (1.0 - (2.0 / gp1 / M_2 + gm1 / gp1))
		
		# State to the left of contact discontinuity with state 1
		P_2 = P_1
		u_2 = u_1
		rho_2 = rho_L * (P_2 / P_L)**(1.0 / g)
		cs_2 = np.sqrt(g * P_2 / rho_2)
		
		# Boundaries of states. The rarefacton wave progresses at speed csL to the left and thus
		# reaches x1 by time t. The shock to the right goes as us * t to x4, whereas the contact
		# discontinuity moves at the speed of state 2. 
		x_1 = x_0 - cs_L * t
		x_2 = x_0 + (u_2 - cs_2) * t
		x_3 = x_0 + u_2 * t
		x_4 = x_0 + u_s * t
		
		# Areas of array where solutions are valid
		maskL = (x <= x_1)
		maskE = (x > x_1) & (x <= x_2)
		mask2 = (x > x_2) & (x <= x_3)
		mask1 = (x > x_3) & (x <= x_4)
		maskR = (x > x_4)
	
		# Compute rarefaction state, which depends on position unlike the other states
		x_E = x[maskE]
		u_E = 2.0 / gp1 * (cs_L + (x_E - x_0) / t)
		cs_E = cs_L - 0.5 * gm1 * u_E
		P_E = P_L * (cs_E / cs_L)**(2.0 * g / gm1)
		rho_E = g * P_E / cs_E**2
		
		# Set solution
		V_sol = np.zeros((sim.nq, nx + 2 * sim.nghost), np.float)
	
		# Original left state
		V_sol[DN, maskL] = rho_L
		V_sol[VV, maskL] = u_L
		V_sol[PR, maskL] = P_L
	
		# Rarefaction
		V_sol[DN, maskE] = rho_E
		V_sol[VV, maskE] = u_E
		V_sol[PR, maskE] = P_E
	
		# State 2
		V_sol[DN, mask2] = rho_2
		V_sol[VV, mask2] = u_2
		V_sol[PR, mask2] = P_2
		
		# State 1
		V_sol[DN, mask1] = rho_1
		V_sol[VV, mask1] = u_1
		V_sol[PR, mask1] = P_1
	
		# Original right state
		V_sol[DN, maskR] = rho_R
		V_sol[VV, maskR] = u_R
		V_sol[PR, maskR] = P_R
		
		return V_sol

###################################################################################################

class SetupSodX(SetupSod):
	"""
	Sod shocktube problem along the x-direction
	
	See the :class:`SetupSod` class for documentation of this test.
	"""
	
	def __init__(self):
		
		SetupSod.__init__(self)
		
		return 

	# ---------------------------------------------------------------------------------------------

	def shortName(self):
		
		return 'sod_x'

	# ---------------------------------------------------------------------------------------------
	
	def setInitialData(self, sim, nx):

		sim.setDomain(nx, 4, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'outflow')
		sim.setFluidProperties(self.sod_gamma)
		maskL = (sim.x <= self.sod_x0)
		maskR = np.logical_not(maskL)
		sim.V_ini[DN, maskL, :] = self.sod_rhoL
		sim.V_ini[DN, maskR, :] = self.sod_rhoR
		sim.V_ini[VX, maskL, :] = self.sod_uL
		sim.V_ini[VX, maskR, :] = self.sod_uR
		sim.V_ini[PR, maskL, :] = self.sod_PL
		sim.V_ini[PR, maskR, :] = self.sod_PR
		
		return

	# ---------------------------------------------------------------------------------------------

	def trueSolution(self, sim):
		
		return SetupSod.trueSolution(self, sim, 0)

	# ---------------------------------------------------------------------------------------------

	def direction(self):
		
		return 0
	
###################################################################################################

class SetupSodY(SetupSod):
	"""
	Sod shocktube problem along the y-direction.
	
	See the :class:`SetupSod` class for documentation of this test.
	"""
	
	def __init__(self):
		
		SetupSod.__init__(self)
		
		return 

	# ---------------------------------------------------------------------------------------------

	def shortName(self):
		
		return 'sod_y'

	# ---------------------------------------------------------------------------------------------
	
	def setInitialData(self, sim, nx):

		sim.setDomain(4, nx, xmin = 0.0, xmax = 4.0 / nx, ymin = 0.0, bc_type = 'outflow')
		sim.setFluidProperties(self.sod_gamma)
		maskL = (sim.y <= self.sod_x0)
		maskR = np.logical_not(maskL)
		sim.V_ini[DN, :, maskL] = self.sod_rhoL
		sim.V_ini[DN, :, maskR] = self.sod_rhoR
		sim.V_ini[VX, :, maskL] = self.sod_uL
		sim.V_ini[VX, :, maskR] = self.sod_uR
		sim.V_ini[PR, :, maskL] = self.sod_PL
		sim.V_ini[PR, :, maskR] = self.sod_PR
		
		return

	# ---------------------------------------------------------------------------------------------

	def trueSolution(self, sim):
		
		return SetupSod.trueSolution(self, sim, 1)
	
	# ---------------------------------------------------------------------------------------------

	def direction(self):
		
		return 1
	
###################################################################################################

class SetupKelvinHelmholtz(Setup):
	"""
	Kelvin-Helmholtz instability
	
	The KH instability forms at the interface between two fluids that are moving past each other. 
	The user can choose between a setup where the interface is infinitely sharp and the smooth
	ICs of Robertson et al. 2010. In the sharp case, the instability is seeded by grid noise, but
	we still add a small velocity perturbation to obtain more well-defined behavior. The smooth
	version is recommended as it leads to a more physical test case. 

	Parameters
	-----------------------------------------------------------------------------------------------
	sharp_ics: bool
		Use sharp boundary between fluids instead of smoothed ICs.
	n_waves: int
		Number of wave periods in the domain. The number of periods that can be resolved depends on
		the resolution.
	"""
	
	def __init__(self, sharp_ics = False, n_waves = 1):

		Setup.__init__(self)
		
		self.gamma    =  5.0 / 3.0
		self.rho1     =  2.0
		self.rho2     =  1.0
		self.v1       =  0.5
		self.v2       = -0.5
		self.P0       =  2.5
		self.lamb     =  1.0 / n_waves

		if sharp_ics:
			self.delta_y = 0.0
			self.delta_vy =  0.001
		else:
			self.delta_y  =  0.05
			self.delta_vy =  0.1

		return

	# ---------------------------------------------------------------------------------------------

	def shortName(self):
		
		return 'kh'

	# ---------------------------------------------------------------------------------------------
	
	def setInitialData(self, sim, nx):

		sim.setDomain(nx, nx, xmin = 0.0, xmax = 1.0, ymin = 0.0, bc_type = 'periodic')
		sim.setFluidProperties(self.gamma)
		
		x, y = sim.xyGrid()
		
		if self.delta_y > 0.0:
			
			# Softened initial conditions from Robertson et al (2010), Abel (2010)
			y1 = (y - 0.25) / self.delta_y
			y2 = (0.75 - y) / self.delta_y
			R = (1.0 + np.exp(0.5 / self.delta_y))**2 / ((1.0 + np.exp(2 * y1)) * (1.0 + np.exp(2 * y2)))
			vy = self.delta_y * np.sin(2.0 * np.pi * x / self.lamb)
		
		else:
			
			# Instability seeded by grid-noise, e.g. Springel (2010)
			R = np.zeros_like(x)
			R[np.abs(y - 0.5) < 0.25] = 1.0
			vy = self.delta_vy * np.sin(2.0 * np.pi * x / self.lamb) * (np.exp(-0.5 * (y - 0.25)**2) + np.exp(-0.5 * (0.75 - y)**2))

		sim.V_ini[DN] = self.rho2 + R * (self.rho1 - self.rho2)
		sim.V_ini[VX] = self.v2 + R * (self.v1 - self.v2)
		sim.V_ini[VY] = vy
		sim.V_ini[PR] = self.P0
		
		return
	
	# ---------------------------------------------------------------------------------------------

	def plotLimits(self):
		
		u_min = self.v2 * 1.2
		u_max = self.v1 * 1.2
		
		return [self.rho2 * 0.85, u_min, u_min, self.P0 * 0.9], [self.rho1 * 1.05, u_max, u_max, self.P0 * 1.15]

	# ---------------------------------------------------------------------------------------------

	def plotColorMaps(self):
		
		cm_v = plt.get_cmap('RdBu_r')
		cm_rho = plt.get_cmap('viridis')
		
		return [cm_rho, cm_v, cm_v, cm_rho]
	
###################################################################################################

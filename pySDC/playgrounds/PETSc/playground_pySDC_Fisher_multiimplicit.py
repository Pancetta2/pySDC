import sys

from mpi4py import MPI
import time
from petsc4py import PETSc

import numpy as np

from pySDC.implementations.problem_classes.GeneralizedFisher_1D_PETSc_multiimplicit import petsc_fisher
from pySDC.implementations.datatype_classes.petsc_dmda_grid import petsc_data, rhs_2comp_petsc_data
from pySDC.implementations.collocation_classes.gauss_radau_right import CollGaussRadau_Right
from pySDC.implementations.sweeper_classes.multi_implicit import multi_implicit
from pySDC.implementations.transfer_classes.TransferPETScDMDA import mesh_to_mesh_petsc_dmda
from pySDC.implementations.controller_classes.allinclusive_multigrid_MPI import allinclusive_multigrid_MPI
from pySDC.implementations.controller_classes.allinclusive_multigrid_nonMPI import allinclusive_multigrid_nonMPI

from pySDC.helpers.stats_helper import filter_stats, sort_stats

def main():

    # set MPI communicator
    comm = MPI.COMM_WORLD

    world_rank = comm.Get_rank()
    world_size = comm.Get_size()

    if len(sys.argv) == 2:
        color = int(world_rank / int(sys.argv[1]))
    else:
        color = int(world_rank / 1)

    space_comm = comm.Split(color=color)
    space_rank = space_comm.Get_rank()
    space_size = space_comm.Get_size()

    if len(sys.argv) == 2:
        color = int(world_rank % int(sys.argv[1]))
    else:
        color = int(world_rank / world_size)

    time_comm = comm.Split(color=color)
    time_rank = time_comm.Get_rank()
    time_size = time_comm.Get_size()

    print("IDs (world, space, time):  %i / %i -- %i / %i -- %i / %i" % (world_rank, world_size, space_rank, space_size,
                                                                        time_rank, time_size))

    # initialize level parameters
    level_params = dict()
    level_params['restol'] = 1E-08
    level_params['dt'] = 0.25
    level_params['nsweeps'] = [1]

    # initialize sweeper parameters
    sweeper_params = dict()
    sweeper_params['collocation_class'] = CollGaussRadau_Right
    sweeper_params['num_nodes'] = [3]
    sweeper_params['Q1'] = ['LU']
    sweeper_params['Q2'] = ['LU']
    sweeper_params['spread'] = False

    # initialize problem parameters
    problem_params = dict()
    problem_params['nu'] = 1
    problem_params['nvars'] = 2047
    problem_params['lambda0'] = 2.0
    problem_params['interval'] = (-50, 50)
    problem_params['comm'] = space_comm
    problem_params['sol_tol'] = 1E-10
    problem_params['sol_maxiter'] = 100

    # initialize step parameters
    step_params = dict()
    step_params['maxiter'] = 50

    # initialize space transfer parameters
    # space_transfer_params = dict()
    # space_transfer_params['rorder'] = 2
    # space_transfer_params['iorder'] = 2
    # space_transfer_params['periodic'] = True

    # initialize controller parameters
    controller_params = dict()
    controller_params['logger_level'] = 20
    # controller_params['predict'] = False
    # controller_params['hook_class'] = error_output

    # fill description dictionary for easy step instantiation
    description = dict()
    description['problem_class'] = petsc_fisher # pass problem class
    description['problem_params'] = problem_params  # pass problem parameters
    description['dtype_u'] = petsc_data  # pass data type for u
    description['dtype_f'] = rhs_2comp_petsc_data  # pass data type for f
    description['sweeper_class'] = multi_implicit  # pass sweeper (see part B)
    description['sweeper_params'] = sweeper_params  # pass sweeper parameters
    description['level_params'] = level_params  # pass level parameters
    description['step_params'] = step_params  # pass step parameters
    # description['space_transfer_class'] = mesh_to_mesh_petsc_dmda  # pass spatial transfer class
    # description['space_transfer_params'] = space_transfer_params  # pass paramters for spatial transfer

    # set time parameters
    t0 = 0.0
    Tend = 1.0

    # instantiate controller
    controller = allinclusive_multigrid_MPI(controller_params=controller_params, description=description, comm=time_comm)
    # controller = allinclusive_multigrid_nonMPI(num_procs=2, controller_params=controller_params, description=description)

    # get initial values on finest level
    P = controller.S.levels[0].prob
    uinit = P.u_exact(t0)

    # call main function to get things done...
    uend, stats = controller.run(u0=uinit, t0=t0, Tend=Tend)

    # compute exact solution and compare
    uex = P.u_exact(Tend)
    err = abs(uex - uend)

    # filter statistics by type (number of iterations)
    filtered_stats = filter_stats(stats, type='niter')

    # convert filtered statistics to list of iterations count, sorted by process
    iter_counts = sort_stats(filtered_stats, sortby='time')

    # compute and print statistics
    # for item in iter_counts:
    #     out = 'Number of iterations for time %4.2f: %2i' % item
    #     print(out)

    niters = np.array([item[1] for item in iter_counts])
    out = '   Mean number of iterations: %4.2f' % np.mean(niters)
    print(out)
    out = '   Range of values for number of iterations: %2i ' % np.ptp(niters)
    print(out)
    out = '   Position of max/min number of iterations: %2i -- %2i' % \
          (int(np.argmax(niters)), int(np.argmin(niters)))
    print(out)
    out = '   Std and var for number of iterations: %4.2f -- %4.2f' % (float(np.std(niters)), float(np.var(niters)))
    print(out)

    print('Iteration count (nonlinear/linear): %i / %i' % (P.snes_itercount, P.ksp_itercount))
    print('Mean Iteration count per call: %4.2f / %4.2f' % (
    P.snes_itercount / max(P.snes_ncalls, 1), P.ksp_itercount / max(P.ksp_ncalls, 1)))

    timing = sort_stats(filter_stats(stats, type='timing_run'), sortby='time')

    print('Time to solution: %6.4f sec.' % timing[0][1])
    print('Error vs. PDE solution: %6.4e' % err)


if __name__ == "__main__":
    main()

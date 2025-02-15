import numpy as np

from pySDC.helpers.stats_helper import filter_stats, sort_stats
from pySDC.implementations.collocation_classes.gauss_radau_right import CollGaussRadau_Right
from pySDC.implementations.controller_classes.controller_nonMPI import controller_nonMPI
from pySDC.implementations.problem_classes.HeatEquation_ND_FD_forced_periodic import heatNd_periodic
from pySDC.implementations.problem_classes.AdvectionEquation_ND_FD_periodic import advectionNd_periodic
from pySDC.implementations.problem_classes.Auzinger_implicit import auzinger
from pySDC.implementations.sweeper_classes.imex_1st_order import imex_1st_order
from pySDC.implementations.sweeper_classes.generic_implicit import generic_implicit
from pySDC.implementations.transfer_classes.TransferMesh import mesh_to_mesh
from pySDC.implementations.transfer_classes.TransferMesh_NoCoarse import mesh_to_mesh as mesh_to_mesh_nc
from pySDC.implementations.convergence_controller_classes.check_iteration_estimator import CheckIterationEstimatorNonMPI
from pySDC.playgrounds.compression.HookClass_error_output import error_output


def setup_diffusion(dt=None, ndim=None, ml=False):

    # initialize level parameters
    level_params = dict()
    level_params['restol'] = 1E-10
    level_params['dt'] = dt  # time-step size
    level_params['nsweeps'] = 1

    # initialize sweeper parameters
    sweeper_params = dict()
    sweeper_params['collocation_class'] = CollGaussRadau_Right
    sweeper_params['num_nodes'] = 3
    sweeper_params['QI'] = ['LU']  # For the IMEX sweeper, the LU-trick can be activated for the implicit part
    # sweeper_params['initial_guess'] = 'zero'

    # initialize problem parameters
    problem_params = dict()
    problem_params['ndim'] = ndim  # will be iterated over
    problem_params['order'] = 8  # order of accuracy for FD discretization in space
    problem_params['nu'] = 0.1  # diffusion coefficient
    problem_params['freq'] = tuple(2 for _ in range(ndim))  # frequencies
    if ml:
        problem_params['nvars'] = [tuple(64 for _ in range(ndim)), tuple(32 for _ in range(ndim))]  # number of dofs
    else:
        problem_params['nvars'] = tuple(64 for _ in range(ndim))  # number of dofs
    problem_params['direct_solver'] = False  # do GMRES instead of LU
    problem_params['liniter'] = 10  # number of GMRES iterations

    # initialize step parameters
    step_params = dict()
    step_params['maxiter'] = 50

    # initialize space transfer parameters
    space_transfer_params = dict()
    space_transfer_params['rorder'] = 2
    space_transfer_params['iorder'] = 6
    space_transfer_params['periodic'] = True

    # setup the iteration estimator
    convergence_controllers = dict()
    convergence_controllers[CheckIterationEstimatorNonMPI] = {'errtol': 1e-7}

    # initialize controller parameters
    controller_params = dict()
    controller_params['logger_level'] = 30
    controller_params['hook_class'] = error_output

    # fill description dictionary for easy step instantiation
    description = dict()
    description['problem_class'] = heatNd_periodic  # pass problem class
    description['problem_params'] = problem_params  # pass problem parameters
    description['sweeper_class'] = imex_1st_order  # pass sweeper (see part B)
    description['sweeper_params'] = sweeper_params  # pass sweeper parameters
    description['level_params'] = level_params  # pass level parameters
    description['step_params'] = step_params  # pass step parameters
    description['space_transfer_class'] = mesh_to_mesh  # pass spatial transfer class
    # description['space_transfer_class'] = mesh_to_mesh_fft  # pass spatial transfer class
    description['space_transfer_params'] = space_transfer_params  # pass paramters for spatial transfer
    description['convergence_controllers'] = convergence_controllers

    return description, controller_params


def setup_advection(dt=None, ndim=None, ml=False):

    # initialize level parameters
    level_params = dict()
    level_params['restol'] = 1E-10
    level_params['dt'] = dt  # time-step size
    level_params['nsweeps'] = 1

    # initialize sweeper parameters
    sweeper_params = dict()
    sweeper_params['collocation_class'] = CollGaussRadau_Right
    sweeper_params['num_nodes'] = 3
    sweeper_params['QI'] = ['LU']  # For the IMEX sweeper, the LU-trick can be activated for the implicit part
    # sweeper_params['initial_guess'] = 'zero'

    # initialize problem parameters
    problem_params = dict()
    problem_params['ndim'] = ndim  # will be iterated over
    problem_params['order'] = 6  # order of accuracy for FD discretization in space
    problem_params['type'] = 'center'  # order of accuracy for FD discretization in space
    problem_params['c'] = 0.1  # diffusion coefficient
    problem_params['freq'] = tuple(2 for _ in range(ndim))  # frequencies
    if ml:
        problem_params['nvars'] = [tuple(64 for _ in range(ndim)), tuple(32 for _ in range(ndim))]  # number of dofs
    else:
        problem_params['nvars'] = tuple(64 for _ in range(ndim))  # number of dofs
    problem_params['direct_solver'] = False  # do GMRES instead of LU
    problem_params['liniter'] = 10  # number of GMRES iterations

    # initialize step parameters
    step_params = dict()
    step_params['maxiter'] = 50

    # initialize space transfer parameters
    space_transfer_params = dict()
    space_transfer_params['rorder'] = 2
    space_transfer_params['iorder'] = 6
    space_transfer_params['periodic'] = True

    # setup the iteration estimator
    convergence_controllers = dict()
    convergence_controllers[CheckIterationEstimatorNonMPI] = {'errtol': 1e-7}

    # initialize controller parameters
    controller_params = dict()
    controller_params['logger_level'] = 30
    controller_params['hook_class'] = error_output

    # fill description dictionary for easy step instantiation
    description = dict()
    description['problem_class'] = advectionNd_periodic
    description['problem_params'] = problem_params  # pass problem parameters
    description['sweeper_class'] = generic_implicit
    description['sweeper_params'] = sweeper_params  # pass sweeper parameters
    description['level_params'] = level_params  # pass level parameters
    description['step_params'] = step_params  # pass step parameters
    description['space_transfer_class'] = mesh_to_mesh  # pass spatial transfer class
    # description['space_transfer_class'] = mesh_to_mesh_fft  # pass spatial transfer class
    description['space_transfer_params'] = space_transfer_params  # pass paramters for spatial transfer
    description['convergence_controllers'] = convergence_controllers

    return description, controller_params


def setup_auzinger(dt=None, ml=False):

    # initialize level parameters
    level_params = dict()
    level_params['restol'] = 1E-10
    level_params['dt'] = dt  # time-step size
    level_params['nsweeps'] = 1

    # initialize sweeper parameters
    sweeper_params = dict()
    sweeper_params['collocation_class'] = CollGaussRadau_Right
    if ml:
        sweeper_params['num_nodes'] = [3, 2]
    else:
        sweeper_params['num_nodes'] = 3
    sweeper_params['QI'] = ['LU']  # For the IMEX sweeper, the LU-trick can be activated for the implicit part
    # sweeper_params['initial_guess'] = 'zero'

    # initialize problem parameters
    problem_params = dict()
    problem_params['newton_tol'] = 1E-12
    problem_params['newton_maxiter'] = 10

    # initialize step parameters
    step_params = dict()
    step_params['maxiter'] = 50

    # setup the iteration estimator
    convergence_controllers = dict()
    convergence_controllers[CheckIterationEstimatorNonMPI] = {'errtol': 1e-7}

    # initialize controller parameters
    controller_params = dict()
    controller_params['logger_level'] = 30
    controller_params['hook_class'] = error_output

    # fill description dictionary for easy step instantiation
    description = dict()
    description['problem_class'] = auzinger
    description['problem_params'] = problem_params  # pass problem parameters
    description['sweeper_class'] = generic_implicit
    description['sweeper_params'] = sweeper_params  # pass sweeper parameters
    description['level_params'] = level_params  # pass level parameters
    description['step_params'] = step_params  # pass step parameters
    description['space_transfer_class'] = mesh_to_mesh_nc  # pass spatial transfer class
    description['convergence_controllers'] = convergence_controllers

    return description, controller_params


def run_simulations(type=None, ndim_list=None, Tend=None, nsteps_list=None, ml=False, nprocs=None):
    """
    A simple test program to do SDC runs for the heat equation in various dimensions
    """

    t0 = None
    dt = None
    description = None
    controller_params = None

    for ndim in ndim_list:
        for nsteps in nsteps_list:

            if type == 'diffusion':
                # set time parameters
                t0 = 0.0
                dt = (Tend - t0) / nsteps
                description, controller_params = setup_diffusion(dt, ndim, ml)
            elif type == 'advection':
                # set time parameters
                t0 = 0.0
                dt = (Tend - t0) / nsteps
                description, controller_params = setup_advection(dt, ndim, ml)
            elif type == 'auzinger':
                assert ndim == 1
                # set time parameters
                t0 = 0.0
                dt = (Tend - t0) / nsteps
                description, controller_params = setup_auzinger(dt, ml)

            print(f'Running {type} in {ndim} dimensions with time-step size {dt}...')
            print()

            # Warning: this is black magic used to run an 'exact' collocation solver for each step within the hooks
            description['step_params']['description'] = description
            description['step_params']['controller_params'] = controller_params

            # instantiate controller
            controller = controller_nonMPI(num_procs=nprocs, controller_params=controller_params,
                                           description=description)

            # get initial values on finest level
            P = controller.MS[0].levels[0].prob
            uinit = P.u_exact(t0)

            # call main function to get things done...
            uend, stats = controller.run(u0=uinit, t0=t0, Tend=Tend)

            # filter statistics by type (number of iterations)
            iter_counts = sort_stats(filter_stats(stats, type='niter'), sortby='time')

            niters = np.array([item[1] for item in iter_counts])
            out = f'   Mean number of iterations: {np.mean(niters):4.2f}'
            print(out)

            # filter statistics by type (error after time-step)
            PDE_errors = sort_stats(filter_stats(stats, type='PDE_error_after_step'), sortby='time')
            coll_errors = sort_stats(filter_stats(stats, type='coll_error_after_step'), sortby='time')
            for iters, PDE_err, coll_err in zip(iter_counts, PDE_errors, coll_errors):
                out = f'   Errors after step {PDE_err[0]:8.4f} with {iters[1]} iterations: ' \
                      f'{PDE_err[1]:8.4e} / {coll_err[1]:8.4e}'
                print(out)
            print()

            # filter statistics by type (error after time-step)
            timing = sort_stats(filter_stats(stats, type='timing_run'), sortby='time')
            out = f'...done, took {timing[0][1]} seconds!'
            print(out)

            print()
        print('-----------------------------------------------------------------------------')


if __name__ == "__main__":
    # run_simulations(type='diffusion', ndim_list=[1], Tend=1.0, nsteps_list=[8], ml=False, nprocs=1)
    # run_simulations(type='diffusion', ndim_list=[1], Tend=1.0, nsteps_list=[8], ml=True, nprocs=1)

    # run_simulations(type='advection', ndim_list=[1], Tend=1.0, nsteps_list=[8], ml=False, nprocs=1)
    # run_simulations(type='advection', ndim_list=[1], Tend=1.0, nsteps_list=[8], ml=True, nprocs=1)\

    run_simulations(type='auzinger', ndim_list=[1], Tend=1.0, nsteps_list=[8], ml=False, nprocs=1)
    run_simulations(type='auzinger', ndim_list=[1], Tend=1.0, nsteps_list=[8], ml=True, nprocs=1)

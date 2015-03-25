
from pySDC import CollocationClasses as collclass

from ProblemClass import fenics_heat2d
from fenics_mesh import fenics_mesh, rhs_fenics_mesh
from TransferClass import mesh_to_mesh_fenics
from pySDC.sweeper_classes.mass_matrix_imex import mass_matrix_imex
import pySDC.Methods as mp
from pySDC import Log
from pySDC.Stats import grep_stats, sort_stats

if __name__ == "__main__":

    # set global logger (remove this if you do not want the output at all)
    logger = Log.setup_custom_logger('root')

    # nvars = [[8,8],[16,16],[32,32],[64,64],[128,128],[256,256]]
    # dt = [0.125]

    num_procs = 1

    # This comes as read-in for the level class
    lparams = {}
    lparams['restol'] = 8E-11

    sparams = {}
    sparams['maxiter'] = 10

    # This comes as read-in for the problem class
    pparams = {}
    pparams['nu'] = 0.1
    pparams['t0'] = 0.0 # ugly, but necessary to set up ProblemClass
    pparams['c_nvars'] = [[32,32]]
    pparams['family'] = 'CG'
    pparams['order'] = 1
    pparams['levelnumber'] = [2,1]

    # This comes as read-in for the transfer operations
    tparams = {}
    tparams['finter'] = False

    # Fill description dictionary for easy hierarchy creation
    description = {}
    description['problem_class'] = fenics_heat2d
    description['problem_params'] = pparams
    description['dtype_u'] = fenics_mesh
    description['dtype_f'] = rhs_fenics_mesh
    description['collocation_class'] = collclass.CollGaussLegendre
    description['num_nodes'] = 3
    description['sweeper_class'] = mass_matrix_imex
    description['level_params'] = lparams
    description['transfer_class'] = mesh_to_mesh_fenics
    description['transfer_params'] = tparams

    # quickly generate block of steps
    MS = mp.generate_steps(num_procs,sparams,description)

    # setup parameters "in time"
    t0 = MS[0].levels[0].prob.t0
    dt = 0.125
    Tend = 1*dt

    # get initial values on finest level
    P = MS[0].levels[0].prob
    uinit = P.u_exact(t0)

    # call main function to get things done...
    uend,stats = mp.run_pfasst_serial(MS,u0=uinit,t0=t0,dt=dt,Tend=Tend)

    # df.plot(uend.values,interactive=True)

    # compute exact solution and compare
    uex = P.u_exact(Tend)

    print('error at time %s: %s' %(Tend,abs(uex-uend)/abs(uex)))

    extract_stats = grep_stats(stats,iter=-1,type='residual')
    sortedlist_stats = sort_stats(extract_stats,sortby='step')
    print(extract_stats,sortedlist_stats)
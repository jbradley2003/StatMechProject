import time
import numpy as np
from seq import *
from setup import *
from mc import *

# Folder location for saving plots (replace)
path_root = '/Users/xxxx/Documents/GitHub/StatMechProject/figures/'

# Figure 1 (modified to show runtime of operator once the ensemble has been created)
def compareRuntime(n_list, file_path, neg_epsilon=2):
    """
    Compares runtime of ensemble generation and calculation of 
    the partition function for that particular ensemble.
    
    :param n_list: List of residue counts (list of integers)
    :param path_name: Figure file save path (string) 
    :param neg_epsilon: Stabilization energy list (list of floats or integers) 
    """
    t_1 = []
    t_2 = []

    for n in n_list:
        start = time.perf_counter()
        g = generateCons(n, [0]*n)
        end_genCons = time.perf_counter()
        z = calcZ(g, neg_epsilon)[0] # Replace with operator that you want to compare with.
        end_calcZ = time.perf_counter()
        t_1.append(end_genCons-start)
        t_2.append(end_calcZ-end_genCons)

    plt.plot(n_list,t_1, label='LD', marker='o')
    plt.plot(n_list, t_2, label='calcZ', marker='o')
    plt.ylabel('Runtime (s)')
    plt.xlabel('Number of residues')
    plt.legend()
    plt.grid()
    plt.savefig(file_path)
    plt.clf()

    print('compareRuntime figure generated.')
    print('Figure Saved to ' + file_path)

n = [i for i in range(1,16)]
# compareRuntime(n,path_root + 'figure1')

# Figure 3
def compareRuntimeSampling(n_list, itr_list, file_path, trials=5, neg_epsilon=2):
    """
    Compares runtime of generateCons function at residue counts taken from input list (n_list), to
    Monte Carlo sampling (main function) at same residue counts and iteration counts taken from an 
    input list (itr_list) at input stabilization energy (neg_epsilon).
    
    :param n_list: List of residue counts (list of integers)
    :param itr_list_list: List of iteration counts (list of integers)
    :param file_path: Figure file save path (string) 
    :param trials: Number of times Monte Carlo sampling is performed, 
    expectation values are averaged over the trial count (integer)
    :param neg_epsilon: Stabilization energy (float)
    """
    t_1 = []
    t_2 = []
    l = len(n_list)
    x_labels = []

    if l != len(itr_list):
        print("Input lists are of different length")
        return
    
    for i in range(l):
        start = time.perf_counter()
        generateCons(n_list[i], [0]*n_list[i])
        end = time.perf_counter()
        t_genCons = end - start
        sum_t = 0
        x_labels.append(str(n_list[i]) + '/' + str(itr_list[i]))
        for j in range(trials):
            start = time.perf_counter()
            main(n_list[i],itr_list[i], [0]*n_list[i],neg_epsilon)
            end = time.perf_counter()
            sum_t += end - start
        t_1.append(t_genCons)
        t_2.append(sum_t/trials)

    x = [i for i in range(l)]
    plt.plot(x,t_1, label='LD', marker='o')
    plt.plot(x, t_2, label='MC', marker='o')
    plt.xticks(x, x_labels)
    plt.ylabel('Runtime (s)')
    plt.xlabel('Number of residues / Iterations')
    plt.legend()
    plt.grid()
    plt.savefig(file_path)
    plt.clf()

    print('compareRuntimeSampling figure generated.')
    print('Figure Saved to ' + file_path)

n_list = [3, 7, 11, 15]
itr_list = [100, 1000, 10000, 100000]
# compareRuntimeSampling(n_list, itr_list, path_root + 'figure3')

# Figure 4
def generateContour(n, itr_list, energy_list, file_path, seq,lvls=10, log=True, color='viridis'):
    """
    Docstring for generateContour
    
    :param n_list: List of residue counts (list of integers)
    :param itr_list: List of iteration counts (list of integers)
    :param energy_list: List of neg_epsilon values (list of integers)
    :param file_path: Figure file save path (string) 
    :param seq: Sequence list (list of integers)
    :param lvls: Number of level curves in contour plot (integer)
    :param log: Toggles log-scale on x-axis (boolean)
    :param color: Sets color scheme for contour plot (string)
    """
    print("Start")
    start = time.perf_counter()
    X, Y = np.meshgrid(itr_list, energy_list)
    w, h = len(itr_list), len(energy_list)
    m_error = [[0 for x in range(w)] for y in range(h)] 
    for i in range(w):
        for j in range(h):
            m_1 = calcAvgM(generateCons(n, seq), energy_list[j]) # Deterministic model
            m_2 = 0
            for k in range(5): # Average over 5 MC ensembles 
                m_2 += calcAvgM(main(n, itr_list[i], seq, energy_list[j]), energy_list[j])
            m_error[j][i] = m_2/5 - m_1

    end = time.perf_counter()
    print("End: ", (end-start)/60)

    cp = plt.contourf(X, Y, m_error, levels=lvls, cmap=color) 
    plt.colorbar(cp, label=r'$<m>_{MC} - <m>_{LD}$')
    plt.title("Sequence " + seqToString(seq))
    plt.xlabel('Number of iterations')
    plt.ylabel(r'$-\epsilon \; (\frac{E}{kT})$')
    plt.contour(X, Y, m_error, colors='black', linestyles='dashed', linewidths=0.8)
    if log is True:
        plt.xscale('log')
    plt.savefig(file_path)
    plt.clf()

    print('generateContour figure generated.')
    print('Figure Saved to ' + file_path)

energy = [i for i in range(1, 13)]

# generateContour(10, itr_list, energy, path_root + 'figure4-1', F)
# generateContour(10, itr_list, energy, path_root + 'figure4-2', NF)

# Figure 5
def compareCompactness(n, energy_list, file_path, seq, trials=5):
    """
    Docstring for compareCompactness
    
    :param n: Residue count (integer)
    :param energy_list: List of neg_epsilon values (list of integers)
    :param file_path: Figure file save path (string) 
    :param seq: Sequence list (list of integers)
    :param trials: Number of times Monte Carlo sampling is performed, 
    expectation values are averaged over the trial count (integer)
    """
    p_1 = []
    p_10k = []
    p_100k = []
    g = generateCons(n, seq)
    for e in energy_list:
        p_1.append(calcAvgP(g, e))
        p_10k_sum = 0
        p_100k_sum = 0
        for i in range(trials):
            p_10k_sum += calcAvgP(main(n, 10000, seq, e))
            p_100k_sum += calcAvgP(main(n, 100000, seq, e))
        p_10k.append(p_10k_sum/trials)
        p_100k.append(p_100k_sum/trials)
    plt.plot(energy_list,p_1,label='LD',marker='o')
    plt.plot(energy_list,p_10k,label='MC-10k', marker='o')
    plt.plot(energy_list,p_100k, label='MC-100k',marker='o')
    plt.title("Sequence " + '(' + seqToString(seq) + ')')
    plt.ylabel(r'<$\rho$>')
    plt.xlabel(r'$-\epsilon \; (\frac{a}{kT})$')
    plt.legend()
    plt.grid()
    plt.savefig(file_path)
    plt.clf()
    
    print('compareCompactness figure generated.')
    print('Figure Saved to ' + file_path)

# compareCompactness(10, energy, path_root + 'figure5-1', F, 10)
# compareCompactness(10, energy, path_root + 'figure5-2', NF, 10)

# Figures 6-7
def sequenceBarCharts(n, iterations, file_path, neg_epsilon=5, e_ns=1000, width=0.4):
    """
    Generates two barcharts (one for each ensemble generation method) where the compactness
    and native state compactness of ensembles assigned with each possible sequence with input size (n)
    is computed. 

    It is easier to analyze these charts through the interactive view (plt.show)
    
    :param n: Residue count (integer)
    :param iterations: Number of iterations for Monte Carlo sampling (integer)
    :param file_path: Figure file save path (string) 
    :param neg_epsilon: Stabilization energy (float)
    :param e_ns: Stabilization energy used to approximate lim neg_epsilon -> inf (float)
    :param width: Width of each bar (float)
    """
    p = []
    p_ns = []
    p_mc = []
    p_mc_ns = []
    x = []

    d = sorted(generateSeqs(n), key=sortCalcPhi)
    g = generateCons(n, [0]*n)
    mc = main(n, iterations, [0]*n, neg_epsilon)  
    mc_ns = main(n, iterations, [0]*n, e_ns)

    for i in range(len(d)):
        x.append(i+1)
        setEnsembleSequence(g, d[i])
        p.append(calcAvgP(g, neg_epsilon))
        p_ns.append(calcNativeP(g))

        setEnsembleSequence(mc, d[i])
        p_mc.append(calcAvgP(mc, 5))

        setEnsembleSequence(mc_ns, d[i])
        p_mc_ns.append(calcAvgP(mc_ns, e_ns))

    plt.bar(x, p, width, color='blue')
    plt.bar([i+width for i in x], p_ns, width, color='orange')
    label = ['']*len(d)
    label[0] = '1'
    label[-1] = str(len(d))
    plt.ylabel(r'<$\rho$>')
    plt.xlabel('Sequence index')
    plt.xticks(x, label)
    plt.legend([r'$-\epsilon=5$', r'$-\epsilon \approx \infty$'])
    plt.grid()
    plt.savefig(file_path + 'figure6')

    plt.cla()
    plt.bar(x, p_mc, width, color='blue')
    plt.bar([i+width for i in x], p_mc_ns, width, color='orange')
    plt.savefig(file_path + 'figure7')
    plt.clf()

    print('sequenceBarCharts figures generated.')

# sequenceBarCharts(8, 100000, path_root)
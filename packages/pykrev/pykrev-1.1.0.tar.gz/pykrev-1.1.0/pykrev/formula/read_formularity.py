import pandas as pd
import numpy as np 

def read_formularity(report_name,pi_col = []):
    """ 
	Docstring for function PyKrev.read_formularity
	====================
	This function reads the report csv file produced by formularity software and saves the formula and associated parameters as variables in python. 
	The function filters out any formula that do not have C and H atoms.
    
	Use
	----
	read_formularity(report_name)
    
	Returns a list of formula, a numpy array of peak intensities, a numpy array of mz ratios, a numpy of mass errors and a list of compound class assignments. 
    
	Parameters
	----------
	report_name: name of csv file that the formularity report to be read is saved as. 
	pi_col: name of the column in that file that peak intensities are found in. If not given the last column is used. 
    """
        
    report = pd.read_csv(report_name)
    
    #sum C and C13 atoms
    C = report['C'] + report['C13']
    H = report['H']
    O = report['O']
    N = report['N'] 
    S = report['S']
    P = report['P']

 
    if not pi_col: 
        I = report.iloc[:,-1] #take the final column of the report file to contain peak intensities. Not sure how stable this is.
    else:
        I = report[pi_col] #user supplied a column name for the peak intensities.
    
    MZ = report['Mass']
    G = report['Class']
    ME = report['Error_ppm']

    molecular_formula = []
    mass_charge = np.array([])
    mass_error = np.array([])
    peak_intensities = np.array([])
    compound_class = []
    
    for n in range(0,len(C)):
        if C[n] == 0 and H[n] == 0: #If there isn't a count for C and H don't include the formula
            pass
        else:
            temp_formula = 'C'+str(C[n])+'H'+str(H[n]) #add C and H then ... 
            if N[n] > 0:
                temp_formula = temp_formula + 'N' + str(N[n])
            if O[n] > 0:
                temp_formula = temp_formula + 'O' + str(O[n])
            if P[n] > 0:
                temp_formula = temp_formula + 'P' + str(P[n])
            if S[n] > 0:
                temp_formula = temp_formula + 'S' + str(S[n])
            
            molecular_formula.append(temp_formula)
            peak_intensities = np.append(peak_intensities,I[n])
            mass_charge =  np.append(mass_charge,MZ[n])
            mass_error = np.append(mass_error,ME[n])
            compound_class.append(G[n])
       
    return molecular_formula, peak_intensities, mass_charge, mass_error, compound_class #return as a tuple, that can be unpacked if necessary
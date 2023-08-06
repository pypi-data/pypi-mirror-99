from .element_counts import element_counts
import numpy as np
def double_bond_equivalent(formula_list):
    
      
    """ 
	Docstring for function pyKrev.double_bond_equivalent
	====================
	This function takes a list of molecular formula strings and returns the double bond equivalent.
    
	Use
	----
	double_bond_equivalent(Y)
    
	Returns a numpy array of len(Y) in which each item is the double bond equivalent.  
    
	Parameters
	----------
	Y: A list of molecular formula strings.
    
	Info
	----------
    
	Double bond equivalent (DBE; UN; degree of unsaturation; PBoR [Pi Bonds or Rings]): 
	The number of molecules of H2 that would have to be added to a molecule to convert all pi bonds to single bonds, 
	and all rings to acyclic structures. 
	The DBE number can be calculated from the formula using the following equation:

	DBE = UN = PBoR = C - (H/2) + (N/2) +1,
	where: C = number of carbon atoms, H = number of hydrogen and halogen atoms, and N = number of nitrogen atoms.
    
    
    """    
    count_list = element_counts(formula_list)
    DBE_array = np.array([])
    warning = 0
    
    for count in count_list:
        Halogens = ['H','Cl','Br','I','F','At','Ts']
        Hal = 0 
        for el in Halogens: 
            try:
                Hal += count[el]
            except KeyError:
                pass 
            
        DBE_counts = count['C'] - (Hal/2) + (count['N']/2) + 1 
        
        if DBE_counts < 0:
            warning = 1
            DBE_counts = 0
        
        DBE_array = np.append(DBE_array,DBE_counts)
    
    if warning == 1:
        print('Warning: negative dbe counts detected and set to zero.')
            
    return DBE_array
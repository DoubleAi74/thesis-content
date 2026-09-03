





# import matplotlib.pyplot as plt

# S0 = 1
# p = 0.45
# maxN = 100

# def nextS(Sprev):
#     return (2*p)*Sprev - p*Sprev**2

# def getSn_A(n):
#     S = S0
#     for i in range(n):
#         S = nextS(S)
#     return S

# def get2pn(n):
#     return (2*p)**n





# for i in [0.1,0.2,0.3,0.4,0.45]:
#     p = i
#     X = [i for i in range(maxN)]
    
#     Y = [getSn_A(n) / get2pn(n) for n in range(maxN)]
    
#     plt.plot(X, Y)
#     plt.scatter([0],[(1-2*p)/(1-p)])
    
 
    
     
# plt.title('Mean population conditioned on non-extinction.\n Values of $P$ vary from bottom to top: 0.3, 0.4, 0.45, 0.48, 0.49.')
# plt.ylabel('Conditional mean')
# plt.ylabel('$n$')

# #plt.savefig('conditionalMean.pdf', dpi = 1000)



    
 
# Pvals = []
# Avals = []

# for i in range(1,50):
#     print(i)
#     p = i/100
    
#     seq = [getSn_A(0) / get2pn(0), getSn_A(1) / get2pn(1)]
    
#     itr = 2
 
#     while abs(seq[-1] - seq[-2]) > 1e-10 and itr < 100000:
#         seq.append( getSn_A(itr) / get2pn(itr) )
        
#         itr += 1
    
#     Pvals.append(p)
#     Avals.append(seq[-1])
    
    
    

#     print(2)
# plt.figure()
# # plt.plot([i/100 for i in range(0,51)], [0.5*(1-2*i/100)/(1-i/100) for i in range(0,51)])
# plt.scatter(Pvals, Avals)


# def write_numbers_to_file(numbers1, numbers2, file_path):
#     try:
#         with open(file_path, 'w') as file:
#             for n1, n2 in zip(numbers1, numbers2):
#                 file.write(str(n1) +','+str(n2) + '\n')
#         print(f"Successfully wrote the numbers to {file_path}")
#     except IOError:
#         print(f"An error occurred while writing the file {file_path}")


    
# write_numbers_to_file(Pvals, Avals, 'Adata.txt')
    
    
    

































import numpy as np 
import matplotlib.pyplot as plt




def iterateSn(Sn, p):
    return 2*p*Sn - p*Sn**2 



def Aprod(p, n_max):
    prev_Aprod = 1/2
    Sn = 1
    
    tol = 1e-300

    
    for n in range(1, n_max+1):
        Sn = iterateSn(Sn, p)
        
        Aprod = prev_Aprod * (1 - Sn/2)
        
       
        # if n>50 and abs(Aprod - prev_Aprod) < tol:
        #     return Aprod
        prev_Aprod = Aprod
    
    return prev_Aprod
    
    
    
    
   

    # whilst computing S_n upto specified n
    # multiply a stored variable by the factor 1-S_n/2 at each step
    # the variable starts at 1/2


def Abasic(p, n_max):
    Sn = 1
    expected = 1
    tol = 1e-300
    prevRatio = 0
    
    for n in range(1, n_max+1):
        Sn = iterateSn(Sn, p)
        expected *= 2*p
        
        ratio = Sn / (2*p)**n
       
        if n>50 and abs(ratio - prevRatio) < tol:
            return ratio
        prevRatio = ratio
    
    return prevRatio
            
        
    
 


p_range = [float(p) for p in np.arange(0.0001,0.5,0.01)]  





# Agood = np.array([Abasic(p, 1000000) for p in p_range])
Agood = np.array([Aprod(p, 1000000) for p in p_range])

plt.scatter(p_range, Agood)


def prod_discrepancy(n):
    
    Aprod_range = np.array([Aprod(p, n) for p in p_range])
    
    float64 = abs(Agood**-1 - Aprod_range**-1)
    out = [float(val) for val in float64]
    
    return abs(Agood**-1 - Aprod_range**-1)
    

def basic_discrepancy(n):
    
    Abasic_range = np.array([Abasic(p, n) for p in p_range])
    
    float64 = abs(Agood**-1 - Abasic_range**-1)
    out = [float(val) for  val in float64]
    
    return abs(Agood**-1 - Abasic_range**-1)






# for n in [10, 100, 1000]:
#     prod_diff = prod_discrepancy(n)
#     basic_diff = basic_discrepancy(n)
    
#     plt.figure()
    
#     print(len(p_range), len(prod_diff))
#     print(p_range[:3], prod_diff[:3])
    
#     plt.scatter(p_range[:-1], prod_diff[:-1])
#     plt.scatter(p_range[:-1], basic_diff[:-1])
#     print()
#     print(n, prod_diff[-3:],basic_diff[-3:])
    
    
    
    
    
    # plt.scatter(p_range[:499], prod_diff[:499], 'r')
    # plt.scatter(p_range[:49], basic_diff[:49], 'b')





# Abasic_range = [Abasic(p, n_max) for p in p_range]
# plt.scatter(p_range, Abasic_range)



# for n_max in [10,100,1000]:
#     Aprod_range = [Aprod(p, n_max) for p in p_range]
#     plt.scatter(p_range, Aprod_range)




# print(Abasic(0.01, 1000000))
    

    
    
    
'''
1. plot a using basic 









In the abscence of an exact formula to describe A(p), we are left with approximation and numerical methods.
For much of the curve between p=0 and p=0.5, these approaches can give us a computation of the non-extinct branching mean (1/A)
with very close tolerance, and requiring only a modest number of algorithmic iterations in the numerical case. But there is an issue. 
As p draws very close to 0.5 corresponding with the near run up to critical branching, A(p) tends to 0 and the nonextict mean 1/A tends to infinity.
And difernences in A of dininishing magnitude can sway 1/A by O(1), which is problematic for the case of an approximate closed formula, but in the case of numerical approximation 
there is a furthur difficulty. When a sub critical branching process is defined ever nearer to criticallity, its lifetime, yet finite, will on the average grow to exceedingly long duration. 
And in tune with this, its survival probability at generation n, will receed to 0, ever more slowly.

For the numerical apprximation to work, $S_{n+1} = f(S_n)$ must be iterated to a to a sufficiently large n whereby $S_n$ is very close to 0 and all but unchanging from one generation to the next. 
And at p\approx 0.5, this can take more generations than is practical to compute, and hence the approximation begins to fail in that specific range.

For this reason, the follwing regime seems best with present knowledge for computing A(p):
    use the infinite product apprximation
    $$INSERT$$
for 0<p<c, where c is a number less than but very close to 0.5 (4.9999) for example. Then, 
for c<p<0.5, use the aysmptotic formula, A=2-4p.












'''
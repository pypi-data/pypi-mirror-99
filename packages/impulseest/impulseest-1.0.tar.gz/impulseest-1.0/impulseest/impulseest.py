from numpy import zeros, identity, transpose, std, hstack, bmat, log, convolve, diag
from numpy.linalg import pinv, qr, det, cholesky
from scipy.optimize import minimize

from impulseest.creation import create_alpha, create_bounds, create_Phi, create_Y

def impulseest(u, y, n=100, RegularizationKernel='none', MinimizationMethod='L-BFGS-B'):
    """Non-parametric impulse response estimation with input-output data

    This function estimates the impulse response with regularization or not. 
    The variance increases linearly with the finite impulse response model order, 
    effect that can be countered by regularizing the estimative.
    Input arguments:
    - u [NumPy array]: input signal (size N x 1);
    - y [NumPy array]: output signal (size N x 1);
    - n [integer]: number of impulse response estimates (default is n = 100);
    - RegularizationKernel [string]: regularization method - 'none', 'DC','DI','TC' (default is 'none');
    - MinimizationMethod [string]: bound-constrained optimization method used to minimize the cost function - 'L-BFGS-B', 'Powell','TNC' (default is 'L-BFGS-B').
    Output:
    - ir [NumPy array]: estimated impulse response (size n x 1).
   """

    #make sure u and y are shaped correctly
    u = u.reshape(len(u),1)
    y = y.reshape(len(y),1)
    N = len(y)  #length of input-output vectors
    
    #check the arguments entered by the user, raise exceptions if something is wrong
    argument_check(u,y,n,N,RegularizationKernel,MinimizationMethod)

    #arrange the regressors to least-squares according to T. Chen et al (2012)
    Phi = create_Phi(u,n,N)
    Y = create_Y(y,n,N)
    
    #calculate impulse response without regularization
    ir_ls = pinv(Phi @ transpose(Phi)) @ Phi @ Y 
    ir_ls = ir_ls.reshape(len(ir_ls),1)   

    #initialize variables for hyper-parameter estimation
    I = identity(n)         #identitity matrix
    sig = std(ir_ls)        #sigma = standard deviation of the LS solution
    P = zeros((n,n))        #zero matrix

    #initialize alpha and choose bounds according to the chosen regularization kernel
    alpha_init = create_alpha(RegularizationKernel,sig)
    bnds = create_bounds(RegularizationKernel)

    #function to create the regularization matrix
    def Prior(alpha):   
        for k in range(n):
            for j in range(n):
                if(RegularizationKernel=='DC'):
                    P[k,j] = alpha[0]*(alpha[2]**abs(k-j))*(alpha[1]**((k+j)/2)) 
                elif(RegularizationKernel=='DI'):
                    if(k==j):
                        P[k,j] = alpha[0]*(alpha[1]**k)
                    else:
                        P[k,j] = 0
                elif(RegularizationKernel=='TC'):
                    P[k,j] = alpha[0]*min(alpha[1]**j,alpha[1]**k)
                else:
                    None            
        return P

    if(RegularizationKernel!='none'):
        #precomputation for the Algorithm 2 according to T. Chen, L. Ljung (2013)
        aux0 = qr(hstack((transpose(Phi),Y)),mode='r')
        Rd1 = aux0[0:n+1,0:n]
        Rd2 = aux0[0:n+1,n]
        Rd2 = Rd2.reshape(len(Rd2),1)

        #cost function written as the Algorithm 2 presented in T. Chen, L. Ljung (2013)
        def cost_func(alpha):
            L = cholesky(Prior(alpha))
            Rd1L = Rd1 @ L
            to_qr = bmat([[Rd1L,Rd2],[alpha[len(alpha)-1]*I,zeros((n,1))]])
            R = qr(to_qr,mode='r')
            R1 = R[0:n,0:n]
            r = R[n,n]
            cost = (r**2)/(alpha[len(alpha)-1]**2) + (N-n)*log(alpha[len(alpha)-1]**2) + 2*sum(log(abs(diag(R1))))
            return cost

        A = minimize(cost_func, alpha_init, method=MinimizationMethod, bounds=bnds)
        alpha = A.x
        L = cholesky(Prior(alpha))
        Rd1L = Rd1 @ L
        to_qr = bmat([[Rd1L,Rd2],[alpha[len(alpha)-1]*I,zeros((n,1))]])
        R = qr(to_qr,mode='r')
        R1 = R[0:n,0:n]
        R2 = R[0:n,n]
        ir = L @ pinv(R1) @ R2

        ir = ir.reshape(len(ir),1)

    else:
        ir = ir_ls

    return ir

#function to check all the arguments entered by the user, raising execption if something is wrong
def argument_check(u,y,n,N,RegularizationKernel,MinimizationMethod):
    if(len(u)!=len(y)):
        raise Exception("u and y must have the same size.")

    if(n>=N):
        raise Exception("n must be at least 1 sample smaller than the length of the signals.")

    if(RegularizationKernel not in ['DC','DI','TC','none']):
        raise Exception("the chosen regularization kernel is not valid.")

    if(MinimizationMethod not in ['Powell','TNC','L-BFGS-B']):
        raise Exception("the chosen minimization method is not valid. Check scipy.minimize.optimize documentation for bound-constrained methods.")

    return None
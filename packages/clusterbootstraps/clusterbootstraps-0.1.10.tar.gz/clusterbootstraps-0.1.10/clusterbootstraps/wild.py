import numpy as np
import pandas as pd
from prettytable import PrettyTable

class wild:
    # Y: matrix of depedent variables, cluster_var: column where variable depended to cluster in, iter: number of iterations, seed: number of seed, constant: including constant term, *args: matrix of indepedent variables,
    def __init__(self, Y, X, cluster_var, iter = 10000, seed = 2020, alpha = 5, constant = 1): 
        np.random.seed(seed)

        if type(X) != type(np.zeros([2,2])):
            self.X = X.values
            l = list(X.columns)
            self.cluster = X.columns.get_loc(cluster_var)
            del l[self.cluster]
            self.column = l
            self.Y_ = Y.values
            self.dataframe = 1
        else:
            self.dataframe = 0
            self.cluster = cluster_var - 1
            self.Y_ = Y
            self.X = X
            l= list(range(1, self.X.shape[1] + 1))
            del l[self.cluster]
            self.column = l
        
        # Change the method of calculating according to constant setting 
        if constant == 1:
            self.X = np.c_[np.ones([self.X.shape[0], 1]), self.X]
            self.column.insert(0, 'Constant')
    
        def cluster_(X, Y, cluster):
            xx = np.linalg.inv(np.dot(X.T,X))
            beta = np.dot(np.dot(xx ,X.T),Y)
            xc = np.unique(X[:, cluster])
            n_cluster = len(xc) # number of clusters 
            X_ = [[] for m in range(n_cluster)]# list of clustered X
            Y_ = [[] for m in range(n_cluster)]# list of Y according to clustered X
            U = [[] for m in range(n_cluster)]# list of U according to clustered X
            U1 = [[] for m in range(n_cluster)]# list of tlide U according to clustered X
            for i in range(n_cluster):
                for n in range(X.shape[0]):
                    if X[n, cluster] == xc[i]:
                        X_[i].append(X[n])
                        Y_[i].append(Y[n])
                        U[i].append(Y[n] - np.dot(X[n], beta))
                X_[i] = np.array(X_[i])
                Y_[i] = np.array(Y_[i])
                U[i] = np.array(U[i])
                U1[i].append(np.array(((n_cluster - 1/n_cluster)**0.5)**np.dot(np.linalg.inv(np.eye(X_[i].shape[0])-np.dot(np.dot(X_[i],xx),X_[i].T)),U[i])))
                if i == 0:
                    X__ = X_[0]
                    Y__ = Y_[0]
                else:
                    X__ = np.r_[X__, X_[i]]
                    Y__ = np.r_[Y__, Y_[i]]
            return n_cluster, X_, X__, U, U1, beta, xx

        # Initialise y_hat_star (y), X (Bsample),beta_hat_theta(Results), standard error(se) ,Wald test statistic(w) and reshaped Wald test statistic(wr)
        self.y = np.zeros([self.X.shape[0],1])  
        self.Bsample = np.zeros([self.X.shape[0],self.X.shape[1]])
        self.Results = np.zeros((iter,self.X.shape[1],1))
        self.se = np.zeros([iter,1,self.X.shape[1]])
        self.w = np.zeros((iter,1,self.X.shape[1]))
        self.wr = np.zeros([self.X.shape[1],1])
        n_cluster, X_, X__, U, U__, beta, xx = cluster_(self.X, self.Y_, self.cluster)[0], cluster_(self.X, self.Y_, self.cluster)[1], cluster_(self.X, self.Y_, self.cluster)[2], cluster_(self.X, self.Y_, self.cluster)[3], cluster_(self.X, self.Y_, self.cluster)[4], cluster_(self.X, self.Y_, self.cluster)[5], cluster_(self.X, self.Y_, self.cluster)[6]             
        self.beta = beta  
        self.iter = iter
        self.alpha = alpha
        for i in range(n_cluster):
            if i == 0:
                xuux = np.dot(np.dot(np.dot(X_[0].T ,U__[0][0]),U__[0][0].T),X_[0])
            else:
                xuux = xuux + np.dot(np.dot(np.dot(X_[i].T ,U__[i][0]),U__[i][0].T),X_[i]) 
        
        def f(x):
            return np.dot(x, beta)
        
        # Calculate Bootstap sample and estimates for each interation 
        # Sample with replacement
        for b in range(iter):
            u = U
            for k in range(n_cluster): 
                self.Bsample = X__
                
                c = np.random.uniform(0,1) # with the probability of 0.5 to choose ug
                # ug_hat_star = ug_hat with probability 0.5 
                if c <= 0.5:
                    u[k] = U[k]                
                # ug_hat_star = -ug_hat with probability 0.5 
                else:
                    u[k] = -U[k]
                
                if k == 0:
                    u_ = u[0]
                else:
                    u_ = np.r_[u_, u[k]]
                
            self.y = f(self.Bsample) + u_
            self.Results[b] = np.dot(np.dot(np.linalg.inv(np.dot(self.Bsample.T, self.Bsample)), self.Bsample.T), self.y)
            self.se[b] = np.diag(np.dot(np.dot(xx ,xuux),xx))**0.5
            self.w[b] = (self.Results[b].T - beta.T)/np.array(self.se[b])
            # Reshape results and w-statistics
            if b == 0:
                self.Results_coef1 =  np.dot(np.dot(xx ,self.X.T),self.y)
                self.wr = self.w[b].T
            else:
                self.Results_coef1 =  np.c_[self.Results_coef1, np.dot(np.dot(xx ,self.X.T),self.y)]
                self.wr = np.c_[self.wr, self.w[b].T]
            
        self.mean = np.mean(self.w, axis = 0)
        obs = np.array([self.iter*(self.alpha*0.01/2)],dtype='i')
        self.low = np.partition(self.wr, obs-1, axis = 1)[:,obs-1]
        self.up = -np.partition(-self.wr, obs-1, axis = 1)[:,obs-1]
        mean_ = np.mean(self.Results_coef1, axis = 1)
        self.mean_coef1 = np.zeros([self.X.shape[1], 1])
        for i in range(self.X.shape[1]):
            self.mean_coef1[i] = mean_[i]
        self.cluster_se = np.mean(self.se, axis = 0)

    # Compute variance    
    def cluster_standard_error(self):
        return self.cluster_se
    
    # Compute mean of Wald tast statistic
    def mean_wald(self):
        return self.mean
    
    # Compute lower bound of (1-alpha)100% confidence interval of Wald test statistic
    def lower_bound(self):
        return self.low
    
    # Compute upper bound of (1-alpha)100% confidence interval of Wald test statistic
    def upper_bound(self):
        return self.up
    
    def new_coef(self):
        return self.mean_coef1
    
    def cluster_standard_error(self):
        return self.cluster_se
    
    # Print a table
    def table(self):
        data1 = np.zeros((4, self.X.shape[1], 1))
        data1[0] =self.beta
        data1[1] =self.mean_coef1
        data1[2] =self.mean.T
        data1[3] =self.cluster_se.T
        data_ci = np.array(["[" + str(format(self.low[i,0],'.4f')) +", " + str(format(self.up[i,0],'.4f')) + "]" \
                            for i in range(self.X.shape[1])])
        data = np.c_[data1[0], data1[1], data1[2], data1[3]]
        data = np.delete(data, self.cluster, 0)
        data_ci = np.delete(data_ci, self.cluster, 0)
        formater="{0:.04f}".format
        df = pd.DataFrame(data,
            columns=['Original Coefs', 'Average Coefs', 'Wild Bootstrap Wald Mean', 'Cluster Standard Error'])
        df = df.applymap(formater)
        tb = PrettyTable()
        tb.add_column('Variables',self.column)
        tb.padding_width = 1 # One space between column edges and contents (default)  
        tb.add_column('Original Coefs',df.iloc[:, 0])
        tb.add_column('Average Coefs',df.iloc[:, 1])
        tb.add_column('Wild Bootstrap Wald Mean',df.iloc[:, 2])
        tb.add_column('Cluster Standard Error',df.iloc[:, 3])
        tb.add_column('Confidence Interval',data_ci)
        print('Wild Cluster Bootstrap-T(iteration = %d)'.center(108)%self.iter)
        print(tb)
        print("* 'The table displays %d"%self.alpha +" % confidence interval of the Wald test statistics.")

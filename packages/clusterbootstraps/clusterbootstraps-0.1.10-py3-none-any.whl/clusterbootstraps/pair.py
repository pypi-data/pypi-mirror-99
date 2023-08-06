import pandas as pd  
import numpy as np  
import statsmodels.api as sm  
from prettytable import PrettyTable

class Pair:
    def __init__(self, Y, X, cluster_var, iter=10000,seed=2020,alpha=5,constant = 1): 
        
        self.iter = iter
        self.alpha = 100 - alpha
        
        Y_data = pd.DataFrame(Y)
        X_data = pd.DataFrame(X)
        y_name = Y_data.columns[0]
        x_name = X_data.columns.values.tolist()
        
        if x_name[0] == 0:
            for i in range(len(x_name)):
                x_name[i] = x_name[i]+1
        
        X_data.columns = x_name
        data = pd.concat([Y_data, X_data], axis=1)
        
        #get cluster list and reset the index
        cluster_list = data.drop_duplicates([cluster_var])[cluster_var]
        self.cluster_value = cluster_list.reset_index(drop = True)
        self.num_cluster = len(self.cluster_value)
        
        #to know the cluster variable is in which column
        n = 0
        for i in range(data.iloc[0,:].size):
            if data.columns[i] == cluster_var:
                n = i
        
        #overall regression
        x0 = data.iloc[:,1:]
        y0 = data.iloc[:,0 ]
                
        x0 = x0.drop(columns=[cluster_var],inplace=False)
        
        Constant = np.ones(data.iloc[:,0].size)
        x0.insert(0,"Constant",Constant)
        
        if constant == 0:
            x0 = x0.drop(columns=["Constant"],inplace=False)
        
        self.var_list = x0.columns.values.tolist()
        
        result = sm.OLS(y0,x0).fit()
        self.coef = result.params                      #get coefficients terms
        self.uhat = result.resid                       
        
        #reform a new sample
        df_group = data.groupby(cluster_var) 
        x_group = []
        for i in range(self.num_cluster):
           #get different groups, and transform into arrays
           x_group.append(df_group.get_group(self.cluster_value[i]).values)
        
        #cluster: cluster array obtained     cluster_value: the list of categorical variables values
        #n: number of clusters      X: independent variables      Y: dependent variables
        def Unbiased_Cluster_Robust(cluster,cluster_value,n,X,Y):
            invxpx = np.linalg.inv(np.dot(X.T,X))     #get the inverse of (X'X) part  
            result = sm.OLS(Y,X).fit()
            coef = result.params                      #get coefficients terms
            uhat = result.resid                       #get residual terms
    
            x,u,unbiased_u,h,uu,middle = [ ],[ ],[ ],[ ],[ ],[ ]
            Sum = np.zeros((len(coef),len(coef)))
    
            g = np.sqrt((n-1)/n)                      
    
            for i in range(0,n):
                
                x.append(X[(cluster==cluster_value[i]),:])
                u.append(uhat[(cluster==cluster_value[i])])
        
                #get H_gg part for each cluster
                h.append(np.dot( np.dot(x[i], invxpx), (x[i]).T ))
                #get unbiased estimator of U_g for each cluster
                unbiased_u.append( g* (np.dot( np.linalg.inv( np.identity(len(h[i][0,:])) - h[i] ), u[i]) ) )
              
                #following part is similar with CRVE method
                uu.append(np.outer( unbiased_u[i] , unbiased_u[i]))
                middle.append(np.dot(np.dot( (x[i]).T, uu[i] ) ,x[i]))
        
                Sum = np.add(Sum,middle[i])
        
            cluster_error = np.dot(np.dot(invxpx,Sum),invxpx)
            std_error = np.sqrt(np.diagonal(cluster_error))
    
            return std_error
        
        np.random.seed(seed)
        self.Results=np.zeros((self.iter,x0.shape[1]))
        self.Results_coef1=np.zeros((self.iter,x0.shape[1]))
        self.Results_cluster=np.zeros((self.iter,x0.shape[1]))
        self.se1 = np.zeros((self.iter,x0.shape[1]))
        self.k=x0.shape[1]
        
    
        for m in range(self.iter):
            #select pseudisample
            Bsample = np.random.choice(x_group,size=self.num_cluster,replace=True)       #randomly choose 5 clusters from the sample with replacement
            new_Bsample = np.concatenate( Bsample , axis=0 )        #convert a list of arrays into a single array        
        
            x1 = sm.add_constant(np.delete(new_Bsample[:,1:],n-1,1)) #choose X variables and add intercept term
            y1 = new_Bsample[:,0]                                    #choose Y variable

            if constant == 0:
                x1 = np.delete(x1,0,1)
            
            #as this sampling method do not guarantee the inverse of (XX') part, so I check it here
            #if the determinant of (XX') is equal 0, that is, it is not invertible, give up this iteration
            if np.linalg.det(np.dot( (x1).T, x1) )==0:          
                continue
        
            #get the column of rep78, that is, cluster array
            self.cluster_array =  new_Bsample[:,n].astype(np.int)     
            #drop duplicated values to get the value of category variable, that is, cluster_ele
            self.cluster_ele = np.unique(self.cluster_array)             
            #count the number of clusters
            self.num = len( self.cluster_ele ) 
        
        
            new_results = sm.OLS(y1, x1).fit()
            self.coef1 = new_results.params
            
            self.x1 = x1
            self.y1 = y1
        
            self.se1 = Unbiased_Cluster_Robust(self.cluster_array, self.cluster_ele, self.num, self.x1, self.y1)
            
            #calculate the Wald test statistic
            new_wald =  (self.coef1 - self.coef)/self.se1
                            
            new_wald[new_wald ==np.inf] = 0                     #in the case that if the number is too small, replace it with 0
            new_wald[new_wald ==-np.inf] = 0
            
            self.Results[m,:] = new_wald
            self.Results_coef1[m,:]= self.coef1
            self.Results_cluster[m,:]=self.se1
    
        self.low = np.zeros(self.k)
        self.up = np.zeros(self.k)  
        self.mean_coef1 = np.zeros(self.k)  
        self.mean_cluster_std = np.zeros(self.k) 
        
        for i in range(self.k):
            delta = self.Results[:,i]
            kth = np.array([delta.size*(alpha*0.01/2)],dtype='i')
            self.low[i] = np.partition(delta, kth-1)[kth-1]
            self.up[i] = -np.partition(-delta, kth-1)[kth-1]
            
        self.mean = [np.nanmean(self.Results[:,i]) for i in range(len(self.coef))]
        self.mean_coef1 = [np.nanmean(self.Results_coef1[:,i]) for i in range(len(self.coef))]
        self.mean_cluster_std = [np.mean(self.Results_cluster[:,i]) for i in range(len(self.coef))]
        
        self.low = ['{:.4f}'.format(i) for i in self.low]
        self.up = ['{:.4f}'.format(i) for i in self.up] 
        self.mean = ['{:.4f}'.format(i) for i in self.mean] 
        self.coef = ['{:.4f}'.format(i) for i in self.coef]
        self.mean_coef1 = ['{:.4f}'.format(i) for i in self.mean_coef1] 
        self.mean_cluster_std = ['{:.4f}'.format(i) for i in self.mean_cluster_std] 
        self.interval = ["[{},{}]".format(self.low[i],self.up[i]) for i in range(len(self.coef))]
       
        temp = data.iloc[:,0:1]
        col_name = temp.columns[0]   
        self.dependent = str(col_name)  
        #adjust the caption of this table
        ylen = len(self.dependent)
        
        self.str_var_list = [str(i) for i in self.var_list]
        xlen = len(max(self.str_var_list, key=len, default=''))
        
        self.varlen = max(xlen,ylen)
       
    def mean_wald(self):
        return self.mean
    
    def interval(self):
        return self.interval
    
    def new_coef(self):
        return self.mean_coef1
    
    def cluster_std_error(self):
        return self.mean_cluster_std
    
    def table(self):
            tb = PrettyTable()
            print(" "*(int(self.varlen/2+32)) +"Pairs Cluster Bootstrap-T(iteration = %d)"%self.iter)
            tb.field_names = ["Variables", "Original Coefs", "Average Coefs",\
                              "Pair Bootstrap Wald mean","Cluster Standard Error","Confidence Interval"]
            for i in range (0,self.k):
                tb.add_row([self.var_list[i],self.coef[i], self.mean_coef1[i], \
                                self.mean[i],self.mean_cluster_std[i],self.interval[i]])
            #tb.align = 'r'
            tb.padding_width = 1
                    
            print(tb)
            print("* 'The table displays %d"%self.alpha +" % confidence interval of the Pair test statistic.")

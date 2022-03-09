import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from termcolor import colored
  
__version__ = '1.0.0'

class comparing_distributions():
     
    """
    Parameters
    ----------
    dataframe : input pandas.dataframe with columns and an optional 'treatment' column
    features : list of strings of column names from the dataframe of the features/measures for distribution comparison
    treatment : string , name of column from dataframe, that is the split value for comparison (e.g. test&control)
    sample_frac : flaot between 0 and 1 to indicate the percentage to randomly keep from the dataframe.
                use this in case of very large dataframe.
    remove_outliers_quintiles : list of range to keep values at. for example [0.05,0.90] will keep 
                the values within 5% to 90% of the population distribution
    """ 

    
    def __init__(self,
                 dataframe,
                 features,
                 treatment=None,
                 remove_outliers_quintiles=[0,1],
                 sample_frac=1):
        
        self.dataframe=dataframe
        self.features=features
        self.treatment=treatment
        self.remove_outliers_quintiles=remove_outliers_quintiles
        self.sample_frac=sample_frac
        self.treatment_check=False
        
        # column types validations
        assert type(self.features)==list,f"""please input 'features' parameter as a list of columns and not {type(self.features)} """
        if treatment is None:
            pass
        if treatment is not None:
            assert (type(treatment)==str)  ,f"""please input treatment parameter as string type and not {type(treatment)} """
            self.treatment_check = True
        
        if len(self.dataframe)*sample_frac>150000:
            print(f'DataFrame containing {len(self.dataframe)*sample_frac} samples. plotting might be slow. consider sampleing for plots.')

            
    def PrepareDF(self):
        
        if self.treatment==None:
            cols=self.features
        elif len(self.treatment)>0:
            cols=self.features+[self.treatment]

        tmp_df=self.dataframe.loc[:,cols].sample(frac=self.sample_frac,random_state=1).copy()

        if self.sample_frac != 1:
            print(f'''Sampled {self.sample_frac*100}% of population. n={len(tmp_df)}''')
            
        if  (self.remove_outliers_quintiles[0]!=0) | (self.remove_outliers_quintiles[1]!=1):
            lower_bound=self.remove_outliers_quintiles[0]
            upper_bound=self.remove_outliers_quintiles[1]
            
            for col in self.features:
                tmp_df[col] = tmp_df[col][tmp_df[col].between(tmp_df[col].quantile(lower_bound),
                                                              tmp_df[col].quantile(upper_bound))]   
            range_=upper_bound-lower_bound
            print(f'''keeping values within {lower_bound}% - {upper_bound}% of distribution . n={round(range_*len(tmp_df),1)}''')

        return tmp_df
        
        
    def PlotECDF(self,figsize=(10,4),**kwargs):

        '''
        Plot ECDF using plotly frameware
        
        
        Parameters
        ----------
        figsize : tuple of 2 int representing size of fig. default = (10,4)
        '''
        
        tmp_df=self.PrepareDF()
        if (len(self.features)==1) & (self.treatment_check):
            plt.figure(figsize=figsize)
            sns.ecdfplot(tmp_df,x=self.features[0],hue=self.treatment,**kwargs)
            plt.show()
        elif (len(self.features)>1) & (self.treatment_check):
            for col in self.features:
                plt.figure(figsize=figsize)
                sns.ecdfplot(tmp_df,x=col,hue=self.treatment,**kwargs )
                plt.show()
        elif (len(self.features)>=1) & (self.treatment_check==False):  
            plt.figure(figsize=figsize)
            sns.ecdfplot(tmp_df[[*self.features]],**kwargs)
            plt.show()

            
    def PlotHist(self,bins=None,histnorm='percent',figsize=(8,4),**kwargs):

        '''
        Plot Historgam (normelized in default) using seaborn frameware
        
        
        Parameters
        ----------
        figsize : tuple of 2 int representing size of fig. default = (10,4)
        bins : Positive integer. Sets the number of bins.
        histnorm : str (default `percent`)
            One of `'percent'`, `'probability'`, `'density'`, or `'probability
            density'` If `None`, the output of `histfunc` is used as is. If
            `'probability'`, the output of `histfunc` for a given bin is divided by
            the sum of the output of `histfunc` for all bins. If `'percent'`, the
            output of `histfunc` for a given bin is divided by the sum of the
            output of `histfunc` for all bins and multiplied by 100. If
            `'density'`, the output of `histfunc` for a given bin is divided by the
            size of the bin. If `'probability density'`, the output of `histfunc`
            for a given bin is normalized such that it corresponds to the
            probability that a random event whose distribution is described by the
            output of `histfunc` will fall into that bin.
        '''
        
        
        tmp_df=self.PrepareDF()       
        if (len(self.features)==1) & (self.treatment_check):
            fig = px.histogram(tmp_df, x=self.features[0], color=self.treatment,nbins=bins,histnorm=histnorm,**kwargs)
            fig.update_layout(width=figsize[0]*100,height=figsize[1]*100,)
            fig.show()
        elif (len(self.features)>1) & (self.treatment_check):
            for col in self.features:
                fig = px.histogram(tmp_df, x=col,color=self.treatment,nbins=bins,opacity=0.75,histnorm=histnorm,**kwargs) 
                fig.update_layout(width=figsize[0]*100,height=figsize[1]*100,barmode='overlay')
                fig.show()
        elif (len(self.features)>=1) & (self.treatment_check==False):  
            fig = px.histogram(tmp_df, x=[*self.features],nbins=bins,opacity=0.75,histnorm=histnorm,**kwargs) 
            fig.update_layout(width=figsize[0]*100,height=figsize[1]*100,barmode='overlay')
            fig.show()    
                

    def KS_Test(self,ks_alternative='two-sided',ks_mode='auto',pval=0.1,):


        """
        ks_alternative: input pandas.DataFrame containing at least 1 column for ECDF plot
        ks_mode: string , name of column from dataframe, that is the split value for the ECDF
        pval: list of range to keep values at. for example [0.05,0.90] will keep 
        the values within 5% to 90% of the population distribution

        see KS documentation if needed:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html
        """
    
        tmp_df=self.PrepareDF()
        if self.treatment==None:
            pass
        else:
            assert len(tmp_df[self.treatment].unique())==2 , f'treatment must contain 2 values only for ks_test, recived {len(tmp_df[self.treatment].unique())} ' 

        if (len(self.features)==1) & (self.treatment_check):
            a,b = tmp_df[self.treatment].unique()
            d1=tmp_df[self.features[0]][tmp_df[self.treatment]==a]
            d2=tmp_df[self.features[0]][tmp_df[self.treatment]==b]
            print('')
            print('***',self.features[0],'***')
            print(stats.ks_2samp(d1, d2, alternative=ks_alternative, mode=ks_mode))
            ks_pval=stats.ks_2samp(d1, d2, alternative=ks_alternative, mode=ks_mode)[1]
            
            if ks_pval<=pval:
                print(colored(f''''{a}' & '{b}' come from different distributions, since KS P-Value is smaller then {pval}  ''','red'))
            if ks_pval>pval:
                print(colored(f''''{a}' & '{b}' come from same distributions, since KS P-Value is higher then {pval}  ''','green'))
                
        elif (len(self.features)>1) & (self.treatment_check):

            for col in self.features:
                a,b = tmp_df[self.treatment].unique()
                d1=tmp_df[col][tmp_df[self.treatment]==a]
                d2=tmp_df[col][tmp_df[self.treatment]==b]
                print('')
                print('***',col,'***')
                print(stats.ks_2samp(d1, d2, alternative=ks_alternative, mode=ks_mode))
                ks_pval=stats.ks_2samp(d1, d2, alternative=ks_alternative, mode=ks_mode)[1]
                
                if ks_pval<=pval:
                    print(colored(f''''{a}' & '{b}' come from different distributions, since KS P-Value is smaller then {pval}  ''','red'))
                if ks_pval>pval:
                    print(colored(f''''{a}' & '{b}' come from same distributions, since KS P-Value is higher then {pval}  ''','green'))

        elif (len(self.features)>=1) & (self.treatment_check==False): 
            
            assert len(self.features)==2,f"""KS test can be applied to 2 distributions. got {len(self.features)} """

            a,b = self.features
            d1=tmp_df[self.features[0]]
            d2=tmp_df[self.features[1]]
            print('')
            print('***',a,'vs',b,'***')
            print(stats.ks_2samp(d1, d2, alternative=ks_alternative, mode=ks_mode))
            ks_pval=stats.ks_2samp(d1, d2, alternative=ks_alternative, mode=ks_mode)[1]

            if ks_pval<=pval:
                print(colored(f''''{a}' & '{b}' come from different distributions, since KS P-Value is smaller then {pval}  ''','red'))
            if ks_pval>pval:
                print(colored(f''''{a}' & '{b}' come from same distributions, since KS P-Value is higher then {pval}  ''','green'))   
    

    def ttest(self,test_group_name='test',pval=0.05):

        tmp_df=self.PrepareDF() 
        if self.treatment==None:
            assert (False), 'ttest must recive a treatment column'
        else:
            assert len(tmp_df[self.treatment].unique())==2 , f'treatment must contain 2 values only for ttest, recived {len(tmp_df[self.treatment].unique())} ' 
            
    
        if (len(self.features)>=1) & (self.treatment_check):
            a,b = tmp_df[self.treatment].unique()
            for col in self.features:
            
                sample1= tmp_df[tmp_df[self.treatment]==test_group_name][col].dropna()
                sample2= tmp_df[tmp_df[self.treatment]!=test_group_name][col].dropna()

                print('')
                print('***',col,'***')
                print(stats.ttest_ind(sample1, sample2,equal_var=False))
                ttest_pval=stats.ttest_ind(sample1, sample2,equal_var=False)[1]

                if ttest_pval<=pval:
                    print(colored(f''''{a}' & '{b}' have different means, since ttest P-Value is smaller then {pval}  ''','red'))
                if ttest_pval>pval:
                    print(colored(f''''{a}' & '{b}' have from same mean, since ttest P-Value is higher then {pval}  ''','green'))   

        elif (len(self.features)>=1) & (self.treatment_check==False): 

            a,b = self.features[0],self.features[1]

            sample1= tmp_df[a].dropna()
            sample2= tmp_df[b].dropna()
            
            print('')
            print('***',a,'vs',b,'***')
            print(stats.ttest_ind(sample1, sample2,equal_var=False))
            ttest_pval=stats.ttest_ind(sample1, sample2,equal_var=False)[1]

            if ttest_pval<=pval:
                print(colored(f''''{a}' & '{b}' have different means, since ttest P-Value is smaller then {pval}  ''','red'))
            if ttest_pval>pval:
                print(colored(f''''{a}' & '{b}'have same means, since ttest P-Value is higher then {pval}  ''','green'))   
            
            
    def create_table_one(self,test_group_name='test'):

        '''
        Report balance in input features between the treatment and control groups.

        References:
            R's tableone at CRAN: https://github.com/kaz-yos/tableone
            Python's tableone at PyPi: https://github.com/tompollard/tableone

        Args:
            data (pandas.DataFrame): total or matched sample data
            treatment_col (str): the column name for the treatment
            features (list of str): the column names of features

        Returns:
            (pandas.DataFrame): A table with the means and standard deviations in
                the treatment and control groups, and the SMD between two groups
                for the features.
                
        SMD = Standardized mean difference
        '''
        
        assert type(self.treatment)==str, f'treatment column must be provided to comparing_distributions()'
        
        from causalml.match import create_table_one
       
        tmp_df=self.PrepareDF()
        tmp_df['treatment_col']=[1 if x==test_group_name else 0 for x in tmp_df[self.treatment]]
        print('values are in following format: mean(std)')
        return create_table_one(data=tmp_df,
                         treatment_col='treatment_col',
                         features=self.features)



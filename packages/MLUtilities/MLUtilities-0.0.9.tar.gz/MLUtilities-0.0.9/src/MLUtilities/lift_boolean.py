import pandas as pd

           
class lift_boolean:
      """take the difference between two time columns"""
      def __init__(self,actual_df,lift_df,lift_threshold):
         self.actual_df = actual_df # array of column names to encode
         self.lift_df = lift_df
         self.lift_threshold = lift_threshold
         """
         This function creates a boolean feature   for a given categorical feature
         by selecting those category levels that provide the highest lift ratio.
         The lift ratio is calculated by dividing the percent of fraud transactions by the
         percent of clean transactions.
         It appends the new boolean feature to the old dataframe that was given as the input
         to the function.
         """         
      def create_boolean(self):
   
          self.lift_df = self.lift_df[self.lift_df.Lift_Ratio > self.lift_threshold ]    
          cols =   self.lift_df.feature_name.unique()
          cols_2 = list(set(self.actual_df.columns) & set(cols))
          for i in cols_2:
            #create a boolean column in Data  if the  column i  elements are in the lift category list
              self.actual_df['Bool_'+ i]= [1 if self.actual_df[i].values.tolist()[j] in self.lift_df.Category_levels.to_list() else 0 for j in range(self.actual_df.shape[0])]
             #Counter(Data['Bool_'+ i])
          return self.actual_df 


           
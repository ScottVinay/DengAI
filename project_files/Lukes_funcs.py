def checkword(s,col_lst):
 
  plural = 0
  for word in col_lst:
    if word not in s.columns:
      plural = plural + 1
      print(word,", ", end="")
      if plural <2:
        print("is not a column name within dataframe, please remove it from the input list")
      else:
        print("are not a column names within dataframe, please remove them from the input list")    
        

        
def drop_columns(s, col_lst = None,):
  
  " | --------------------------------------------------------------------------- | "
  " | This function is passed a dataframe s and a list of column names to drop.   | "
  " | It will alert the user if an invalid column key is passed and exit.         | "
  " | --------------------------------------------------------------------------- | "
  
  if len(col_lst) != 0:
    try:
        s.drop(col_lst, axis=1,inplace=True)      
    except(KeyError):
      checkword(s,col_lst)
      return      
  else:
    print("Please provide a occupied list of columns to drop")
  print("Remaining columns:\n",s.columns.values)            
  
  
  
def merge_columns(s, col_lst = None, operation = 'mean', remove_old = True, new_col_name = None ):
  
  from numpy import mean as npmean
  
  " | --------------------------------------------------------------------------- | "
  " | merge_columns is passed a dataframe s and a list of column names to merge   | "
  " | It will alert the user if an invalid column key is passed and exit. The     | "
  " | columns must represent numerical data such that they can be fused           | "
  " | accoringly.                                                                 | "
  " | --------------------------------------------------------------------------- | "
   
  operation = operation.lower()
  if new_col_name == None:
    new_col_name = operation +"_"+ ''.join(col_lst)
  
  case_mean = ['mean','avg']
  nmdtype = ['float64','float32','int64','int32']

  
  # | --- B O R I N G --- A S S --- D A T A --- C H E C K S --- | "
  
  try:
    s[col_lst]
  except(KeyError):
    checkword(s,col_lst)
    return
  
  if len(col_lst) == 0:
    print("Please provide a occupied list of columns to drop")  
  
  if len(col_lst) <2:
    print("Merge's input list requires at least 2 data-series keys")
    return

  for a in col_lst:
    if s[a].dtype not in nmdtype:
      print("Column: '",a,"' is not of numerical type, cannot perform arithmetic.")
      return
    
  # | --- O P E R A T I O N S --- | "
  
  if operation in case_mean:
    print("Mean merging: ",col_lst)
    s[new_col_name] = npmean(s[col_lst],axis =1)
  
  
  
  # | --- C L E A N --- U P --- | "
  
  if remove_old == True:
    for a in col_lst:
      del s[a]  
  print("New columns:\n",s.columns.values)    

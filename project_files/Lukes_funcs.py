def drop_columns(s, drp_lst = None,):
  
  
  " | --------------------------------------------------------------------------- | "
  " | This function is passed a dataframe s and a list of column names to drop.   | "
  " | It will alert the user if an invalid column key is passed and exit.         | "
  " | --------------------------------------------------------------------------- | "
  
  
  if len(drp_lst) != 0:
    try:
        s.drop(drop_list, axis=1,inplace=True)
         
    except(KeyError):
          plural = 0
          for word in drp_lst:
            if word not in s.columns:
              plural = plural + 1
              print(word,", ", end="")
              
          if plural ==0:
            print("is not a column name within dataframe, please remove it from the drop list")
          else:
            print("are not a column names within dataframe, please remove them from the drop list")
         
  else:
    print("Please provide a occupied list of columns to drop")
  print("Remaining columns:\n",s.columns.values)    

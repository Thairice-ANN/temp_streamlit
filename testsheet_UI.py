import streamlit as st
import pandas as pd
import numpy as np

def get_values_list(Test):
	value_list = []
	for i in Test.values():
		value_list = i
	return value_list

def df_from_dict(Test):
	data = np.zeros((1,len(get_values_list(Test))))
	df = pd.DataFrame(data=data,index=Test.keys(),columns=get_values_list(Test))
	return df

#Make DataFrame, Show TestSheet
R051_A = {('R051','A'):['min','max','Param1']}
R051_B = {('R051','B'):['min','max','Param1']}
R051_C = {('R051','C'):['min','max','Param1']}
R052_A = {('R052','A'):['min','max','Param2','Param3','Param4']}
R053_B = {('R053','B'):['Param2','Param5','Param10','Param11']}
R053_C = {('R053','C'):['Param2','Param5','Param10','Param11']}

R051_DF = pd.concat([df_from_dict(R051_A),df_from_dict(R051_B),df_from_dict(R051_C)])
R052_DF = df_from_dict(R052_A)
R053_DF = pd.concat([df_from_dict(R053_B),df_from_dict(R053_C)])

Test_DataFrame = pd.concat([R051_DF,R052_DF,R053_DF])
st.write(Test_DataFrame)

#所持しているTestIDのリスト作成
narrow_TestID_list = Test_DataFrame.index.get_level_values(0).unique()

Select_TestID = st.multiselect("Choose TestID", narrow_TestID_list)
st.write(Test_DataFrame.loc[Select_TestID,].dropna(how='all', axis=1))
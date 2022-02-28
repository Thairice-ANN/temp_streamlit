import streamlit as st
import numpy as np
import itertools
import pandas as pd

def main():
	st.title('抵抗値並列計算')

	Which_Cal = st.selectbox('並列?直列?',['並列','直列'])
	if Which_Cal == '直列':
		st.write('残念！整備中です！')
	else:
		Objective_R = st.number_input('INPUT!! And Press!! Combined R[Ω]', 0.0, 10000000.0, 0.0)
		E_array = st.selectbox('E系列',['E3','E6','E12','E24','E48'])
		if E_array == 'E3':
			E_array = np.array([1.0,2.2,4.7])
		elif E_array == 'E6':
			E_array = np.array([1.0,1.5,2.2,3.3,4.7,6.8])
		elif E_array == 'E12':
			E_array = np.array([1.0,1.2,1.5,1.8,2.2,2.7,3.3,3.9,4.7,5.6,6.8,8.2])
		elif E_array == 'E24':
			E_array = np.array([1.0,1.1,1.2,1.3,1.5,1.6,1.8,2.0,2.2,2.4,2.7,3.0,3.3,3.6,3.9,4.3,4.7,5.1,5.6,6.2,6.8,7.5,8.2,9.1])
		elif E_array == 'E48':
			E_array = np.array([10.0,10.5,11.0,11.5,12.1,12.7,13.3,14.0,14.7,15.4,16.2,16.9,17.8,18.7,19.6,20.5,21.5,22.6,23.7,24.9,26.1,27.4,28.7,30.1,31.6,33.2,34.8,36.5,38.3,40.2,42.2,44.2,46.4,48.7,51.1,53.6,56.2,59.0,61.9,64.9,68.1,71.5,75.0,78.7,82.5,86.6,90.9,95.3])

		R_num = st.selectbox('抵抗の数',[1,2,3])
		st.write(f'Selected: {R_num}')

		R_ratio_array = np.arange(R_num)

		if st.checkbox('Choise R Proportion'):
			for i in range(R_num):
				R_ratio_array[i] = st.slider('R'+str(i+1)+' [%]', 0, 100, 0, 1)

		Optional_Setting = st.selectbox('Optional Setting?',['No','Yes'])
		if Optional_Setting == 'Yes':
			R_order_min = st.selectbox('from 10^(x) [Ω]',[-1,-2,-3])
			R_order_max = st.selectbox('until 10^(x) [Ω]',[1,2,3,4,5])
			More_Setting = st.selectbox('More Setting?',['No','Yes'])
			if More_Setting == 'Yes':
				dif_Objective_R = st.slider('dif_Objective_R', 0.0, 1.0, 0.0, 0.0001)
				error_thres = st.slider('error_thres', 0.0, 1.0, 0.0, 0.000001)
		else:
			R_order_min = -2
			R_order_max = 4
			dif_Objective_R = 0.01
			error_thres = 0.001


		R_range = np.arange(2)
		R_ratio_array = sorted(R_ratio_array, reverse=True)
		num_R = len(R_ratio_array)
		R_ratio_array_normalize = R_ratio_array/sum(R_ratio_array)

		answer_R = np.arange(num_R)
		error_array = np.array(num_R)
		error_value = 10000
		R_range_min = float(Objective_R) * float(1 - dif_Objective_R)
		R_range_max = float(Objective_R) * float(1 + dif_Objective_R)
		E_array_append = []
		answer_R_para = []

		#違うオーダー同士で直列組めるようにしたい
		for i in range(R_order_min,R_order_max):
		    E_array_append = np.append(E_array_append,E_array*pow(10,i))
		    Calculate_R = list(itertools.combinations_with_replacement(E_array_append, num_R))
		    cmb_num = len(Calculate_R)
		    df = pd.DataFrame(Calculate_R)
		    df_T = 1/df
		    df_new = df_T.assign(Sum_R = df_T.sum(axis=1))
		    df_new_T = 1/df_new
		    tmp_array = df_new_T.loc[:,"Sum_R"]
		    for j in range(len(tmp_array)):
		        if tmp_array[j] >= R_range_min and tmp_array[j] <= R_range_max:
		            #print(tmp_array[j])
		            tmp = df.iloc[j]/np.linalg.norm(df.iloc[j],ord=2)
		            tmp = sorted(tmp, reverse=True)
		            error_array = abs((tmp - R_ratio_array_normalize)) / np.linalg.norm(R_ratio_array_normalize,ord=2)
		            if error_value > sum(error_array):
		                error_value = sum(error_array)
		                answer_R = df.iloc[j]
		                answer_R_para = tmp_array[j]

		st.write('<span style="color:red">Check cal Combined_R</span> : ' + str(answer_R_para) + ' [Ω]', unsafe_allow_html=True)
		for i in range(len(answer_R)):
			st.write('R' + str(i+1) + '：' + str(answer_R[i])+ ' [Ω] ' + str(round(answer_R[i]/sum(answer_R)*100,1))+' [%]')
			#st.write(f'{i/sum(i)*100}')

if __name__=='__main__':
	main()
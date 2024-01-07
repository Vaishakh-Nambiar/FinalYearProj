# FinalYearProject 💐💐🌻
 
Google drive : https://drive.google.com/drive/folders/1HydWnhc03M59UdBc88fNNnP-KGH4oqGo?usp=drive_link

- BackendFile: DataTrans.py
- Mattry.py - configured tha above code based on parameters like materials used and 'good' or 'Bad' classification and added te functionality of putting it into my google drive 
- Mattry2.py - configured tha above code based on parameters like materials used only and has a datasheet that has values of both 'good' and 'bad'


- vaishakh-nambiar@finalyearop.iam.gserviceaccount.com

- https://drive.google.com/drive/folders/1HydWnhc03M59UdBc88fNNnP-KGH4oqGo?usp=sharing




- DataShow.py - The code for data that we are making 
- Sensor_get.py - The code that we'll show 
![Alt text](image.png) - install these 



<!-- I need a help
this is my syntehtic data:
# Load the dataset
data = {
    'Temperature': [26.84, 30.19, 29.48, 31.76, 25.93, 27.45, 31.92, 31.71, 31.83, 29.37, 28.07, 26.27, 26.96, 28.39, 31.53],
    'Vibration_X': [-2.68, -23.72, 1.24, -13.17, -13.71, -2.78, -7.38, -0.67, -11.12, -11.81, -18.92, -22.18, -11.35, -0.69, 3.73],
    'Vibration_Y': [23.09, 23.3, 19.01, 21.69, 21.47, 27.26, 24.9, 5.46, 32.04, 19.66, 29.78, 14.3, 14.83, 17.6, 12.25],
    'Vibration_Z': [-1014.33, -1011.56, -1012.23, -1018.05, -1016.73, -1025.36, -1024.68, -1018.47, -1016.76, -1028.73, -1026.08, -1020.9, -1019.04, -1021.89, -1021.73]
}

df = pd.DataFrame(data)


Scenario:
Say two excel sheets, A and B
A has data of 10 days with 1200 records, that ll be used for training, and B has the actual value for the 11th day
My regression models predict values for the 11th day based on the patterns it learned from the data of 10 days that is from data of sheet A
And sheet B is used to find the correctness of the data


Give me the codes that help me load this dataset 
data from A in the 'data' part of my code which I gave 
And data from B in place holder of : actual_vibration_11th_day = np.array([[-2.51,5,-1021]])
Replcae the np.array part and add all the data from sheet B into this such as the regression model runs and gives me the correct values -->

<!-- Linear Regression - Actual Vibration on the 11th day: 
 [[    1.69    12.06 -1028.63]
 [   -7.66    14.37 -1028.32]
 [   -1.13    10.25 -1028.11]
 ...
 [   -1.66     6.28 -1028.14]
 [   -1.98     9.66 -1022.77]
 [   -1.86    34.75 -1019.18]]
Linear Regression - Predicted Vibration on the 11th day: 
 [   -2.68    23.09 -1014.33]
Linear Regression - Vibration Error for the 11th day: 
 [[ 4.37 11.03 14.3 ]
 [ 4.98  8.72 13.99]
 [ 1.55 12.84 13.78]
 ...
 [ 1.02 16.81 13.81]
 [ 0.7  13.43  8.44]
 [ 0.82 11.66  4.85]]
Linear Regression - Mean Vibration Error for the 11th day: 
 [9.24011667 7.68758333 6.85400833]

Linear Regression - Actual Temperature on the 11th day: 
 0       26.45
1       31.60
2       28.22
3       30.94
4       27.73
        ...  
1195    30.33
1196    26.44
1197    25.97
1198    25.68
1199    28.17
Name: Temperature, Length: 1200, dtype: float64
Linear Regression - Predicted Temperature on the 11th day: 
 29.10503617452745
Linear Regression - Temperature Error for the 11th day: 
 0       2.655036
1       2.494964
2       0.885036
3       1.834964
4       1.375036
          ...   
1195    1.224964
1196    2.665036
1197    3.135036
1198    3.425036
1199    0.935036
Name: Temperature, Length: 1200, dtype: float64
Linear Regression - Mean Temperature Error for the 11th day: 
 2.021884720023553
------------------------------
RFG - Actual Vibration on the 11th day: 
 [[    1.69    12.06 -1028.63]
 [   -7.66    14.37 -1028.32]
 [   -1.13    10.25 -1028.11]
 ...
 [   -1.66     6.28 -1028.14]
 [   -1.98     9.66 -1022.77]
 [   -1.86    34.75 -1019.18]]
RFG - Predicted Vibration on the 11th day: 
 [  -23.2189    26.5809 -1028.2292]
RFG - Vibration Error for the 11th day: 
 [[24.9089 14.5209  0.4008]
 [15.5589 12.2109  0.0908]
 [22.0889 16.3309  0.1192]
 ...
 [21.5589 20.3009  0.0892]
 [21.2389 16.9209  5.4592]
 [21.3589  8.1691  9.0492]]
RFG - Mean Vibration Error for the 11th day: 
 [13.3686135   8.8921155   7.78050433]

RFG - Actual Temperature on the 11th day: 
 0       26.45
1       31.60
2       28.22
3       30.94
4       27.73
        ...  
1195    30.33
1196    26.44
1197    25.97
1198    25.68
1199    28.17
Name: Temperature, Length: 1200, dtype: float64
RFG - Predicted Temperature on the 11th day: 
 27.265000000000022
RFG - Temperature Error for the 11th day: 
 0       0.815
1       4.335
2       0.955
3       3.675
4       0.465
        ...  
1195    3.065
1196    0.825
1197    1.295
1198    1.585
1199    0.905
Name: Temperature, Length: 1200, dtype: float64
RFG - Mean Temperature Error for the 11th day: 
 2.385916666666657

-----------------------------------------------------------

XGBoost - Actual Vibration on the 11th day: 
 [[    1.69    12.06 -1028.63]
 [   -7.66    14.37 -1028.32]
 [   -1.13    10.25 -1028.11]
 ...
 [   -1.66     6.28 -1028.14]
 [   -1.98     9.66 -1022.77]
 [   -1.86    34.75 -1019.18]]
XGBoost - Predicted Vibration on the 11th day: 
 [  -23.348892    26.688473 -1028.9445  ]
XGBoost - Vibration Error for the 11th day: 
 [[25.03889221 14.62847275  0.31445801]
 [15.68889221 12.31847275  0.62445801]
 [22.21889221 16.43847275  0.83445801]
 ...
 [21.68889221 20.40847275  0.80445801]
 [21.36889221 17.02847275  6.17445801]
 [21.48889221  8.06152725  9.76445801]]
XGBoost - Mean Vibration Error for the 11th day: 
 [13.48397704  8.94195395  8.37799805]

XGBoost - Actual Temperature on the 11th day: 
 0       26.45
1       31.60
2       28.22
3       30.94
4       27.73
        ...  
1195    30.33
1196    26.44
1197    25.97
1198    25.68
1199    28.17
Name: Temperature, Length: 1200, dtype: float64
XGBoost - Predicted Temperature on the 11th day: 
 26.011068
XGBoost - Temperature Error for the 11th day: 
 0       0.438932
1       5.588932
2       2.208932
3       4.928932
4       1.718932
          ...   
1195    4.318932
1196    0.428932
1197    0.041068
1198    0.331068
1199    2.158932
Name: Temperature, Length: 1200, dtype: float64
XGBoost - Mean Temperature Error for the 11th day: 
 3.1143373449961342

---------------------------------------------------------

Now take all the outputs I gave above and make a detailed report.
Give a Comparison of the models 
And make the report as of 'Result and Analysis' part of a report

Give it to me in detailed paragraphs and not points -->
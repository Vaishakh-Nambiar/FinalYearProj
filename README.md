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
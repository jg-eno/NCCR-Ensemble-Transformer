import xarray as xr
import numpy as np

start_year,end_year = 1990,2022
time_slices = 2
Temp_T = xr.open_dataset(f'{start_year}.nc')
Temp_T = Temp_T['t2m'].loc[f"{start_year}-12-01":f"{start_year}-12-31"] 
Temp_T = Temp_T.to_numpy()

for x in range(start_year+1,end_year+1):
    f = xr.open_dataset(f"{x}.nc")
    f = f['t2m'].loc[f"{x}-12-01":f"{x}-12-31"]
    Temp_T = Temp_T + f.to_numpy()
Temp_T = Temp_T / (end_year - start_year + 2)

Temp_T = xr.DataArray(Temp_T)
Temp_T = Temp_T.rename(dim_0='time',dim_1='latitude',dim_2='longitude')

Climatology_T = Temp_T.sel(time=slice(0,time_slices))
Climatology_T = Climatology_T.sum(dim="time")
Climatology_T = Climatology_T/time_slices

for x in range(2,31*time_slices,time_slices):
    Var_T = Temp_T.sel(time=slice(x,x+time_slices))
    Var_T = Var_T.sum(dim='time')
    Var_T = Var_T/time_slices
    Climatology_T = xr.concat([Climatology_T,Var_T],dim='time')

#Input File
d_2023 = xr.open_dataset('Prediction.nc')

T_current_min = d_2023.sel(time=slice("2023-12-03T00:00:00.000000000","2023-12-03T12:00:00.000000000"))
T_current_min = T_current_min.min(dim="time")

Obs = xr.open_dataset('2023.nc')
T_Obs = Obs.sel(time=slice("2023-12-03T00:00:00.000000000","2023-12-03T12:00:00.000000000"))
T_Obs = T_Obs.min(dim='time')

for y in range(4,32):
    Vari_T = d_2023.sel(time=slice(f"2023-12-{y}T00:00:00.000000000",f"2023-12-{y}T12:00:00.000000000"))
    T_current_min = xr.concat([T_current_min,Vari_T.min(dim='time')],dim='time')
    V = Obs.sel(time=slice(f"2023-12-{y}T00:00:00.000000000",f"2023-12-{y}T12:00:00.000000000"))
    T_Obs = xr.concat([T_Obs,V.min(dim='time')],dim='time')

#Now we have Climatology_T, Current_Min_T,Current_Mean_T
#Slicing it for Delhi
Climatology_T = Climatology_T.sel(longitude=slice(41,62),latitude=slice(31,52,1))
Climatology_T = Climatology_T.sel(time=slice(2,31))

T_Obs = T_Obs.sel(latitude=28.75,longitude=77.75)
T_Obs = T_Obs - 273.15

'''
lat = 0
count = 0
for a in data['latitude']:
    lon = 0
    for b in data['longitude']:
        for z in range(0,29):
            if(data.sel(latitude=a,longitude=b,time=z) < Climatology_T.sel(latitude=lat,longitude=lon,time=z) and 
               data.sel(latitude=a,longitude=b,time=z+1) < Climatology_T.sel(latitude=lat,longitude=lon,time=z+1) and 
               data.sel(latitude=a,longitude=b,time=z+2) < Climatology_T.sel(latitude=lat,longitude=lon,time=z+2)):
                print(f"2023-12-{z} to 2023-12-{z+2} on Latitude : {a.item()} Longitude : {b.item()} Current Temperature : {data.sel(latitude=a,longitude=b,time=z).item() - 273.15} Climatology Temperture : {Climatology_T.sel(latitude=lat,longitude=lon,time=z).item() - 273.15}")'''   


import matplotlib.pyplot as plt
Climatology_T = Climatology_T - 273.15
'''T_current_mean = T_current_mean.sel(time=slice(0,29))'''
Mean = T_current_min.sel(latitude=28.875,longitude=77.75)['mean'].sum(dim='time').item() / 29
T_current_min = T_current_min.sel(time=slice(0,29))
time_axis = []
for x in range(3,32):
    time_axis.append(x)
T_current_min = T_current_min.fillna(Mean)
print(T_current_min.sel(latitude=28.875,longitude=77.75)['mean'])
print("Cold Waves Detected : ")
plt.plot(time_axis, Climatology_T.sel(latitude=10,longitude=10),color='r',label = 'Climatology',linestyle='solid')
plt.plot(time_axis, T_current_min.sel(latitude=28.875,longitude=77.75)['mean'],color = 'g',label='Predicted_Min',linestyle='solid')
plt.plot(time_axis,T_Obs['t2m'],color='b',label='Observation',linestyle='solid')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.legend()
plt.show()

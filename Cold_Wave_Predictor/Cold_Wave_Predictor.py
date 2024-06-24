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
d_2023 = xr.open_dataset('2023.nc')
d_2023 = d_2023['t2m'].loc["2023-12-01":"2023-12-31"]

T_current_mean = d_2023.sel(time=slice("2023-12-01","2023-12-01"))
T_current_mean = T_current_mean.sum(dim="time")
T_current_mean = T_current_mean/time_slices

T_current_min = d_2023.sel(time=slice("2023-12-01","2023-12-31"))
T_current_min = T_current_min.min(dim="time")

for y in range(2,31*time_slices,time_slices):
    Vari_T = d_2023.sel(time=slice(f"2023-12-{int(y/2)}",f"2023-12-{int(y/2)}"))
    T_current_min = xr.concat([T_current_min,Vari_T.min(dim='time')],dim='time')
    Vari_T = Vari_T.sum(dim='time')
    Vari_T = Vari_T/time_slices
    T_current_mean = xr.concat([T_current_mean,Vari_T],dim='time')

#Now we have Climatology_T, Current_Min_T,Current_Mean_T
#Slicing it for Delhi
T_current_mean = T_current_mean.sel(longitude=slice(75.25,80.25),latitude=slice(31.25,26.25,1))
T_current_min = T_current_min.sel(longitude=slice(75.25,80.25),latitude=slice(31.25,26.25,1))
Climatology_T = Climatology_T.sel(longitude=slice(41,62),latitude=slice(31,52,1))


#Threshold = (-4.5 + 273.15) * 3 
#We can change the data of Current Temperature : Min or Mean
#Threshold - Current Temperature
'''Threshold = (-4.5 + 273.15) * 3 #Three Days Average
data = T_current_mean
for x in range(0,29):
    Agg = data.sel(time=[x,x+1,x+2]).sum(dim='time')
    Agg = Agg < Threshold
    print(f'Places experiencing cold waves during 2023-12-{x+1} to 2023-12-{x+3}')
    for y in Agg['latitude']:
        for z in Agg['longitude']:
            if(Agg.sel(latitude=y,longitude=z) == True):
                print(f'Latitude : {y.item()} Longitude : {z.item()}')'''

#Climatology - Current Temperature
data = T_current_mean
print(len(data['latitude']))
for x in range(0,29):
    Agg = data.sel(time=[x,x+1,x+2]).sum(dim='time')
    Clim_Agg = Climatology_T.sel(time=[x,x+1,x+2]).sum(dim='time')
    print(f'Places experiencing cold waves during 2023-12-{x+1} to 2023-12-{x+3}')
    lat = 0
    for y in Agg['latitude']:
        lon = 0
        for z in Agg['longitude']:
            if(Agg.sel(latitude=y,longitude=z) < Clim_Agg.sel(latitude=lat,longitude=lon)):
                print(f'Latitude : {y.item()} Longitude : {z.item()}')
            lon += 1            
        lat += 1


    

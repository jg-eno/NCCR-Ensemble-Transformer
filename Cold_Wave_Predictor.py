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
Temp_T = Temp_T.rename(dim_0='time',dim_1='lat',dim_2='lon')

Climatology_T = Temp_T.sel(time=slice(0,time_slices))
Climatology_T = Climatology_T.sum(dim="time")
Climatology_T = Climatology_T/time_slices

for x in range(2,31*time_slices,time_slices):
    Var_T = Temp_T.sel(time=slice(x,x+time_slices))
    Var_T = Var_T.sum(dim='time')
    Var_T = Var_T/time_slices
    Climatology_T = xr.concat([Climatology_T,Var_T],dim='time')

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

#Mean-Climatology Method:
Truth_Map = np.full((31,125,121),False,dtype=bool)
Threshold_Temp = -4
for i in range(T_current_mean.sizes['time']):
    for j in range(T_current_mean.sizes['latitude']):
        for k in range(T_current_mean.sizes['longitude']):
            tc = T_current_mean.isel(time=i,latitude=j,longitude=k)
            clim_t = Climatology_T.isel(time=i,latitude=j,longitude=k)
            if(tc-clim_t <= Threshold_Temp):
                Truth_Map[i][j][k] = True

print(Truth_Map)


    

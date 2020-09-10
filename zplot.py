"""
Using astroplan and astropy for observation planning


"""
#from astropy.coordinates import EarthLocation

from astroplan import Observer, FixedTarget
from astropy.time import Time
from astropy import units as u
import numpy as np
from astroplan.plots import plot_airmass
import matplotlib.pyplot as plt


star_name = 'DQ Her'
star_name2 = 'V392 Per'
site = 'Roque de los Muchachos'

obs = Observer.at_site(site)
star = FixedTarget.from_name(star_name)
star2 = FixedTarget.from_name(star_name2)

now = Time.now()

if obs.target_is_up(now,star):
    print(f"{star_name:s} is up at {now}")

# Sunrise and Sunset
horizon = 2.5*u.degree
sunset_tonight = obs.sun_set_time(now, which='nearest',horizon=-2.5*u.degree)
sunrise_tomorrow = obs.sun_rise_time(now,which='next',horizon=-2.5*u.degree)
print("Sunset",sunset_tonight.iso)
print("Sunrise",sunrise_tomorrow.iso)
night_length = sunrise_tomorrow - sunset_tonight
night_length_h = night_length.sec/3600
print(f"Length of night {night_length_h:.2f} hours")

# Object rise / set

star_rise = obs.target_rise_time(now,star)
star_set = obs.target_set_time(now,star)
print(star_name,"rise time",star_rise.iso)
print(star_name,"set  time",star_set.iso)

# Observation window
start = np.max([sunset_tonight,star_rise])
end = np.min([sunrise_tomorrow,star_set])
print(star_name,"obs_start",start.iso)
print(star_name,"obs_end  ",end.iso)

# Make Plot of airmass vs time.
fig, ax = plt.subplots()

# Time array for sunset to sunrise
times = sunset_tonight + np.linspace(0,night_length_h,100)*u.hour
etwil = sunset_tonight + 0.5*u.hour*np.ones(2)
mtwil = sunrise_tomorrow - 0.5*u.hour*np.ones(2)

plot_airmass(star,obs,times,ax=ax,max_airmass=2.5)
plot_airmass(star2,obs,times,ax=ax,max_airmass=2.5)
plt.legend(shadow=True)

ax.plot_date(etwil.plot_date,[1.0,2.5],'red',alpha=0.5) # sunset plus 1/2 hour
ax.plot_date(mtwil.plot_date,[1.0,2.5],'red',alpha=0.5)
plt.show()

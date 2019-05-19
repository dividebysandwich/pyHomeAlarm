# pyHomeAlarm

This is an extremely simple home alarm system that can easily be integrated with Domoticz, Hubitat, Homey, or any other system that is able to send HTTP requests. 
It's a two-zone alarm system with persistent state. The intended use is on a raspi pi or similar single board computer, and allows you to do things like switching GPIOs, play back sounds, and other things. My main usecase here is really to initiate playback of sounds inside the house, as I'm a firm believer in that my alarm system needs to wake me up, not my neighbors.

This code comes with no claim to be fit for any particular purpose. I simply found that if you want to do a home alarm system, this is basically what 99% of folks need. I wanted to do this in python simply because I'm sick of redoing the alarm logic everytime I have to switch to another home automation system. This way you just configure the http operations and all the details about how to make multiple speakers in the house do exactly what you want remain untouched.
Also this is a stateful system so it'll come up after a restart exactly the way it was shut down, which is another feature I found not every home automation system has.


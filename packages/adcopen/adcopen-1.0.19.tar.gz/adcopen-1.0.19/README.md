## ADCOpen
### Open-source python libraries for data integration with ADC equipment.

Licensed for use with ADC equipment. 
automateddesign.com

#1.0.19
- Adds ONDATACHANGE support to events.py, which is now the default. Option to
always receive the event can be passed as argument to subscribe method.

#1.0.18
- API change to Ton.start() to make it easier to use in state machines.


#1.0.17
- Add Ton and edge trigger classes.


#1.0.16
- Convert to socketio


#1.0.15
- Trying to fix bug where pressing ctrl-c causes hard crash instead of graceful shutdown.



#1.0.13:
- Fix issue with traceback library swallowing ctrl-c events when program interrupted by keyboard
- Add minimal CoreLink client for integration with autocore-js webserver. 
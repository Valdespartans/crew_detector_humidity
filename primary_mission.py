from sense_hat import SenseHat
import time
import datetime
sense = SenseHat()
 
p = [0, 0, 0] # blank
w = [255, 255, 255] # white
b = [0, 0, 200] # blue
r = [255,0,0] # red
g = [0, 255, 0] # green
o = [255,127,0] # orange
v = [159,0,255] # purple

bg_nobody = [225,100,10]#orange
bg_crew = [25,70,200]#blue
 

#log file
data = open('log.csv','w')
data.write("Time\tHumidity\n")


initial_date = datetime.datetime.now()
final_date = initial_date + datetime.timedelta(seconds=600)
humidity_vector = [] # list storing humidity values

# During the next 10 minutes, store humidity data every 2~3 sec to calculate avg, min and max values 
while datetime.datetime.now() < final_date:
  	h = sense.get_humidity()

  	h = round(h, 1)
  	humidity_vector.append(h)
  	current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
  	data.write(current_time + "\t" + str(h) + "\n")
  	
  	msg = "H = {0}".format(h)
	sense.show_message(msg, scroll_speed=0.05, back_colour=bg_nobody)

# Calculate avg, min and max values
avg_h = sum(humidity_vector)/len(humidity_vector)
min_h = min(humidity_vector)
max_h = max(humidity_vector)

print "Avg. {0} , Min {1},  Max{2}".format(avg_h,min_h,max_h)

# set threshold
threshold = avg_h + 3.0
only_hour=False #use this boolean to detect if the astronaut is still there and, in that case, only the hour is displayed

initial_date = datetime.datetime.now()
final_date = initial_date + datetime.timedelta(seconds=3000)

# During the next 50 minutes, detect if an astronaut enters into the room. If the astronaut enters for the first time or leaves the room and reenters after a while , it displays a face and a message. While the astronaut is working, only displays the hour.
while datetime.datetime.now() < final_date:
  	h = sense.get_humidity()

  	h = round(h, 1)
  	current_time = datetime.datetime.now()
  	log_time = current_time.strftime('%d/%m/%Y %H:%M:%S')
  	screen_time = current_time.strftime('%H:%M:%S')
  	data.write(log_time + "\t" + str(h) + "\n")
  	print h
  	
  	if h > threshold:
		# the astronaut was not in the room before
                if only_hour == False:
			image_crew= [
                    	p,p,p,v,v,p,p,p,
                    	p,p,v,v,v,v,p,p,
                    	p,p,b,b,b,b,p,p,
                    	p,b,o,o,o,o,b,p,
                    	b,o,g,o,o,g,o,b,
                    	p,o,o,o,o,o,o,p,
                    	p,o,o,r,r,o,o,p,
                    	p,p,o,o,o,o,p,p
                    	]

        		sense.set_pixels(image_crew) 
			time.sleep (2)
        		msg = "Are you having a 'spacial' day?"
        		sense.show_message(msg, scroll_speed=0.05, back_colour=bg_crew) 
			time.sleep (2)
			msg = "{0}".format(screen_time)
        		sense.show_message(msg, scroll_speed=0.05, back_colour=bg_crew)
			only_hour = True
		# the astronaut is in the room and has already been detected
		else:
		 	msg = "{0}".format(screen_time)
        		sense.show_message(msg, scroll_speed=0.05, back_colour=bg_crew)   	
        	  	
  	else:
		# the astronaut is not in the room
		image_esa = [
  		p,p,b,b,b,b,p,p,
  		p,b,b,b,b,b,b,p,
  		b,b,b,b,w,w,w,b,
  		b,w,b,b,w,b,w,b,
  		b,b,b,b,w,w,w,b,
  		b,b,b,b,w,b,b,b,
  		p,b,b,b,b,w,w,p,
  		p,p,b,b,b,b,p,p,
  		]
   
		sense.set_pixels(image_esa)
		only_hour = False
	# next measure in two seconds
	time.sleep(2)		
data.close()


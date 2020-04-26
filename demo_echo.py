from time import sleep
from pixel_ring import pixel_ring

sleep_time=5

print("starting...")
pixel_ring.set_brightness(10)
pixel_ring.change_pattern('echo')
pixel_ring.wakeup()
sleep(sleep_time)


print("listening")
pixel_ring.listen()
sleep(sleep_time)

print("thinking")
pixel_ring.think()
sleep(sleep_time)

print("speaking")
pixel_ring.speak()
sleep(sleep_time)

pixel_ring.off()
print("done.")

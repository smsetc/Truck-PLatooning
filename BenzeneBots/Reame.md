docker run -p 500<truck_id>:5000 -d --name=truck<truck_id> --net=mynet --ip=192.168.50.1<truck_id> truck <truck_id>

add trucks 


Truck 7
docker run -p 5007:5000 -d --name=truck7 --net=mynet --ip=192.168.50.17 truck 7

Truck 11
docker run -p 50011:5000 -d --name=truck11 --net=mynet --ip=192.168.50.111 truck 11

##################

Remove trucks: Program files ->> Mosquitto

.\mosquitto_pub.exe -t "unregister" -m "<Truckid>"

.\mosquitto_pub.exe -t "unregister" -m "11"

#########################
.\mosquitto_pub.exe -t "<truckid>/set/speedoracceleration" -m "value"

.\mosquitto_pub.exe -t "5/set/speed" -m "30"

############################

feedback(watchdog) and commandline monitoring

python .\truck.py <truckid>

python .\truck.py 5




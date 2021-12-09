# Chat-App
Multi client chat application using TCP Socket:
Implemented 2 way communication between client and server through a TCP socket, whereby 
- server remains on 24 X 7
- Client is able to reconnect at any time
- Connection teardown is clean without leaving any loose ends and scope of error in program further ahead

Multiple threads are used to cater to different clinets, enabling
- Clients to send messages to selective clients using predefined syntax
- Broadcast, Unicast as well as multicast.

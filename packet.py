import random

class Packet:
	version: ""			#(4 bits) version of IP currently used
	ihl: "" 			#(4 bits) indicates how many 32-bit words are in the IP header
	type_of_service: "" #(8 bits) specifies how a particular upper-layer protocol would like the current datagram to be handled. Datagrams can be assigned various levels of importance through this field
	total_length: ""	#(16 bits) specifies the length of the entire IP packet including data and header in bytes
	identification: ""  #(16 bits) contains an integer that identifies the current datagram. This field is used to help reconstruct datagram fragments
	ip_flags: ""		#(4 bits) controls whether routers are allowed fragment a packet and indicates the parts of a packet to the receiver.
	fragment_offset: ""  #(12 bits) 
	time_to_live: "" 	#(8 bits) maintains a counter that gradually decrements to zero, at which point the datagram is discarded.
	protocol: ""		#(8 bits) indicates which upper-layer protocol receives incoming packets after IP processing is complete.
	header_checksum: "" #(16 bits) helps ensure IP header integrity.
	src_addr: ""		#(32 bits) specifies the sending node.
	dst_addr: ""		#(32 bits) specifies the receiving node.
	ip_options: ""		#(24 bits) allows IP to support various options, such as security.
	padding: ""			#(8 bits)

	src_port: ""		#(16 bits) identifies the sending end-point of the connection
	dst_port: ""		#(16 bits) identifies the receiving end-point of the connection
	seq_num: ""			#(32 bits) specifies the number assigned to the first byte of data in the current message.
	ack_num: ""			#(32 bits) contains the value of the next sequence number that the sender of the segment is expecting to receive, if the ACK control bit is set.
	header_length: ""   #(variable length) tells how many 32-bit words are contained in the TCP header. This information is needed because the Options field has variable length, so the header length is variable too.
	reserved: "" 		#(6 bits) must be zero. This is for future use.
	tcp_flags: ""		#(6 bits) contains the various flags:
							#URG—Indicates that some urgent data has been placed.
							#ACK—Indicates that acknowledgement number is valid.
							#PSH—Indicates that data should be passed to the application as soon as possible.
							#RST—Resets the connection.
							#SYN—Synchronizes sequence numbers to initiate a connection.
							#FIN—Means that the sender of the flag has finished sending data.
	window: ""			#(16 bits) specifies the size of the sender's receive window (that is, buffer space available for incoming data).
	tcp_checksum: "" 	#(16 bits) indicates whether the header was damaged in transit.
	urgent_pointer: ""  #(16 bits) points to the first urgent data byte in the packet.
	tcp_options: "" 	#(variable length) specifies various TCP options.
	data: ""			#(variable length) payload
	MAC: ""

	def __init__(self, src_addr, MAC):
		self.version = "0110" # 6 for IPv6
		self.ihl = "0000"
		self.type_of_service = "00000000"
		self.total_length = "0000000000000000"
		self.identification = "0000000000000000"
		self.ip_flags = "0000"
		self.fragment_offset = "000000000000"
		self.time_to_live = "00001000"
		self.protocol =  "00000110" #protocol = 6 for TCP, 17 for UDP
		self.header_checksum = "0000000000000000"
        self.src_addr = src_addr
		self.dst_addr = "00000000000000000000000000000000"
		self.ip_options = "000000000000000000000000"
		self.padding = "00000000"
		self.src_port = "0000000000000001"
		self.dst_port = "0000000000000000"
		self.seq_num = "00000000000000000000000000000000"
		self.ack_num = "00000000000000000000000010000000"
		self.header_length = "0101"
		self.tcp_flags = "000010"
		self.window = "0000000000000000"
		self.tcp_checksum = "0000000000000000"
		self.urgent_pointer = "0000000000000000"
		self.data = data
		self.MAC = MAC

	def returnString(self):
		packet = self.version+self.ihl+self.type_of_service+self.total_length+self.identification
		packet = packet+self.ip_flags+self.fragment_offset+self.time_to_live+self.protocol
		packet = packet+self.header_checksum+self.src_addr+self.dst_addr+self.ip_options+self.padding
		packet = packet+self.src_port+self.dst_port+self.seq_num+self.ack_num+self.header_length
		packet = packet+self.tcp_flags+self.window+self.tcp_checksum+self.urgent_pointer+self.data+self.MAC
		return packet


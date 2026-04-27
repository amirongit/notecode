# Computer Networking, A Top Down Approach
## Computer Networks & The Internet

communication link: made of physical media, used for data transmission.<br>
packet: piece of data paired with header bytes.

steps to transmit data between two end systems
1. sender segments it into packets
2. packets are sent through communication links
3. reciever reassmbles packets back into original data

packet switch: device with incoming & outgoing communication links which is used to forward packets toward their destination (namely routers & link layer switches).<br>
route (aka path): sequence of communication links & packet switches traversed by packets between two end systems.<br>
internet service provider (ISP): network of communication links & switches which allows end systems to access the internet; must be interconnected to other ISPs.

lower tier ISPs interconnect through higher tier ones which themselves interconnect directly.

protocol: defines order & format of messages exchanged between communicating components & actions taken upon data transmission or other events.<br>
host: end system which hosts applications which is either client or server.

software & hardware centered standards are developed & maintained by the internet engineering task force (IETF) & institute of electrical & electronics engineers (IEEE) respectively.<br>
the internet can be thought of as an infrastructure for applications which is exposed through socket interfaces by operating systems; this interface allows applications to send & recieve data to & from different applications & instances.

access network: network which physically connects end systems to the first router on their desired paths (aka edge router) toward another end system.<br>
digital subscriber line (DSL): method to provide internet access on telephone lines.<br>
DSL modem: device used to convert digital to analog data & encode it in different frequencies.<br>
DSL access multiplexer (DSLAM): device used to separate network from traditional telephone data & convert it back to digital data (used by ISPs).<br>
splitter: device used to separate network from traditional telephone data & forward it to DSL modems (used by customers).

telephone companies can act as ISPs which are access networks for residential houses having telephone lines.<br>
using DSL, telephone lines are splitted into three channels
1. highe speed downstream
2. medium speed upstream
3. traditional two way for telephone usage

this allows using the same telephone line to transmit analog & digital data at the same time.

bits are usually passed around by several pairs of physical senders & recievers through one route.<br>
each pair shares a common physical medium which is either
- guided: transmits data to one specific destination, usually solid
- unguided: broadcasts data in all directions

store & forward: transmission method used by packet switches in which the entire packet is buffered before its transmission begins.<br>
output buffer: queue within packet switches which exist per outgoing communication link & used to put packets in order of arrival.<br>

packet losses may happen when new packets arrive & their destined output buffer is full.

forwarding table: map within routers which associates addresses (or parts of them) to outgoing communication links.<br>
circuit switched network: network in which resources are reserved per communication session.

in packet switched networks, resources are used on demand in contrast to circuit switched networks.<br>
chunks of data may have to wait in queues within packet switched networks but this is not the case in circuit switched networks.

frequency: amount of repetition of waves within physical medium.<br>
frequency spectrum: possible frequencies of physical medium.<br>
bandwidth: quantified value of frequency spectrum.

two major methods to establish circuits are
1. frequency division multiplexing (FDM): frequency spectrum of links are divided by established connections
2. time division multiplexing (TDM): time is splitted into frames of duration which themselves are splitted into slots per established connections

point of presence (PoP): set of routers within provider ISPs which allow communication to high tier ISPs.<br>
internet exchange point (IXP): meeting point where multiple ISPs peer (connection without payment) together.

internet can be considered a network of networks which allows end systems communicate with each other.<br>
access ISPs use regional ISPs which themselves use tier-1 ISPs to interconnect & gain coverage.

multi homing: when ISPs use multiple higher tier ISPs in order to guard themselves from failures.

throughput: amount of transferable data within given periods.<br>
prcessing delay: time it takes packet switches to examin & process arriving packets.<br>
transmission rate
- amount transmitted data per given unit of time between two nodes
- usually calculated as `d/t` where `d` & `t` are amount of data & time respectively

transmission delay
- time it takes to push all bits of given packets into the physical medium
- calculated as `L/R` where `L` & `R` are length of packets & transmission rate of the communication link respectively

propagation delay
- time it takes for one bit to travel the distance of given communication links
- calculated as `d/s` where `d` & `s` are distance & propagation speed of given physical media respectively

queuing delay: time it takes for packets to wait in output buffers within packet switches.<br>
throughput
- amount of transmitted data within given amount of time between two end systems
- usually limited by the least transmission rate (because of either high traffic or capacity of physical media) within give paths

layered architecture allows changing implementations without side effects by enforcing service specifications.<br>
within computer networks, layers provide services to their upper layers & only depends on services provided by the layer below themselves.

<!-- 49, protocol layering -->

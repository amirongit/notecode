# Computer Networking, A Top Down Approach
## Computer Networks & The Internet
### What Is The Internet?
#### A Nuts & Bolts Description

the internet is a computer networks which connects billions of devices throughout the world. considering the fact that a good percentage of these devices aren't traditional computers, the term "computer network" is somewhat inaccurate.

communication links within computer networks are made of physical media & their transmission rate is measured in bits per second.

upon sending data, end systems segment it & add header bytes to each segment. segments & their header byte together are called packets. packets are used to reassmble the original data in the destination.

packet switches take packets from their incoming communication links & forward them to outgoing ones. routers & link layer switches are two kinds of packets switches which forward incoming packets toward their destination.

the sequence of communication links & packet switches traversed by packets between two end systems is called path or route.

internet service providers (ISP) allow end systems to access the internet & are networks of packet switches & communication links in themselves. they provide internet access to end users & content providers (servers) & must also be interconnected. lower tier ISPs interconnect through higher tier ISPs which themselves interconnect directly.

components of computer networks run standard protocols in order to manage their communications. software & hardware centered standards are developed & maintained by the internet engineering task force (IETF) & institute of electrical & electronics engineers (IEEE) respectively.

#### A Service Description

the internet acts as an infrastructure for distributed applications (applications which involve multiple end systems). this infrastructure is exposed to applications through socket interface by operating systems which allows applications to send & recieve data to & from different destinations.

#### What Is A Protocol?

communications within networks are governed by protocols which should be conformed by engaged components.

protocols define order & format of messages exchanged between communicating components & actions taken upon data transmission or other events.

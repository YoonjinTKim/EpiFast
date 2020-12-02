# EpiFast
Algorithm 1 in EpiFast: A fast algorithm for large scale realistic epidemic simulations on distributed memory systems in python2 using networkx

Bisset, Keith & Chen, Jiangzhuo & Feng, Xizhou & Kumar, Sritesh & Marathe, Madhav. (2009). EpiFast: A fast algorithm for large scale realistic epidemic simulations on distributed memory systems. Proceedings of the International Conference on Supercomputing. 430-439. 10.1145/1542275.1542336. 


### Arguments
"--input_format"      = {json/raw} whether the file is in networkx json('nodes'=[], 'edges'=[]) or format of space separated as Dr. Eubank's portland reduced data<br/>
"--input_file"        = Name of the input file<br/>
"--output_file"       = Name of the output file<br/>
"--time"              = default="100", Simulation period in days<br/>
"--init_infection"    = type=int, default="20", Number of initial infectious people<br/>
"--transmission_rate" = type=str, default="0.5", range = [0.0 - 1], probability of disease transmission for a contact of one unit time<br/>
"--incubation_period" = type=int, default="2", Average time period(in days) to be in exposed phase<br/>
"--infectious_period" = type=int, default="4", Average time period(in days) to be infectious to other nodes<br/>

### Dependencies
  python2.7 <br/>
  networkx<br/>
  numpy<br/>
  pandas<br/>
  json<br/>
  
### Sample json files
  1000_subgraph.map<br/>
  100000_subgraph.map<br/>
  portland_graph_reduced.json<br/>
  
### Sample raw files
  portland_graph_reduced<br/>
  
### Sample code
  > python epifast_sequential.py --input_format json --input_file 100000_subgraph.map --output_file output.log <br/>
  > python epifast_sequential.py --input_format json --input_file 1000_subgraph.map --output_file output.log --transmission_rate 0.9

**Multi-Agent Accelerator for Data Science Using Transactional Machine Learning (MAADSTML)**

*Revolutionizing Data Stream Science with Transactional Machine Learning*

**Overview**

*MAADSTML combines Artificial Intelligence, Auto Machine Learning with Data Streams Integrated with Apache Kafka to create frictionless and elastic machine learning solutions.*  

This library allows users to harness the power of agent-based computing using hundreds of advanced linear and non-linear algorithms. Users can easily integrate Predictive Analytics, Prescriptive Analytics and Optimization in any data stream solution by wrapping additional code around the functions below. It connects with **Apache KAFKA brokers** for cloud based computing using Kafka as the data backbone. 

It uses VIPER as a **KAFKA connector and seamlessly combines Auto Machine Learning, with Real-Time Machine Learning, Real-Time Optimization and Real-Time Predictions** while publishing these insights in to a Kafka cluster in real-time at scale, while allowing users to consume these insights from anywhere, anytime and in any format.  We also provide management of algorithms and insights using our AiMS product integrated with VIPER and Kafka, to **help businesses reduce cloud compute and storage costs by tracking and controlling what algorithms are producing, and who is consuming these insights.**  If no one is consuming these insights, AiMS can **automatically deactivate** these algorithms thus STOPPING its use of storage and compute, saving organizations upto 20% in cloud costs. 

It also HPDE as the AutoML technology for TML.  Linux/Windows/Mac versions can be downloaded from [Github](https://github.com/smaurice101/transactionalmachinelearning)

It uses VIPERviz to visualize streaming insights over HTTP(S). Linux/Windows/Mac versions can be downloaded from [Github](https://github.com/smaurice101/transactionalmachinelearning)

MAADSTML details can be found in the forthcoming book: [Transactional Machine Learning with Data Streams and AutoML](https://github.com/smaurice101/transactionalmachinelearning_Book)


To install this library a request should be made to **support@otics.ca** for a username and a MAADSTOKEN.  Once you have these credentials then install this Python library.

**Compatibility**
    - Python 3.5 or greater
    - Minimal Python skills needed

**License**
   - Author: Sebastian Maurice, PhD
   - OTICS Advanced Analytics Inc.

**Installation**
   - At the command prompt write:
     **pip install maadstml**
     - This assumes you have [Downloaded Python](https://www.python.org/downloads/) and installed it on your computer.  


**MAADS-VIPER Connector to Manage Apache KAFKA:** 
  - MAADS-VIPER python library connects to VIPER instances on any servers; VIPER manages Apache Kafka.  VIPER is REST based and cross-platform that can run on windows, linux, MAC, etc.. It also fully supports SSL/TLS encryption in Kafka brokers for producing and consuming.
  
- **viperlisttopics** 
  - List all topics in Kafka brokers
 
- **viperdeactivatetopic**
  - Deactivate topics in kafka brokers and prevent unused algorithms from consuming storage and computing resources that cost money 

- **viperactivatetopic**
  - Activate topics in Kafka brokers 

- **vipercreatetopic**
  - Create topics in Kafka brokers 
  
- **viperstats**
  - List all stats from Kafka brokers allowing VIPER and KAFKA admins with a end-end view of who is producing data to algorithms, and who is consuming the insights from the algorithms including date/time stamp on the last reads/writes to topics, and how many bytes were read and written to topics and a lot more

- **vipersubscribeconsumer**
  - Admins can subscribe consumers to topics and consumers will immediately receive insights from topics.  This also gives admins more control of who is consuming the insights and allows them to ensures any issues are resolved quickly in case something happens to the algorithms.
  
- **viperunsubscribeconsumer**
  - Admins can unsubscribe consumers from receiving insights, this is important to ensure storage and compute resources are always used for active users.  For example, if a business user leaves your company or no longer needs the insights, by unsubscribing the consumer, the algorithm will STOP producing the insights.

- **viperhpdetraining**
  - Users can do real-time machine learning (RTML) on the data in Kafka topics. This is very powerful and useful for "transactional learnings" on the fly using our HPDE technology.  HPDE will find the optimal algorithm for the data in less than 60 seconds.  

- **viperhpdepredict**
  - Using the optimal algorithm - users can do real-time predictions from streaming data into Kafka Topics.
  
- **viperhpdeoptimize**
  -  Users can even do optimization to MINIMIZE or MAXIMIZE the optimal algorithm to find the BEST values for the independent variables that will minimize or maximize the dependent variable.

- **viperproducetotopic**
  - Users can produce to any topics by injesting from any data sources.

- **viperproducetotopicbulk**
  - Users can produce to any topics by injesting from any data sources.  Use this function to write bulk transactions at high speeds.  With the right architecture and
  network you can stream 1 million transactions per second (or more).
  
- **viperconsumefromtopic**
  - Users can consume from any topic and graph the data. 
  
- **viperconsumefromstreamtopic**
  - Users can consume from a multiple stream of topics at once

- **vipercreateconsumergroup**
  - Admins can create a consumer group made up of any number of consumers.  You can add as many partitions for the group in the Kafka broker as well as specify the replication factor to ensure high availaibility and no disruption to users who consume insights from the topics.

- **viperconsumergroupconsumefromtopic**
  - Users who are part of the consumer group can consume from the group topic.

- **viperproducetotopicstream**
  - Users can join multiple topic streams and produce the combined results to another topic.
  
- **vipercreatejointopicstreams**
  - Users can join multiple topic streams
  
- **vipercreatetrainingdata**
  - Users can create a training data set from the topic streams for Real-Time Machine Learning (RTML) on the fly.

- **vipermodifyconsumerdetails**
  - Users can modify consumer details on the topic.  When topics are created an admin must indicate name, email, location and description of the topic.  This helps to better manage the topic and if there are issues, the admin can contact the individual consuming from the topic.
  
- **vipermodifytopicdetails**
  - Users can modify details on the topic.  When topics are created an admin must indicate name, email, location and description of the topic.  This helps to better manage the topic and if there are issues, the admin can contact the developer of the algorithm and resolve issue quickly to ensure disruption to consumers is minimal.
 
- **vipergroupdeactivate**
  - Admins can deactive a consumer group, which will stop all insights being delivered to consumers in the group.
  
- **vipergroupactivate**
  - Admins can activate a group to re-start the insights.
 
- **viperdeletetopics**
  - Admins can delete topics in VIPER database and Kafka clusters.
		
- **viperanomalytrain**
  - Perform anomaly/peer group analysis on text or numeric data stream using advanced unsupervised learning. VIPER automatically joins 
    streams, and determines the peer group of "usual" behaviours using proprietary algorithms, which are then used to predict anomalies with 
	*viperanomalypredict* in real-time.  Users can use several parameters to fine tune the peer groups.  
	
	*VIPER is one of the very few, if not only, technology to do anomaly/peer group analysis using unsupervised learning on data streams 
	with Apache Kafka.*

- **viperanomalypredict**
  - Predicts anomalies for text or numeric data using the peer groups found with *viperanomalytrain*.  VIPER automatically joins streams
  and compares each value with the peer groups and determines if a value is anomalous in real-time.  Users can use several parameters to fine tune
  the analysis. 
  
  *VIPER is one of the very few, if not only, technology to do anomaly detection/predictions using unsupervised learning on data streams
  with Apache Kafka.*
		
		
**First import the Python library.**

**import maadstml**


**1. maadstml.viperstats(vipertoken,host,port=-999,brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.


*brokerhost* : string, optional

- Address where Kafka broker is running - if none is specified, the Kafka broker address in the VIPER.ENV file will be used.


*brokerport* : int, optional

- Port on which Kafka is listenting.

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: A JSON formatted object of all the Kafka broker information.

**21. maadstml.viperlisttopics(vipertoken,host,port=-999,brokerhost='', brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.


*brokerhost* : string, optional

- Address where Kafka broker is running - if none is specified, the Kafka broker address in the VIPER.ENV file will be used.


*brokerport* : int, optional

- Port on which Kafka is listenting.

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: A JSON formatted object of all the topics in the Kafka broker.


**2. maadstml.vipersubscribeconsumer(vipertoken,host,port,topic,companyname,contactname,contactemail,
		location,description,brokerhost='',brokerport=-999,groupid='',microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required

- Topic to subscribe to in Kafka broker

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*description* : string, required

- Description of why consumer wants to subscribe to topic

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*groupid* : string, optional

- Subscribe consumer to group

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Consumer ID that the user must use to receive insights from topic.


**3. maadstml.viperunsubscribeconsumer(vipertoken,host,port,consumerid,brokerhost='',brokerport=-999,
	microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumerid* : string, required
       
- Consumer id to unsubscribe

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

RETURNS: Success/failure 

**4. maadstml.viperproducetotopic(vipertoken,host,port,topic,producerid,enabletls=0,delay=100,inputdata='',maadsalgokey='',
	maadstoken='',getoptimal=0,externalprediction='',brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required

- Topic or Topics to produce to.  You can separate multiple topics by a comma.  If using multiple topics, you must 
  have the same number of producer ids (separated by commas), and same number of externalprediction (separated by
  commas).  Producing to multiple topics at once is convenient for synchronizing the timing of 
  streams for machine learning.

*producerid* : string, required
       
- Producer ID of topic to produce to in the Kafka broker

*enabletls* : int, optional
       
- Set to 1 if Kafka broker is enabled with SSL/TLS encryption, otherwise 0 for plaintext.

*delay*: int, optional

- Time in milliseconds from VIPER backsout from writing messages

*inputdata* : string, optional

- This is the inputdata for the optimal algorithm found by MAADS or HPDE

*maadsalgokey* : string, optional

- This should be the optimal algorithm key returned by maadstml.dotraining function.

*maadstoken* : string, optional
- If the topic is the name of the algorithm from MAADS, then a MAADSTOKEN must be specified to access the algorithm in the MAADS server

*getoptimal*: int, optional
- If you used the maadstml.OPTIMIZE function to optimize a MAADS algorithm, then if this is 1 it will only retrieve the optimal results in JSON format.

*externalprediction* : string, optional
- If you are using your own custom algorithms, then the output of your algorithm can be still used and fed into the Kafka topic.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns the value produced or results retrieved from the optimization.

**4.1. maadstml.viperproducetotopicbulk(vipertoken,host,port,topic,producerid,inputdata,enabletls=1,delay=100,brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required

- Topic or Topics to produce to.  You can separate multiple topics by a comma.  If using multiple topics, you must 
  have the same number of producer ids (separated by commas), and same number of externalprediction (separated by
  commas).  Producing to multiple topics at once is convenient for synchronizing the timing of 
  streams for machine learning.

*producerid* : string, required
       
- Producer ID of topic to produce to in the Kafka broker.  Separate multiple producer ids with comma.

*inputdata* : string, required
       
- You can write multiple transactions to each topic.  Each group of transactions must be separated by a tilde (~).  
  Each transaction in the group must be separate by a comma (,).  The number of groups must match the producerids and 
  topics.  For example, if you are writing to two topics: topic1,topic2, then the inputdata should be:
  trans1,transn2,...,transnN~trans1,transn2,...,transnN.  The number of transactions and topics can be any number.
  This function can be very powerful if you need to analyse millions or billions of transactions very quickly.

*enabletls* : int, optional
       
- Set to 1 if Kafka broker is enabled with SSL/TLS encryption, otherwise 0 for plaintext.

*delay*: int, optional

- Time in milliseconds from VIPER backsout from writing messages

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: None

**5. maadstml.viperconsumefromtopic(vipertoken,host,port,topic,consumerid,companyname,partition=-1,enabletls=0,delay=100,offset=0,
	brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to consume from in the Kafka broker

*consumerid* : string, required

- Consumer id associated with the topic

*companyname* : string, required

- Your company name

*partition* : int, optional

- set to Kafka partition number or -1 to autodect

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*offset*: int, optional

- Offset to start the reading from..if 0 then reading will start from the beginning of the topic. If -1, VIPER will automatically go to the last offset.  Or, you 
  can extract the LastOffet from the returned JSON and use this offset for your next call.  

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the contents read from the topic.


**6. maadstml.viperhpdepredict(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,
		hpdehost,inputdata,algokey='',partition=-1,offset=-1,enabletls=1,delay=1000,hpdeport=-999,brokerhost='',
		brokerport=-999,timeout=120,usedeploy=0,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*inputdata*: string, required

- This is a comma separated list of values that represent the independent variables in your algorithm. 
  The order must match the order of the independent variables in your algorithm. OR, you can enter a 
  data stream that contains the joined topics from *vipercreatejointopicstreams*.

*algokey*: string, optional

- If you know the algorithm key that was returned by VIPERHPDETRAIING then you can specify it here.
  Specifying the algokey can drastically speed up the predictions.

*partition* : int, optional

- If you know the kafka partition used to store data then specify it here.
  Most cases Kafka will dynamically store data in partitions, so you should
  use the default of -1 to let VIPER find it.
 
*offset* : int, optional

- Offset to start consuming data.  Usually you can use -1, and VIPER
  will get the last offset.
  
*hpdehost*: string, required

- Address of HPDE 

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encryted traffic, otherwise 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*hpdeport*: int, required

- Port number HPDE is listening on 

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.

*usedeploy* : int, optional

 - If 0 will use algorithm in test, else if 1 use in production algorithm. 
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the prediction.


**7. maadstml.viperhpdeoptimize(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,
		hpdehost,partition=-1,offset=-1,enabletls=0,delay=100,hpdeport=-999,usedeploy=0,ismin=1,constraints='best',
		stretchbounds=20,constrainttype=1,epsilon=10,brokerhost='',brokerport=-999,timeout=120,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*hpdehost*: string, required

- Address of HPDE 

*partition* : int, optional

- If you know the kafka partition used to store data then specify it here.
  Most cases Kafka will dynamically store data in partitions, so you should
  use the default of -1 to let VIPER find it.
 
*offset* : int, optional

- Offset to start consuming data.  Usually you can use -1, and VIPER
  will get the last offset.
  
*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*hpdeport*: int, required

- Port number HPDE is listening on 

*usedeploy* : int, optional
 - If 0 will use algorithm in test, else if 1 use in production algorithm. 

*ismin* : int, optional
- If 1 then function is minimized, else if 0 the function is maximized

*constraints*: string, optional

- If "best" then HPDE will choose the best values of the independent variables to minmize or maximize the dependent variable.  Users can also specify their own constraints for each variable and must be in the following format: varname1:min:max,varname2:min:max,...

*stretchbounds*: int, optional

- A number between 0 and 100, this is the percentage to stretch the bounds on the constraints.

*constrainttype*: int, optional

- If 1 then HPDE uses the min/max of each variable for the bounds, if 2 HPDE will adjust the min/max by their standard deviation, if 3 then HPDE uses stretchbounds to adjust the min/max for each variable.  

*epsilon*: int, optional

- Once HPDE finds a good local minima/maxima, it then uses this epsilon value to find the Global minima/maxima to ensure you have the best values of the independent variables that minimize or maximize the dependent variable.
					 
*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.

 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the optimization details and optimal values.


**8. maadstml.viperhpdetraining(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,
                 hpdehost,viperconfigfile,enabletls=1,partition=-1,deploy=0,modelruns=50,modelsearchtuner=80,hpdeport=-999,offset=-1,islogistic=0,brokerhost='',
				 brokerport=-999,timeout=120,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*hpdehost*: string, required

- Address of HPDE 

*viperconfigfile* : string, required

- Full path to VIPER.ENV configuration file on server.

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*partition*: int, optional

- Partition used by kafka to store data. NOTE: Kafka will dynamically store data in partitions.
  Unless you know for sure the partition, you should use the default of -1 to let VIPER
  determine where your data is.

*deploy*: int, optional

- If deploy=1, this will deploy the algorithm to the Deploy folder.  This is useful if you do not
  want to use this algorithm in production, and just testing it.  If just testing, then set deploy=0 (default).  

*modelruns*: int, optional

- Number of iterations for model training

*modelsearchtuner*: int, optional

- An integer between 0-100, this variable will attempt to fine tune the model search space.  A number close to 0 means you will have lots of models but their quality may be low, a number close to 100 (default=80) means you will have fewer models but their quality will be higher

*hpdeport*: int, required

- Port number HPDE is listening on 

*offset* : int, optional

 - If 0 will use the training data from the beginning of the topic
 
*islogistic*: int, optional

- If is 1, the HPDE will switch to logistic modeling, else continous.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the optimal algorithm that best fits your data.

**9. maadstml.viperproducetotopicstream(vipertoken,host,port,topic,producerid,offset,maxrows=0,enabletls=0,delay=100,
	brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topics to produce to in the Kafka broker - this is a topic that contains multiple topics, VIPER will consume from each topic and write results to the produceto topic

*producerid* : string, required

- Producerid of the topic producing to  

*offset* : int
 
 - If 0 will use the stream data from the beginning of the topics, -1 will automatically go to last offset

*maxrows* : int, optional
 
 - If offset=-1, this number will rollback the streams by maxrows amount i.e. rollback=lastoffset-maxrows
 
*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise 0 for plaintext

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the optimal algorithm that best fits your data.

**10. maadstml.vipercreatetrainingdata(vipertoken,host,port,consumefrom,produceto,dependentvariable,
		independentvariables,consumerid,producerid,companyname,partition=-1,enabletls=0,delay=100,
		brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from 

*produceto* : string, required
       
- Topic to produce to 

*dependentvariable* : string, required
       
- Topic name of the dependentvariable 
 
*independentvariables* : string, required
       
- Topic names of the independentvariables - VIPER will automatically read the data streams.  
  Separate multiple variables by comma. 

*consumerid* : string, required

- Consumerid of the topic to consume to  

*producerid* : string, required

- Producerid of the topic producing to  
 
*partition* : int, optional

- This is the partition that Kafka stored the stream data.  Specifically, the streams you joined 
  from function *viperproducetotopicstream* will be stored in a partition by Kafka, if you 
  want to create a training dataset from these data, then you should use this partition.  This
  ensures you are using the right data to create a training dataset.
    
*companyname* : string, required

- Your company name  

*enabletls*: int, optional

- Set to 1 if Kafka broker is enabled for SSL/TLS encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backout from reading messages

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the training data set.

**11. maadstml.vipercreatetopic(vipertoken,host,port,topic,companyname,contactname,contactemail,location,
description,enabletls=0,brokerhost='',brokerport=-999,numpartitions=1,replication=1,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to create 

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*description* : string, required

- Description of why consumer wants to subscribe to topic

*enabletls* : int, optional

- Set to 1 if Kafka is SSL/TLS enabled for encrypted traffic, otherwise 0 for no encryption (plain text)

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*numpartitions*: int, optional

- Number of the parititons to create in the Kafka broker - more parititons the faster Kafka will produce results.

*replication*: int, optional

- Specificies the number of brokers to replicate to - this is important for failover
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the producer id for the topic.

**12. maadstml.viperconsumefromstreamtopic(vipertoken,host,port,topic,consumerid,companyname,partition=-1,
        enabletls=0,delay=100,offset=0,brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to consume from 

*consumerid* : string, required

- Consumerid associated with topic

*companyname* : string, required

- Your company name

*partition*: int, optional

- Set to a kafka partition number, or -1 to autodetect partition.

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*offset* : int, optional

- Offset to start reading from ..if 0 VIPER will read from the beginning

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the contents of all the topics read


**13. maadstml.vipercreatejointopicstreams(vipertoken,host,port,topic,topicstojoin,companyname,contactname,contactemail,
		description,location,enabletls=0,brokerhost='',brokerport=-999,replication=1,numpartitions=1,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to consume from 

*topicstojoin* : string, required

- Enter two or more topics separated by a comma and VIPER will join them into one topic

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*description* : string, required

- Description of why consumer wants to subscribe to topic

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled, otherwise set to 0 for plaintext.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*numpartitions* : int, optional

- Number of partitions

*replication* : int, optional

- Replication factor

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the producerid of the joined streams
								
**14. maadstml.vipercreateconsumergroup(vipertoken,host,port,topic,groupname,companyname,contactname,contactemail,
		description,location,enabletls=1,brokerhost='',brokerport=-999,microserviceid='')**
		
**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*groupname* : string, required

- Enter the name of the group

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled, otherwise set to 0 for plaintext.

*description* : string, required

- Description of why consumer wants to subscribe to topic

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the groupid of the group.
								
**15. maadstml.viperconsumergroupconsumefromtopic(vipertoken,host,port,topic,consumerid,groupid,companyname,
		partition=-1,enabletls=0,delay=100,offset=0,rollbackoffset=0,brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*consumerid* : string, required

- Enter the consumerid associated with the topic

*groupid* : string, required

- Enter the groups id

*companyname* : string, required

- Enter the company name

*partition*: int, optional

- set to Kakfa partition number or -1 to autodetect

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*offset* : int, optional

- Offset to start reading from.  If 0, will read from the beginning of topic, or -1 to automatically go to end of topic.

*rollbackoffset* : int, optional

- The number of offsets to rollback the data stream.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the contents of the group.
    
**16. maadstml.vipermodifyconsumerdetails(vipertoken,host,port,topic,companyname,consumerid,contactname='',
contactemail='',location='',brokerhost='',brokerport=9092,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*consumerid* : string, required

- Enter the consumerid associated with the topic

*companyname* : string, required

- Enter the company name

*contactname* : string, optional

- Enter the contact name 

*contactemail* : string, optional
- Enter the contact email

*location* : string, optional

- Enter the location

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure

**17. maadstml.vipermodifytopicdetails(vipertoken,host,port,topic,companyname,partition=0,enabletls=1,
          isgroup=0,contactname='',contactemail='',location='',brokerhost='',brokerport=9092,microserviceid='')**
     
**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*companyname* : string, required

- Enter the company name

*partition* : int, optional

- You can change the partition in the Kafka topic.

*enabletls* : int, optional

- If enabletls=1, then SSL/TLS is enables in Kafka, otherwise if enabletls=0 it is not.

*isgroup* : int, optional

- This tells VIPER whether this is a group topic if isgroup=1, or a normal topic if isgroup=0

*contactname* : string, optional

- Enter the contact name 

*contactemail* : string, optional
- Enter the contact email

*location* : string, optional

- Enter the location

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure

**18. maadstml.viperactivatetopic(vipertoken,host,port,topic,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to activate

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure
    
**19. maadstml.viperdeactivatetopic(vipertoken,host,port,topic,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to deactivate

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure

**20. maadstml.vipergroupactivate(vipertoken,host,port,groupname,groupid,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*groupname* : string, required
       
- Name of the group

*groupid* : string, required
       
- ID of the group

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure
   
**21.  maadstml.vipergroupdeactivate(vipertoken,host,port,groupname,groupid,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*groupname* : string, required
       
- Name of the group

*groupid* : string, required
       
- ID of the group

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure
   
**22. maadstml.viperdeletetopics(vipertoken,host,port,topic,enabletls=1,brokerhost='',brokerport=9092,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to delete.  Separate multiple topics by a comma.

*enabletls* : int, optional

- If enabletls=1, then SSL/TLS is enable on Kafka, otherwise if enabletls=0, it is not.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- microservice to access viper
   
**23.  maadstml.balancebigdata(localcsvfile,numberofbins,maxrows,outputfile,bincutoff,distcutoff,startcolumn=0)**

**Parameters:**	

*localcsvfile* : string, required

- Local file, must be CSV formatted.

*numberofbins* : int, required

- The number of bins for the histogram. You can set to any value but 10 is usually fine.

*maxrows* :  int, required

- The number of rows to return, which will be a subset of your original data.

*outputfile* : string, required

- Your new data will be writted as CSV to this file.

*bincutoff* : float, required. 

-  This is the threshold percentage for the bins. Specifically, the data in each variable is allocated to bins, but many 
   times it will not fall in ALL of the bins.  By setting this percentage between 0 and 1, MAADS will choose variables that
   exceed this threshold to determine which variables have data that are well distributed across bins.  The variables
   with the most distributed values in the bins will drive the selection of the rows in your dataset that give the best
   distribution - this will be very important for MAADS training.  Usually 0.7 is good.

*distcutoff* : float, required. 

-  This is the threshold percentage for the distribution. Specifically, MAADS uses a Lilliefors statistic to determine whether 
   the data are well distributed.  The lower the number the better.  Usually 0.45 is good.
   
*startcolumn* : int, optional

- This tells MAADS which column to start from.  If you have DATE in the first column, you can tell MAADS to start from 1 (columns are zero-based)

RETURNS: Returns a detailed JSON object and new balaced dataset written to outputfile.

**24. maadstml.viperanomalytrain(vipertoken,host,port,consumefrom,produceto,producepeergroupto,produceridpeergroup,consumeridproduceto,
                      streamstoanalyse,companyname,consumerid,producerid,flags,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,hpdeport=-999,brokerhost='',brokerport=9092,delay=1000,timeout=120,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*producepeergroupto* : string, required

- Topic to produce the peer group for anomaly comparisons 

*produceridpeergroup* : string, required

- Producerid for the peer group topic

*consumeridproduceto* : string, required

- Consumer id for the Produceto topic 

*streamstoanalyse* : string, required

- Comma separated list of streams to analyse for anomalies

*flags* : string, required

- These are flags that will be used to select the peer group for each stream.  The flags must have the following format:
  *topic=[topic name],topictype=[numeric or string],threshnumber=[a number between 0 and 10000, i.e. 200],
  lag=[a number between 1 and 20, i.e. 5],zthresh=[a number between 1 and 5, i.e. 2.5],influence=[a number between 0 and 1 i.e. 0.5]*
  
  *threshnumber*: decimal number to determine usual behaviour - only for numeric streams, numbers are compared to the centroid number, 
  a standardized distance is taken and all numbers below the thresholdnumeric are deemed as usual i.e. thresholdnumber=200, any value 
  below is close to the centroid  - you need to experiment with this number.
  
  *lag*: number of lags for the moving mean window, works to smooth the function i.e. lag=5
  
  *zthresh*: number of standard deviations from moving mean i.e. 3.5
  
  *influence*: strength in identifying outliers for both stationary and non-stationary data, i.e. influence=0 ignores outliers 
  when recalculating the new threshold, influence=1 is least robust.  Influence should be between (0,1), i.e. influence=0.5
  
  Flags must be provided for each topic.  Separate multiple flags by ~

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*hpdehost*: string, required

- Address of HPDE 

*viperconfigfile* : string, required

- Full path to VIPER.ENV configuration file on server.

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*partition*: int, optional

- Partition used by kafka to store data. NOTE: Kafka will dynamically store data in partitions.
  Unless you know for sure the partition, you should use the default of -1 to let VIPER
  determine where your data is.

*hpdeport*: int, required

- Port number HPDE is listening on 

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*delay* : int, optional

- delay parameter to wait for Kafka to respond - in milliseconds.

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the peer groups for all the streams.


**25. maadstml.viperanomalypredict(vipertoken,host,port,consumefrom,produceto,consumeinputstream,produceinputstreamtest,produceridinputstreamtest,
                      streamstoanalyse,consumeridinputstream,companyname,consumerid,producerid,flags,hpdehost,viperconfigfile,
                      enabletls=1,partition=-1,hpdeport=-999,brokerhost='',brokerport=9092,delay=1000,timeout=120,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*consumeinputstream* : string, required

- Topic of the input stream to test for anomalies

*produceinputstreamtest* : string, required

- Topic to store the input stream data for analysis

*produceridinputstreamtest* : string, required

- Producer id for the produceinputstreamtest topic 

*streamstoanalyse* : string, required

- Comma separated list of streams to analyse for anomalies

*flags* : string, required

- These are flags that will be used to select the peer group for each stream.  The flags must have the following format:
  *riskscore=[a number between 0 and 1]~complete=[and, or, pvalue i.e. p50 means streams over 50% that have an anomaly]~type=[and,or this will 
  determine what logic to apply to v and sc],topic=[topic name],topictype=[numeric or string],v=[v>some value, v<some value, or valueany],
  sc=[sc>some number, sc<some number - this is the score for the anomaly test]
  
  if using strings, the specify flags: type=[and,or],topic=[topic name],topictype=string,stringcontains=[0 or 1 - 1 will do a substring test, 
  0 will equate the strings],v2=[any text you want to test - use | for OR or ^ for AND],sc=[score value, sc<some value, sc>some value]
 
  *riskscore*: this the riskscore threshold.  A decimal number between 0 and 1, use this as a threshold to flag anomalies.

  *complete* : If using multiple streams, this will test each stream to see if the computed riskscore and perform an AND or OR on each risk value
  and take an average of the risk scores if using AND.  Otherwise if at least one stream exceeds the riskscore it will return.
  
  *type*: AND or OR - if using v or sc, this is used to apply the appropriate logic between v and sc.  For example, if type=or, then VIPER 
  will see if a test value is less than or greater than V, OR, standarzided value is less than or greater than sc.  
  
  *sc*: is a standarized variavice between the peer group value and test value.
  
  *v1*: is a user chosen value which can be used to test for a particular value.  For example, if you want to flag values less then 0, 
  then choose v<0 and VIPER will flag them as anomolous.

  *v2*: if analysing string streams, v2 can be strings you want to check for. For example, if I want to check for two
  strings: Failed and Attempt Failed, then set v2=Failed^Attempt Failed, where ^ tells VIPER to perform an AND operation.  
  If I want either to exist, 2=Failed|Attempt Failed, where | tells VIPER to perform an OR operation.

  *stringcontains* : if using string streams, and you want to see if a particular text value exists and flag it - then 
  if stringcontains=1, VIPER will test for substrings, otherwise it will equate the strings. 
  
  
  Flags must be provided for each topic.  Separate multiple flags by ~

*consumeridinputstream* : string, required

- Consumer id of the input stream topic: consumeinputstream

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*hpdehost*: string, required

- Address of HPDE 

*viperconfigfile* : string, required

- Full path to VIPER.ENV configuration file on server.

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*partition*: int, optional

- Partition used by kafka to store data. NOTE: Kafka will dynamically store data in partitions.
  Unless you know for sure the partition, you should use the default of -1 to let VIPER
  determine where your data is.

*hpdeport*: int, required

- Port number HPDE is listening on 

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*delay* : int, optional

- delay parameter to wait for Kafka to respond - in milliseconds.

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the peer groups for all the streams.



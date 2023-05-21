# DESIGN DOC



## Problem Statement

Design an instagram like photo sharing application where users can post photo or videos, can follow other users, browse through the posted photos and videos by the following users, like and comment on the posts by following users.

## Functional Requirements

1. Photo and video sharing functionality - allow users to upload and share photos and videos on the application.
2. Following functionality - enable users to follow other users on the application to view their posts.
3. Browsing functionality - allow users to browse through the posts of the users they are following.
4. Liking functionality - enable users to like the posts of the users they are following.
5. Commenting functionality - allow users to comment on the posts of the users they are following.

## Components

### Storage
1. Requirement: The component should be able to store user data, posts, and comments.

2. Approaches:
   a. Relational Database Management System (RDBMS): RDBMS is a traditional approach to store structured data. It provides ACID (Atomicity, Consistency, Isolation, Durability) properties and supports SQL queries. It is suitable for storing user data and comments, but not ideal for storing posts as they can be unstructured.

   b. NoSQL Database: NoSQL databases are designed to handle unstructured data. They provide high scalability and availability. They are suitable for storing posts as they can be unstructured. However, they may not provide ACID properties and may require more complex queries.

   c. Object Storage: Object storage is a type of storage that stores data as objects rather than files or blocks. It is suitable for storing large amounts of unstructured data, such as posts. It provides high scalability and availability but may not provide ACID properties.

   Based on the use case, a combination of RDBMS and NoSQL database can be used. User data and comments can be stored in an RDBMS, while posts can be stored in a NoSQL database. This approach provides the benefits of both types of databases.

3. Data types and appropriate databases:
   a. User data: User data is structured data and can be stored in an RDBMS such as MySQL or PostgreSQL.
   b. Posts: Posts are unstructured data and can be stored in a NoSQL database such as MongoDB or Cassandra.
   c. Comments: Comments are structured data and can be stored in an RDBMS such as MySQL or PostgreSQL.

4. Cloud offering:
   a. For RDBMS: Amazon Relational Database Service (RDS) is a fully managed relational database service that provides easy setup, scaling, and management of databases. It supports MySQL, PostgreSQL, and other popular RDBMS.
   b. For NoSQL: Amazon DynamoDB is a fully managed NoSQL database service that provides high scalability and availability. It supports document and key-value data models.
   c. For Object Storage: Amazon Simple Storage Service (S3) is a fully managed object storage service that provides high scalability and availability. It supports storing and retrieving any amount of data from anywhere on the web.

   Amazon Web Services (AWS) provides a well-known cloud offering that satisfies the requirement of the component. AWS provides a wide range of services that can be used to build a distributed system.

### Photo and Video Service
#### Requirements:
The Photo and Video Service component should be able to handle uploading and sharing of photos and videos.
#### APIs
	uploadPhoto
	uploadVideo
	sharePhoto
	shareVideo
	
#### Comments
The Photo and Video Service component is designed to meet the requirements of uploading and sharing photos and videos in a distributed system.


### Following Service
#### Requirements:
Enables users to follow other users
#### APIs
	followUser(userId)
	unfollowUser(userId)
	getFollowers(userId)
	getFollowing(userId)
	
#### Comments
This service component provides the necessary APIs to allow users to follow and unfollow other users, as well as retrieve their followers and following lists.


### Browsing Service
#### Requirements:
The browsing service should allow users to browse through the posts of the users they are following
#### APIs
	getFollowedUsers(userId)
	getPostsByUser(userId)
	getPostsByFollowedUsers(userId)
	likePost(postId, userId)
	unlikePost(postId, userId)
	commentOnPost(postId, userId, comment)
	getCommentsForPost(postId)
	
#### Comments
The browsing service component is designed to allow users to easily browse through the posts of the users they are following, with a set of APIs that cover all necessary functionalities.


### Liking Service
#### Requirements:
Enables users to like the posts of the users they are following
#### APIs
	likePost(postId, userId)
	getLikes(postId)
	getLikedPosts(userId)
	
#### Comments
The Liking Service component allows users to like posts and retrieve information about likes and liked posts.


### Commenting Service
#### Requirements:
Allow users to comment on the posts of the users they are following
#### APIs
	addComment(postId, userId, comment)
	getComments(postId)
	deleteComment(commentId)
	
#### Comments
The Commenting Service component allows users to interact with each other by commenting on posts. It provides necessary APIs to add, get, and delete comments.


### Cache
1. Requirement: The Cache component should store frequently accessed data to improve the performance of the system by reducing the time taken to retrieve data from the main storage.

2. Approaches:
    a. In-memory caching: This approach involves storing frequently accessed data in the memory of the Cache component. This approach is fast and efficient but has limited storage capacity.
    b. Distributed caching: This approach involves distributing the cache across multiple nodes in the system. This approach provides higher storage capacity and better fault tolerance.
    c. Hybrid caching: This approach combines both in-memory and distributed caching to provide a balance between speed and storage capacity.

3. Cloud offering: Amazon ElastiCache is a well-known cloud offering that satisfies the requirement of the Cache component. It provides both in-memory and distributed caching options and supports popular caching engines like Redis and Memcached. It also offers automatic scaling and high availability features to ensure the cache is always available and responsive.

### Load Balancer
1. Requirement: The Load Balancer component should be able to distribute incoming requests across multiple instances of the service components.

2. Approaches:
- Round Robin: The Load Balancer distributes incoming requests in a round-robin fashion to each instance of the service component.
- Least Connections: The Load Balancer distributes incoming requests to the instance with the least number of active connections.
- IP Hash: The Load Balancer uses the client's IP address to determine which instance of the service component to send the request to.

3. Cloud Offering: Amazon Web Services (AWS) Elastic Load Balancer (ELB) satisfies the requirement of the Load Balancer component. ELB provides three types of load balancers: Application Load Balancer, Network Load Balancer, and Classic Load Balancer. Each type of load balancer has its own set of features and capabilities, but all of them can distribute incoming requests across multiple instances of the service components. ELB also provides auto-scaling capabilities, which can automatically add or remove instances of the service component based on the incoming traffic.


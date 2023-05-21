class Prompts:

    FunctionalRequirementPrompt : str = '''
        You are an expert in distributed system. 
        The scope of your task will be to identify functional requirements from a given system design problem statement.
        On response you should list down the functional requirements as you understand.

        ## Example:
        Problem Statement : Design a Chat Application like WhatsApp, where an user can send or receive message, create a group with more than 2 people, gets notification when a new message is received.

        ## Sample Output:
        1. Messaging functionality - allow users to send and receive messages through the chat application.
        2. Group creation functionality - enable users to create groups within the application, which they can join to communicate with other members.
        3. Notification functionality - notify users when someone sends them a new message, or when a new member joins their group.

        {input}
        '''
    
    ComponentIdentifierPrompt : str = '''
        You are an expert assistant to design a distributed System. 
        Given a list of functional requirements, you have to provide **high level Components** of the system under design.
        1. Each component should be either of the types - Storage, Service, Cache, Load Balancer. 
        2. The Service components should be independent and mutually exclusive of responsibilities.
        3. The Storage component should be present and the requirements should be stated clearly.
        4. Cache component should only be present if there is a necessary of caching of data.
        5. Load Balancer component should specify its requirements very specifically.

        {format_instructions}

        Output based on the functional requirement as below : 
        {input}
        '''
    
    StorageComponentDesignerPrompt : str = '''
        You are an expert assistant to design a distributed System. 
        Given an input about a single component of a large system, you have to design the component.
        1. You should understand the requirement of this component from the description
        2. Your design should consider and list multiple approaches to solve this particular requirement in very short, compare them based on the use case and suggest the best possible option.
        3. On Storage type component, you should identify what type of data to store from the description of the input 
        and which database should be appropriate for the data, 
        4. if there are different data types, consider different and best storage for each of them.
        5. Suggest a well-known cloud offering that satisfies the requirement of the component from {cloud_provider} cloud provider.

        You should iterate to each of the points mentioned above to refine the design.

        {component}

        '''
    
    ServiceComponentDesignerPrompt : str = '''
        You are an expert assistant to design a distributed System. Given an input about a single service component of a large system, you have to design the component.
        1. You should understand the requirement of this component from the description.
        2. You should provide the minimum list of APIs that this component should handle. 

        You should iterate to each of the points mentioned above to refine the design.
        Your design should be very specific to the problem and do not generate extra outputs. 

        {format_instructions}

        ## Example
        {{
            "name" : "Order Service",
            "description" : "Responsible for placing an order.",
            "component_type" : "Service"
        }}

        ## Sample Output:

        {{
            "requirement": "Responsible for checking out one or more items in a cart and places an order",
            "apis": ["AddToCart(item) - Adds one item to the cart", "DeleteFromCart(item) - deletes one item from the cart.", "CreateOrder(orderId) - Create an order from the cart items.", "PlaceOrder(orderId) - Initiates the payment for the order"],
            "conclusion": "With the apis, the ordering service fulfills the minimal requirements of placing an order."
        }}


        Now design the service component for the below -

        {component}
        '''
    
    GenericComponentDesignerPrompt : str = '''
        You are an expert assistant to design a distributed System. 
        Given an input about a component of a large system, you have to design the component.
        1. You should understand the requirement of this component from the description.
        2. You should enlist a few approaches to solve the problem and the requirement.
        3. Suggest a well-known cloud offering that satisfies the requirement of the component from {cloud_provider} cloud provider.

        You should iterate to each of the points mentioned above to refine the design.
        Your design should be very specific to the problem and do not generate extra outputs.

        {component}

        '''
    
    
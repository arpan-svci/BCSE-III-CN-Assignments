from channel import Resource
from P_Persistent import Node

if __name__ == "__main__":
    data = """My name is Arpan"""
    resource = Resource(30)
    node_list = [Node(7, resource, True,3 , data), Node(2, resource, True, 14, data),
                 Node(12, resource, True, 18, data),
                 Node(13, resource, True, 25, data), Node(23, resource, True, 28, data),
                 Node(3, resource, False, 3), Node(14, resource, False, 14), Node(18, resource, False, 18),
                 Node(25, resource, False, 25), Node(28, resource, False, 28)]
    # nodes = [Node(7, resource, True, 2, data), Node(2, resource, False, 2)]

    # print(f"Sender {node_list[0].location} takes ", node_list[0].time_taken)
    # print(f"Sender {node_list[1].location} takes ", node_list[1].time_taken)
    # print(f"Sender {node_list[2].location} takes ", node_list[2].time_taken)

from rosbags.rosbag1 import Reader

def extract_message_formats(bag_path):
    print(f"Extracting message definitions from: {bag_path}")
    print("=" * 60)
    
    seen_types = set()

    # The rosbags library reads ROS 1 bags seamlessly
    with Reader(bag_path) as reader:
        # reader.connections contains the metadata and schema for every topic
        for connection in reader.connections:
            msg_type = connection.msgtype
            
            if msg_type not in seen_types:
                seen_types.add(msg_type)
                
                print(f"\n--- Message Type: {msg_type} ---")
                # msgdef contains the raw text definition embedded in the bag!
                print(connection.msgdef)
                print("-" * 60)

if __name__ == "__main__":
    # Ensure this matches the path to your bag file
    extract_message_formats('output.bag')
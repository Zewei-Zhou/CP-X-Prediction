from bagpy import bagreader
import os

bag_path = 'output.bag'
output_dir = 'output_data'

os.makedirs(output_dir, exist_ok=True)

# Load bag
bag = bagreader(bag_path)

print("\n=== Dumping ALL topics ===")

for topic in bag.topics:
    print(f"\nProcessing topic: {topic}")
    
    try:
        # Convert topic to CSV
        csv_file = bag.message_by_topic(topic)
        
        # Clean filename (replace / with _)
        clean_name = topic.replace('/', '_').strip('_') + '.csv'
        new_path = os.path.join(output_dir, clean_name)
        
        # Move/rename file
        os.rename(csv_file, new_path)
        
        print(f"Saved: {new_path}")
    
    except Exception as e:
        print(f"Failed for topic {topic}: {e}")

print("\n✅ Done. All topics saved.")
import os
import re
import json
import argparse

def get_guid_map(folder_path):
    guid_map = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.meta'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    guid_match = re.search(r'guid: ([0-9a-f]{32})', content)
                    if guid_match:
                        guid = guid_match.group(1)
                        file_name = file[:-5]  # Remove '.meta' extension
                        file_path = os.path.join(root, file_name)
                        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else None
                        guid_map[guid] = {'file_name': file_name, 'file_size': file_size}
    return guid_map

def replace_guids(folder_path, guid_map):
    summary = {
        'replaced': {},
        'not_found': [],
        'size_mismatch': []
    }

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()

            modified = False
            for old_guid, file_data in guid_map.items():
                if old_guid in content:
                    file_name = file_data['file_name']
                    expected_size = file_data['file_size']
                    if file_name in new_guid_map:
                        if expected_size is None or os.path.getsize(file_path) == expected_size:
                            new_guid = new_guid_map[file_name]
                            content = content.replace(old_guid, new_guid)
                            modified = True
                            if old_guid not in summary['replaced']:
                                summary['replaced'][old_guid] = new_guid
                        else:
                            if old_guid not in summary['size_mismatch']:
                                summary['size_mismatch'].append(old_guid)
                    else:
                        if old_guid not in summary['not_found']:
                            summary['not_found'].append(old_guid)

            if modified:
                with open(file_path, 'w') as f:
                    f.write(content)

    return summary

parser = argparse.ArgumentParser(description='Update Unity project GUIDs.')
parser.add_argument('old_project_path', help='Path to the old Unity project.')
parser.add_argument('new_project_path', help='Path to the new Unity project.')

args = parser.parse_args()

old_guid_map = get_guid_map(args.old_project_path)
new_guid_map = {v['file_name']: k for k, v in get_guid_map(args.new_project_path).items()}

with open('guid_map.json', 'w') as f:
    json.dump(old_guid_map, f, indent=2)

summary = replace_guids(args.new_project_path, old_guid_map)

print('Summary:')
print(json.dumps(summary, indent=2))

with open('summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

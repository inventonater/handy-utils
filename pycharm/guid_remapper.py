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
                        guid_map[guid] = file[:-5]  # Remove '.meta' extension
    return guid_map


def replace_guids(folder_path, guid_map):
    replaced = 'replaced'
    not_found = 'not_found'
    summary = {
        replaced: {},
        not_found: []
    }

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()

            modified = False
            for old_guid, file_name in guid_map.items():
                if old_guid in content:
                    if file_name in new_guid_map:
                        new_guid = new_guid_map[file_name]
                        content = content.replace(old_guid, new_guid)
                        modified = True
                        if old_guid not in summary[replaced]:
                            summary[replaced][old_guid] = new_guid
                    else:
                        if old_guid not in summary[not_found]:
                            summary[not_found].append(old_guid)

            if modified:
                with open(file_path, 'w') as f:
                    f.write(content)

    return summary


parser = argparse.ArgumentParser(description='Update Unity project GUIDs.')
parser.add_argument('old_project_path', help='Path to the old Unity project.')
parser.add_argument('new_project_path', help='Path to the new Unity project.')

args = parser.parse_args()

old_guid_map = get_guid_map(args.old_project_path)
new_guid_map = {v: k for k, v in get_guid_map(args.new_project_path).items()}

with open('guid_map.json', 'w') as f:
    json.dump(old_guid_map, f, indent=2)

output = replace_guids(args.new_project_path, old_guid_map)

print('Summary:')
print(json.dumps(output, indent=2))

with open('summary.json', 'w') as f:
    json.dump(output, f, indent=2)

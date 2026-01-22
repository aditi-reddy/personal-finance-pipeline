"""
Great Expectations Setup - Version 2
Creates GX project structure
"""

print("=" * 60)
print("GREAT EXPECTATIONS SETUP")
print("=" * 60)

import great_expectations as gx
from great_expectations.data_context import FileDataContext
import os

# Get current directory
current_dir = os.getcwd()
print(f"\nWorking directory: {current_dir}")

# Define GX directory
gx_dir = os.path.join(current_dir, "great_expectations")

print(f"GX directory will be: {gx_dir}")

# Check if it already exists
if os.path.exists(gx_dir):
    print("\n⚠️  Great Expectations folder already exists")
    print("   Loading existing context...")
    context = gx.get_context(context_root_dir=gx_dir)
else:
    print("\n📁 Creating Great Expectations folder...")
    
    # Create the directory structure
    os.makedirs(gx_dir, exist_ok=True)
    os.makedirs(os.path.join(gx_dir, "expectations"), exist_ok=True)
    os.makedirs(os.path.join(gx_dir, "checkpoints"), exist_ok=True)
    os.makedirs(os.path.join(gx_dir, "plugins"), exist_ok=True)
    os.makedirs(os.path.join(gx_dir, "uncommitted"), exist_ok=True)
    
    # Create minimal config file
    config = {
        "config_version": 3.0,
        "datasources": {},
        "data_docs_sites": {
            "local_site": {
                "class_name": "SiteBuilder",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "uncommitted/data_docs/local_site/"
                },
                "site_index_builder": {
                    "class_name": "DefaultSiteIndexBuilder"
                }
            }
        }
    }
    
    # Write config file
    import yaml
    config_path = os.path.join(gx_dir, "great_expectations.yml")
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print("✅ Created GX folder structure")
    print("✅ Created configuration file")
    
    # Initialize context
    context = gx.get_context(context_root_dir=gx_dir)

print(f"\n✅ Great Expectations initialized!")
print(f"📁 Root directory: {context.root_directory}")

# List what was created
print(f"\n📂 Created folders:")
for folder in ['expectations', 'checkpoints', 'plugins', 'uncommitted']:
    folder_path = os.path.join(gx_dir, folder)
    if os.path.exists(folder_path):
        print(f"   ✅ {folder}/")

print("\n" + "=" * 60)
print("SETUP COMPLETE!")
print("=" * 60)
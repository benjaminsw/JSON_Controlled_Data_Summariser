import os
import sys


# Split the extension from the path and normalise it to lowercase.
ext = os.path.splitext(sys.argv[1])[-1].lower()
print ext
# Now we can simply use == to check for equality, no need for wildcards.
if ext == ".csv":
    print fp, "is a csv file"
elif ext == ".json":
    print fp, "is a json file"
else:
    print fp, "is an unknown file format."

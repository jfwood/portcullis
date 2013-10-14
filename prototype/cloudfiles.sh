#!/bin/sh

# Cloud Files related cURL requests.
#   See http://www.rackspace.com/knowledge_center/article/cloud-files-curl-cookbook#N


# Step 1: Create an 'auth.xml' file per the link above.


# Step 2: Use this call to get the API token: curl -X POST -d @auth.xml -H "Content-Type: application/xml" -H "Accept: application/xml" https://auth.api.rackspacecloud.com/v1.1/auth


# Step 3: Fill out the AUTH_TOKEN per the 'token' ID returned from the call above:
AUTH_TOKEN=<token ID here>


# Step 4: Select your desired cloud endpoint, with 'localhost' used to hit a local proxy for development:
#CF_END=https://storage101.dfw1.clouddrive.com:443/v1/MossoCloudFS_a1d4e46d-4091-49f4-a532-7ce73823623b
CF_END=http://localhost:8080/v1/MossoCloudFS_a1d4e46d-4091-49f4-a532-7ce73823623b


# Step 5: Configure which containers/files to interact with in the cloud account:
#   NOTE: Make sure only one TEST_FILE_SRC/TEST_FILE_DST file is defined at a time.
CONTAINER=test_container
TEST_FILE_GET=testdata_get.dat

# - Small file: 
TEST_FILE_SRC=testdata_out.txt
TEST_FILE_DST=testdata_out.dat
# - Medium file (115838 bytes):
TEST_FILE_SRC_M=/Applications/VirtualBox.app/Contents/MacOS/vboxshell.py
TEST_FILE_DST_M=file115838.py
# - Large file (1668880 bytes):
TEST_FILE_SRC_L=/Applications/VirtualBox.app/Contents/MacOS/VMMR0.r0
TEST_FILE_DST_L=file1668880.py
# - GIANT file (492000000 bytes):
TEST_FILE_SRC_G=/Users/john.wood/projects/security/disk_write_challenge/partition_large_file/test_big_file.txt
TEST_FILE_DST_G=file492000000.py


# Step 6: Run commands and profit:

# - List containers in Cloud Files:
#curl -H "X-Auth-Token: $AUTH_TOKEN" $CF_END

# - Create a test container:
#curl -X PUT -H "X-Auth-Token: $AUTH_TOKEN" $CF_END/$CONTAINER

# - Upload file to the container:
# Doesn't handle binary: curl -X PUT -T $TEST_FILE -H "Content-Type: application/octet-stream" -H "X-Auth-Token: $AUTH_TOKEN" $CF_END/$CONTAINER/$TEST_FILE
curl -v -X PUT -H "Transfer-Encoding: chunked" -H "Expect: 100-continue" -H "X-Auth-Token: $AUTH_TOKEN" --data-binary @$TEST_FILE_SRC $CF_END/$CONTAINER/$TEST_FILE_DST

# - Retrieve file from container:
curl -o $TEST_FILE_GET -X GET -H "X-Auth-Token: $AUTH_TOKEN" -H "Transfer-Encoding: chunked" $CF_END/$CONTAINER/$TEST_FILE_DST

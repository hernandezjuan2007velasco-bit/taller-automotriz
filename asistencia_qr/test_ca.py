import urllib.request
import mysql.connector

# Download CA cert
print("Downloading CA cert...")
urllib.request.urlretrieve('https://curl.se/ca/cacert.pem', 'cacert.pem')
print("Downloaded cacert.pem")

try:
    print("Connecting...")
    conn = mysql.connector.connect(
        host='gateway01.us-east-1.prod.aws.tidbcloud.com',
        port=4000,
        user='NDfuuQXvqct8w5L.root',
        password='O9KREUQSja93XZD1',
        ssl_ca='cacert.pem',
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )
    print('Success with O9KREUQSja93XZD1!')
    conn.close()
except Exception as e:
    print('Error with O9KREUQSja93XZD1:', e)

# Test with l instead of 1
try:
    print("Connecting with Dl...")
    conn = mysql.connector.connect(
        host='gateway01.us-east-1.prod.aws.tidbcloud.com',
        port=4000,
        user='NDfuuQXvqct8w5L.root',
        password='O9KREUQSja93XZDl',
        ssl_ca='cacert.pem',
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )
    print('Success with O9KREUQSja93XZDl!')
    conn.close()
except Exception as e:
    print('Error with O9KREUQSja93XZDl:', e)

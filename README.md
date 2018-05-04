# O-Kerberos

# Testing
## Test Full Stack
Assumes all services on localhost

	python client.py -c http://127.0.0.1:5000/login -a http://127.0.0.1:5001 -u testclient -p testpass

## Testing Application Server
python /path/to/directory/O-Kerberos/application_server/unit_test.py

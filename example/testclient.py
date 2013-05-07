import json
import logging

from securest.modules.client import SecurestClient
from jinja2 import Template

logging.basicConfig(level=logging.DEBUG)

params = {
	'client_certificate_id': 'client1',
	'client_public_key': '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC4q0hQ6Faa8A+dXEPTHqWtKLKG\nMgP9J3v7NmkYle6i8khHZCVWVSBpG4zpj8A7cf0+UyvcirxoCaKnvFyE1vDDBNx/\n/ckv/tgp4+zQDD1lIFerXEEwiEgKTsJ8SlV03sFb2qq2xRooGY5lMo1AlG6Fgbxm\nrS0Dbau26t27tKm36QIDAQAB\n-----END PUBLIC KEY-----',
	'server_public_key': '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxKrTkA3UVbziDZwPlsQY5zJBE\n4riPZaakJZSwgAQ6bkKpvJuMlOIN0eRQ/eZMwMtOnVqWDWCiMujHiwyFxbFR12Wz\nLjT50Y36DCozDWm3zJnu0bUHP7fdRirhEKQ1B7dEeWwgQcNsOZmy6XFt81drGh3z\nmOnKCD5DfTjzE9xHdwIDAQAB\n-----END PUBLIC KEY-----',
	'server_certificate_id': 'cert123',
	'private_key': '-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQC4q0hQ6Faa8A+dXEPTHqWtKLKGMgP9J3v7NmkYle6i8khHZCVW\nVSBpG4zpj8A7cf0+UyvcirxoCaKnvFyE1vDDBNx//ckv/tgp4+zQDD1lIFerXEEw\niEgKTsJ8SlV03sFb2qq2xRooGY5lMo1AlG6FgbxmrS0Dbau26t27tKm36QIDAQAB\nAoGAcxKYf4In5WhN8pq50Oa6Corfo+uqvKdMBKBFIQLcr0EWdRYchg2JorV+O1RO\nTzyat6mQHV9+Q74tUyR26ngdkfklOp86WN5H3HrW/+OL1vF7uko/3dYiuI/Ve3iz\n3d4fKYg6kcEr076LhKnTnOwbV9jQe8EhIO5cOmmI5hc9v/kCQQDN080v6PoLtfdb\nQvw0Cm39Cx468xsFwMZ1tzl/DqIVxOxPOgKN23veMN07zdz8dODVWXfVAF6aQ/fz\n3Ttha34vAkEA5a8lSteL/VWbt76PSXNapqk9xNQexmO3oHAHI+UNuSUb6XHR5LBk\nrc+TY7U6pgC28HZP6TUEtvAvXRXXmMN9ZwJBAI6D8vUTed8V9dno/bwC5LlrM1lZ\n7wICwufLIDKLrUspeP46in4y1Qe6CdVY64SaYPsY4dJIWTizi0H9kxoXVd0CQGL1\n9L5rYpCTaxVfEIOYJQ27y7Zboqrd2gdRXXI0xZXpDD6n4MSEz8wnrJyAQDW4BxpS\nD5ouUsqzb+TOfWb/i68CQQCRCO1+SgSQnhIl3fPCmFuwAq4/IeImtJoEAdqrb6fj\nlNEV8dAhzEyqn3gmNTK+LCg7yq+BjhmFJTkFuGtiBSgw\n-----END RSA PRIVATE KEY-----',
}

def response_test():
	"""
	Response test.
	"""
	client = SecurestClient(**params)

	data = {'name': 'ashish', 'last': 'dubey'}
	(status, headers, res) = client.make_request(
								'http://localhost:8000/test/', headers={},
								data=json.dumps(data))

	logging.info('Received finally (decrypted): %s' % res)
	return (status, headers, res)

def bad_client_cert():
	"""
	Test with a wrong client certificate.
	Expected: Should give a 'Bad certificate id.' response.
	"""
	global params
	client = SecurestClient(client_certificate_id='client',
				client_public_key=params['client_public_key'],
				server_public_key=params['server_public_key'],
				server_certificate_id=params['server_certificate_id'],
				private_key=params['private_key'])

	data = {'name': 'ashish', 'last': 'dubey'}
	(status, headers, res) = client.make_request(
								'http://localhost:8000/test/',headers={},
								data=json.dumps(data))

	logging.info('Received finally (decrypted): %s' % res)
	return (status, headers, res)

def bad_server_public_key():
	"""
	Test with a wrong server public key.
	Expected: Should give a 'Bad signature.' response.
	"""
	bad_key = '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxKrTkA3UVbziDZwPlsQY5zJBE\n4riPGaakJZSwgAQ6bkKpvJuMlOIN0eRQ/eZMwMtOnVqWDWCiMujHiwyFxbFR12Wz\nLjT50Y36DCozDWm3zJnu0bUHP7fdRirhEKQ1B7dEeWwgQcNsOZmy6XFt81drGh3z\nmOnKCD5DfTjzE9xHdwIDAQAB\n-----END PUBLIC KEY-----',

	global params
	client = SecurestClient(
			client_certificate_id=params['client_certificate_id'],
			client_public_key=params['client_public_key'],
			server_public_key=bad_key,
			server_certificate_id=params['server_certificate_id'],
			private_key=params['private_key'])

	data = {'name': 'ashish', 'last': 'dubey'}
	(status, headers, res) = client.make_request(
								'http://localhost:8000/test/', headers={},
								data=json.dumps(data))

	logging.info('Received finally (decrypted): %s' % res)
	return (status, headers, res)

def bad_client_private_key():
	"""
	Test with a wrong client private key.
	Expected: The final response should not match with the server's response.
	"""
	bad_key = '-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQC4q0hQ6Faa8A+dXEPTHqWtKLKGMgP9J3v7NmkYle6i8khHZCVW\nVSBpG4zpj9A7cf0+UyvcirxoCaKnvFyE1vDDBNx//ckv/tgp4+zQDD1lIFerXEEw\niEgKTsJ8SlV03sFb2qq2xRooGY5lMo1AlG6FgbxmrS0Dbau26t27tKm36QIDAQAB\nAoGAcxKYf4In5WhN8pq50Oa6Corfo+uqvKdMBKBFIQLcr0EWdRYchg2JorV+O1RO\nTzyat6mQHV9+Q74tUyR26ngdkfklOp86WN5H3HrW/+OL1vF7uko/3dYiuI/Ve3iz\n3d4fKYg6kcEr076LhKnTnOwbV9jQe8EhIO5cOmmI5hc9v/kCQQDN080v6PoLtfdb\nQvw0Cm39Cx468xsFwMZ1tzl/DqIVxOxPOgKN23veMN07zdz8dODVWXfVAF6aQ/fz\n3Ttha34vAkEA5a8lSteL/VWbt76PSXNapqk9xNQexmO3oHAHI+UNuSUb6XHR5LBk\nrc+TY7U6pgC28HZP6TUEtvAvXRXXmMN9ZwJBAI6D8vUTed8V9dno/bwC5LlrM1lZ\n7wICwufLIDKLrUspeP46in4y1Qe6CdVY64SaYPsY4dJIWTizi0H9kxoXVd0CQGL1\n9L5rYpCTaxVfEIOYJQ27y7Zboqrd2gdRXXI0xZXpDD6n4MSEz8wnrJyAQDW4BxpS\nD5ouUsqzb+TOfWb/i68CQQCRCO1+SgSQnhIl3fPCmFuwAq4/IeImtJoEAdqrb6fj\nlNEV8dAhzEyqn3gmNTK+LCg7yq+BjhmFJTkFuGtiBSgw\n-----END RSA PRIVATE KEY-----',
	global params
	client = SecurestClient(
			client_certificate_id=params['client_certificate_id'],
			client_public_key=params['client_public_key'],
			server_public_key=params['server_public_key'],
			server_certificate_id=params['server_certificate_id'],
			private_key=bad_key)

	data = {'name': 'ashish', 'last': 'dubey'}
	(status, headers, res) = client.make_request(
								'http://localhost:8000/test/', headers={},
								data=json.dumps(data))

	logging.info('Received finally (decrypted): %s' % res)
	return (status, headers, res)

def tampered_payload():
	"""
	Change the payload without changing the signature
	expected: Should give a 'Bad signature.' response.
	"""
	global params
	client = SecurestClient(**params)

	data = {'name': 'ashish', 'last': 'dubey'}
	(url, headers, content) = client.create_request(
								'http://localhost:8000/test/', headers={},
								data=json.dumps(data))

	(status, headers, res) = client.send((url, headers, 'tampered'))

	logging.info('received finally: %s' % res)
	return (status, headers, res)


tests = [response_test,
	bad_client_cert,
	bad_server_public_key,
	bad_client_private_key,
	tampered_payload]

test_result = []
for test in tests:
	test_func = test

	name = test_func.__doc__
	res = test_func()

	test_result.append({'name': name, 'status': res[0], 'headers': res[1],
		'res': res[2]})

template = Template(open('test_template.html', 'r').read())
open('test_result.html', 'w').write(template.render({'tests': test_result}))
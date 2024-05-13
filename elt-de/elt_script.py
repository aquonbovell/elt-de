import subprocess, time

def wait_for_process(host, max_retries=10, delay=5):
	retries = 0
	while retries < max_retries:
		try:
			result = subprocess.run(['pg_isready', '-h', host], check=True, capture_output=True, text=True)
			if "accepting connections" in result.stdout:
				print("Server is ready to accept Postgres connections")
				return True
		except subprocess.CalledProcessError as e:
			print(f"Error connecting to Postgres: {e}")
			retries += 1
			print(f"Retrying in {delay} seconds... (Attempt {retries}/{max_retries})")
			time.sleep(delay)
	print("Server is not ready to accept Postgres connections")
	print("Max retries reached. Exiting...")
	return False


if not wait_for_process(host="source_postgres"):
	exit(1)

# Continue with the rest of the script
print("Starting ELT process...")

source_config = {
	'dbname': 'source_db',
	'user': 'postgres_user',
	'password': 'postgres_secret',
	'host': 'source_postgres',
}

target_config = {
	'dbname': 'dest_db',
	'user': 'postgres_user',
	'password': 'postgres_secret',
	'host': 'dest_postgres',
}

dump_command = [
	'pg_dump',
	'-h', source_config['host'],
	'-U', source_config['user'],
	'-d', source_config['dbname'],
	'-f', 'data_dump.sql',
	'-w'  # Do not prompt for password
]

subprocess_env = dict(PGPASSWORD=source_config['password'])

subprocess.run(dump_command, env=subprocess_env, check=True)

load_command = [
	'psql',
	'-h', target_config['host'],
	'-U', target_config['user'],
	'-d', target_config['dbname'],
	'-a','-f', 'data_dump.sql',
]

subprocess_env = dict(PGPASSWORD=target_config['password'])

subprocess.run(load_command, env=subprocess_env, check=True)

print("ELT process completed successfully")
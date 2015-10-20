import logging
import argparse
import sys
import psycopg2

    
# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets'")
logging.debug("Database connection established.")

def put(name, snippet):
	"""Store a snippet with an associated name."""
	logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
	cursor = connection.cursor()
	try:
		command = "insert into snippets values (%s, %s)"
		cursor.execute(command, (name, snippet))
	except psycopg2.IntegrityError as e:
		connection.rollback()
		command = "update snippets set message=%s where keyword=%s"
		cursor.execute(command, (snippet, name))
	connection.commit()
	logging.debug("Snippet stored successfully.")
	get(name)
	return name, snippet
			

def get(name):
	"""Retrieve the snippet with a given name.
	
	If there is no such snippet... (create one and be awesome)
	
	Returns the snippet.
	"""
	logging.error("FIXME: Unimplemented - get({!r})".format(name))
	cursor = connection.cursor()
	command = "select * from snippets where keyword='" + name + "'"
	cursor.execute(command)
	#fetchone()'s output is a tuple. You retireve the the values as you do it with arrays
	message = cursor.fetchone()
	connection.commit()
	logging.debug("Snippet fetched successfully.")
	if not message:
		print "No matching keywords found. We're creating new one for you"
		put(name, 'Created one since none found')
		return get(name)
	else:
		return message[0]
			
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    get_parser = subparsers.add_parser("get", help="Get snippet info")
    get_parser.add_argument("name", help="The name of the snippet")
    arguments = parser.parse_args(sys.argv[1:])
	# Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
if __name__ == "__main__":
    main()

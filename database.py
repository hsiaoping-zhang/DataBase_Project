import sqlite3

def search(query):

	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	try:
		cursor = c.execute(query)
		columns = list(map(lambda x: x[0], cursor.description))  # get columns
	# query error
	except Exception as e:
		print("Query Error!!")
		return str(e), [], []

	final = cursor.fetchall()
	conn.close()

	return "Query Success", final, columns


def insert_delete_update(operand, query):
	print("query:", query)
	conn = sqlite3.connect('data.db')
	c = conn.cursor()
	try:
		cursor = c.execute(query)
		conn.commit()
	# insert error
	except Exception as e:
		return str(e)

	conn.close()
	return "%s Success" % operand


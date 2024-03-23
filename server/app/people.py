PEOPLE = {
	'Sirakov': {
		'lname': 'Sirakov',
		'fname': 'Dmitry'
	},
	# ... ещё куча людей
}

def get_all_people():
	return list(PEOPLE.values())


def create_person(body):
    people = body
    lname = people.get("lname", "")
    fname = people.get("fname", "")
    PEOPLE[lname] = {"lname": lname, "fname": fname}


def get_person(lname):
    if lname and lname in PEOPLE:
        return PEOPLE.get(lname, None)
    # Тут надо дописать abort(404, ...)
    
all:

init:
	pybabel extract -F babel.cfg -o messages.pot .
	pybabel init -i messages.pot -d app/translations -l de

update:
	pybabel extract -F babel.cfg -o messages.pot .
	pybabel update -i messages.pot -d app/translations -l de
	

import requests, json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

## My toggl api key
toggletoken = 'some-very-sectet-token-from-toggl-dashboard'

## Quick and dirty localstorage in a simple file...
localfileDB = '/home/andrius/www-vitamin/toggl-data.json'

def updatecache():
	url = 'https://toggl.com/reports/api/v2/details?workspace_id=3112973&user_agent=andrius.daugela@gmail.com&since=2018-11-01&display_hours=decimal'
	result = requests.get(url, auth=(toggletoken, 'api_token')) ## According to toggl docs..
	with open(localfileDB, 'w') as file:
		json.dump(json.loads(result.text), file)
		file.close()

# Fetches all time entries form toggl to a local file
@app.route("/cache")
def cache():
	updatecache()
	return "OK - updated"

# Serves cached time entries from local file
@app.route("/serve")
def serve():
	file = open(localfileDB, 'r')
	json_string = file.read()
	file.close()
	return jsonify(json.loads(json_string))

# Main page
@app.route("/")
def base():
	return render_template("base.html")

# Handle new entries
@app.route("/create-time-entry", methods=['GET', 'POST'])
def createentry():
	if request.method == 'POST':
		url = 'https://www.toggl.com/api/v8/time_entries'

		content = request.json

		description = content['description']
		duration = int(content['duration']) ##duration: time entry duration in seconds
		month = content['month']

		jsonentry = '{"time_entry":{"description":"%s","duration": %d,"start":"2018-%s-04T15:00:00+02:00","pid":148144231,"created_with":"Test app"}}' % (description, duration, month)
		result = requests.post(url, data=jsonentry, auth=(toggletoken, 'api_token')) ## According to toggl docs..

		updatecache()

		return result.content
	else:
		return "Invalid request"

if __name__ == "__main__":
	app.run()
########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '0a262268ddda47fab90091594d36936a',
}

params = urllib.urlencode({
    # Request parameters
    'faceRectangles': '{string}',
})

filePath = "../Data/1450656001/faces/1290435672271888384/112.jpg"
payload = "{ 'url': 'www.inf.kcl.ac.uk/pg/sagarj/images/Sagar_Pic.jpg' }"


def makeEmoRequest(filePath):
	with open(filePath) as image_file:
		encoded_image = base64.b64encode(image_file.read())
	
	try:
		conn = httplib.HTTPSConnection('api.projectoxford.ai')
		conn.request("POST", "/emotion/v1.0/recognize?", payload , headers)
		response = conn.getresponse()
		data = response.read()
		print response.status, response.reason
		conn.close()
	except Exception as e:
		print e
		
if __name__ == '__main__':
    makeEmoRequest(filePath)


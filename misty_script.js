var subscribeMsg = {
    "Operation": "subscribe",
    "Type": "FaceRecognition",
    "DebounceMs": 1000,
    "EventName": "FaceRecognition"
};

var unsubscribeMsg = {
    "Operation": "unsubscribe",
    "EventName": "FaceRecognition"
};

var subMsg = JSON.stringify(subscribeMsg);
var unsubMsg = JSON.stringify(unsubscribeMsg);
var messageCount = 0;
var socket;

function startFaceDetection(){
    socket = new WebSocket("ws://10.11.175.16/pubsub");
    socket.onopen = function(event){
        console.log("Connected to websocket");
        socket.send(subMsg);
    }

    socket.onmessage = function(event){
        var message = JSON.parse(event.data).message;
        console.log(message);
    }

    socket.onerror = function(error){
        console.log("Error: " + error);
    }

    socket.onclose = function(event){
        console.log("Connection closed");
    }
}

startFaceDetection();

//POST http://10.11.175.16/api/faces/detection/start
Promise.race([
	fetch('http://10.11.175.16/api/faces/detection/start', {
		method: 'POST',
		body: '{ }'
	}),
	new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 10000))
])
.then(response => response.json())
.then(jsonData => console.log(jsonData))


////////////////////////////////////////////////////////////
/*
{
    "@odata.context": "https://azureaisearchbishnu.search.windows.net/$metadata#skillsets/$entity",
    "@odata.etag": "\"0x8DCA7E93C7820EC\"",
    "name": "test-skillset",
    "description": "Skillset to generate embeddings",
    "skills": [
      {
        "@odata.type": "#Microsoft.Skills.Vision.VectorizeSkill",
        "name": "image-embedding-skill",
        "description": "",
        "context": "/document",
        "modelVersion": "2023-04-15",
        "inputs": [
          {
            "name": "image",
            "source": "/document"
          }
        ],
        "outputs": [
          {
            "name": "vector",
            "targetName": "imageVector"
          }
        ]
      }
    ],
    "cognitiveServices": {
      "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
      "description": null,
      "key": "0e09d224051146aab52a709978f58837"
    },
    "knowledgeStore": null,
    "indexProjections": null,
    "encryptionKey": null
  }*/
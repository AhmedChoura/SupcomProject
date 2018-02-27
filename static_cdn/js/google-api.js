if('webkitSpeechRecognition' in window){
	var speechRecognizer = new webkitSpeechRecognition();
	speechRecognizer.continuous = true;
	speechRecognizer.interimResults = true;
	speechRecognizer.lang = 'en-US';
	$('#trash2').click(function (event) {
		event.preventDefault();
		speechRecognizer.start();

		var finalTranscripts = '';

		speechRecognizer.onresult = function(event){
			var interimTranscripts = '';
			for(var i = event.resultIndex; i < event.results.length; i++){
				var transcript = event.results[i][0].transcript;
				transcript.replace("\n", "<br>");
				if(event.results[i].isFinal){
					finalTranscripts += transcript;
				
				}else{
					interimTranscripts += transcript;
				}
			}
			$('#result').text(finalTranscripts + interimTranscripts);

			if (interimTranscripts == 'username') {
				var finalTranscripts = '';
				speechRecognizer.onresult = function(event){
					var interimTranscripts = '';
					for(var i = event.resultIndex; i < event.results.length; i++){
						var transcript = event.results[i][0].transcript;
						transcript.replace("\n", "<br>");
						if(event.results[i].isFinal){
							finalTranscripts += transcript;
							$('#id_username').val(transcript)
						
						}else{
							interimTranscripts += transcript;
						}
					}
					$('#result').text(finalTranscripts + interimTranscripts);
					
				};
			} else if (interimTranscripts == 'password'){
				var finalTranscripts = '';
				speechRecognizer.onresult = function(event){
					var interimTranscripts = '';
					for(var i = event.resultIndex; i < event.results.length; i++){
						var transcript = event.results[i][0].transcript;
						transcript.replace("\n", "<br>");
						if(event.results[i].isFinal){
							finalTranscripts += transcript;
							$('#id_password').val(transcript)
						
						}else{
							interimTranscripts += transcript;
						}
					}
					$('#result').text(finalTranscripts + interimTranscripts);
					
				};
				
			}else if(interimTranscripts == 'submit') {
				$('#login').click();
				speechRecognizer.stop() ;
			}

			
		};
	})
	$('#trash3').click(function (event) {
		event.preventDefault();
		speechRecognizer.stop() ;	
	})

}else{
	r.innerHTML = 'Your browser is not supported. If google chrome, please upgrade!';
}


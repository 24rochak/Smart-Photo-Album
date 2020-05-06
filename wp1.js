function encodeImageFileAsURL(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
      //console.log('RESULT', reader.result)
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this);
        }
    };
    xhttp.open("POST", "https://jqqqx4qdnd.execute-api.us-east-1.amazonaws.com/prod/upload-to-s3", false);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(reader.result));
    }
    reader.readAsDataURL(file);
  }
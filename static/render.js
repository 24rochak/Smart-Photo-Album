

document.getElementById("displaytext").style.display = "none";

function searchPhoto()
{

  //var apigClient = apigClientFactory.newClient();

    // document.getElementById("displaytext").innerHTML = ""
    // document.getElementById("img-container").innerHTML = "";
    // document.getElementById("displaytext").innerHTML = "";

    var user_message = document.getElementById('transcript').value;
    console.log(user_message)

  //   var body = { };
  //   var params = {q : user_message};
  //   var additionalParams = {headers: {
  //   'Content-Type':"application/json"
  // }};

  //   apigClient.searchGet(params, body , additionalParams).then(function(res){
  //       var data = {}
  //       var data_array = []
  //       resp_data  = res.data
  //       length_of_response = resp_data.length;
  //       if(length_of_response == 0)
  //       {
  //         document.getElementById("displaytext").innerHTML = "No Images Found !!!"
  //         document.getElementById("displaytext").style.display = "block";

  //       }

  //       resp_data.forEach( function(obj) {

  //           var img = new Image();
  //           //img.src = "https://s3.amazonaws.com/photo-s3/"+obj;
  //           img.src = "https://s3.amazonaws.com/photo-s3/"+user_message;
  //           img.setAttribute("class", "banner-img");
  //           img.setAttribute("alt", "effy");
  //           document.getElementById("displaytext").innerHTML = "Images returned are : "
  //           document.getElementById("img-container").appendChild(img);
  //           document.getElementById("displaytext").style.display = "block";

  //         });
  //     }).catch( function(result){

  //     });

  var requestOptions = {
  method: 'GET',
  redirect: 'follow'
};
user_message = " ' " + user_message + " ' ";
url = "https://ik2j7rq6eg.execute-api.us-east-1.amazonaws.com/p/search?photo=" + user_message;
console.log(url);
var res = " ";

// fetch(url, requestOptions)
//   .then(response => response.text())
//   .then(result => res = JSON.parse(result))
//   .catch(error => console.log('error', error));


fetch(url, requestOptions)
  .then(response => response.text())
  .then(result => {
    var res = JSON.parse(result)
    console.log(res);
    for (image in res.photos) {
      console.log(res.photos[image]);
      var img = new Image();
      img.src = "https://s3.amazonaws.com/photo-s3/"+res.photos[image];
      img.setAttribute("class", "banner-img");
      img.setAttribute("alt", "effy");
      document.getElementById("displaytext").innerHTML = "Images returned are : "
      document.getElementById("img-container").appendChild(img);
      document.getElementById("displaytext").style.display = "block";
    }
    
  })
  .catch(error => console.log('error', error));

  //.then(result => console.log(result))
  console.log(res)


  // var img = new Image();
  // img.src = "https://s3.amazonaws.com/photo-s3/photos/"+user_message;
  // img.setAttribute("class", "banner-img");
  // img.setAttribute("alt", "effy");
  // document.getElementById("displaytext").innerHTML = "Images returned are : "
  // document.getElementById("img-container").appendChild(img);
  // document.getElementById("displaytext").style.display = "block";
}

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    // reader.onload = () => resolve(reader.result)
    reader.onload = () => {
      let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
      if ((encoded.length % 4) > 0) {
        encoded += '='.repeat(4 - (encoded.length % 4));
      }
      resolve(encoded);
    };
    reader.onerror = error => reject(error);
  });
}



function uploadPhoto()
{

   var file_data;
   // var file = document.querySelector('#file_path > input[type="file"]').files[0];
   var file = document.getElementById('file_path').files[0];
   const reader = new FileReader();
   var file_data;
  //  var encoded_image = getBase64(file).then(
  //    data => {
  //    //console.log(data)
  //    var apigClient = apigClientFactory.newClient();

  //    // var data = document.getElementById('file_path').value;
  //    // var x = data.split("\\")
  //    // var filename = x[x.length-1]
  //    var file_type = file.type + ";base64"

  //    var body = file
  //    var params = {"key" : file.name, "bucket" : "test-photo-storage", "Content-Type" : file.type};
  //    var additionalParams = {
  //     // If there are any unmodeled query parameters or headers that must be
  //     //   sent with the request, add them here.
  //     headers: {
  //       "Content-Type" : file.type, 
  //       "ContentEncoding": "base64"
  //     }
  //   };
  //    apigClient.uploadBucketKeyPut(params, body , additionalParams).then(function(res){
  //      if (res.status == 200)
  //      {
  //        document.getElementById("uploadText").innerHTML = "Image Uploaded  !!!"
  //        document.getElementById("uploadText").style.display = "block";
  //      }
  //    })
  //  });

  // let config = {
  //     headers: { 'Content-Type': file.type }
  // };
  // //url = 'https://cors-anywhere.herokuapp.com/https://ldtdq1nrgb.execute-api.us-east-1.amazonaws.com/s1/upload/test-photo-storage/' + file.name
  // url = 'https://ik2j7rq6eg.execute-api.us-east-1.amazonaws.com/p/upload/' + file.name 
  // axios.put(url, file, config).then(response => {
  //     // console.log(response.data)
  //     alert("Image uploaded successfully!");
  // });


  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "image/jpeg");


  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: file,
    redirect: 'follow'
  };

  fetch("https://ik2j7rq6eg.execute-api.us-east-1.amazonaws.com/p/upload/", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));

}
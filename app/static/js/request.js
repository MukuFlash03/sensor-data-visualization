// This file contains a refreshPlots() function to make an asynchronous GET request to the server
// and refresh the plots on the page. It is called by the refresh button on the page.
// The callback function is called when the request is successful and the response is received.
// The callback function should take the response as an argument and use it to update the plots.
// The callback function should be defined in the file that calls refreshPlots().
// The callback function should be passed to refreshPlots() as an argument.


export function refreshPlots(endpoint, callback) {

  // Get the start and end times from the form
  const refreshButton = document.getElementById("refresh");
  const startTime = document.getElementById("start-time").value;
  const endTime = document.getElementById("end-time").value;

  console.log(startTime + " to " + endTime);

  refreshButton.disabled = true;
  refreshButton.innerHTML = "Refreshing...";

  // Create a new request
  const request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      // Wait 750ms before re-enabling the refresh button
      setTimeout(function() {
          refreshButton.disabled = false;
          refreshButton.innerHTML = "Refresh Data";
        }, 750); 
      callback(request.response);
    } else if (this.readyState == 4) {
      alert("Error: " + this.statusText);
      refreshButton.disabled = false;
      refreshButton.innerHTML = "Refresh Data";
    }
  };

  // Add the start and end times to the endpoint
  let endpointTime = "?start_time=" + startTime + "&end_time=" + endTime

  // Make the request
  request.open("GET", endpoint + endpointTime, true);
  request.send();
}
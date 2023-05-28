/*
Load the plot data buttons and handle the click events
for the download and refresh buttons.
The download button should download a CSV file of the data.
The refresh button should refresh the plots on the page.
The refresh button should call the refreshPlots() function from request.js.
The refresh button should pass the showStatus() function as a callback to refreshPlots().
The showStatus() function should be defined in this file.
The showStatus() function should take the response as an argument and use it to update the status text.
The showStatus() function should be called by the callback function in request.js.
*/
import { refreshPlots } from "./request.js";

export class PlotData {

  // Load the plot data buttons and handle the click events
    constructor() {
      this.plotdata = document.querySelector(".plot-buttons");
      this.downloadButton = this.plotdata.querySelector(".download");
      this.downloadButton.addEventListener("click", this.handleDownloadClick.bind(this));
      this.refreshButton = this.plotdata.querySelector(".refresh");
      this.refreshButton.addEventListener("click", this.handleRefreshClick.bind(this));
    }

    // Handle the download button click event
    handleDownloadClick(event) {
      event.preventDefault();
      const startTime = document.getElementById("start-time").value;
      const endTime = document.getElementById("end-time").value;
      console.log(startTime + " to " + endTime);

      // Redirect to the endpoint with the start and end times
      const endpoint = '/csv';
      let endpointTime = "?start_time=" + startTime + "&end_time=" + endTime;
      window.location.href = endpoint + endpointTime;
    }

    // Handle the refresh button click event
    handleRefreshClick(event) {
      event.preventDefault();

      // Refresh the plots
      // const endpoint = '/refresh';
      const endpoint = '/';
      refreshPlots(endpoint, this.showStatus);
    }

    // Update the status text
    showStatus(data) {
      let statusText = document.querySelector(".status");
      console.log("Status: \n" + data);
    }
  }
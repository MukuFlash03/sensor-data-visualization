import { PlotData } from "./plotData.js";

function main() {
  if (document.querySelector(".plot-app")) {
    const plotdata = new PlotData();
    plotdata.showStatus("Initiated");
  }
}

main();
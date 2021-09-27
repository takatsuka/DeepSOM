
// Function to be called when valid data file is passed
const processDataFile = (file) => {
    // Open data file for reading
    let fr = new FileReader();
    fr.readAsText(file);

    // Event listeners to trigger 
    fr.addEventListener('loadStart', changeStatus('starting loading'));
    fr.addEventListener('load', changeStatus('loaded'));
    fr.addEventListener('loadend', dataLoaded);
    fr.addEventListener('progress', setProgress);
    fr.addEventListener('error', errorHandler);
}

// Function to be called when valid weights file is passed
const processWeightsFile = (file) => {
    // Open weights file for reading
    let fr = new FileReader();
    fr.readAsText(file);

    // Event listeners to trigger
    fr.addEventListener('loadStart', changeStatus('starting loading'));
    fr.addEventListener('load', changeStatus('loaded'));
    fr.addEventListener('loadend', weightsLoaded)
    fr.addEventListener('progress', setProgress);
    fr.addEventListener('error', errorHandler);
}

// Function to update file reading status message
const changeStatus = (status) => {
    document.getElementById('status').innerHTML = status;
}

// File reader event listener to trigger file read progress visualisation
const setProgress = (e) => {
    const fr = e.target;
    const loadingPercentage = 100 * e.loaded / e.total;
    document.getElementById('progress-bar').value = loadingPercentage;
}

// File reader event listener to trigger when data file has been loaded
const dataLoaded = (e) => {
    const fr = e.target;
    let data = fr.result;
    dataCoordinates = loadData(data);
    currentCoordinates = dataCoordinates;
    updatePlot();
    // Show svg plot now that data has been loaded
    document.getElementById('plot').style.display = "block";
}

// File reader event listener to trigger when weights file has been loaded
const weightsLoaded = (e) => {
    const fr = e.target;
    let weights = fr.result;
    weightsCoordinates = loadData(weights);
    // Show slider now that weights have been loaded
    document.getElementById("progressSlider").style.display = "block";
    document.getElementById("progressSlider").oninput = updateProgressPlot;
}

// File reader event listener to trigger when file read has error
const errorHandler = (e) => {
    changeStatus('Error: ' + e.target.error.name);
}

// Function to run when file is successfully loaded and contents are read in
function loadData(data) {
    scatter = [], xLine = [], yLine = [], zLine = [];
    var counter = 0; // For assigning point IDs
    
    // Preprocess data
    data = data.trim();
    let lines = data.split("\n");

    // Iterate through each line of data
    for (let i = 0; i < lines.length; i++) {
        let tokens = lines[i].split(",");
        let pointX = parseFloat(tokens[0]);
        let pointY = parseFloat(tokens[1]);
        let pointZ = parseFloat(tokens[2]);
        // Append float data to list
        scatter.push({x: pointX, y: pointY, z: pointZ, id: 'point_' + counter++});
    }

    // Define values for xyz scales
    for (let i=-1; i <= 1; i=i+0.5) {
        xLine.push([-i, 1, -1]);
        yLine.push([-1, i, -1]);
        zLine.push([-1, 1, -i]);
    }

    // Input data for d3 drawing
    var result = [
        scatter,
        [xLine],
        [yLine],
        [zLine]
    ];

    return result;
}
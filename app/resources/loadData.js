
// Function to be called when valid file is passed
const processFile = (file) => {
    // Open file for reading
    const fr = new FileReader();
    fr.readAsText(file);

    // Event listeners to trigger 
    fr.addEventListener('loadStart', changeStatus('starting loading'));
    fr.addEventListener('load', changeStatus('loaded'));
    fr.addEventListener('loadend', loaded);
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

// File reader event listener to trigger when file has been loaded
const loaded = (e) => {
    const fr = e.target;
    var data = fr.result;
    loadData(data);
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
        point3d(scatter),
        xScale3d([xLine]),
        yScale3d([yLine]),
        zScale3d([zLine])
    ];

    // Preprocess data array
    processData(result, 1000);
}
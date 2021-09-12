var currentSlide = null;
var totalSoms = 0;

// Overwrites submit SOM button to constantly query worker for status
function overwrite_submit_som(){
    $('#som_wtform').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        var graph = extract_graph();
        if (graph["success"] == false) {
            alert(graph["result"]);
            return null;
        }
        graph = JSON.stringify(graph["result"]);
        formData.append("graph", graph);
        $.ajax({
            type: "POST",
            url: $('#som_wtform').attr('action'),
            data: formData, 
            success: function(data) {
                console.log(data)
                if (data.result==42) {
                  get_status(data.status_url, data.task_id)
                } else {
                  alert(data.result)
                }
            },
            contentType: false,
            processData: false
        });
    });
}

// Get SOM worker status
function get_status(status_url, task_id) {
    var som_img = document.getElementById(task_id);
    if (som_img == null) {
        hideAll()// hide all iframes, then present the new frame
        currentSlide = totalSoms
        totalSoms += 1
        $('<iframe id=' +task_id+ ' height="550" class="sompic""></iframe>').appendTo('#somgallery')
        $('<div class=pnums>' + totalSoms.toString() + '/' + totalSoms.toString() + '</div>').appendTo('#somgallery')
        som_img = document.getElementById(task_id);
    }
    
    $.getJSON(status_url, function(data) {
        if (data['state'] == 'PENDING' || data['state'] == 'WORKING' || data['state'] == 'VISUALISING') {
            som_img.src = data['display_url'];
            setTimeout(function() {
                get_status(status_url, task_id);
            }, 2000);
        } else {
            som_img.src = data['display_url'];
        }
    });
}

function hideAll(){
    var gallery = document.getElementsByClassName("sompic");
    var nums = document.getElementsByClassName("pnums");
    var next = document.getElementsByClassName("next");
    var prev = document.getElementsByClassName("prev");
    for(i = 0;i < gallery.length;i++){ // hide all iframes, numbers
        gallery[i].style.display = "none";
        nums[i].style.display = "none";
    }
    next[0].style.display = "block";
    prev[0].style.display = "block";
}
// Open help overlay
function open_overlay() {
    document.getElementById("info_popup").style.display = "block";
}
//Close help overlay
function close_overlay() {
    document.getElementById("info_popup").style.display = "none";
}

function moveSlide(val){
    display(currentSlide += val);
}

function display(newIndex){
    var gallery = document.getElementsByClassName("sompic");
    var nums = document.getElementsByClassName("pnums");
    if(newIndex >= totalSoms){
        currentSlide = 0;
    }
    else if(newIndex < 0){
        currentSlide = totalSoms - 1;
    }
    for(i = 0;i < gallery.length;i++){ // hide all 
        gallery[i].style.display = "none";
        nums[i].style.display = "none";
        nums[i].innerHTML = (i+1).toString() + "/" + totalSoms.toString();
    }
    nums[currentSlide].style.display = "block"; // display for current
    gallery[currentSlide].style.display = "block";
}
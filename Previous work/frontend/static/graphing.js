var init = true;
var tagged = null;
var line_starts = {};
var line_ends = {};
var som_params = {};
var current_param = null;

const param_options = ["Side Length", "Learning Rate", "Neighbourhood Radius", "Decay Constant", "Input Dimensions"];
const default_val = ["10 10", 0.5, 0, 0, "null"];
const min_val = [1, 0, 0, 0, 0];
const max_val = [null, 1, null, null, null];
const is_list = [true, false, false, false, true];
const parser = [parseListInput, parseFloat, parseInt, parseFloat, parseListInput];

// Generates a UUID for identifying dynamically created nodes
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
}

// Binds the add button to create a new draggable SOM
function bind_add_button() {
    $("#add-button").click(function(){
        var id = uuidv4();
        $("<div class='draggable' style='background-color: white;top: 10px;left: 10px;' onclick='tag(event, this)'>SOM</div>")
            .appendTo('#containment-wrapper')
            .attr("id", id)
            .draggable({ 
                containment: "parent",
                drag: function( event, ui ) {
                    redraw_lines(ui['helper'][0]);
                }
            });
        if (init) {
            init = false;
            delete_line(null, line_starts['input-node'][0]);
        }
        var form = create_form();
        som_params[id] = form;
        highlight(id);
    });
}

// Creates the default input and output nodes in the graphing UI
function init_input_output() {
    const input_node = $("<div id='input-node' class='draggable' style= 'top: 5px; left: 5px; background-color: lightblue' onclick='tag(event, this, true)'>Input</div>")
    const output_node = $("<div id='output-node' class='draggable' style= 'bottom: 5px; right: 5px; background-color: lightblue' onclick='tag(event, this, true)'>Output</div>")

    input_node.appendTo('#containment-wrapper');
    output_node.appendTo('#containment-wrapper');

    var form = create_form();
    som_params['output-node'] = form;

    draw_line(input_node, output_node);
    highlight("output-node");
}

// Returns the centre, radius and x-y offset of given elements
function get_centre(jquery_element, jquery_element2 = null) {
    const radius = jquery_element.height()/2;
    const offset = Math.sqrt(Math.pow(radius,2)/2);
    const pos = jquery_element.position();
    const centre_x1 = pos.left + offset;
    const centre_y1 = pos.top + offset;
    if (jquery_element2 == null) {
        return [centre_x1, centre_y1, radius, offset];
    }
    const pos2 = jquery_element2.position();
    const centre_x2 = pos2.left + offset;
    const centre_y2 = pos2.top + offset;
    return [centre_x1, centre_y1, centre_x2, centre_y2, radius, offset];
}

// Given a line start, line end and element radius returns a new line
// end that points at the nearest edge of the end element
function get_line_end(start_x, start_y, end_x, end_y, radius) {
    const vector_x = end_x - start_x;
    const vector_y = end_y - start_y;
    const vector_length = Math.sqrt(Math.pow(vector_x,2)+Math.pow(vector_y,2));
    const final_x = start_x + vector_x/vector_length*(vector_length-radius-3);
    const final_y = start_y + vector_y/vector_length*(vector_length-radius-3);

    return [final_x, final_y];
}

// draws a line between 2 elements
function draw_line(element1, element2) {
    var centre_info = get_centre(element1, element2);
    var line_end = get_line_end(centre_info[0],centre_info[1],centre_info[2],centre_info[3],centre_info[4],centre_info[5]);

    var newLine = document.createElementNS('http://www.w3.org/2000/svg','line');
    newLine.setAttribute('marker-end',"url(#red-arrowhead)");
    newLine.setAttribute('stroke','#746ce0');
    newLine.setAttribute('stroke-width',2.5);
    newLine.setAttribute('style','cursor: pointer');
    newLine.setAttribute('x1',centre_info[0]);
    newLine.setAttribute('y1',centre_info[1]);
    newLine.setAttribute('x2',line_end[0]);
    newLine.setAttribute('y2',line_end[1]);
    newLine.setAttribute('endcentrex',centre_info[2]);
    newLine.setAttribute('endcentrey',centre_info[3]);
    newLine.setAttribute('start',element1.attr('id'));
    newLine.setAttribute('end',element2.attr('id'));
    newLine.setAttribute('onclick','delete_line(event, this)');

    if (line_starts[element1.attr('id')] == null) {
        line_starts[element1.attr('id')] = [newLine]
    } else {
        line_starts[element1.attr('id')].push(newLine);
    }
    if (line_ends[element2.attr('id')] == null) {
        line_ends[element2.attr('id')] = [newLine]
    } else {
        line_ends[element2.attr('id')].push(newLine);
    }

    $("#line-container").append(newLine);
}

// Dynamically redraws lines as elements are dragged around
function redraw_lines(element) {
    var element_jquery = $(element);
    var element_id = element_jquery.attr('id');
    if (line_starts[element_id] != null) {
        var centre = get_centre(element_jquery);
        for (var line of line_starts[element_id]) {
            line.setAttribute('x1',centre[0]);
            line.setAttribute('y1',centre[1]);
            var line_end = get_line_end(centre[0], centre[1], parseFloat($(line).attr('endcentrex')), parseFloat($(line).attr('endcentrey')), centre[2]);
            line.setAttribute('x2',line_end[0]);
            line.setAttribute('y2',line_end[1]);
        }
    }
    if (line_ends[element_id] != null) {
        var centre = get_centre(element_jquery);
        for (var line of line_ends[element_id]) {
            var line_end = get_line_end(parseFloat($(line).attr('x1')), parseFloat($(line).attr('y1')), centre[0], centre[1], centre[2]);
            line.setAttribute('x2',line_end[0]);
            line.setAttribute('y2',line_end[1]);
            line.setAttribute('endcentrex',centre[0]);
            line.setAttribute('endcentrey',centre[1]);
        }
    }
}

// Deletes a given line and cleans up the line_ends, line_start associative arrays
function delete_line(event, element) {
    if (event == null || event.ctrlKey) {
        const start_node_id = $(element).attr('start');
        var remove_idx = line_starts[start_node_id].indexOf(element);
        if (remove_idx > -1) {
            if (line_starts[start_node_id].length == 1) {
                delete line_starts[start_node_id];
            } else {
                line_starts[start_node_id].splice(remove_idx, 1);
            }
        } else {
            console.log("Could not find line in starting nodes");
        }

        const end_node_id = $(element).attr('end');
        remove_idx = line_ends[end_node_id].indexOf(element);
        if (remove_idx > -1) {
            if (line_ends[end_node_id].length == 1) {
                delete line_ends[end_node_id];
            } else {
                line_ends[end_node_id].splice(remove_idx, 1);
            }
        } else {
            console.log("Could not find line in ending nodes");
        }
        element.parentNode.removeChild(element);
    }
}

// elements tagged with SHIFT mark the start/end of a line to be craeted
// elements tagged with CTRL are to be deleted
function tag(event, element, disable_delete=false) {
    if (event.ctrlKey) {
        if (!disable_delete) {
            var element_id = $(element).attr('id');
            if (line_starts[element_id] != null) {
                var ele_line_starts = [...line_starts[element_id]];
                for (var line of ele_line_starts) {
                    delete_line(null, line);
                }
            }

            if (line_ends[element_id] != null) {
                var ele_line_ends = [...line_ends[element_id]];
                for (var line of ele_line_ends) {
                    delete_line(null, line);
                }
            }
            if (current_param == element_id) {
                highlight('output-node');
            }
            som_params[element_id].remove();
            delete som_params[element_id];
            element.parentNode.removeChild(element);
        }
        if (tagged == element) {
            create_tag(null);
        }
    } else if (event.shiftKey) {
        if (tagged == null) {
            // Tag new element
            create_tag(element);
        } else if (tagged == element ){
            // Untag if shift clicked twice
            create_tag(null);
        } else {
            // Draw a line
            var element1 = $(tagged);
            var element2 = $(element);
            draw_line(element1, element2);
            create_tag(null);
        }
    } else {
        // Display SOM parameters and highlight otherwise
        highlight($(element).attr('id'));
    }
}

function highlight(element_id) {
    if (element_id == 'input-node') {
        return
    }
    if (current_param != null) {
        $("#"+current_param).css("border","2px solid rgb(0,0,0)");
    }

    if (element_id != "input_node"){
        $(som_params[current_param]).hide();
        $(som_params[element_id]).show();
        current_param = element_id;
        $("#"+element_id).css("border","2px solid rgb(0,0,255)");
    }

}

function create_tag(element) {
    if (tagged != null) {
        $(tagged).css("border","2px solid rgb(0,0,0)");
        highlight(current_param);
    }
    if (element == null) {
        tagged = null;
    } else {
        tagged = element;
        $(tagged).css("border","2px solid rgb(255,0,0)");
    }
}

// Creates and returns a new SOM parameter form
function create_form() {
    var form = document.createElement("table");

    // Adding iterations input
    var tr, td_label, td_input, input;
    for (var i=0; i<param_options.length; i++) {
        tr = document.createElement('tr');
        td_label = document.createElement('td');
        td_label.innerHTML = param_options[i];
        td_input = document.createElement('td');
        input = document.createElement("input"); 
        if (is_list[i]) {
            input.setAttribute("type", "text");
            input.addEventListener('input', function() {
                this.value = this.value.replace(/[^0-9 ]/, '');
            });
        } else {
            input.setAttribute("type", "number");
        }
        input.setAttribute("placeholder", default_val[i]);
        td_input.appendChild(input);
        tr.appendChild(td_label);
        tr.appendChild(td_input);
        form.appendChild(tr);
    }

    $(form).appendTo("#som_form")
    return form;
}

function parseListInput(input) {
    if (input == "null"){
        return null;
    }
    input = input.split(/ +/);
    for(var i=0; i<input.length;i++) input[i] = parseInt(input[i]);
    return input;
}


// Extracts the SOM network graph and parameters
// Returns associative array of the form 
// {node : {parameters:{}, neighbours:[] }}
// Returns false on bad graph structure
function extract_graph() {
    // Nothing connected to input node
    if (line_starts['input-node']==null) {
        return {"success":false, "result":"Invalid graph structure: input node not connected"};
    }

    var result = {};
    // BFS starting from the input node
    var to_visit = ['input-node'];
    var visited = {};
    while (to_visit.length > 0) {
        curr = to_visit.pop();
        visited[curr] = true;
        result[curr] = {"parameters":{}, "neighbours":new Array()};
        // Grabbing neighbours
        if (line_starts[curr] != null) {
            for (var line of line_starts[curr]) {
                var endpoint = $(line).attr('end');
                if (!result[curr]["neighbours"].includes(endpoint)) {
                    result[curr]["neighbours"].push(endpoint);
                }
                if (!visited[endpoint]) {
                    to_visit.push(endpoint);
                }
                
            }
        }
        // Extracting parameters
        if (som_params[curr] != null) {
            for (var i=0; i < som_params[curr].rows.length; i++) {
                if (som_params[curr].rows[i].cells[1].children[0].value == "") {
                    result[curr]["parameters"][param_options[i]] = parser[i](default_val[i]);
                } else {
                    result[curr]["parameters"][param_options[i]] = 
                        parser[i](som_params[curr].rows[i].cells[1].children[0].value);
                }
                if (result[curr]["parameters"][param_options[i]] == null) {
                    continue;
                }
                if (is_list[i]) {
                    for (var x of result[curr]["parameters"][param_options[i]]) {
                        if (x < min_val[i]) {
                                return {"success":false, "result":param_options[i]+ " less than min value"};
                        }
                        if (max_val[i] != null && x > max_val[i]) {
                            return {"success":false, "result":param_options[i]+ " larger than max value"};
                        }
                    }
                } else {
                    if (result[curr]["parameters"][param_options[i]] < min_val[i]) {
                        return {"success":false, "result":param_options[i]+ " less than min value"};
                    }
                    if (max_val[i] != null && result[curr]["parameters"][param_options[i]] > max_val[i]) {
                        return {"success":false, "result":param_options[i]+ " larger than max value"};
                    }
                }
            }
        } 
    }

    // Verify the final SOM is connected
    if (result['output-node'] == null) {
        return {"success":false, "result":"Invalid graph structure: output node not connected"};
    }

    visited = {};
    var traversing = {};
    if (!traverse(result, 'input-node', visited, traversing)) {
        return {"success":false, "result":"graph has a cycle"};
    }

    console.log(result);
    
    return {"success":true, "result":result};
}

function traverse(graph, node, visited, traversing) {
    traversing[node] = true;
    visited[node] = true;
    for (var n of graph[node]["neighbours"]) {
        if (visited[n]!=true) {
            if (traverse(graph, n, visited, traversing) == false) {
                return false;
            }
        } else if (traversing[n] == true) {
            return false;
        }
        
    }
    traversing[node] = false;
    return true;
}
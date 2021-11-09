const regeneratorRuntime = require("regenerator-runtime");
const MAX_RETRIES = 5;
const RETRY_DELAY = 100;

// command prompt controller
$(document).ready(async function() {

    debug_log("Welcome to PySOM Shell V0.0.1");

    $("#cmd").submit(function(e) {
        $("#test-overlay").show();
        cmd = $("#cmd input").val();
        $("#cmd input").val("");
        e.preventDefault();

        debug_log(`>>>> ${cmd}`);


        // process command
        switch (cmd) {
            case "open":
                $("#test-overlay").show();
                break;
            case "close":
                $("#test-overlay").hide();
                break;
            case "stress":
                editor_stress();
                break;
            case "complex":
                editor_dist();
                break
            case "complex_full":
                editor_complex();
                break
            case "ls":
                debug_log("stress_editor");
                debug_log("complex_full");
                debug_log("complex");
                debug_log("random");
                debug_log("dance1");
                debug_log("dance2");
                break
            default:
                debug_log("Unknown command");
        }

    });
});

// automation scripts
async function editor_stress() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

    await click("#view-btn");
    await click("#menu-editor");

    await update_location(input_node_id, 850, 100);
    await update_location(output_node_id, 450, 950);

    for (var i = 3; i < 15; i++) {
        await click("#add-node-btn");
        await click("#single-som-btn");
        await update_location(`#ddn_${i}`, 140 * (i - 2), 300);

        await click("#add-link-btn")
        await click(input_node_btn_id)
        await click(`#ddn_add_${i}`)

        await click("#add-link-btn")
        await click(`#ddn_add_${i}`)
        await click(output_node_btn_id)
    }

    for (var i = 15; i < 27; i++) {
        await click("#add-node-btn");
        await click("#sampler-btn");
        await update_location(`#ddn_${i}`, 140 * (i - 14), 600);

        await click("#add-link-btn")
        await click(`#ddn_add_${i-1}`)
        await click(`#ddn_add_${i}`)
    }

    for (var i = 27; i < 35; i++) {
        await click("#add-node-btn");
        await click("#bypass-btn");
        await update_location(`#ddn_${i}`, 2000, 300 + 110 * (i - 26));

        await click("#add-link-btn")
        await click(`#ddn_add_${i-1}`)
        await click(`#ddn_add_${i}`)
    }

    for (var i = 35; i < 43; i++) {
        await click("#add-node-btn");
        await click("#bypass-btn");
        await update_location(`#ddn_${i}`, 2150, 300 + 110 * (43 - i));

        await click("#add-link-btn")
        await click(`#ddn_add_${i-1}`)
        await click(`#ddn_add_${i}`)
    }

    for (var i = 43; i < 51; i++) {
        await click("#add-node-btn");
        await click("#bypass-btn");
        await update_location(`#ddn_${i}`, 2300, 300 + 110 * (i - 42));

        await click("#add-link-btn")
        await click(`#ddn_add_${i-1}`)
        await click(`#ddn_add_${i}`)
    }
}

async function editor_dist(){
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";
    await update_location(input_node_id, 9, 9);
    await update_location(output_node_id, 1089, 311);
    await update_location(`#ddn_3`, 23, 169);

    await contextmenu("#ddn_3");
    await update_value("#dist-ip1", "3,4,5,6,7,8,9,10,11,12");
}

async function editor_complex() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";



    // SOM SIZE
    await contextmenu("#ddn_4");
    await update_value("#input-name", "Size");
    await update_value("#input-trainiter", "10000");
    await click(".bp3-drawer-header button");
    await update_location(`#ddn_4`, 221, 144);

    // Calibrate
    await click("#add-node-btn");
    await click("#calibrate-btn");
    await update_location(`#ddn_5`, 413, 52);

    await click("#add-link-btn");
    await click("#ddn_add_4");
    await click("#ddn_add_5");

    // SOM REST
    await click("#add-node-btn");
    await click("#single-som-btn");
    await contextmenu("#ddn_6");
    await update_value("#input-name", "Rest");
    await update_value("#input-indim", "10");
    await update_value("#input-dim", "10");
    await click(".bp3-drawer-header button");
    await update_location(`#ddn_6`, 223, 397);

    await click("#add-link-btn");
    await click("#ddn_add_3");
    await click("#ddn_add_6");

    await contextmenu("#ddn_3");
    await update_value("#input-outgoing-1", 2);
    await click(".bp3-drawer-header button");

    // Calibrate
    await click("#add-node-btn");
    await click("#calibrate-btn");
    await update_location(`#ddn_7`, 463, 637);

    await click("#add-link-btn");
    await click("#ddn_add_6");
    await click("#ddn_add_7");

    // BMU TOP
    await click("#add-node-btn");
    await click("#get-bmu-btn");
    await update_location(`#ddn_8`, 492, 211);

    await click("#add-link-btn");
    await click("#ddn_add_4");
    await click("#ddn_add_8");

    // BMU bottom
    await click("#add-node-btn");
    await click("#get-bmu-btn");
    await update_location(`#ddn_9`, 512, 466);

    await click("#add-link-btn");
    await click("#ddn_add_6");
    await click("#ddn_add_9");

    // Concat
    await click("#add-node-btn");
    await click("#concatenator-btn");
    await update_location(`#ddn_10`, 561, 309);

    await click("#add-link-btn");
    await click("#ddn_add_8");
    await click("#ddn_add_10");

    await click("#add-link-btn");
    await click("#ddn_add_9");
    await click("#ddn_add_10");

    // SOM right

    await click("#add-node-btn");
    await click("#single-som-btn");
    await contextmenu("#ddn_11");
    await update_value("#input-indim", "13");
    await update_value("#input-dim", "10");
    await click(".bp3-drawer-header button");
    await update_location(`#ddn_11`, 775, 256);

    await click("#add-link-btn");
    await click("#ddn_add_10");
    await click("#ddn_add_11");

    await contextmenu("#ddn_8");
    await update_value("#input-outgoing-0", 1);
    await click(".bp3-drawer-header button");
    await contextmenu("#ddn_9");
    await update_value("#input-outgoing-0", 1);
    await click(".bp3-drawer-header button");

    await contextmenu("#ddn_10");
    await update_value("#input-incoming-0", 1);
    await update_value("#input-incoming-1", 1);
    await update_value("#input-outgoing-0", 1);
    await click(".bp3-drawer-header button");

    // Calibrate
    await click("#add-node-btn");
    await click("#calibrate-btn");
    await update_location(`#ddn_12`, 933, 538);

    await click("#add-link-btn");
    await click("#ddn_add_11");
    await click("#ddn_add_12");

    await click("#add-link-btn");
    await click("#ddn_add_12");
    await click("#ddn_add_2");


}

// helper functions

$(document).keydown(function(e){
    if (e.which == 38) { // up
       $(".cmd-prompt").show();
       return false;
   } else if (e.which == 40) { // down
       $(".cmd-prompt").hide();
       $("#test-overlay").hide();
       return false;
   }
});

async function click(selector) {
    await sleep(RETRY_DELAY);
    for (var i = 0; i < MAX_RETRIES; i++) {
        if ($(selector).length && $(selector).is(":visible")) {
            $(selector)[0].click();
            debug_log(`Clicked ${selector}`);
            return true;
        } else {
            debug_log(`Waiting for ${selector} to become available`);
            await sleep(RETRY_DELAY);
        }
    }
    throw `ERROR: ${selector} not available`;
}

async function contextmenu(selector) {
    await sleep(RETRY_DELAY);
    for (var i = 0; i < MAX_RETRIES; i++) {
        if ($(selector).length && $(selector).is(":visible")) {
            var ev2 = new Event('contextmenu', {
                bubbles: true
            });
            document.getElementById(selector.substring(1)).dispatchEvent(ev2);
            debug_log(`Right clicked ${selector}`);
            return true;
        } else {
            debug_log(`Waiting for ${selector} to become available`);
            await sleep(RETRY_DELAY);
        }
    }
    throw `ERROR: ${selector} not available`;
}

async function update_location(selector, x, y) {
    await sleep(RETRY_DELAY);
    for (var i = 0; i < MAX_RETRIES; i++) {
        if ($(selector).length && $(selector).is(":visible")) {
            $(selector).attr({
                "data-api-x": x,
                "data-api-y": y
            });
            $(selector)[0].click();
            debug_log(`Moved ${selector} to ${x}, ${y}`);
            return true;
        } else {
            debug_log(`Waiting for ${selector} to become available`);
            await sleep(RETRY_DELAY);
        }
    }
    throw `ERROR: ${selector} not available`;
}

async function update_value(selector, text) {
    await sleep(RETRY_DELAY);
    for (var i = 0; i < MAX_RETRIES; i++) {
        if ($(selector).length && $(selector).is(":visible")) {

            // https://stackoverflow.com/a/46012210
            var input = document.getElementById(selector.substring(1));
            var set_val = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            set_val.call(input, text);
            var ev2 = new Event('change', {
                bubbles: true
            });
            input.dispatchEvent(ev2);

            debug_log(`Updated value in ${selector} to ${text}`);
            return true;
        } else {
            debug_log(`Waiting for ${selector} to become available`);
            await sleep(RETRY_DELAY);
        }
    }
    throw `ERROR: ${selector} not available`;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function debug_log(msg) {
    $("pre#debug-output").append(`${msg}<br>`);
    var elem = document.getElementById("debug-output");
    elem.scrollTop = elem.scrollHeight;
}

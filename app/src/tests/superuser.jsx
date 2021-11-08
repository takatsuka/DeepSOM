const regeneratorRuntime = require("regenerator-runtime");
const MAX_RETRIES = 5;
const RETRY_DELAY = 10;

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

// helper functions

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

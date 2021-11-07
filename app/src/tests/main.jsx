const regeneratorRuntime = require("regenerator-runtime");
const MAX_RETRIES = 10;
const RETRY_DELAY = 10;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function debug_log(msg) {
    $("pre#test-debug-output").append(`${msg}<br>`);
    var elem = document.getElementById("test-debug-output");
    elem.scrollTop = elem.scrollHeight;
}

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

async function update_location(selector, x, y) {
    await sleep(RETRY_DELAY);
    for (var i = 0; i < MAX_RETRIES; i++) {
        if ($(selector).length && $(selector).is(":visible")) {
            $(selector).attr({"data-api-x":x, "data-api-y":y});
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

async function open_editor() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

    debug_log("Starting test open_editor");
    try {
        await click("#view-btn");
        await click("#menu-editor");

        await update_location(input_node_id, 850, 100);
        await update_location(output_node_id, 450, 950);

        for (var i = 3; i < 20; i++) {
            await click("#add-node-btn");
            await click("#single-som-btn");
            await update_location(`#ddn_${i}`, 100 * i, 300);

            await click("#add-link-btn")
            await click(input_node_btn_id)
            await click(`#ddn_add_${i}`)

            await click("#add-link-btn")
            await click(`#ddn_add_${i}`)
            await click(output_node_btn_id)
        }

        for (var i = 20; i < 37; i++) {
            await click("#add-node-btn");
            await click("#sampler-btn");
            await update_location(`#ddn_${i}`, 100 * (i-17), 600);

            await click("#add-link-btn")
            await click(input_node_btn_id)
            await click(`#ddn_add_${i}`)

            await click("#add-link-btn")
            await click(`#ddn_add_${i}`)
            await click(output_node_btn_id)
        }
    } catch(err) {
        debug_log(err);
    }
}


$(document).ready(async function(){
    await open_editor();
});

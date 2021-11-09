const regeneratorRuntime = require("regenerator-runtime");
const MAX_RETRIES = 5;
const RETRY_DELAY = 10;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function summary_log(msg) {
    $("pre#summary-output").append(`${msg}<br>`);
    var elem = document.getElementById("summary-output");
    elem.scrollTop = elem.scrollHeight;
}

function debug_log(msg) {
    $("pre#verbose-output").append(`${msg}<br>`);
    var elem = document.getElementById("verbose-output");
    elem.scrollTop = elem.scrollHeight;
}

function update_test_stats(passed, failed, pending) {
    $("#test-passed").text(passed);
    $("#test-failed").text(failed);
    $("#test-pending").text(pending);
}

function update_time() {
    var time = parseInt($("#test-time").text());
    $("#test-time").text(time + 1);
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

async function contextmenu(selector) {
    await sleep(RETRY_DELAY);
    for (var i = 0; i < MAX_RETRIES; i++) {
        if ($(selector).length && $(selector).is(":visible")) {
            var ev2 = new Event('contextmenu', { bubbles: true});
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
            $(selector).attr({"data-api-x": x, "data-api-y": y});
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

async function check_errmsg(msg) {

    var selector = "span.bp3-toast-message";
    await sleep(RETRY_DELAY);
    for (var i = 0; i < MAX_RETRIES; i++) {
        if ($(selector).length && $(selector).is(":visible")) {
            debug_log(`Found ${selector}`);
            var actual = $(selector).first().text();
            $(selector).text("Error message checked by test driver");
            var is_correct = actual === msg;
            if (!is_correct) {
                throw `ERROR: message does not match: ${actual} != ${msg}`;
            }
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
            var ev2 = new Event('change', { bubbles: true});
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

async function is_class_exist() {
    if ($("body.bp3-dark")[0]) {
        debug_log("Detected dark mode");
        return true;
    }
    debug_log("Detected light mode");
    return false;
}

// Begin test cases

async function test_dark_mode() {
    try {
        await click("#view-btn");
        var expect = true;
        for (var i = 0; i < 6; i++) {
            if (await is_class_exist() != expect) {
                return false;
            }

            expect = !expect;
            await click("#dark-mode-switch");

            if (await is_class_exist() != expect) {
                return false;
            }
        }
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_open() {
    try {
        await click("#view-btn");
        await click("#menu-editor");
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_add_link_basic() {
    try {
        await click("#view-btn");
        await click("#menu-editor");
        await click("#add-link-btn");
        await click("#ddn_add_1");
        await click("#ddn_add_2");
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_add_link_duplicate() {
    try {
        await click("#view-btn");
        await click("#menu-editor");
        await click("#add-link-btn");
        await click("#ddn_add_1");
        await click("#ddn_add_2");
        await click("#add-link-btn");
        await click("#ddn_add_1");
        await click("#ddn_add_2");
        await check_errmsg("Cannot add link - an identical link exists.");
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_add_link_loop() {
    try {
        await click("#view-btn");
        await click("#menu-editor");
        await click("#add-link-btn");
        await click("#ddn_add_1");
        await click("#ddn_add_1");
        await check_errmsg("Cannot add link - self loop not allowed.");
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_add_simple_som() {

    try {
        await click("#view-btn");
        await click("#menu-editor");
        await click("#add-node-btn");
        await click("#single-som-btn");
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_stress() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

    try {
        await click("#view-btn");
        await click("#menu-editor");

        await update_location(input_node_id, 850, 100);
        await update_location(output_node_id, 450, 950);

        for (var i = 3; i < 15; i++) {
            await click("#add-node-btn");
            await click("#single-som-btn");
            await update_location(`#ddn_${i}`, 140 * (i-2), 300);

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
            await update_location(`#ddn_${i}`, 140 * (i-14), 600);

            await click("#add-link-btn")
            await click(`#ddn_add_${i-1}`)
            await click(`#ddn_add_${i}`)
        }

        for (var i = 27; i < 35; i++) {
            await click("#add-node-btn");
            await click("#bypass-btn");
            await update_location(`#ddn_${i}`, 2000, 300 + 110 * (i-26));

            await click("#add-link-btn")
            await click(`#ddn_add_${i-1}`)
            await click(`#ddn_add_${i}`)
        }

        for (var i = 35; i < 43; i++) {
            await click("#add-node-btn");
            await click("#bypass-btn");
            await update_location(`#ddn_${i}`, 2150, 300 + 110 * (43-i));

            await click("#add-link-btn")
            await click(`#ddn_add_${i-1}`)
            await click(`#ddn_add_${i}`)
        }

        for (var i = 43; i < 51; i++) {
            await click("#add-node-btn");
            await click("#bypass-btn");
            await update_location(`#ddn_${i}`, 2300, 300 + 110 * (i-42));

            await click("#add-link-btn")
            await click(`#ddn_add_${i-1}`)
            await click(`#ddn_add_${i}`)
        }

    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_various_nodes() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

    try {
        await click("#view-btn");
        await click("#menu-editor");

        await update_location(input_node_id, 850, 100);
        await update_location(output_node_id, 750, 850);

        let soms = [
            "bypass-btn",
            "distributor-btn",
            "concatenator-btn",
            "single-som-btn",
            "sampler-btn",
            "mini-patcher-btn",
            "get-bmu-btn",
            "calibrate-btn"
        ]

        for (var i = 0; i < soms.length; i++) {
            await click("#add-node-btn");
            await click(`#${soms[i]}`);
            await update_location(`#ddn_${i+3}`, 200 * (i+3), 400);

            await click("#add-link-btn")
            await click(input_node_btn_id)
            await click(`#ddn_add_${i+3}`)

            await click("#add-link-btn")
            await click(`#ddn_add_${i+3}`)
            await click(output_node_btn_id)
        }
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_contextual_open() {

    try {
        await click("#view-btn");
        await click("#menu-editor");
        await click("#add-node-btn");
        await click("#single-som-btn");
        await contextmenu("#ddn_1");
        await click(".bp3-drawer-header button");
    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_contextual_edit() {

    try {
        await click("#view-btn");
        await click("#menu-editor");
        // SOM NODE
        await click("#add-node-btn");
        await click("#single-som-btn");
        await contextmenu("#ddn_3");
        await update_value("#input-name", "SOM testing");
        await update_value("#input-indim", "4");
        await update_value("#input-dim", "12");
        await update_value("#input-trainiter", "2000");
        await update_value("#input-sigma", "3");
        await update_value("#input-lr", "0.8");
        await click(".bp3-drawer-header button");

        // SAMPLER
        await click("#add-node-btn");
        await click("#sampler-btn");
        await contextmenu("#ddn_4");
        await update_value("#input-name", "Sampler testing");
        for (var i = 0; i < 40; i++) {
            await update_value("#input-dim", i * 50);
        }
        await click(".bp3-drawer-header button");

        // MINI PATCHER
        await click("#add-node-btn");
        await click("#mini-patcher-btn");
        await contextmenu("#ddn_5");
        await update_value("#input-name", "MP test");
        for (var i = 0; i < 20; i++) {
            await update_value("#input-kernel", 2 ** i);
            await update_value("#input-stride", 8 ** i);
            await update_value("#input-dim", 16 ** i);
        }
        await click(".bp3-drawer-header button");

        // DIST
        await click("#add-node-btn");
        await click("#distributor-btn");
        await contextmenu("#ddn_6");
        await update_value("#input-name", "D test");
        for (var i = 0; i < 40; i++) {
            await update_value("#input-axis", 2 ** i);
        }
        await click(".bp3-drawer-header button");

        // CONCAT
        await click("#add-node-btn");
        await click("#concatenator-btn");
        await contextmenu("#ddn_7");
        await update_value("#input-name", "C test");
        for (var i = 40; i > 0; i--) {
            await update_value("#input-axis", 3 ** i);
        }
        await click(".bp3-drawer-header button");

    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_various_nodes_dancing() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

    try {
        await click("#view-btn");
        await click("#menu-editor");

        await update_location(input_node_id, 850, 100);
        await update_location(output_node_id, 750, 850);

        let soms = [
            "bypass-btn",
            "distributor-btn",
            "concatenator-btn",
            "single-som-btn",
            "sampler-btn",
            "mini-patcher-btn",
            "get-bmu-btn",
            "calibrate-btn"
        ]

        for (var i = 0; i < soms.length; i++) {
            await click("#add-node-btn");
            await click(`#${soms[i]}`);
            await update_location(`#ddn_${i+3}`, 200 * (i+3), 400);

            await click("#add-link-btn")
            await click(input_node_btn_id)
            await click(`#ddn_add_${i+3}`)

            await click("#add-link-btn")
            await click(`#ddn_add_${i+3}`)
            await click(output_node_btn_id)
        }

        for (var i = 0; i < 15; i++) {
            await update_location(input_node_id, i * 100, 100);
            await update_location(output_node_id, i * 100, 850);
        }

        for (var i = 15; i > 0; i--) {
            await update_location(input_node_id, i * 100, 100);
            await update_location(output_node_id, i * 100, 850);
        }

        for (var i = 0; i < 7; i++) {
            await update_location(input_node_id, i * 100, 100);
            await update_location(output_node_id, i * 100, 850);
        }

        for (var i = 0; i < soms.length; i++) {
            for (var z = 300; z < 800; z += 50) {
                await update_location(`#ddn_${i+3}`, 200 * (i+3), z);
            }
        }

        for (var z = 800; z > 300; z -= 30) {
            for (var i = 0; i < soms.length; i++) {
                await update_location(`#ddn_${i+3}`, 200 * (i+3), z);
            }
        }

        for (var i = 0; i < 360; i += 15) {
            var x = Math.cos(i*Math.PI/180);
            var y = Math.sin(i*Math.PI/180);
            await update_location(input_node_id, 500 + x * 300, 300 + y * 300);
            await update_location(output_node_id, 700 + x * 300, 800 + y * 300);
        }

        for (var r = 50; r < 700; r += 30) {
            for (var i = 0; i < soms.length; i++) {
                var d = i * 45;
                var x = Math.cos(d*Math.PI/180);
                var y = Math.sin(d*Math.PI/180);

                await update_location(`#ddn_${i+3}`, 800 + x * r, 500 + y * r);
            }
        }


    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_random_nodes() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

    try {
        await click("#view-btn");
        await click("#menu-editor");

        await update_location(input_node_id, 850, 100);
        await update_location(output_node_id, 750, 850);

        let soms = [
            "bypass-btn",
            "distributor-btn",
            "concatenator-btn",
            "single-som-btn",
            "sampler-btn",
            "mini-patcher-btn",
            "get-bmu-btn",
            "calibrate-btn"
        ]

        for (var i = 0; i < 40; i++) {
            var som_idx = Math.floor(Math.random() * soms.length);
            await click("#add-node-btn");
            await click(`#${soms[som_idx]}`);
            await update_location(`#ddn_${i+3}`, 80 + Math.floor(Math.random() * 2000), 80 + Math.floor(Math.random() * 1000));
        }
        for (var z = 0; z < 2; z++) {
            for (var i = 0; i < 40; i++) {
                await update_location(`#ddn_${i+3}`, 80 + Math.floor(Math.random() * 2000), 80 + Math.floor(Math.random() * 1000));
            }
        }

    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_random_links() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

    try {
        await click("#view-btn");
        await click("#menu-editor");

        await update_location(input_node_id, 850, 100);
        await update_location(output_node_id, 750, 850);

        let soms = [
            "bypass-btn",
            "distributor-btn",
            "concatenator-btn",
            "single-som-btn",
            "sampler-btn",
            "mini-patcher-btn",
            "get-bmu-btn",
            "calibrate-btn"
        ]

        for (var i = 0; i < 20; i++) {
            var som_idx = Math.floor(Math.random() * soms.length);
            await click("#add-node-btn");
            await click(`#${soms[som_idx]}`);
            await update_location(`#ddn_${i+3}`, 80 + Math.floor(Math.random() * 2000), 80 + Math.floor(Math.random() * 1000));

            await click("#add-link-btn")
            await click(`#ddn_add_${i+2}`)
            await click(`#ddn_add_${i+3}`)
        }

    } catch(err) {
        debug_log(err);
        return false;
    }
    return true;
}

// run tests
$(document).ready(async function(){
    var tests = [
        test_dark_mode,
        test_editor_open,
        test_editor_add_link_basic,
        test_editor_add_link_duplicate,
        test_editor_add_link_loop,
        test_editor_add_simple_som,
        test_editor_stress,
        test_editor_various_nodes,
        test_editor_contextual_open,
        test_editor_contextual_edit,
        test_editor_various_nodes_dancing,
        test_editor_random_nodes,
        test_editor_random_links
    ];

    var passed = 0;
    var failed = 0;
    var pending = tests.length;
    $("#test-time").text(0);
    var timer = setInterval(update_time, 1000);
    update_test_stats(passed, failed, pending);

    for (var i = 0; i < tests.length; i++) {
        summary_log(`Starting test "${tests[i].name}"`);
        debug_log(`Starting test "${tests[i].name}"`);
        var result = await tests[i]();
        if (result) {
            summary_log(">>>PASSED");
            passed++;
        } else {
            summary_log("!!!FAILED");
            failed++;
        }
        pending--;
        update_test_stats(passed, failed, pending);

    }
    for (var i = 1; i < tests.length; i++) {
        await click(`#close_tab_${i}`);
    }

    clearInterval(timer);
});

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
        console.log(err);
        debug_log(err);
        return false;
    }
    return true;
}

async function test_editor_abuse() {
    let input_node_id = "#ddn_1";
    let output_node_id = "#ddn_2";
    let input_node_btn_id = "#ddn_add_1";
    let output_node_btn_id = "#ddn_add_2";

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
        return false;
    }
    return true;
}

$(document).ready(async function(){
    var tests = [
        test_editor_open,
        test_editor_add_link_basic,
        test_editor_add_link_duplicate,
        test_editor_add_link_loop,
        test_editor_abuse
    ];

    var passed = 0;
    var failed = 0;
    var pending = tests.length;
    update_test_stats(passed, failed, pending);

    for (var i = 0; i < tests.length; i++) {
        summary_log(`Starting test "${tests[i].name}"`);
        var result = await tests[i]();
        if (result) {
            summary_log(`Test "${tests[i].name}" PASSED`);
            passed++;
        } else {
            summary_log(`Test "${tests[i].name}" FAILED`);
            failed++;
        }
        await click(`#close_tab_${i+1}`);
        pending--;
        update_test_stats(passed, failed, pending);

    }
});

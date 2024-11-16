// ==UserScript==
// @name        ai-stare
// @version     1.0
// @description :aistare:
// @author      jniena
// @match       https://discord.com/*
// @grant       none
// @license     MIT

// ==/UserScript==

setTimeout(function () {
    "use strict";

    function hash(object) {
        const jsonString = JSON.stringify(object);
        let hash = 0;
        for (let i = 0; i < jsonString.length; i++) {
            const char = jsonString.charCodeAt(i);
            hash = (hash << 5) - hash + char;
            hash |= 0;
        }
        return hash.toString(16);
    }

    function random(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function advancePage() {
        const button = document.querySelector(".pageButton_b48941[rel='next']");
        if (button) {
            button.click();
            return true;
        }
        return false;
    }

    function getMessages() {
        const messages = {};
        const results = document.querySelectorAll("[class^='searchResult_ddc613']");
        results.forEach(result => {
            const message = {
                "username": result.querySelector(".username_f9f2ca").textContent,
                "timestamp": result.querySelector(".timestamp_f9f2ca").textContent.substring(3),
                "content": result.querySelector(".messageContent_f9f2ca").textContent
            };
            if (message.content.length > 0) {
                messages[hash(message)] = message;
            }
        });
        return messages;
    }

    function start() {
        const messages = getMessages();
        for (const [hash, message] of Object.entries(messages)) {
            console.log(`${JSON.stringify(message, null, 2)}\n`);
            sessionStorage.setItem(hash, JSON.stringify(message));
        }
        if (advancePage()) {
            setTimeout(start, random(2000, 3000));
        }
    }

    start();
}, 10000);

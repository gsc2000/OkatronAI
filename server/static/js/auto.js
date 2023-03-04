console.log("auto")

const btn_ai_start = document.getElementById("ai_start");
const btn_ai_stop = document.getElementById("ai_stop");

btn_ai_start.addEventListener("click", () => {
    btn_ai_start.disabled = true;
    btn_ai_stop.disabled = false;
    fetch('/mode/1/ai', {
        method: 'POST',
        body: JSON.stringify({sw: "start"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        console.log("Response: "+response)
    })
    .catch(error => {
        console.log("POST Failure")
    });
});

btn_ai_stop.addEventListener("click", () => {
    btn_ai_start.disabled = false;
    btn_ai_stop.disabled = true;
    fetch('/mode/1/ai', {
        method: 'POST',
        body: JSON.stringify({sw: "stop"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        console.log("Response: "+response)
    })
    .catch(error => {
        console.log("POST Failure")
    });
});

const btn_class1 = document.getElementById("class1");
const btn_class2 = document.getElementById("class2");
const btn_class3 = document.getElementById("class3");

btn_class1.addEventListener("click", function() {
btn_class1.disabled = true;
btn_class2.disabled = false;
btn_class3.disabled = false;
fetch('/mode/1/class1', {
    method: 'POST'
})
});
btn_class2.addEventListener("click", function() {
btn_class1.disabled = false;
btn_class2.disabled = true;
btn_class3.disabled = false;
fetch('/mode/1/class2', {
    method: 'POST'
})
});
btn_class3.addEventListener("click", function() {
btn_class1.disabled = false;
btn_class2.disabled = false;
btn_class3.disabled = true;
fetch('/mode/1/class3', {
    method: 'POST'
})
});

const btn_model1 = document.getElementById("model1");
const btn_model2 = document.getElementById("model2");
const btn_model3 = document.getElementById("model3");

btn_model1.addEventListener("click", function() {
btn_model1.disabled = true;
btn_model2.disabled = false;
btn_model3.disabled = false;
// fetch('/mode/1/class1', {
//   method: 'POST'
// })
});
btn_model2.addEventListener("click", function() {
btn_model1.disabled = false;
btn_model2.disabled = true;
btn_model3.disabled = false;
// fetch('/mode/1/class2', {
//   method: 'POST'
// })
});
btn_model3.addEventListener("click", function() {
btn_model1.disabled = false;
btn_model2.disabled = false;
btn_model3.disabled = true;
// fetch('/mode/1/class3', {
//   method: 'POST'
// })
});
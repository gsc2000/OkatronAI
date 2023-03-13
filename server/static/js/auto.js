console.log("auto")

// AI開始・終了ボタン
const btn_ai_start = document.getElementById("ai_start");
const btn_ai_stop = document.getElementById("ai_stop");

btn_ai_start.addEventListener("click", () => {
    btn_ai_start.disabled = true;
    btn_ai_stop.disabled = false;
    fetch('/mode/1/ai', {
        method: 'POST',
        body: JSON.stringify({switch: true}),
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
        body: JSON.stringify({switch: false}),
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

// モデルサイズ選択
const btn_model1 = document.getElementById("model1");
const btn_model2 = document.getElementById("model2");
const btn_model3 = document.getElementById("model3");

btn_model1.addEventListener("click", () => {
    btn_model1.disabled = true;
    btn_model2.disabled = false;
    btn_model3.disabled = false;
    fetch('/mode/1/modelsize', {
        method: 'POST',
        body: JSON.stringify({model: "nano"}),
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

btn_model2.addEventListener("click", () => {
    btn_model1.disabled = false;
    btn_model2.disabled = true;
    btn_model3.disabled = false;
    fetch('/mode/1/modelsize', {
        method: 'POST',
        body: JSON.stringify({model: "small"}),
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

btn_model3.addEventListener("click", () => {
    btn_model1.disabled = false;
    btn_model2.disabled = false;
    btn_model3.disabled = true;
    fetch('/mode/1/modelsize', {
        method: 'POST',
        body: JSON.stringify({model: "large"}),
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

const class_buttons = document.querySelectorAll('button[id^="class"]');
class_buttons[0].addEventListener("click", () => {
    class_buttons[0].disabled = true;
    class_buttons[1].disabled = false;
    class_buttons[2].disabled = false;
})

class_buttons[1].addEventListener("click", () => {
    class_buttons[0].disabled = false;
    class_buttons[1].disabled = true;
    class_buttons[2].disabled = false;
})

class_buttons[2].addEventListener("click", () => {
    class_buttons[0].disabled = false;
    class_buttons[1].disabled = false;
    class_buttons[2].disabled = true;
})

const imgsize_buttons = document.querySelectorAll('button[id^="imgsize"]');
imgsize_buttons[0].addEventListener("click", () => {
    imgsize_buttons[0].disabled = true;
    imgsize_buttons[1].disabled = false;
    imgsize_buttons[2].disabled = false;
})

imgsize_buttons[1].addEventListener("click", () => {
    imgsize_buttons[0].disabled = false;
    imgsize_buttons[1].disabled = true;
    imgsize_buttons[2].disabled = false;
})

imgsize_buttons[2].addEventListener("click", () => {
    imgsize_buttons[0].disabled = false;
    imgsize_buttons[1].disabled = false;
    imgsize_buttons[2].disabled = true;
})

const submit = document.getElementById("submit");
submit.addEventListener("click", () => {
    let sel_class = ""
    for (let i = 0; i < class_buttons.length; i++) {
        if (class_buttons[i].disabled === true) {
            console.log(class_buttons[i].id)
            let class_info = class_buttons[i].id.split("_");
            sel_class = class_info[1] // 選択されたクラスを取得
            // console.log(sel_class)
        }
      }

    let sel_imgsize = ""
    for (let i = 0; i < imgsize_buttons.length; i++) {
        if (imgsize_buttons[i].disabled === true) {
            console.log(imgsize_buttons[i].id)
            let imgsize_info = imgsize_buttons[i].id.split("_");
            sel_imgsize = imgsize_info[1]
        }
      }
    // 各テキストボックス
    let iou_val = document.getElementById('iou').value;
    let conf_val = document.getElementById('conf').value;

    let data = {
        classes: sel_class,
        imgsize: sel_imgsize,
        iou: iou_val,
        conf: conf_val
    }
    console.log(data)
    fetch("/mode/1/param", {
        method: 'POST',
        body: JSON.stringify(data),
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
})

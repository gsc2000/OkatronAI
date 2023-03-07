console.log("manual")
const userAgent = navigator.userAgent;

class PostButton {
    constructor(button) {
        console.log(button)
        this.postUrl = "/mode/2/crosskey";
        this.button = button;

        this.info = this.button.id.split("_");

        this.isPressed = false;
        if (userAgent.indexOf("iPhone") != -1 ||
            userAgent.indexOf("Android") != -1) {
              this.button.addEventListener('touchstart', this.handleTouchStart.bind(this));
              this.button.addEventListener('touchend', this.handleTouchEnd.bind(this));
            }
        else {
          this.button.addEventListener('mousedown', this.handleMouseDown.bind(this));
          this.button.addEventListener('mouseup', this.handleMouseUp.bind(this));
          this.button.addEventListener('mouseleave', this.handleLeave.bind(this));
        }
    }

    handleMouseDown() {
        this.isPressed = true;
        this.button.classList.add("active");
        let data = {kind: this.info[0],
                    direction: this.info[1]}
        this.postData(data);
    }

    handleMouseUp(event) {
        this.isPressed = false;
        this.button.classList.remove("active");
        if (this.button.contains(event.target)) {
            let data = {kind: this.info[0],
                        direction: "stop"}
            this.postData(data);
          }
    }

    handleLeave() {
        if (this.isPressed === true){
            this.isPressed = false;
            this.button.classList.remove("active");
            let data = {kind: this.info[0],
                        direction: "stop"}
            this.postData(data);
        }
    }

    handleTouchStart() {
        this.isPressed = true;
        this.button.classList.add("active");
        let data = {kind: this.info[0],
                    direction: this.info[1]}
        this.postData(data);
    }

    handleTouchEnd() {
        this.isPressed = false;
        this.button.classList.remove("active");
        let data = {kind: this.info[0],
                    direction: "stop"}
        this.postData(data);
    }

    postData(data) {
        console.log("ID: "+this.button.id)
        console.log("Type: "+this.info)
      fetch(this.postUrl, {
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
    }
  }

const move_buttons = document.querySelectorAll('button[id^="move_"]');
const camera_buttons = document.querySelectorAll('button[id^="camera_"]');
move_buttons.forEach(button => new PostButton(button))
camera_buttons.forEach(button => new PostButton(button))

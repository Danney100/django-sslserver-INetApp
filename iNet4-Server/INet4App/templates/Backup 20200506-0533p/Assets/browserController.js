
var AU = document.getElementById("AudioBLC");
var haveEvents = 'GamepadEvent' in window;
var haveWebkitEvents = 'WebKitGamepadEvent' in window;
var controllers = {};

loopy = true;
var startTime;
var firstLoop = true;
var pressed_temp = -1;
var rAF = window.mozRequestAnimationFrame ||
  window.webkitRequestAnimationFrame ||
  window.requestAnimationFrame;

 function playAudio() {
      if (AU.currentTime == 0)
            AU.play();
      else{
          AU.currentTime -=0.5;
          AU.play();
          }
    }

 function toStart() {
        AU.currentTime = 0;
        AU.play();
    }

   function toEnd() {
        AU.currentTime = AU.duration;
    }

 function pauseAudio() {
      AU.pause();
    }

 function FasterplaySpeed(){
  AU.playbackRate += 0.5;

 }

  function SlowerplaySpeed(){
    AU.playbackRate -= 0.5;
 }


 function backwardAudio() {
      new Audio(BeepSound).play();
      AU.currentTime -= 3;
    }

 function forwardAudio() {
      new Audio(BeepSound).play();
      AU.currentTime += 3;
    }



function connecthandler(e) {
  addgamepad(e.gamepad);
}

function addgamepad(gamepad) {
  controllers[gamepad.index] = gamepad;
  rAF(updateStatus);
}

function disconnecthandler(e) {
  removegamepad(e.gamepad);
}

function removegamepad(gamepad) {
  delete controllers[gamepad.index];
}

function updateStatus() {
  scangamepads();
  for (j in controllers) {
    var controller = controllers[j];
    for (var i=0; i<3; i++) {
           var val = controller.buttons[i];
            //console.log("var: " + i +  ", pressed: " + val.pressed);
            if(val.pressed == true)
            {
                if(i == 1)
                {
                    pressed_temp = 1;
                    if(firstLoop == true){
                      if (AU.currentTime == 0)
                            AU.play();
                      else{
                            AU.currentTime -=0.5;
                            AU.play();
                          }
                      firstLoop = false;
                    }
                }
                else if( i == 0){
                    pressed_temp = 0;
                    //console.log("Box");
                    if (loopy == true) {
                        new Audio(BeepSound).play();
                        AU.currentTime -= 3;
                        loopy = false;
                        startTime = new Date();
                    }else
                    {
                        //console.log("Timer: " + Math.round((new Date() - startTime) /1000))
                        if (Math.round((new Date() - startTime) /1000) >= 0.5)
                        {
                            loopy = true;
                            startTime = new Date();
                        }
                    }
                }
                else if(i == 2){
                    pressed_temp = 2;
                    if (loopy == true) {
                        new Audio(BeepSound).play();
                        AU.currentTime += 3;
                        loopy = false;
                        startTime = new Date();
                    }else
                    {
                        //console.log("Timer: " + Math.round((new Date() - startTime) /1000))
                        if (Math.round((new Date() - startTime) /1000) >= 0.5)
                        {
                            loopy = true;
                            startTime = new Date();
                        }
                    }
                }
            }
            else if (val.pressed == false && i == pressed_temp){
                //console.log("pressed_temp: " + pressed_temp);
                if (pressed_temp == 1){
                   AU.pause();
                   firstLoop = true;
                   pressed_temp = -1;
                }
//                else if (pressed_temp == 2){
//                   loopy = true;
//                   pressed_temp = -1;
//                }
//                else if (pressed_temp == 0){
//                   loopy = true;
//                   pressed_temp = -1;
//                }
            }
    }
  }
  rAF(updateStatus);
}

function scangamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  for (var i = 0; i < gamepads.length; i++) {
    if (gamepads[i]) {
      if (!(gamepads[i].index in controllers)) {
        addgamepad(gamepads[i]);
      } else {
        controllers[gamepads[i].index] = gamepads[i];
      }
    }
  }
}

if (haveEvents) {
  window.addEventListener("gamepadconnected", connecthandler);
  window.addEventListener("gamepaddisconnected", disconnecthandler);
} else if (haveWebkitEvents) {
  window.addEventListener("webkitgamepadconnected", connecthandler);
  window.addEventListener("webkitgamepaddisconnected", disconnecthandler);
} else {
  setInterval(scangamepads, 500);
}
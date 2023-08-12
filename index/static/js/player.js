/* 相关组件的变量定义 */
var media = document.querySelector(".myvideo");
var controls = document.querySelector(".controls");

var play = document.querySelector(".play");
var stop = document.querySelector(".stop");
var rwd = document.querySelector(".rwd");
var fwd = document.querySelector(".fwd");

var speed = document.querySelector(".speed");
var fullscreen = document.querySelector(".fullscreen")

var timerWrapper = document.querySelector(".timer");
var timer = document.querySelector(".timer span");

media.removeAttribute("controls");  // 移除自带的控件
controls.style.visibility = "visible";  // 设置控件可见

/* 播放和暂停 */
play.addEventListener("click", playPauseMedia);
media.addEventListener("click", playPauseMedia);
function playPauseMedia() {
    if (media.paused) {
      media.play();
      play.setAttribute("src", "/media/icons/zanting.png");
    } else {
      media.pause();
      play.setAttribute("src", "/media/icons/bofang.png");
    }
  }

/* 停止视频 */
stop.addEventListener("click", stopMedia);
media.addEventListener("ended", stopMedia);

function stopMedia() {
  media.pause();
  media.currentTime = 0;
}

/* 视频的快进与回退 */
rwd.addEventListener("click", mediaBackward);
fwd.addEventListener("click", mediaForward);

function mediaBackward() {  // 视频的回退函数
  if(media.currentTime != 0){
    media.currentTime -= 5;
  }
}

function mediaForward() {  // 视频的快进函数
  if(media.currentTime != 0){
    media.currentTime += 5;
  }
}

/* 视频的倍速 */
speed.addEventListener("click", mediaSpeed);

function mediaSpeed() {  // 调节视频倍速
  if(media.playbackRate == 1){
    media.playbackRate = 3;
    speed.setAttribute("src", "/media/icons/3beisu.png")
  }else if(media.playbackRate == 3) {
    media.playbackRate = 1;
    speed.setAttribute("src", "/media/icons/1beisu.png")
  }
  
}

fullscreen.addEventListener("click", fullMedia);

function fullMedia() {
  if(document.fullscreenElement){
    media.exitFullscreen();
  } else {
    media.requestFullscreen();
  }
}

/* 更新视频时长 */
media.addEventListener("timeupdate", setTime);

function setTime() {
  var minutes = Math.floor(media.currentTime / 60);
  var seconds = Math.floor(media.currentTime - minutes * 60);
  var minuteValue;
  var secondValue;

  if (minutes < 10) {
    minuteValue = "0" + minutes;
  } else {
    minuteValue = minutes;
  }

  if (seconds < 10) {
    secondValue = "0" + seconds;
  } else {
    secondValue = seconds;
  }

  var mediaTime = minuteValue + ":" + secondValue + "/";
  timer.textContent = mediaTime;

}
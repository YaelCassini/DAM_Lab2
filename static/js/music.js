
var audio=document.getElementById("audio");
var rotateVal = 0 // 旋转角度
var InterVal // 定时器
	window.onload = function () {
    document.getElementById("audio").onpause=function()
    {
      clearInterval(InterVal);
    }
    document.getElementById("audio").onplay=function()
    {
      rotate();
    }

	}
  
  
	// 设置定时器
	function rotate () {
		InterVal = setInterval(function () {
			var img = document.getElementById('disc_pic')
			rotateVal += 1//每次增加的角度
			// 设置旋转属性(顺时针)
			img.style.transform = 'rotate(' + rotateVal + 'deg)'
			// 设置旋转属性(逆时针)
			//img.style.transform = 'rotate(-' + rotateVal + 'deg)'
			// 设置旋转时的动画  匀速0.1s
			img.style.transition = '0.1s linear'
		}, 10)
	}
